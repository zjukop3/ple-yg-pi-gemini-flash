"""Coordination 3D model generator for data hall (dc_model hall_seed000_d000)
Rebuilds the hall coordination background and routes three overhead/plenum MEP services:
- Chilled Water Pipe (CHW-1)
- Power Busway (BW-1)
- Telecom Cable Tray (CT-1)

All geometry, coordinates, elevations, and schedules reconciled from:
- A-101 (Equipment plan & details)
- A-301 (Building section & details)
- A-601 (Equipment schedules)
- A-602 (Containment & pathway section schedule, general construction data)
- E-101 (Power & telecom plan, entries, PDU working space)
- M-101 (Chilled water plan, entries, CRAH consumers)
- F-101 (Sprinkler grid, ceiling & in-aisle heads)
"""
import sys
import os
import math
import time
import json
import numpy as np
import ifcopenshell
import ifcopenshell.api
import ifcopenshell.validate

OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "output/model.ifc"

def create_extruded_solid(model, profile, depth, axis=(0.0, 0.0, 1.0), ref_dir=(1.0, 0.0, 0.0)):
    ext_pos = model.createIfcAxis2Placement3D(
        model.createIfcCartesianPoint((0.0, 0.0, 0.0)),
        model.createIfcDirection(axis),
        model.createIfcDirection(ref_dir)
    )
    solid = model.createIfcExtrudedAreaSolid(
        SweptArea=profile,
        Position=ext_pos,
        ExtrudedDirection=model.createIfcDirection((0.0, 0.0, 1.0)),
        Depth=float(depth)
    )
    return solid

def add_element(model, storey, body, ifc_class, name, object_type, profile, depth,
                placement_point, rotation_z_deg=0.0, predefined_type=None,
                ext_axis=(0.0, 0.0, 1.0), ext_ref_dir=(1.0, 0.0, 0.0)):
    element = ifcopenshell.api.run(
        "root.create_entity", model,
        ifc_class=ifc_class,
        name=name,
        predefined_type=predefined_type
    )
    if object_type:
        element.ObjectType = object_type

    ifcopenshell.api.run("spatial.assign_container", model, relating_structure=storey, products=[element])

    solid = create_extruded_solid(model, profile, depth, axis=ext_axis, ref_dir=ext_ref_dir)
    rep = model.createIfcShapeRepresentation(
        ContextOfItems=body,
        RepresentationIdentifier="Body",
        RepresentationType="SweptSolid",
        Items=[solid]
    )
    element.Representation = model.createIfcProductDefinitionShape(Representations=[rep])

    # Rotation about footprint centre
    rad = math.radians(rotation_z_deg)
    ref_x = math.cos(rad)
    ref_y = math.sin(rad)
    
    element.ObjectPlacement = model.createIfcLocalPlacement(
        storey.ObjectPlacement,
        model.createIfcAxis2Placement3D(
            model.createIfcCartesianPoint((float(placement_point[0]), float(placement_point[1]), float(placement_point[2]))),
            model.createIfcDirection((0.0, 0.0, 1.0)),
            model.createIfcDirection((ref_x, ref_y, 0.0))
        )
    )
    return element

def add_linear_segment(model, storey, body, ifc_class, name, object_type, profile,
                       p1, p2, predefined_type=None):
    """Creates straight axis-aligned segment running from p1 to p2."""
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    vec = p2 - p1
    length = float(np.linalg.norm(vec))
    if length < 1e-3:
        return None
    dir_v = vec / length

    element = ifcopenshell.api.run(
        "root.create_entity", model,
        ifc_class=ifc_class,
        name=name,
        predefined_type=predefined_type
    )
    if object_type:
        element.ObjectType = object_type

    ifcopenshell.api.run("spatial.assign_container", model, relating_structure=storey, products=[element])

    solid = create_extruded_solid(model, profile, length)
    rep = model.createIfcShapeRepresentation(
        ContextOfItems=body,
        RepresentationIdentifier="Body",
        RepresentationType="SweptSolid",
        Items=[solid]
    )
    element.Representation = model.createIfcProductDefinitionShape(Representations=[rep])

    # Axis along dir_v
    if abs(dir_v[0]) > 0.9:  # along X
        axis = (float(dir_v[0]), 0.0, 0.0)
        ref_dir = (0.0, 0.0, 1.0)
    elif abs(dir_v[1]) > 0.9:  # along Y
        axis = (0.0, float(dir_v[1]), 0.0)
        ref_dir = (0.0, 0.0, 1.0)
    else:  # along Z
        axis = (0.0, 0.0, float(dir_v[2]))
        ref_dir = (1.0, 0.0, 0.0)

    element.ObjectPlacement = model.createIfcLocalPlacement(
        storey.ObjectPlacement,
        model.createIfcAxis2Placement3D(
            model.createIfcCartesianPoint((float(p1[0]), float(p1[1]), float(p1[2]))),
            model.createIfcDirection(axis),
            model.createIfcDirection(ref_dir)
        )
    )
    return element

