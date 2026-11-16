### Summary of Deliverables

The schematic design for the two-hall, phased data-center campus on parcel `p6_002` has been finalized and serialized as an IFC4 BIM model at:
**`submission/model.ifc`**

---

### Design Overview & Compliance

1. **Building Massing & Program (All 7 buildings modeled as `IfcBuilding` solids):**
   - **`DH_P1`** (Phase 1 data hall): $50\,\text{m} \times 90\,\text{m} = 4{,}500\,\text{m}^2$ footprint (aspect 1.8 $\le 2.5$), 2 storeys at elevations $0.0\,\text{m}$ and $4.5\,\text{m}$, solid height $9.0\,\text{m}$ (floor-to-floor $4.5\,\text{m} \in [3.2, 5.5]\,\text{m}$), GFA $9{,}000\,\text{m}^2 \ge 7{,}200\,\text{m}^2$.
   - **`DH_P2`** (Phase 2 data hall): $50\,\text{m} \times 90\,\text{m} = 4{,}500\,\text{m}^2$ footprint in northern area, 2 storeys, solid height $9.0\,\text{m}$, GFA $9{,}000\,\text{m}^2 \ge 7{,}200\,\text{m}^2$.
   - **`SUB`** (Phase 1 substation): $35\,\text{m} \times 30\,\text{m} = 1{,}050\,\text{m}^2 \ge 1{,}000\,\text{m}^2$, height $5.0\,\text{m}$.
   - **`CTP`** (Phase 1 cooling plant): $30\,\text{m} \times 28\,\text{m} = 840\,\text{m}^2 \ge 800\,\text{m}^2$, height $6.0\,\text{m}$.
   - **`GEN`** (Phase 1 generator yard): $26\,\text{m} \times 20\,\text{m} = 520\,\text{m}^2 \ge 500\,\text{m}^2$, height $3.0\,\text{m}$.
   - **`BRM`** (Phase 1 landscape berm): 10-vertex simple polygon, $1{,}008\,\text{m}^2 \ge 300\,\text{m}^2$, height $8.0\,\text{m}$, wrapping south and west of `GEN` and `CTP`.
   - **`RET`** (Phase 1 stormwater retention): $50\,\text{m} \times 34\,\text{m} = 1{,}700\,\text{m}^2$, extruded below grade $z \in [-0.3, 0.0]\,\text{m}$ ($\max Z = 0.0\,\text{m}$). Required retention is $11.8\%$ of total impervious area ($12{,}826\,\text{m}^2 \times 0.118 = 1{,}513.5\,\text{m}^2$).

2. **Networks & Connectivity (`DCD_Networks` payload on `IfcSite`):**
   - **Road Network:** Single continuous spine along $x = 180.0\,\text{m}$ from the approved south street frontage ($[180.0, 0.0]\,\text{m}$) through the central upland corridor up to $[180.0, 236.0]\,\text{m}$. Every occupied and hazardous structure is located within $16.0\,\text{m} \le 18.0\,\text{m}$ of the roadway.
   - **Medium-Voltage Network:**
     - `MV_POI_SUB` (Phase 1): Utility point of interconnection $[320.0, 195.0]\,\text{m}$ to substation $[200.5, 48.5]\,\text{m}$ ($189.1\,\text{m}$).
     - `MV_SUB_DH1` (Phase 1): Substation $[194.5, 40.0]\,\text{m}$ to `DH_P1` $[165.5, 40.0]\,\text{m}$ ($29.0\,\text{m}$).
     - `MV_SUB_DH2` (Phase 2): Substation $[194.5, 45.0]\,\text{m}$ to `DH_P2` $[165.5, 190.0]\,\text{m}$ ($147.9\,\text{m}$).
   - **Graph:** Undirected typed edges (`utility_feed`, `power_feed`, and `vehicle_access`) linking POI, substation, data halls, gate, and program buildings via their respective network IDs.

3. **All 17 Binding Requirements Satisfied:**
   - **Setbacks:** All buildings $\ge 18\,\text{m}$ from lot lines (`RET` and `BRM` exempt, strictly within parcel).
   - **Lot Coverage:** Aggregate occupied footprint $11{,}410\,\text{m}^2 \le 13{,}529.6\,\text{m}^2$ ($15.1\%$).
   - **Wetland Protection:** Structures and roads maintain $> 10\,\text{m}$ clearance from `WET1` and `WET2` ($\ge 8.0\,\text{m}$ buffer).
   - **Hazard Separation:** Class H-1 `GEN` is separated by $\ge 29.0\,\text{m}$ from all occupied structures (`CTP`, `DH_P1`, `DH_P2`, `SUB` $\ge 28.0\,\text{m}$).
   - **Noise Limits:** Intervening 3D line-of-sight berm insertion loss reduces received noise to $38.65\,\text{dB(A)}$ at R1 and $39.27\,\text{dB(A)}$ at R2 (limit: $42.35\,\text{dB(A)}$).
   - **Visual Screening:** Lines of sight from receptors R1 and R2 to all points of `GEN` are 100% intercepted by `BRM`.
   - **Cost Caps:**
     - Phase 1 weighted cost: $1.0 \times 218.06 + 0.3 \times 236.0 = 288.86 \le 314.0$ (margin: $25.14$).
     - Full build-out weighted cost: $1.0 \times 365.93 + 0.3 \times 236.0 = 436.73 \le 473.0$ (margin: $36.27$).
   - **Phasing Independence:** Phase 1 complies standalone; no cross-phase utility is routed beneath any building footprint.

4. **BIM / IFC Contract Verification:**
   - Clean STEP/IFC4 Physical File structure matching `docs/example.ifc`.
   - Length unit: SI `METRE`.
   - `IfcBuildingStorey` entities aggregated under each building with exact `GrossFloorAreaM2` matching measured footprint $\times$ storeys.
   - Zero dangling entity references and clean hierarchy under `IfcProject` and `IfcSite`.