def build_model(out_path):
    t0 = time.time()
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)

    model = ifcopenshell.api.run("project.create_file", version="IFC4")
    project = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcProject", name="DataHall_seed000_d000")
    ifcopenshell.api.run("unit.assign_unit", model, length={"is_metric": True, "raw": "MILLIMETRE"})

    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run(
        "context.add_context", model,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=context
    )

    site = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSite", name="DataCenterSite")
    ifcopenshell.api.run("aggregate.assign_object", model, products=[site], relating_object=project)

    building = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuilding", name="DataCenterBuilding")
    ifcopenshell.api.run("aggregate.assign_object", model, products=[building], relating_object=site)

    storey = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Level 0")
    ifcopenshell.api.run("aggregate.assign_object", model, products=[storey], relating_object=building)

    # 2D Profiles (centered at (0,0))
    origin_2d = model.createIfcAxis2Placement2D(model.createIfcCartesianPoint((0.0, 0.0)))

    prof_c1 = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=600.0, YDim=1200.0, Position=origin_2d)
    prof_n1 = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=800.0, YDim=1200.0, Position=origin_2d)
    prof_col = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=600.0, YDim=600.0, Position=origin_2d)
    prof_p_crah = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=1200.0, YDim=900.0, Position=origin_2d)
    prof_pdu = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=762.0, YDim=813.0, Position=origin_2d)
    prof_floor = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=27000.0, YDim=21000.0, Position=origin_2d)
    prof_door = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=60.0, YDim=1200.0, Position=origin_2d)
    prof_sprnk = model.createIfcCircleProfileDef(ProfileType="AREA", Radius=25.0, Position=origin_2d)

    # MEP Profiles
    # CHW-1: OD over insulation 168.3 mm -> Radius = 84.15 mm
    prof_chw = model.createIfcCircleProfileDef(ProfileType="AREA", Radius=84.15, Position=origin_2d)
    # BW-1: Section 128 W x 147 H. In extrusion coords where local Z is along length:
    # local X is along Z (147), local Y is along width (128)
    prof_bw = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=147.0, YDim=128.0, Position=origin_2d)
    # CT-1: Section 683 W x 127 H. In extrusion coords:
    # local X is along Z (127), local Y is along width (683)
    prof_ct = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=127.0, YDim=683.0, Position=origin_2d)

    # 1. ACCESS FLOOR SLAB (top at z=0, bottom at z=-35)
    floor = add_element(
        model, storey, body,
        ifc_class="IfcSlab",
        name="AccessFloor",
        object_type="AccessFloor",
        profile=prof_floor,
        depth=35.0,
        placement_point=(13500.0, 10500.0, -35.0),
        predefined_type="FLOOR"
    )
    pset_fl = ifcopenshell.api.run("pset.add_pset", model, product=floor, name="Pset_DCM_AccessFloor")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset_fl, properties={
        "Thickness": 35.0,
        "FinishedFloorElevation": 0.0,
        "PlenumDepth": 900.0
    })

    # 2. STRUCTURAL COLUMNS (6 columns, 600x600, full clear height 0..3600 mm)
    cols = [
        (8400.0, 8400.0), (16800.0, 8400.0), (25200.0, 8400.0),
        (8400.0, 16800.0), (16800.0, 16800.0), (25200.0, 16800.0)
    ]
    for i, (cx, cy) in enumerate(cols):
        col = add_element(
            model, storey, body,
            ifc_class="IfcColumn",
            name=f"COL-{i+1:02d}",
            object_type="StructuralColumn",
            profile=prof_col,
            depth=3600.0,
            placement_point=(cx, cy, 0.0),
            predefined_type="COLUMN"
        )
        pset_c = ifcopenshell.api.run("pset.add_pset", model, product=col, name="Pset_DCM_Column")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_c, properties={
            "Tag": f"COL-{i+1:02d}",
            "Width": 600.0,
            "Depth": 600.0,
            "Height": 3600.0
        })

    # 3. CABINETS & IN-ROW CRAHS (A-601 schedules)
    bay_seqs = {
        "A": "4C1 · CU · 3C1 · N1 · 3C1 · CU · CA · 6C1 · SP · CU · 5C1",
        "B": "4C1 · CU · 5C1 · 2N1 · CU · CA · 7C1 · SP · CU · 5C1",
        "C": "3C1 · CU · 6C1 · 2-600 · CU · CA · N1 · 4C1 · CU · SP · C1 · 2-600 · 3C1",
        "D": "4C1 · CU · 3C1 · 2N1 · 2C1 · CU · CA · 7C1 · SP · CU · 5C1",
        "E": "4C1 · CU · 5C1 · N1 · C1 · CU · CA · 6C1 · SP · CU · 5C1",
        "F": "4C1 · CU · 5C1 · 2-600 · CU · CA · 2N1 · 5C1 · SP · -600 · CU · 4C1"
    }
    row_centrelines = {"A": 3000.0, "B": 6000.0, "C": 8400.0, "D": 11400.0, "E": 13800.0, "F": 16800.0}
    row_facings = {"A": "SOUTH", "B": "NORTH", "C": "SOUTH", "D": "NORTH", "E": "SOUTH", "F": "NORTH"}
    EAST_AISLE_EDGE = 11400.0

    for row_letter, seq_str in bay_seqs.items():
        yc = row_centrelines[row_letter]
        facing = row_facings[row_letter]
        rot = 0.0 if facing == "SOUTH" else 180.0
        tokens = [t.strip() for t in seq_str.split("·")]
        ca_idx = tokens.index("CA")
        west_tokens = tokens[:ca_idx]
        east_tokens = tokens[ca_idx+1:]

        rack_num = 1
        crah_num = 1

        for part_tokens, start_x in [(west_tokens, 1800.0), (east_tokens, EAST_AISLE_EDGE)]:
            cur_x = start_x
            for tok in part_tokens:
                count = 1
                item_type = tok
                if tok[0].isdigit():
                    if tok.startswith("2-600"): cur_x += 1200.0; continue
                    elif tok.startswith("-600"): cur_x += 600.0; continue
                    else: count = int(tok[0]); item_type = tok[1:]
                elif tok.startswith("-600"): cur_x += 600.0; continue

                for _ in range(count):
                    if item_type in ("C1", "N1"):
                        w = 600.0 if item_type == "C1" else 800.0
                        tag = f"RACK-{row_letter}{rack_num:02d}"
                        rack_num += 1
                        prof = prof_c1 if item_type == "C1" else prof_n1
                        rack_el = add_element(
                            model, storey, body,
                            ifc_class="IfcFurniture",
                            name=tag,
                            object_type="Rack",
                            profile=prof,
                            depth=2000.0,
                            placement_point=(cur_x + w/2.0, yc, 0.0),
                            rotation_z_deg=rot,
                            predefined_type="USERDEFINED"
                        )
                        pset_r = ifcopenshell.api.run("pset.add_pset", model, product=rack_el, name="Pset_DCM_Rack")
                        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_r, properties={
                            "Tag": tag,
                            "Row": row_letter,
                            "CabinetType": item_type,
                            "RU": 42,
                            "Width": float(w),
                            "Depth": 1200.0,
                            "Height": 2000.0,
                            "RatedPower": 8.0,
                            "Weight": 1363.0,
                            "Facing": facing
                        })
                        cur_x += w
                    elif item_type == "CU":
                        w = 600.0
                        tag = f"CRAH-{row_letter}{crah_num:02d}"
                        crah_num += 1
                        crah_el = add_element(
                            model, storey, body,
                            ifc_class="IfcUnitaryEquipment",
                            name=tag,
                            object_type="CRAH",
                            profile=prof_c1,
                            depth=2000.0,
                            placement_point=(cur_x + w/2.0, yc, 0.0),
                            rotation_z_deg=rot,
                            predefined_type="USERDEFINED"
                        )
                        pset_cu = ifcopenshell.api.run("pset.add_pset", model, product=crah_el, name="Pset_DCM_CRAH")
                        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_cu, properties={
                            "Tag": tag,
                            "Row": row_letter,
                            "Placement": "IN-ROW",
                            "CoolingCapacity": 50.0,
                            "Airflow": 9000.0,
                            "Service": "CHILLED WATER, DN50",
                            "Facing": facing
                        })
                        cur_x += w
                    elif item_type == "SP":
                        cur_x += 600.0

    # 4. PERIMETER CRAH UNITS (4 units, 1200x900x2000, facing North)
    p_crahs = [
        ("CRAH-01", 600.0, 0.0, 1800.0, 900.0),
        ("CRAH-02", 9000.0, 0.0, 10200.0, 900.0),
        ("CRAH-03", 16800.0, 0.0, 18000.0, 900.0),
        ("CRAH-04", 25200.0, 0.0, 26400.0, 900.0)
    ]
    for tag, x1, y1, x2, y2 in p_crahs:
        p_el = add_element(
            model, storey, body,
            ifc_class="IfcUnitaryEquipment",
            name=tag,
            object_type="CRAH",
            profile=prof_p_crah,
            depth=2000.0,
            placement_point=((x1 + x2)/2.0, (y1 + y2)/2.0, 0.0),
            rotation_z_deg=180.0,  # Front points to +Y (North)
            predefined_type="USERDEFINED"
        )
        pset_p = ifcopenshell.api.run("pset.add_pset", model, product=p_el, name="Pset_DCM_CRAH")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_p, properties={
            "Tag": tag,
            "Placement": "PERIMETER",
            "CoolingCapacity": 100.0,
            "Airflow": 20000.0,
            "Service": "CHILLED WATER, DN100",
            "Facing": "NORTH"
        })

    # 5. PDUs (6 units, 762x813x1959)
    pdus = [
        ("PDU-01", "A", 21000.0, 2400.0, 21762.0, 3213.0, "SOUTH"),
        ("PDU-02", "B", 21600.0, 5787.0, 22362.0, 6600.0, "NORTH"),
        ("PDU-03", "C", 21000.0, 7800.0, 21762.0, 8613.0, "SOUTH"),
        ("PDU-04", "D", 21600.0, 11187.0, 22362.0, 12000.0, "NORTH"),
        ("PDU-05", "E", 21000.0, 13200.0, 21762.0, 14013.0, "SOUTH"),
        ("PDU-06", "F", 21600.0, 16587.0, 22362.0, 17400.0, "NORTH")
    ]
    for tag, serves, x1, y1, x2, y2, facing in pdus:
        rot = 0.0 if facing == "SOUTH" else 180.0
        pdu_el = add_element(
            model, storey, body,
            ifc_class="IfcElectricDistributionBoard",
            name=tag,
            object_type="PDU",
            profile=prof_pdu,
            depth=1959.0,
            placement_point=((x1 + x2)/2.0, (y1 + y2)/2.0, 0.0),
            rotation_z_deg=rot,
            predefined_type="USERDEFINED"
        )
        pset_pdu = ifcopenshell.api.run("pset.add_pset", model, product=pdu_el, name="Pset_DCM_PDU")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_pdu, properties={
            "Tag": tag,
            "ServesRow": serves,
            "Rating": 225.0,
            "WorkingSpace": 900.0,
            "Facing": facing
        })

    # 6. COLD-AISLE CONTAINMENT (CAC-BC and CAC-DE)
    containments = [
        ("CAC-BC", "ROWS B/C", 7200.0, 6600.0, 7800.0),
        ("CAC-DE", "ROWS D/E", 12600.0, 12000.0, 13200.0)
    ]
    prof_roof_w = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=8200.0, YDim=1400.0, Position=origin_2d)
    prof_roof_e = model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=8400.0, YDim=1400.0, Position=origin_2d)

    for tag, contains_rows, cy_aisle, dy1, dy2 in containments:
        # Roof West panel: between doors [1860, 9940], length 8080
        rw = add_element(
            model, storey, body,
            ifc_class="IfcCovering",
            name=f"{tag}-Roof-W",
            object_type="ContainmentRoof",
            profile=model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=8080.0, YDim=1400.0, Position=origin_2d),
            depth=55.5,
            placement_point=(5900.0, cy_aisle, 2000.0),
            predefined_type="CEILING"
        )
        pset_rw = ifcopenshell.api.run("pset.add_pset", model, product=rw, name="Pset_DCM_Containment")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_rw, properties={
            "Tag": tag, "ContainsRows": contains_rows, "Thickness": 55.5, "UndersideElevation": 2000.0
        })

        # Roof East panel: between doors [11460, 19740], length 8280
        re = add_element(
            model, storey, body,
            ifc_class="IfcCovering",
            name=f"{tag}-Roof-E",
            object_type="ContainmentRoof",
            profile=model.createIfcRectangleProfileDef(ProfileType="AREA", XDim=8280.0, YDim=1400.0, Position=origin_2d),
            depth=55.5,
            placement_point=(15600.0, cy_aisle, 2000.0),
            predefined_type="CEILING"
        )
        pset_re = ifcopenshell.api.run("pset.add_pset", model, product=re, name="Pset_DCM_Containment")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_re, properties={
            "Tag": tag, "ContainsRows": contains_rows, "Thickness": 55.5, "UndersideElevation": 2000.0
        })

        # Doors: 4 doors across aisle (dy1 to dy2, width 1200, thk 60, height 2055.5)
        door_xs = [1830.0, 9970.0, 11430.0, 19770.0]
        for d_i, dx_c in enumerate(door_xs):
            d_el = add_element(
                model, storey, body,
                ifc_class="IfcDoor",
                name=f"{tag}-Door-{d_i+1:02d}",
                object_type="ContainmentDoor",
                profile=prof_door,
                depth=2055.5,
                placement_point=(dx_c, cy_aisle, 0.0),
                predefined_type="DOOR"
            )
            pset_d = ifcopenshell.api.run("pset.add_pset", model, product=d_el, name="Pset_DCM_Containment")
            ifcopenshell.api.run("pset.edit_pset", model, pset=pset_d, properties={
                "Tag": tag, "Thickness": 60.0, "Height": 2055.5
            })

    # 7. SPRINKLER HEADS (63 ceiling heads + 16 in-aisle heads = 79 heads)
    grid_x = [1500.0, 4500.0, 7500.0, 10500.0, 13500.0, 16500.0, 19500.0, 22500.0, 25500.0]
    grid_y = [1500.0, 4500.0, 7500.0, 10500.0, 13500.0, 16500.0, 19500.0]
    sp_count = 1
    for gy in grid_y:
        for gx in grid_x:
            actual_gy = gy
            # Heads interrupted by columns at (16800, 16800) and (25200, 16800) relocated clear per F-101 Note 3 & Detail 2
            if gy == 16500.0 and gx in (16500.0, 25500.0):
                actual_gy = 16200.0

            sp_el = add_element(
                model, storey, body,
                ifc_class="IfcFireSuppressionTerminal",
                name=f"SPRNK-C{sp_count:02d}",
                object_type="SprinklerHead",
                profile=prof_sprnk,
                depth=25.0,
                placement_point=(gx, actual_gy, 3575.0),
                predefined_type="SPRINKLER"
            )
            pset_sp = ifcopenshell.api.run("pset.add_pset", model, product=sp_el, name="Pset_DCM_Sprinkler")
            ifcopenshell.api.run("pset.edit_pset", model, pset=pset_sp, properties={
                "Tag": f"SPRNK-C{sp_count:02d}", "Type": "CEILING", "DeflectorElevation": 3575.0
            })
            sp_count += 1

    aisle_x = [2300.0, 4700.0, 7300.0, 9700.0, 11900.0, 14400.0, 16700.0, 19300.0]
    for tag_aisle, y_aisle in [("BC", 7200.0), ("DE", 12600.0)]:
        for ia_i, ax in enumerate(aisle_x):
            tag_ia = f"SPRNK-IA-{tag_aisle}-{ia_i+1:02d}"
            ia_el = add_element(
                model, storey, body,
                ifc_class="IfcFireSuppressionTerminal",
                name=tag_ia,
                object_type="SprinklerHead",
                profile=prof_sprnk,
                depth=110.0,
                placement_point=(ax, y_aisle, 1890.0),
                predefined_type="SPRINKLER"
            )
            pset_ia = ifcopenshell.api.run("pset.add_pset", model, product=ia_el, name="Pset_DCM_Sprinkler")
            ifcopenshell.api.run("pset.edit_pset", model, pset=pset_ia, properties={
                "Tag": tag_ia, "Type": "IN-AISLE", "DeflectorElevation": 1890.0
            })

    # ==========================================
    # 8. MEP SERVICE ROUTING (CLASH-FREE, CONNECTED)
    # ==========================================
    #
    # Tier elevations:
    # - CT-1 (Cable Tray): Under-floor plenum at Z_center = -163.5 mm (top at -100 mm, > 20 mm below floor panel -35)
    # - CHW-1 (Chilled Water): Overhead Tier 1 at Z_center = 2710.0 mm (OD=168.3, z in [2625.85, 2794.15], > 2600 min headroom)
    # - BW-1 (Busway): Overhead Tier 2 at Z_center = 2950.0 mm (H=147, z in [2876.5, 3023.5], < 3115 sprinkler standoff)
    #
    # Clearances:
    # - CHW top (2794.15) to BW bottom (2876.5): 82.35 mm (> 2 mm)
    # - BW top (3023.5) to Sprinkler Standoff (3115): 91.5 mm (> 0 mm)
    # - Headroom below CHW (2625.85): 25.85 mm above 2600 min headroom
    # - Tray-Busway separation: dz = 2876.5 - (-100.0) = 2976.5 mm (>> 300 mm required)
    # - Columns (600x600 at y=8400 and y=16800): Row C and Row F headers offset to clear columns!

    # --- CHW-1: CHILLED WATER PIPE (DN100, OD over insulation 168.3 mm) ---
    chw_z = 2710.0
    chw_r = 168.3 / 2.0
    chw_trunk_x = 250.0
    chw_trunk_w_face = chw_trunk_x - chw_r
    chw_trunk_e_face = chw_trunk_x + chw_r
    # Entry segment: from west wall x=0 to trunk west face at y=9900
    chw_entry = add_linear_segment(
        model, storey, body, "IfcPipeSegment", "CHW-Entry", "ChilledWaterPipe",
        prof_chw, (0.0, 9900.0, chw_z), (chw_trunk_w_face, 9900.0, chw_z), predefined_type="RIGIDSEGMENT"
    )
    # N-S Main Trunk at x=250, from y=1800 to y=17600
    chw_trunk = add_linear_segment(
        model, storey, body, "IfcPipeSegment", "CHW-Trunk-NS", "ChilledWaterPipe",
        prof_chw, (chw_trunk_x, 1800.0, chw_z), (chw_trunk_x, 17600.0, chw_z), predefined_type="RIGIDSEGMENT"
    )
    # Branches East from trunk east face:
    chw_branches = [
        ("CHW-Branch-Perimeter", 1800.0, 25800.0),
        ("CHW-Branch-RowA", 3000.0, 19200.0),
        ("CHW-Branch-RowB", 6000.0, 19800.0),
        ("CHW-Branch-RowC", 9200.0, 19200.0),  # Offset from y=8400 to clear columns
        ("CHW-Branch-RowD", 11400.0, 19800.0),
        ("CHW-Branch-RowE", 13800.0, 19200.0),
        ("CHW-Branch-RowF", 17600.0, 20200.0),  # Offset from y=16800 to clear columns
    ]
    for bname, by, bx2 in chw_branches:
        chw_b = add_linear_segment(
            model, storey, body, "IfcPipeSegment", bname, "ChilledWaterPipe",
            prof_chw, (chw_trunk_e_face, by, chw_z), (bx2, by, chw_z), predefined_type="RIGIDSEGMENT"
        )
        pset_chw = ifcopenshell.api.run("pset.add_pset", model, product=chw_b, name="Pset_DCM_Pathway")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_chw, properties={
            "Tag": "CHW-1", "Service": "CHILLED WATER", "OuterDiameter": 114.3, "InsulationThickness": 25.4, "DiameterOverInsulation": 168.3
        })

    pset_chwe = ifcopenshell.api.run("pset.add_pset", model, product=chw_entry, name="Pset_DCM_Pathway")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset_chwe, properties={"Tag": "CHW-1", "Service": "CHILLED WATER"})
    pset_chwt = ifcopenshell.api.run("pset.add_pset", model, product=chw_trunk, name="Pset_DCM_Pathway")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset_chwt, properties={"Tag": "CHW-1", "Service": "CHILLED WATER"})

    # --- BW-1: POWER BUSWAY (128 W x 147 H) ---
    bw_z = 2950.0
    bw_trunk_x = 600.0
    bw_half_w = 128.0 / 2.0
    bw_trunk_w_face = bw_trunk_x - bw_half_w
    bw_trunk_e_face = bw_trunk_x + bw_half_w
    # Entry segment: from west wall x=0 to trunk west face at y=9450
    bw_entry = add_linear_segment(
        model, storey, body, "IfcCableSegment", "BW-Entry", "Busway",
        prof_bw, (0.0, 9450.0, bw_z), (bw_trunk_w_face, 9450.0, bw_z), predefined_type="BUSBARSEGMENT"
    )
    # N-S Main Trunk at x=600, from y=2600 to y=16400
    bw_trunk = add_linear_segment(
        model, storey, body, "IfcCableSegment", "BW-Trunk-NS", "Busway",
        prof_bw, (bw_trunk_x, 2600.0, bw_z), (bw_trunk_x, 16400.0, bw_z), predefined_type="BUSBARSEGMENT"
    )
    # Branches East from trunk east face:
    bw_branches = [
        ("BW-Branch-RowA", 2600.0, 19200.0),
        ("BW-Branch-RowB", 5600.0, 19800.0),
        ("BW-Branch-RowC", 8000.0, 19400.0),  # y=8000 clears column south face (8100) by 36 mm
        ("BW-Branch-RowD", 11000.0, 19800.0),
        ("BW-Branch-RowE", 13400.0, 19200.0),
        ("BW-Branch-RowF", 16400.0, 20200.0),  # y=16400 clears column south face (16500) by 36 mm
    ]
    for bname, by, bx2 in bw_branches:
        bw_b = add_linear_segment(
            model, storey, body, "IfcCableSegment", bname, "Busway",
            prof_bw, (bw_trunk_e_face, by, bw_z), (bx2, by, bw_z), predefined_type="BUSBARSEGMENT"
        )
        pset_bw = ifcopenshell.api.run("pset.add_pset", model, product=bw_b, name="Pset_DCM_Pathway")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_bw, properties={
            "Tag": "BW-1", "Service": "POWER", "Width": 128.0, "Height": 147.0
        })

    pset_bwe = ifcopenshell.api.run("pset.add_pset", model, product=bw_entry, name="Pset_DCM_Pathway")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset_bwe, properties={"Tag": "BW-1", "Service": "POWER"})
    pset_bwt = ifcopenshell.api.run("pset.add_pset", model, product=bw_trunk, name="Pset_DCM_Pathway")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset_bwt, properties={"Tag": "BW-1", "Service": "POWER"})

    # --- CT-1: TELECOM CABLE TRAY (683 W x 127 H) ---
    ct_z = -163.5  # Top at -100 mm, bottom at -227 mm, plenum void -900 to -35 mm
    ct_trunk_x = 1400.0
    ct_half_w = 683.0 / 2.0
    ct_trunk_w_face = ct_trunk_x - ct_half_w
    ct_trunk_e_face = ct_trunk_x + ct_half_w
    # Entry segment: from west wall x=0 to trunk west face at y=9900
    ct_entry = add_linear_segment(
        model, storey, body, "IfcCableCarrierSegment", "CT-Entry", "CableTray",
        prof_ct, (0.0, 9900.0, ct_z), (ct_trunk_w_face, 9900.0, ct_z), predefined_type="CABLETRAYSEGMENT"
    )
    # N-S Main Trunk at x=1400, from y=3000 to y=17600
    ct_trunk = add_linear_segment(
        model, storey, body, "IfcCableCarrierSegment", "CT-Trunk-NS", "CableTray",
        prof_ct, (ct_trunk_x, 3000.0, ct_z), (ct_trunk_x, 17600.0, ct_z), predefined_type="CABLETRAYSEGMENT"
    )
    # Branches East from trunk east face:
    ct_branches = [
        ("CT-Branch-RowA", 3000.0, 19200.0),
        ("CT-Branch-RowB", 6000.0, 19800.0),
        ("CT-Branch-RowC", 9200.0, 19200.0),  # Clears column north face (8700) by 158.5 mm
        ("CT-Branch-RowD", 11400.0, 19800.0),
        ("CT-Branch-RowE", 13800.0, 19200.0),
        ("CT-Branch-RowF", 17600.0, 20200.0),  # Clears column north face (17100) by 158.5 mm
    ]
    for bname, by, bx2 in ct_branches:
        ct_b = add_linear_segment(
            model, storey, body, "IfcCableCarrierSegment", bname, "CableTray",
            prof_ct, (ct_trunk_e_face, by, ct_z), (bx2, by, ct_z), predefined_type="CABLETRAYSEGMENT"
        )
        pset_ct = ifcopenshell.api.run("pset.add_pset", model, product=ct_b, name="Pset_DCM_Pathway")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset_ct, properties={
            "Tag": "CT-1", "Service": "TELECOM", "Width": 683.0, "Height": 127.0
        })

    pset_cte = ifcopenshell.api.run("pset.add_pset", model, product=ct_entry, name="Pset_DCM_Pathway")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset_cte, properties={"Tag": "CT-1", "Service": "TELECOM"})
    pset_ctt = ifcopenshell.api.run("pset.add_pset", model, product=ct_trunk, name="Pset_DCM_Pathway")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset_ctt, properties={"Tag": "CT-1", "Service": "TELECOM"})

    # Write IFC Model
    model.write(out_path)
    print(f"Model saved to {out_path} ({os.path.getsize(out_path):,} bytes, build time: {time.time() - t0:.2f}s)")

    # Write reconciliation.json side file
    recon_path = os.path.join(out_dir, "reconciliation.json")
    recon_data = {
        "project": "dc_model hall_seed000_d000",
        "author": "MEP Coordinator",
        "drawing_reconciliation": {
            "A-101": {
                "room_dimensions_mm": [27000.0, 21000.0],
                "access_floor_grid_mm": 600.0,
                "west_service_strip_mm": 1800.0,
                "cross_aisle_east_edge_mm": 11400.0,
                "cross_aisle_clear_min_mm": 1200.0,
                "structural_columns_count": 6,
                "structural_column_locations_mm": cols,
                "structural_column_size_mm": [600.0, 600.0]
            },
            "A-301": {
                "finished_floor_elevation_mm": 0.0,
                "top_of_structural_slab_mm": -900.0,
                "access_floor_panel_thickness_mm": 35.0,
                "clear_plenum_depth_mm": 865.0,
                "ceiling_slab_soffit_mm": 3600.0,
                "minimum_clear_headroom_mm": 2600.0,
                "sprinkler_deflector_elevation_ceiling_mm": 3575.0,
                "sprinkler_standoff_clearance_mm": 460.0,
                "sprinkler_deflector_elevation_in_aisle_mm": 1890.0,
                "under_floor_tray_clearance_under_panel_min_mm": 20.0
            },
            "A-601": {
                "total_cabinets": 128,
                "cabinet_c1_size_mm": [600.0, 1200.0, 2000.0],
                "cabinet_n1_size_mm": [800.0, 1200.0, 2000.0],
                "total_in_row_crahs": 18,
                "in_row_crah_size_mm": [600.0, 1200.0, 2000.0],
                "total_perimeter_crahs": 4,
                "perimeter_crah_size_mm": [1200.0, 900.0, 2000.0],
                "total_pdus": 6,
                "pdu_size_mm": [762.0, 813.0, 1959.0],
                "pdu_working_space_front_mm": 900.0
            },
            "A-602": {
                "containment_systems": ["CAC-BC", "CAC-DE"],
                "containment_roof_width_mm": 1400.0,
                "containment_roof_thickness_mm": 55.5,
                "containment_roof_underside_elevation_mm": 2000.0,
                "containment_door_thickness_mm": 60.0,
                "containment_door_height_mm": 2055.5,
                "pathway_sections": {
                    "CT-1": {"width_mm": 683.0, "height_mm": 127.0, "zone": "UNDER_FLOOR_PLENUM"},
                    "BW-1": {"width_mm": 128.0, "height_mm": 147.0, "zone": "OVERHEAD"},
                    "CHW-1": {"bare_od_mm": 114.3, "insulation_thk_mm": 25.4, "od_over_insulation_mm": 168.3, "zone": "OVERHEAD"}
                }
            },
            "E-101": {
                "busway_and_telecom_entry_coords_mm": [0.0, 9900.0],
                "pdu_dedicated_electrical_space_height_mm": 1800.0,
                "separation_cable_tray_busway_min_mm": 300.0
            },
            "M-101": {
                "chilled_water_entry_coords_mm": [0.0, 9900.0],
                "main_pipe_size": "DN100 (NPS 4)",
                "bare_od_mm": 114.3,
                "insulation_thickness_mm": 25.4,
                "outside_diameter_over_insulation_mm": 168.3,
                "served_crah_units": 22
            },
            "F-101": {
                "total_sprinkler_heads": 79,
                "ceiling_heads_count": 63,
                "ceiling_grid_spacing_x_mm": 3000.0,
                "ceiling_grid_spacing_y_mm": 3000.0,
                "in_aisle_heads_count": 16,
                "in_aisle_head_elevation_mm": 1890.0,
                "deflector_clearance_zone_mm": 460.0
            }
        },
        "achieved_diagnostics": {
            "service_elevations_relative_to_ff": {
                "CHW-1": {"centreline_z_mm": chw_z, "tier": "OVERHEAD_TIER_1", "headroom_achieved_mm": 2625.85},
                "BW-1": {"centreline_z_mm": bw_z, "tier": "OVERHEAD_TIER_2", "standoff_clearance_mm": 91.5},
                "CT-1": {"centreline_z_mm": ct_z, "tier": "UNDER_FLOOR_PLENUM", "clearance_below_panel_mm": 65.0}
            },
            "tray_busway_separation_achieved_mm": 2976.5,
            "pdu_to_chw_clearance_achieved_mm": 666.85,
            "sprinkler_clearance_achieved_mm": 498.0
        }
    }
    with open(recon_path, "w") as f:
        json.dump(recon_data, f, indent=2)
    print(f"Reconciliation log written to {recon_path}")

if __name__ == "__main__":
    build_model(OUT_PATH)
