import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_memo():
    doc = docx.Document()

    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Helper function for headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.bold = True
        run.font.color.rgb = RGBColor(0x00, 0x33, 0x66) # Deep Navy
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12.5)
        run.bold = True
        run.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.bold = True
        run.italic = True
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    # Header / Title Block
    header_p = doc.add_paragraph()
    header_p.paragraph_format.space_after = Pt(2)
    r_hdr1 = header_p.add_run("THE CFD MECHANICAL ENGINEER, LLC\n")
    r_hdr1.bold = True
    r_hdr1.font.size = Pt(14)
    r_hdr1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    r_hdr2 = header_p.add_run("4820 E River Rd, Suite 220, Tucson, AZ 85718 | Engineering Simulation & Thermal Physics")
    r_hdr2.font.size = Pt(9.5)
    r_hdr2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # Memo metadata table
    tbl_meta = doc.add_table(rows=6, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_meta, color="003366", sz="8", val="single")

    meta_data = [
        ("TO:", "Marguerite Falk, PE — Technical Director & Reviewing Engineer (AZ PE #42798)"),
        ("FROM:", "Gordon Selby, PE — Owner & Principal Engineer (AZ PE #48213)"),
        ("DATE:", "October 10, 2025 (10/10/2025)"),
        ("PROJECT:", "CFDME-2025-041 — Ocotillo Additive Structures WUI Wildfire Exposure, Phase 1"),
        ("DELIVERABLE:", "Phase 1 Draft Report rev B — Section 7 Validation Memo & Peer Review Closure"),
        ("SUBJECT:", "ASTM E119 Companion Simulation Validation Assessment, Model-Error Rollup (ASME V&V 20), Diagnostic Thermal-Bridge Evaluation, Wildfire Scope Boundaries, and Peer-Review Checklist Disposition")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = tbl_meta.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(1.4)
        cell_val.width = Inches(5.1)
        
        p_l = cell_lbl.paragraphs[0]
        p_l.paragraph_format.space_after = Pt(2)
        r_l = p_l.add_run(label)
        r_l.bold = True
        r_l.font.size = Pt(10)
        r_l.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

        p_v = cell_val.paragraphs[0]
        p_v.paragraph_format.space_after = Pt(2)
        r_v = p_v.add_run(val)
        r_v.font.size = Pt(10)
        if label == "SUBJECT:":
            r_v.bold = True

        set_cell_background(cell_lbl, "F0F4F8")
        set_cell_background(cell_val, "FAFAFA")
        set_cell_margins(cell_lbl, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_val, top=60, bottom=60, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------------------------
    # SECTION 1
    # ---------------------------------------------------------------------------
    add_h1("1. Purpose, Executive Summary & Client Communication")

    p = doc.add_paragraph()
    p.add_run(
        "This validation memorandum responds directly to your review of the Phase 1 draft report (CFDME-2025-041 rev B) "
        "and resolves the Section 7 placeholder. It provides a definitive, standards-governed evaluation of whether the "
        "ASTM E119 companion simulation validated against the physical test of record for the Ocotillo Additive Structures "
        "(OAS) 305 mm double-wythe 3D-printed concrete cavity wall assembly. Per your direction, this evaluation is "
        "conducted strictly from the artifacts existing on the firm file server as of today, October 10, 2025 (10/10/2025), "
        "including the companion simulation results (E119_companion_sim_results.csv), the certified third-party laboratory test report "
        "(Red Butte report RBFMT-25-0918, dated 09/24/2025), the professional certification memorandum (Ironwood Fire Protection "
        "Engineering memo IWFPE-CERT-25-0374, dated 09/29/2025), client correspondence and amended figures transmitted by Bianca Rennert "
        "on 10/09/2025 (burn_data_original_vs_revised.csv), and the dimensioned architectural wall assembly drawing "
        "(OAS_wall_assembly_section.png). No new simulation runs or physical tests were commissioned, and no changes were made to file server contents."
    )

    p = doc.add_paragraph()
    r = p.add_run("Executive Determination: ")
    r.bold = True
    p.add_run(
        "The companion simulation DOES NOT VALIDATE against the certified physical test under our governing quality procedure "
        "(CFDME-QA-VAL-002 rev 2). With the certified experimental endurance established as D = 118 min and the companion simulation "
        "predicting S = 131 min under the governing single-point rise criterion, the comparison error is E = +13 min (+11.0% of D). "
        "This error exceeds both the firm's primary percentage-of-D acceptance tolerance (|E| ≤ 10% of D = 11.8 min) and the combined "
        "validation uncertainty (u_val = ±9 min). Under ASME V&V 20 and firm QA rules, because |E| > u_val, the discrepancy is resolved "
        "as an actionable model error rather than measurement noise. Furthermore, Bianca Rennert's proposed figure of 129 min cannot "
        "be adopted because client-amended numbers lacking laboratory reissuance and calibration certificates are strictly inadmissible. "
        "Consequently, Ocotillo cannot describe the simulation as validated in its Friday product launch materials, nor can it claim a "
        "validated 2-hour rating."
    )

    add_h2("1.1 Recommended Transmittal Text for Bianca Rennert (Ocotillo Additive Structures)")
    p = doc.add_paragraph()
    p.add_run(
        "The following standalone paragraph is provided for you to transmit directly to Bianca Rennert, VP of Product Marketing "
        "at Ocotillo Additive Structures, in response to her October 9, 2025 inquiry:"
    )

    # Callout box for Bianca's paragraph
    tbl_callout = doc.add_table(rows=1, cols=1)
    tbl_callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = tbl_callout.rows[0].cells[0]
    c_cell.width = Inches(6.5)
    set_cell_background(c_cell, "F9F9F9")
    set_cell_margins(c_cell, top=140, bottom=140, left=180, right=180)

    tcPr = c_cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p_c = c_cell.paragraphs[0]
    p_c.paragraph_format.space_after = Pt(0)
    p_c.paragraph_format.line_spacing = 1.15
    r_c_bold = p_c.add_run("Draft Transmittal to Bianca Rennert (10/10/2025):\n")
    r_c_bold.bold = True
    r_c_text = p_c.add_run(
        "\"Bianca: Under our firm QA procedures and ASME V&V 20 guidelines, we cannot state that the E119 companion simulation "
        "has validated against the physical test for Ocotillo's launch materials, and the simulation results cannot be used to claim "
        "a validated 2-hour rating. Our validation procedure strictly requires that experimental reference data be drawn from the "
        "certified third-party laboratory report of record (Red Butte Report No. RBFMT-25-0918), which establishes the governing "
        "single-point endurance at 118 min. Informal post-test thermocouple calibration adjustments cannot be adopted without a formal "
        "amended test report and calibration certificate issued directly by Red Butte; substituting uncertified figures would invalidate "
        "our professional review. Against the certified 118 min test endurance, our simulation predicts a governing single-point "
        "endurance of 131 min, yielding a comparison error of +13 min (+11.0%). This exceeds our mandatory 10% acceptance tolerance "
        "(11.8 min) as well as our validation uncertainty (±9 min), establishing a resolved model error that requires technical "
        "remediation. Furthermore, professional engineering standards prohibit extrapolating an ASTM E119 furnace endurance rating to "
        "a wildland-urban interface (WUI) wildfire survival claim; E119 is a comparative building compartment fire exposure rather than "
        "a transient, wind-driven vegetation fire. Formal validation of wildfire performance must await physical test data from the "
        "confirmatory testing window scheduled at Red Butte on 10/27/2025. Finally, official certification or modification of assembly "
        "fire-resistance ratings remains reserved exclusively to the fire-protection professional engineer of record (Ironwood Fire "
        "Protection Engineering). Consequently, launch materials should rely solely on Ironwood's certified 1-hour rating and must avoid "
        "unsubstantiated claims of simulation validation or 2-hour performance.\""
    )
    r_c_text.italic = True
    r_c_text.font.size = Pt(10.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ---------------------------------------------------------------------------
    # SECTION 2
    # ---------------------------------------------------------------------------
    add_h1("2. Assembly Identity & Scope of Certification")

    p = doc.add_paragraph()
    r = p.add_run("2.1 Definitive Settlement of Assembly Identity\n")
    r.bold = True
    p.add_run(
        "I have conducted a thorough cross-examination of all physical test records, professional certification documents, "
        "architectural drawings, and engineering CAD case files on the file server. On the basis of this audit, I settle that "
        "the physical wall assembly modeled in the companion simulation run IS THE IDENTICAL ASSEMBLY covered by the Ironwood "
        "certification memorandum (IWFPE-CERT-25-0374) and tested in Red Butte Report No. RBFMT-25-0918."
    )

    p = doc.add_paragraph()
    r = p.add_run("2.2 Evidentiary Foundation of Assembly Identity\n")
    r.bold = True
    p.add_run("This determination rests upon the convergence of four independent, authoritative technical artifacts:\n")

    p1 = doc.add_paragraph(style='List Bullet')
    r = p1.add_run("Ironwood Certification Memo (IWFPE-CERT-25-0374, dated 09/29/2025): ")
    r.bold = True
    p1.add_run(
        "Signed and sealed by Marla Kettering, PE (AZ PE #45106). Section 1.2 specifies a 305 mm double-wythe printed concrete wall "
        "comprising two 50 mm siliceous-aggregate leaves, a 205 mm open-air unfilled cavity (no insulation, membrane, or fill), "
        "and continuous 9-gauge (3.8 mm diameter) galvanized steel truss-type ties spaced 600 mm on-center vertically with 25 mm "
        "embedment into each leaf. Section 1.2 concludes: 'Any deviation from the tabulated geometry places the assembly outside the scope of this certification.'"
    )

    p2 = doc.add_paragraph(style='List Bullet')
    r = p2.add_run("Red Butte Test Report (RBFMT-25-0918, dated 09/24/2025): ")
    r.bold = True
    p2.add_run(
        "Signed by Glen Whitfield, Laboratory Manager. Section 2 records the testing of one 3.05 m × 3.05 m (10 ft × 10 ft) non-load-bearing "
        "specimen constructed to the identical geometry: two 50 mm siliceous-aggregate printed leaves, 205 mm open-air cavity, 305 mm overall thickness, "
        "and continuous 9-gauge (3.8 mm) galvanized steel truss-type wire ties placed at 600 mm vertical courses with 25 mm embedment."
    )

    p3 = doc.add_paragraph(style='List Bullet')
    r = p3.add_run("Dimensioned Assembly Drawing (OAS_wall_assembly_section.png): ")
    r.bold = True
    p3.add_run(
        "Prepared by the Ocotillo Additive Structures design team, titled 'PRINTED WALL ASSEMBLY SECTION — 305 mm DOUBLE-WYTHE CAVITY SYSTEM', "
        "dated 09/15/2025, Drawing Rev A. In Detail A (Horizontal Section), Detail B (Vertical Elevation), and the Tie Schedule, the drawing explicitly "
        "labels: Outer Printed Concrete Leaf = 50 mm, Air Cavity = 205 mm (unfilled, open — no insulation), Inner Printed Concrete Leaf = 50 mm, "
        "Overall Thickness = 305 mm, Tie Material = 9-gauge (3.8 mm) galvanized steel, Tie Type = Truss-type continuous triangular zigzag diagonals, "
        "Vertical Spacing = 600 mm on-center, and Embedment = 25 mm each leaf. The title block carries Assembly ID OAS-WA-305mm-DW."
    )

    p4 = doc.add_paragraph(style='List Bullet')
    r = p4.add_run("Engineering CAD Geometry of Record and Case Build Logs: ")
    r.bold = True
    p4.add_run(
        "The meshing log (/Projects/CFDME-2025-041_Ocotillo_WUI/Case/logs/log.snappyHexMesh_20251009.txt) confirms that snappyHexMesh was executed "
        "on the morning of 10/09/2025 at 07:14:22 MST using source geometry OAS-WUI-01_revC.FCStd (SHA-256: a4f2c8b91d3e5f7a...). Phase 1 draft "
        "report rev B §3.4–§3.5 and scoping memo rev A §6 explicitly crosswalk the architectural drawing identifier OAS-WA-305mm-DW to the CAD geometry "
        "OAS-WUI-01_revC, confirming they describe the identical physical entity."
    )

    # Assembly Comparison Table
    add_h3("Table 2.1 — Cross-Artifact Assembly Parameter Verification")
    tbl_asm = doc.add_table(rows=9, cols=5)
    tbl_asm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_asm)

    asm_headers = ["Parameter", "Ironwood Cert §1.2", "Red Butte Lab §2", "OAS Drawing Rev A", "Companion Run (revC)"]
    for c_idx, h in enumerate(asm_headers):
        cell = tbl_asm.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        set_cell_background(cell, "E6ECF2")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    asm_rows = [
        ("Outer Leaf Thickness", "50 mm", "50 mm", "50 mm", "50 mm"),
        ("Inner Leaf Thickness", "50 mm", "50 mm", "50 mm", "50 mm"),
        ("Cavity Width (Open Air)", "205 mm", "205 mm", "205 mm", "205 mm"),
        ("Overall Thickness", "305 mm", "305 mm", "305 mm", "305 mm"),
        ("Concrete Aggregate", "Siliceous", "Siliceous", "Siliceous (k=1.4 W/m·K)", "Siliceous (temp-dep)"),
        ("Tie Material / Profile", "Galv. Steel, Truss", "Galv. Steel, Truss", "9-ga (3.8 mm) Galv. Truss", "Galv. Steel (k=45 W/m·K)"),
        ("Tie Vertical Spacing", "600 mm o.c.", "600 mm o.c.", "600 mm o.c.", "600 mm o.c."),
        ("Tie Embedment per Leaf", "25 mm", "25 mm", "25 mm", "25 mm")
    ]

    for r_idx, row_vals in enumerate(asm_rows):
        row = tbl_asm.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.bold = True
            set_cell_margins(cell, top=40, bottom=40, left=80, right=80)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    p = doc.add_paragraph()
    r = p.add_run("2.3 Geometry Revision Audit: Disposition on Revision D\n")
    r.bold = True
    p.add_run(
        "On the afternoon of October 9, 2025 at 16:12 MST, Trevor Buckhalter transmitted an updated FreeCAD file, OAS-WUI-01_revD.FCStd, "
        "which added a 610 mm continuous hollow parapet (bringing total wall height to 3355 mm) with a 50 mm coping cap and 25 mm drip overhang. "
        "I confirm that the companion simulation and the mesh study of record were built exclusively from OAS-WUI-01_revC on the morning of "
        "October 9, prior to receipt of revD. Revision C represents the planar 3.05 m × 3.05 m vertical panel tested at Red Butte and certified "
        "by Ironwood. The parapet in revD represents architectural scoping for future roofline junctions and is not part of the certified E119 "
        "specimen. Retaining revC as the basis of record is physically correct and preserves geometric identity with the test."
    )

    # ---------------------------------------------------------------------------
    # SECTION 3
    # ---------------------------------------------------------------------------
    add_h1("3. Companion Simulation Results & Crossing Times")

    p = doc.add_paragraph()
    r = p.add_run("3.1 Governing Standard & Unexposed-Face Criteria\n")
    r.bold = True
    p.add_run(
        "Per ASTM E119 Section 8 and External Standards Digest Section 1, fire endurance for a non-load-bearing wall assembly is evaluated "
        "against two thermal-transmission criteria on the unexposed face, measured as temperature rise above the initial ambient temperature "
        "(T_amb = 21.0 °C):\n"
    )
    p_c1 = doc.add_paragraph(style='List Bullet')
    r = p_c1.add_run("Average Unexposed-Face Rise Criterion: ")
    r.bold = True
    p_c1.add_run("Temperature rise across the nine symmetrically disposed thermocouples shall not exceed 139.0 °C (250.0 °F) above initial ambient. Limiting absolute temperature = 21.0 °C + 139.0 °C = 160.0 °C.")

    p_c2 = doc.add_paragraph(style='List Bullet')
    r = p_c2.add_run("Single-Point Unexposed-Face Rise Criterion: ")
    r.bold = True
    p_c2.add_run("Temperature rise at any individual thermocouple location shall not exceed 181.0 °C (325.0 °F) above initial ambient. Limiting absolute temperature = 21.0 °C + 181.0 °C = 202.0 °C.")

    p = doc.add_paragraph()
    p.add_run(
        "ASTM E119 mandates that the earlier of the two criteria governs the reported fire endurance. It is neither the later of the two, "
        "nor an average, nor an interpolation between them."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.2 Continuous Crossing Times vs. Tripping Discrete Samples\n")
    r.bold = True
    p.add_run(
        "Per your explicit instruction and sound numerical practice, endurances in this memorandum are determined from continuous "
        "crossing times obtained by linear interpolation between output time steps, rather than discrete samples that trip the limit. "
        "In the companion simulation output (E119_companion_sim_results.csv), data is written at 1 min increments from t = 0 min to t = 180 min:\n"
    )

    p_step1 = doc.add_paragraph(style='List Bullet')
    r = p_step1.add_run("Single-Point Maximum Temperature (T_unexposed_max_C):\n")
    r.bold = True
    p_step1.add_run(
        "At t = 130 min, T_max = 200.5 °C (rise = 179.5 °C).\n"
        "At t = 131 min, T_max = 202.1 °C (rise = 181.1 °C).\n"
        "The 202.0 °C threshold falls between 130 min and 131 min. Linear interpolation yields:\n"
        "t_cross,single = 130 min + [(202.0 °C − 200.5 °C) / (202.1 °C − 200.5 °C)] × (131 min − 130 min)\n"
        "t_cross,single = 130 min + (1.5 °C / 1.6 °C) × 1 min = 130 min + 0.9375 min = 130.94 min.\n"
        "Rounded to the nearest minute per procedure: t_single = 131 min. (Note: The discrete sample tripping the threshold is also 131 min)."
    )

    p_step2 = doc.add_paragraph(style='List Bullet')
    r = p_step2.add_run("Average Unexposed-Face Temperature (T_unexposed_avg_C):\n")
    r.bold = True
    p_step2.add_run(
        "At t = 176 min, T_avg = 159.9 °C (rise = 138.9 °C).\n"
        "At t = 177 min, T_avg = 160.9 °C (rise = 139.9 °C).\n"
        "The 160.0 °C threshold falls between 176 min and 177 min. Linear interpolation yields:\n"
        "t_cross,avg = 176 min + [(160.0 °C − 159.9 °C) / (160.9 °C − 159.9 °C)] × (177 min − 176 min)\n"
        "t_cross,avg = 176 min + (0.1 °C / 1.0 °C) × 1 min = 176 min + 0.1000 min = 176.10 min.\n"
        "Rounded to the nearest minute per procedure: t_avg = 176 min. (Note: The discrete sample tripping the threshold is 177 min, demonstrating why continuous crossing calculation is required)."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.3 Governing Criterion & Confirmation of Section 7 Stub Prediction\n")
    r.bold = True
    p.add_run(
        "Comparing the two crossing times, the single-point rise criterion is reached at 131 min (130.94 min), which occurs 45 min earlier "
        "than the average-rise criterion at 176 min (176.10 min). Therefore, the single-point rise criterion GOVERNS the simulation endurance.\n"
        "Governing simulation endurance prediction: S = 131 min.\n"
        "Disposition on Phase 1 draft report rev B Section 7 stub: The prediction stated in the Section 7 stub "
        "('Companion simulation predicts S = 131 min for the ASTM E119 exposure') STANDS FULLY CONFIRMED. It is numerically exact and requires no change."
    )

    # ---------------------------------------------------------------------------
    # SECTION 4
    # ---------------------------------------------------------------------------
    add_h1("4. Certified Experimental Reference Value (D) & Client-Amended Figure")

    p = doc.add_paragraph()
    r = p.add_run("4.1 Adoption of the Certified Experimental Value (D)\n")
    r.bold = True
    p.add_run(
        "Under Section 6 of CFDME Validation QA Procedure (CFDME-QA-VAL-002 rev 2), experimental data D must be drawn strictly from the "
        "certified third-party test report of record. The governing experimental reference value adopted for this validation is:\n"
        "D = 118 min\n"
        "This value is taken directly from Section 5.2 and Section 5.3 of Red Butte Report No. RBFMT-25-0918 (test date 09/24/2025, issued 09/24/2025). "
        "In the physical test, the single-point rise criterion of 181.0 °C was reached at 118 min at thermocouple TC-6 (which was positioned directly "
        "over a continuous 3.8 mm horizontal steel tie course), while the nine-thermocouple average rise reached its 139.0 °C limit later at 163 min. "
        "The single-point criterion reached at 118 min governs the certified endurance of record, and forms the sole legal basis of Ironwood's "
        "certification memorandum (IWFPE-CERT-25-0374)."
    )

    p = doc.add_paragraph()
    r = p.add_run("4.2 Disposition on Bianca Rennert's Proposed Figure (129 min)\n")
    r.bold = True
    p.add_run(
        "In her transmittal of October 9, 2025 (burn_data_original_vs_revised.csv and accompanying correspondence), Bianca Rennert, VP of Product "
        "Marketing at Ocotillo, asserted a revised single-point endurance of 129 min, stating: 'After we walked through TC-6's response with our "
        "thermocouple vendor, we're applying a post-test calibration correction that puts the single-point endurance at 129 min. That aligns much "
        "more closely with your simulation's 131 min, and internally we're treating that as a validation.'\n\n"
        "Disposition: Bianca Rennert's figure of 129 min is FORMALLY REJECTED AND DISALLOWED from use in any CFD ME engineering deliverable. "
        "Under Section 6 of our Validation QA Procedure, client-amended figures may not be substituted for D under any circumstances absent "
        "three mandatory conditions:\n"
    )

    p_cond1 = doc.add_paragraph(style='List Bullet')
    p_cond1.add_run("A reissued test report from the testing laboratory of record (Red Butte Fire & Materials Testing), bearing the original report number with an amendment sequence (e.g., RBFMT-25-0918-R1), signed by the authorized laboratory manager (Glen Whitfield).")
    
    p_cond2 = doc.add_paragraph(style='List Bullet')
    p_cond2.add_run("An official calibration certificate covering the specific thermocouple channel (TC-6) issued by an accredited calibration authority, documenting traceable deviation data.")

    p_cond3 = doc.add_paragraph(style='List Bullet')
    p_cond3.add_run("An explicit supersession statement in the reissued laboratory report confirming that the amended value supersedes the original 118 min endurance for all downstream regulatory and engineering use.")

    p = doc.add_paragraph()
    p.add_run(
        "None of these conditions are met. Red Butte's certified report of record explicitly incorporates Certificate No. RBFMT-CAL-25-0812-TC "
        "(dated 2025-08-12), confirming NIST-traceable calibration for all ten unexposed-face thermocouples in force on the test date. An informal "
        "post-test conversation between a client and a thermocouple vendor carries zero standing under professional engineering standards. "
        "As stated in CFDME-QA-VAL-002 §6: 'D is the physical anchor of the validation; if D moves for any reason other than a documented laboratory action, "
        "the validation ceases to be against the physical test and becomes a comparison against a preferred number. The two states are indistinguishable "
        "in the report if the substitution is silent, and the record of the exercise is corrupted.' D = 118 min stands as the sole admissible value."
    )

    # ---------------------------------------------------------------------------
    # SECTION 5
    # ---------------------------------------------------------------------------
    add_h1("5. ASME V&V 20 Validation Rollup & Uncertainty Analysis")

    p = doc.add_paragraph()
    r = p.add_run("5.1 Model Error Formulation (ASME V&V 20 / CFDME-QA-VAL-002 §3)\n")
    r.bold = True
    p.add_run(
        "Per ASME V&V 20-2009 (R2016) and firm procedure CFDME-QA-VAL-002 rev 2, validation is expressed strictly as the comparison error "
        "E = S − D with its associated validation uncertainty u_val. Validation shall never be reported as a binary yes/no, pass/fail, or qualitative "
        "characterization. The sign of E is retained throughout all reporting:\n"
        "• S (simulation prediction) = 131 min (crossing time = 130.94 min)\n"
        "• D (certified experimental value) = 118 min (Red Butte report RBFMT-25-0918)\n"
        "• E (model error) = S − D = 131 min − 118 min = +13 min (+11.0% of D)\n"
        "(Evaluating from fractional crossing time gives E = 130.94 min − 118.00 min = +12.94 min, which rounds to +13 min)."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.2 Acceptance Criterion (CFDME-QA-VAL-002 §5)\n")
    r.bold = True
    p.add_run(
        "The firm's primary acceptance criterion scales with endurance: |E| ≤ 10% of D.\n"
        "Acceptance limit = 0.10 × 118.0 min = 11.8 min (limit as it falls: 11.8 min).\n"
        "Primary Acceptance Comparison:\n"
        "|E| = 13 min > 11.8 min (or |E| = 12.94 min > 11.8 min).\n"
        "The model error exceeds the firm's primary acceptance criterion by 1.2 min (1.14 min on raw crossing). "
        "The companion simulation FAILS the primary validation acceptance criterion."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.3 Validation Uncertainty Build-Up (CFDME-QA-VAL-002 §4)\n")
    r.bold = True
    p.add_run(
        "The validation uncertainty u_val is computed via root-sum-square (RSS) combination of three independent standard uncertainties:\n"
        "1. Numerical uncertainty (u_num): ±4 min (default for three-grid conjugate thermal compartment-wall studies per §4).\n"
        "2. Input uncertainty (u_inp): ±6 min (uncertainty in concrete k(T), rho, c_p, tie geometry, and furnace-side heat flux).\n"
        "3. Experimental uncertainty (u_exp): ±5 min (NIST-traceable Type-K thermocouple instrumentation and furnace control per lab SOP).\n"
        "u_val = sqrt( u_num² + u_inp² + u_exp² ) = sqrt( 4² + 6² + 5² ) = sqrt( 16 + 36 + 25 ) = sqrt( 77 ) = ±8.77 min.\n"
        "Reported to whole minutes per procedure: u_val = ±9 min."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.4 Secondary Comparison to Validation Uncertainty & Diagnostic Meaning\n")
    r.bold = True
    p.add_run(
        "Per CFDME-QA-VAL-002 §5, two secondary tests are mandatory in every rollup:\n"
        "• Secondary Comparison: |E| = 13 min vs. u_val = ±9 min (or 12.94 min vs. 8.77 min). |E| > u_val by 4 min.\n"
        "• Diagnostic Determination: Under ASME V&V 20, if |E| ≤ u_val, the discrepancy sits within combined measurement and modeling noise. "
        "However, because |E| > u_val, the discrepancy is RESOLVED AS A MODEL ERROR. It is larger than the noise floor of the exercise and "
        "constitutes an actionable engineering finding that cannot be explained away by experimental or numerical scatter.\n"
        "• Sign Evaluation: E = +13 min is positive, indicating that the simulation over-predicts assembly fire endurance (i.e., it predicts that "
        "thermal breakthrough occurs later than in the physical test). In life-safety and structural thermal design, an over-prediction of "
        "endurance is non-conservative because it overestimates the time available before critical unexposed-face temperature limits are exceeded."
    )

    p = doc.add_paragraph()
    r = p.add_run("5.5 Largest Prediction that Would Have Cleared the Criterion\n")
    r.bold = True
    p.add_run(
        "The upper bound of the acceptance band is defined by S_max = D + 0.10 × D = 118.0 min + 11.8 min = 129.8 min.\n"
        "• Limiting real value (limit as it falls): S_max = 129.8 min.\n"
        "• Largest whole-minute integer prediction clearing the criterion: S = 129 min (at S = 129 min, E = +11 min ≤ 11.8 min; at S = 130 min, E = +12 min > 11.8 min).\n"
        "Note the critical engineering irony: If the companion simulation had predicted S = 129 min (or if the model had been tuned by 2 min), "
        "it would have cleared the 10% criterion against the true physical test (D = 118 min). Conversely, Bianca Rennert sought to move D to 129 min "
        "to artificially force validation against Gordon's 131 min prediction. Both maneuvers are mathematically illustrative, but under strict QA rules, "
        "with S = 131 min and D = 118 min, the run fails validation."
    )

    # Required Single-Line Rollup Table per Section 3
    add_h3("Table 5.1 — ASME V&V 20 Validation Rollup Table (Mandatory Reporting Form)")
    tbl_val = doc.add_table(rows=2, cols=8)
    tbl_val.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_val)

    val_hdrs = ["Run ID (S)", "Test Ref (D)", "S [min]", "D [min]", "E = S − D [min]", "10% of D [min]", "u_val [min]", "Outcome / Finding"]
    for c_idx, h in enumerate(val_hdrs):
        cell = tbl_val.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        set_cell_background(cell, "003366")
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)

    val_vals = [
        "E119 Companion (OAS revC)",
        "RBFMT-25-0918 §5.2",
        "131 min (130.94)",
        "118 min",
        "+13 min (+11.0%)",
        "11.8 min",
        "±9 min (±8.77)",
        "NON-VALIDATING (|E| > 10% & > u_val; Resolved Error)"
    ]
    for c_idx, v in enumerate(val_vals):
        cell = tbl_val.rows[1].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(v)
        r.font.size = Pt(8.5)
        if c_idx == 7:
            r.bold = True
            r.font.color.rgb = RGBColor(0x99, 0x00, 0x00) # Dark red
        set_cell_margins(cell, top=50, bottom=50, left=40, right=40)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ---------------------------------------------------------------------------
    # SECTION 6
    # ---------------------------------------------------------------------------
    add_h1("6. Diagnostic Thermal-Bridge Physics & Model Rework Plan")

    p = doc.add_paragraph()
    p.add_run(
        "To diagnose why the simulation over-predicted fire endurance, we examine two diagnostic physical metrics that compare "
        "the local thermal bridging across the metallic ties against the bulk through-wall conduction:\n"
    )

    p_d1 = doc.add_paragraph()
    r = p_d1.add_run("6.1 Diagnostic Comparison 1: Temporal Separation Between Criteria (Test vs. Run)\n")
    r.bold = True
    p_d1.add_run(
        "• In Physical Test (RBFMT-25-0918): Average-rise criterion reached at t = 163 min; single-point criterion reached at t = 118 min.\n"
        "  Test Separation = 163 min − 118 min = 45 min.\n"
        "• In Companion Run (E119_companion_sim_results.csv): Average-rise crossing reached at t = 176 min (176.10 min); single-point crossing reached at t = 131 min (130.94 min).\n"
        "  Run Separation = 176 min − 131 min = 45 min (or 176.10 min − 130.94 min = 45.16 min ≈ 45 min).\n"
        "• Temporal Delta: Separation in test (45 min) vs. separation in run (45 min) = EXACT MATCH (0 min difference)."
    )

    p_d2 = doc.add_paragraph()
    r = p_d2.add_run("6.2 Diagnostic Comparison 2: Governing Point Elevation Above Nine-Point Mean at Governance\n")
    r.bold = True
    p_d2.add_run(
        "• In Physical Test (RBFMT-25-0918 §5.2): At the moment of single-point governance (t = 118 min), thermocouple TC-6 reached an unexposed-face "
        "temperature rise of 181.0 °C (absolute temperature = 202.0 °C), while the nine-thermocouple mean rise stood at approximately 96.0 °C "
        "(absolute temperature = 117.0 °C).\n"
        "  Test Elevation = 181.0 °C − 96.0 °C = 85.0 °C (85.0 K) above the nine-point mean.\n"
        "• In Companion Run (E119_companion_sim_results.csv): At continuous crossing (t = 130.94 min), T_unexposed_max_C reaches a rise of 181.0 °C "
        "(202.0 °C), while T_unexposed_avg_C sits at 110.83 °C (rise = 89.83 °C). (At the integer minute t = 131 min, T_max = 202.1 °C, rise = 181.1 °C, "
        "and T_avg = 110.9 °C, rise = 89.9 °C).\n"
        "  Run Elevation = 181.0 °C − 89.83 °C = 91.17 °C ≈ 91.2 °C (91.2 K) above the nine-point mean.\n"
        "• Elevation Delta: The governing point sits 91.2 °C above the mean in the run versus 85.0 °C in the test, a difference of only 6.2 °C (6.2 K)."
    )

    # Diagnostic Table
    add_h3("Table 6.1 — Diagnostic Comparison: Physical Test vs. Companion Simulation")
    tbl_diag = doc.add_table(rows=4, cols=4)
    tbl_diag.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_diag)

    diag_hdrs = ["Diagnostic Metric", "Physical Test (RBFMT-25-0918)", "Companion Run (revC)", "Variance / Agreement"]
    for c_idx, h in enumerate(diag_hdrs):
        cell = tbl_diag.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        set_cell_background(cell, "E6ECF2")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)

    diag_data = [
        ("Separation: Average Rise vs. Single Point", "45 min (163 min − 118 min)", "45 min (176 min − 131 min)", "0 min delta (Identical 45 min lag)"),
        ("Single-Point Elevation Above 9-TC Mean", "85.0 °C (181.0 °C − 96.0 °C)", "91.2 °C (181.0 °C − 89.8 °C)", "+6.2 °C delta (Excellent structural match)"),
        ("Uniform Time Delay Across Both Criteria", "Baseline of Record", "+13 min at Single Point\n+13 min at Average Rise", "+13 min uniform translation across full assembly")
    ]
    for r_idx, row_vals in enumerate(diag_data):
        row = tbl_diag.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    p = doc.add_paragraph()
    r = p.add_run("6.3 What the Diagnostics Say About the Model\n")
    r.bold = True
    p.add_run(
        "These two diagnostic comparisons provide profound physical insight into the model's internal formulation:\n"
        "1. The 3D conjugate thermal bridging mechanism is remarkably well-resolved. The model captures the intense localized conduction "
        "through the 3.8 mm continuous steel ties, producing a ~91 °C hot spot above the bulk unexposed face that mirrors the 85 °C hot spot "
        "observed at TC-6 in the test. Furthermore, the pacing of local tie breakthrough relative to bulk concrete heating is reproduced with "
        "exact fidelity (exactly 45 min in both test and simulation).\n"
        "2. However, the ENTIRE thermal response of the assembly is shifted later in time by a uniform +13 minute translation:\n"
        "   • Single-point criterion: Test = 118 min, Run = 131 min (Delay = +13 min).\n"
        "   • Average-rise criterion: Test = 163 min, Run = 176 min (Delay = +13 min).\n"
        "This uniform translation demonstrates that the error is not a spatial or geometric defect of the wall ties or embedment refinement, "
        "but rather a 1D through-thickness bulk thermal inertia error that retards the entire thermal wave through the concrete leaves."
    )

    p = doc.add_paragraph()
    r = p.add_run("6.4 Where the Rework Belongs\n")
    r.bold = True
    p.add_run(
        "Because the tie thermal bridging delta is physically sound, rework does NOT belong in the tie mesh or tie conduction model. "
        "Instead, the rework belongs squarely in the bulk printed concrete leaf properties and exposed-face boundary conditions:\n"
    )

    p_rw1 = doc.add_paragraph(style='List Bullet')
    r = p_rw1.add_run("Concrete Thermal Conductivity k(T): ")
    r.bold = True
    p_rw1.add_run(
        "The temperature-dependent conductivity curve for printed siliceous-aggregate concrete currently used in the case setup appears to "
        "underestimate conductivity at elevated temperatures (> 400 °C), retarding heat diffusion through the 50 mm leaves."
    )

    p_rw2 = doc.add_paragraph(style='List Bullet')
    r = p_rw2.add_run("Volumetric Heat Capacity & Moisture Desorption: ")
    r.bold = True
    p_rw2.add_run(
        "The model currently models concrete heat capacity as dry sensible energy. In the physical Red Butte test, 28-day cured printed concrete "
        "contains free and chemically bound moisture. Evaporation of pore water produces an endothermic latent heat plateau around 100–120 °C. "
        "If the model's effective specific heat c_p or moisture desorption model artificially prolongs this plateau, thermal penetration is delayed."
    )

    p_rw3 = doc.add_paragraph(style='List Bullet')
    r = p_rw3.add_run("Furnace Exposed-Face Boundary Treatment: ")
    r.bold = True
    p_rw3.add_run(
        "The radiative and convective heat flux from the ASTM E119 standard curve into the exposed leaf surface may be under-predicted due to "
        "an assumed surface emissivity (currently epsilon = 0.90) or an effective convection coefficient that transfers insufficient net heat flux "
        "during the initial 30 min of the standard fire curve."
    )

    p = doc.add_paragraph()
    r = p.add_run("6.5 Status of Model Rework on the File Server\n")
    r.bold = True
    p.add_run(
        "Has any of this rework been started yet? NO. I have audited the project directory (/Projects/CFDME-2025-041_Ocotillo_WUI/Case/) "
        "and cluster logs as of today, 10/10/2025. No rework on bulk concrete thermal conductivity, moisture enthalpy, or furnace heat flux has "
        "been initiated. The case directory contains only the original companion run, and subcontractor logs (log.solve_20251009_attempt3.txt) "
        "show that Mulshi Simulation Labs was inappropriately attempting steady RANS aerodynamic solves rather than transient thermal-conjugate "
        "model refinement. The companion simulation stands exactly as executed."
    )

    p = doc.add_paragraph()
    r = p.add_run("6.6 Engineering Implications for the Rest of Phase 1\n")
    r.bold = True
    p.add_run(
        "The non-validating E119 companion simulation carries four critical consequences for the Phase 1 deliverable:\n"
        "1. Phase 1 Report rev B Section 7 cannot claim validation. It must explicitly present the numerical rollup (S = 131 min, D = 118 min, "
        "E = +13 min, u_val = ±9 min) and report the outcome as a resolved model error finding.\n"
        "2. Non-Conservative Thermal Bias: Because the model over-predicts thermal endurance by +13 min (+11%), any unexposed-face temperature "
        "histories generated for the SOW §3.1 wildfire cases using this conjugate wall treatment will be non-conservative (i.e., predicting "
        "that interior surfaces stay cooler longer than they would in reality).\n"
        "3. Reviewer Sign-Off Withheld: Marguerite Falk, PE cannot close checklist Item 10 or sign the Phase 1 report until Section 7 is incorporated "
        "and the client agrees to release the deliverable with a documented finding or contract a rework sprint.\n"
        "4. Client Positioning Reset: Ocotillo marketing must be formally informed that no simulation validation claim or 2-hour fire endurance "
        "claim can appear in their November product launch materials."
    )

    # ---------------------------------------------------------------------------
    # SECTION 7
    # ---------------------------------------------------------------------------
    add_h1("7. Wildfire Performance Claims vs. ASTM E119 Scope Limitations")

    p = doc.add_paragraph()
    r = p.add_run("7.1 What this Exercise Does and Does Not Establish\n")
    r.bold = True
    p.add_run(
        "In accordance with CFDME Validation QA Procedure rev 2 §7 and External Standards Digest rev 1 §4, the boundary between building "
        "compartment fire ratings and wildland-urban interface (WUI) wildfire survival must be rigorously maintained:\n"
    )

    p_w1 = doc.add_paragraph(style='List Bullet')
    r = p_w1.add_run("What this exercise DOES establish: ")
    r.bold = True
    p_w1.add_run(
        "It evaluates the numerical fidelity of the firm's conjugate heat transfer model against a standardized, fuel-continuous, monotonically "
        "rising furnace time-temperature curve (ASTM E119). It establishes that the model currently over-predicts E119 thermal transmission "
        "endurance by +13 min (+11.0%) under single-point tie governance."
    )

    p_w2 = doc.add_paragraph(style='List Bullet')
    r = p_w2.add_run("What this exercise DOES NOT establish: ")
    r.bold = True
    p_w2.add_run(
        "It DOES NOT substantiate, validate, or support Ocotillo's marketing claim that the 3D-printed concrete wall assembly 'outperforms "
        "conventional wood-frame construction in a Sonoran WUI wildfire,' nor does it establish that the assembly can survive an Avra Valley "
        "buffelgrass wildfire for 2 hours (or any other duration). An ASTM E119 endurance rating is not a wildfire survival prediction."
    )

    p = doc.add_paragraph()
    r = p.add_run("7.2 Physical & Procedural Contrast: E119 Furnace vs. WUI Wildfire\n")
    r.bold = True
    p.add_run(
        "The ASTM E119 exposure and a Sonoran Desert buffelgrass wildfire represent fundamentally disjoint physical regimes:\n"
        "• ASTM E119 is a smooth, enclosed, fuel-continuous compartment fire curve designed to compare relative fire endurance under standard "
        "furnace conditions (reaching 927 °C at 1 hr and 1010 °C at 2 hr). It imposes a monotonically increasing thermal soak under quiescent gas flow.\n"
        "• A Sonoran WUI Wildfire is an open-domain, wind-driven, highly turbulent, transient fire-front passage. Driven by 5–12 m/s winds, it involves "
        "severe flame tilt, localized flame impingement, intense fluctuating radiative fluxes (peaking at ~100–150 kW/m²), transient convective heating "
        "and cooling cycles, and firebrand showers. Most critically, a surface buffelgrass fire has a finite fuel bed and rapid rate of spread "
        "(R = 0.9 m/s per scoping memo §3), meaning the flaming front passes a given structure in minutes rather than dwelling for multiple hours.\n"
        "No algebraic formula, scaling factor, or equivalence ratio exists to convert an ASTM E119 furnace endurance (in minutes) into a wildfire "
        "survival duration. Extrapolating a furnace rating to a wildfire claim is scientifically invalid and commercially misleading."
    )

    p = doc.add_paragraph()
    r = p.add_run("7.3 Evidence Required to Close the Validation Gap\n")
    r.bold = True
    p.add_run(
        "To substantiate Ocotillo's wildfire performance claim under firm standards, the model must be validated against wildfire-specific "
        "physical test data. This gap can only be closed by:\n"
        "1. Physical fire-front exposure testing of the double-wythe printed assembly at a recognized laboratory (such as the full-scale radiant/flame "
        "exposure window scheduled at Red Butte on October 27, 2025).\n"
        "2. Time-resolved measurements of heat flux, surface flame impingement, cavity air temperature, and unexposed-face thermal rise under an "
        "imposed boundary heat load matching the Byram fireline intensity (I = 10,040 kW/m) and flame length (L = 5.4 m) of the Avra Valley fuel model.\n"
        "3. A formal validation rollup of simulation predictions against those physical measurements following Section 3 of our procedure."
    )

    p = doc.add_paragraph()
    r = p.add_run("7.4 Mandatory Reporting Format for Future Wildfire Validation\n")
    r.bold = True
    p.add_run(
        "Whenever wildfire physical test data becomes available, any future validation comparison must be reported in the strict ASME V&V 20 "
        "tabular format mandated by CFDME-QA-VAL-002 §3. Specifically, it must state the simulation prediction S, certified test measurement D, "
        "signed comparison error E = S − D, and validation uncertainty u_val in a single line or table, citing test report and run IDs, accompanied "
        "by the primary comparison to |E| ≤ 10% of D and secondary comparison to u_val. Binary characterizations ('validated,' 'passes,' 'matches') "
        "remain strictly prohibited."
    )

    # ---------------------------------------------------------------------------
    # SECTION 8
    # ---------------------------------------------------------------------------
    add_h1("8. Certified Rating Authority, Stamp Boundary & Bianca's Figure")

    p = doc.add_paragraph()
    r = p.add_run("8.1 Impact of Bianca's Figure on Certified Rating if Ever Substantiated\n")
    r.bold = True
    p.add_run(
        "In Ironwood Certification Memorandum IWFPE-CERT-25-0374 §3, Marla Kettering, PE certified the assembly for a 1-hour fire-resistance "
        "rating (60 min). Kettering noted: 'The next higher standard rung is a 2-hour rating, which requires 120 min of demonstrated endurance "
        "under the governing criterion; the measured endurance falls short of that rung by 2 min [118 min measured]. Because the certified rating "
        "is limited by the governing single-point result to the highest standard rung fully demonstrated by the certified test, the assembly is "
        "certified at 1-hour and not at any higher rung.'\n\n"
        "If Bianca Rennert's figure of 129 min were ever formally substantiated by Red Butte in an authorized, reissued test report (RBFMT-25-0918-R1):\n"
        "• The governing endurance would become min(129 min single-point, 163 min average-rise) = 129 min.\n"
        "• Because 129 min ≥ 120 min, the assembly would fully clear the 2-hour standard endurance threshold by 9 min.\n"
        "• This would legally allow the certifying fire protection engineer to upgrade the assembly's certification from a 1-hour fire-resistance "
        "rating (60 min) to a 2-hour fire-resistance rating (120 min)."
    )

    p = doc.add_paragraph()
    r = p.add_run("8.2 Professional Authority Entitled to Act on the Rating\n")
    r.bold = True
    p.add_run(
        "Neither Ocotillo Additive Structures (Trevor Buckhalter or Bianca Rennert), nor the testing laboratory (Red Butte), nor The CFD ME "
        "(Gordon Selby, PE or Marguerite Falk, PE) has the legal authority to certify, amend, or restate a building fire-resistance rating.\n"
        "Authority: Certification of fire-resistance ratings is reserved EXCLUSIVELY to the fire-protection professional engineer of record: "
        "Marla Kettering, PE (Arizona Fire Protection PE #45106), Principal of Ironwood Fire Protection Engineering. "
        "Per Ironwood memo §4: 'Any change to the certified rating requires a reissued test report from the testing laboratory of record and a new "
        "certification issued by Ironwood Fire Protection Engineering. No other party may certify or restate this rating.'"
    )

    p = doc.add_paragraph()
    r = p.add_run("8.3 Firm Professional Stamp Boundary\n")
    r.bold = True
    p.add_run(
        "Per CFDME Validation QA Procedure rev 2 §9 and Phase 1 draft report rev B §9.2, The CFD ME stamps computational thermal analysis only. "
        "The mandatory professional stamp language that must appear on every deliverable carrying a validation claim under this procedure is:\n"
    )

    p_st = doc.add_paragraph()
    p_st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_st = p_st.add_run("\"CFD thermal analysis only. Fire-resistance rating certified separately by others.\"")
    r_st.bold = True
    r_st.font.size = Pt(11)
    r_st.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # ---------------------------------------------------------------------------
    # SECTION 9
    # ---------------------------------------------------------------------------
    add_h1("9. Peer-Review Checklist Disposition (CFDME-2025-041)")

    p = doc.add_paragraph()
    p.add_run(
        "In your peer review of the Phase 1 draft report (CFDME-2025-041_peer_review_checklist.docx, opened 10/09/2025), eight items (2, 3, 4, 5, "
        "6, 7, 9, and 10) were marked OPEN. Below is the formal checklist disposition enabled by this memorandum:\n"
    )

    p_cl6 = doc.add_paragraph()
    r = p_cl6.add_run("9.1 Item Enabled for Immediate Closure: Item 6\n")
    r.bold = True
    p_cl6.add_run(
        "• Item 6 ('Validation reported as E ± u_val against acceptance criterion, NOT yes/no, per Validation Procedure rev 2 §3–§5'): "
    )
    r = p_cl6.add_run("CLOSED [X]. ")
    r.bold = True
    p_cl6.add_run(
        "This memorandum provides the complete, standards-governed ASME V&V 20 validation rollup (S = 131 min, D = 118 min, E = +13 min, "
        "u_val = ±9 min, tolerance = 11.8 min), documents the resolved model error finding, establishes the diagnostic physics, and provides "
        "the verbatim text for Section 7 of the report. This fully satisfies the reviewer's note and allows Item 6 to be marked closed."
    )

    p_cl_rest = doc.add_paragraph()
    r = p_cl_rest.add_run("9.2 Open Items Requiring Continued Open Status\n")
    r.bold = True
    p_cl_rest.add_run(
        "The remaining seven open items CANNOT be closed by this validation memo and must remain [ ] OPEN pending technical resolution:\n"
    )

    open_items = [
        ("Item 2 — Regime selection documented against firm modeling standard:",
         "OPEN [ ]. The Froude-based regime classification (Fr ≈ 0.92–2.21 across 5–12 m/s wind) and resulting mixed-convection solver selection "
         "per Modeling Standard rev 4 §2–§3 are referenced in scoping memo rev A §4, but have not yet been formally compiled and documented into "
         "the production case-setup record."),
        ("Item 3 — Solver package confirmed per Modeling Standard rev 4 §3:",
         "OPEN [ ]. Must remain open because subcontractor logs (log.solve_20251009_attempt3.txt) reveal that Mulshi Simulation Labs improperly "
         "attempted a steady RANS solve (rhoSimpleFoam) inherited from an external aerodynamics template. The fireFoam transient LES solver stack "
         "with adjustableRunTime time-stepping must be verified in the live case controlDict before sign-off."),
        ("Item 4 — Resolution basis (D*/dx and Pope resolved-TKE) in Verification body:",
         "OPEN [ ]. QA Verification Standard rev 3 §5–§6 requires D*/dx = 7.5 and Pope resolved-TKE fraction = 84% to appear in the body of Section 6 "
         "rather than solely in Appendix C. Section 6 of draft rev B still contains an unconverged three-grid table that the reviewer has not accepted."),
        ("Item 5 — Through-wall CFD treatment confirmed per Modeling Standard rev 4 §6:",
         "OPEN [ ]. Section 3.4 describes wall geometry, but the through-wall multi-region conjugate CFD treatment (mesh refinement at tie-concrete interfaces "
         "by 4x) has not been audited or verified against constant/regionProperties in the production case."),
        ("Item 7 — Geometry revision tagged and matches case log:",
         "OPEN [ ]. While this memo confirms that revC matches the morning meshing log and Red Butte specimen, the transmittal record must formally "
         "archive and caveat Trevor Buckhalter's revD parapet transmittal (received 10/09/2025 afternoon) to ensure no downstream meshing inadvertently incorporates revD."),
        ("Item 9 — All reported pressures cross-checked against case boundary conditions per Units SOP rev 2 §4:",
         "OPEN [ ]. A severe unit defect exists in the interim wind-load extraction (interim_wall_pressures.csv and interim_summary_draft.docx Table 1), "
         "where ASCE 7-22 windward wall pressure was reported as 12.4 Pa instead of 594 Pa (12.4 psf × 47.88 Pa/psf ≈ 594 Pa). The draft report lacks "
         "the mandatory Section 1 conversion table, and pressures must be reconciled before closure."),
        ("Item 10 — Reviewer sign-off and stamp block completed:",
         "OPEN [ ]. Held open per firm QA protocol until Items 2, 3, 4, 5, 7, and 9 are fully resolved and closed by the Reviewing Engineer.")
    ]

    for item_title, item_desc in open_items:
        p_item = doc.add_paragraph(style='List Bullet')
        r = p_item.add_run(item_title + " ")
        r.bold = True
        p_item.add_run(item_desc)

    # Checklist Table
    add_h3("Table 9.1 — Peer-Review Checklist Disposition Summary (CFDME-2025-041)")
    tbl_chk = doc.add_table(rows=11, cols=4)
    tbl_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_chk)

    chk_hdrs = ["Item #", "Checklist Requirement", "Status", "Reviewer Disposition Basis"]
    for c_idx, h in enumerate(chk_hdrs):
        cell = tbl_chk.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        set_cell_background(cell, "E6ECF2")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)

    chk_rows = [
        ("1", "Deliverable identifies governing SOW and revision", "[X] CLOSED", "Closed in rev B (cites SOW 10/08/2025 §3.1 & §3.2)."),
        ("2", "Regime selection documented against modeling standard", "[ ] OPEN", "Fr-based classification not yet compiled in case-setup record."),
        ("3", "Solver package confirmed per Modeling Standard §3", "[ ] OPEN", "Mulshi steady-RANS attempt requires replacement with fireFoam LES."),
        ("4", "LES resolution (D*/dx, Pope TKE) in Verification body", "[ ] OPEN", "Metrics must be incorporated into Section 6 body from Appendix C."),
        ("5", "Through-wall CFD treatment confirmed per standard §6", "[ ] OPEN", "Conjugate region properties and tie refinement require case audit."),
        ("6", "Validation reported as E ± u_val, NOT yes/no", "[X] CLOSED", "CLOSED by this memo (CFDME-2025-041-MEMO-VAL-01) and Section 7 text."),
        ("7", "Geometry revision tagged and matches case log", "[ ] OPEN", "revC confirmed for test; revD parapet transmittal must be formally fenced."),
        ("8", "Stamp boundary respected (rating referred to Ironwood)", "[X] CLOSED", "Closed in rev B (Section 9.2 standard stamp block in place)."),
        ("9", "Pressures cross-checked against BCs (Units SOP §4)", "[ ] OPEN", "Defect: 12.4 Pa reported instead of 594 Pa (12.4 psf); units table required."),
        ("10", "Reviewer sign-off and stamp block completed", "[ ] OPEN", "Held open pending closure of Items 2, 3, 4, 5, 7, and 9.")
    ]

    for r_idx, row_vals in enumerate(chk_rows):
        row = tbl_chk.rows[r_idx+1]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
            elif c_idx == 2:
                r.bold = True
                if "CLOSED" in val and c_idx == 2 and r_idx == 5:
                    r.font.color.rgb = RGBColor(0x00, 0x66, 0x00) # Green
                elif "OPEN" in val:
                    r.font.color.rgb = RGBColor(0x99, 0x00, 0x00) # Red
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ---------------------------------------------------------------------------
    # SECTION 10
    # ---------------------------------------------------------------------------
    add_h1("10. Ready-to-Issue Replacement Text for Report Section 7")

    p = doc.add_paragraph()
    p.add_run(
        "To enable you to close Section 7 of the Phase 1 draft report immediately, the complete, fully compliant text "
        "is provided below, ready for insertion into CFDME-2025-041_Phase1_report_revB.docx:\n"
    )

    # Section 7 Text Box
    tbl_s7 = doc.add_table(rows=1, cols=1)
    tbl_s7.alignment = WD_TABLE_ALIGNMENT.CENTER
    s7_cell = tbl_s7.rows[0].cells[0]
    s7_cell.width = Inches(6.5)
    set_cell_background(s7_cell, "FCFDFD")
    set_cell_margins(s7_cell, top=140, bottom=140, left=180, right=180)

    tcPr = s7_cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="003366"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="003366"/>'
        f'  <w:left w:val="single" w:sz="16" w:space="0" w:color="003366"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="003366"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    s7_p = s7_cell.paragraphs[0]
    s7_p.paragraph_format.space_after = Pt(4)
    s7_p.paragraph_format.line_spacing = 1.15

    r = s7_p.add_run("7. Validation — ASTM E119 Companion Simulation\n")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    s7_body = (
        "7.1 Purpose & Reference Standard\n"
        "This section documents the formal validation of the Phase 1 conjugate thermal wall model against the certified third-party "
        "fire endurance test of record. Reporting follows ASME V&V 20-2009 (R2016) and firm procedure CFDME-QA-VAL-002 rev 2. "
        "Validation is expressed strictly as the comparison error E = S − D with its validation uncertainty u_val against the firm's "
        "acceptance criterion (|E| ≤ 10% of D), and never as a qualitative characterization.\n\n"
        "7.2 Certified Physical Test of Record (D)\n"
        "Experimental reference data D is drawn from Red Butte Fire & Materials Testing Report No. RBFMT-25-0918, dated 09/24/2025. "
        "The test subjected a 3.05 m × 3.05 m non-load-bearing specimen of the double-wythe printed concrete cavity wall (OAS-WUI-01_revC / "
        "OAS-WA-305mm-DW) to the standard ASTM E119 furnace curve. Per ASTM E119 §8, endurance is governed by the earlier of two unexposed-face "
        "temperature rise criteria above initial ambient (21.0 °C): the 9-thermocouple average rise (139.0 °C limit, reached at 163 min) or the "
        "single-point rise (181.0 °C limit, reached at 118 min at TC-6). TC-6 was positioned directly over a continuous 3.8 mm steel wall tie. "
        "The single-point criterion governed the test: Certified Experimental Endurance D = 118 min. Informal client-amended figures (e.g. 129 min) "
        "transmitted post-test are disallowed under CFDME-QA-VAL-002 §6 absent laboratory reissuance and calibration certification.\n\n"
        "7.3 Companion Simulation Prediction (S)\n"
        "A conjugate heat transfer simulation of the identical assembly under the E119 exposure was executed as the companion run "
        "(E119_companion_sim_results.csv). Evaluating unexposed-face response by continuous crossing times yields:\n"
        "• Single-point rise (181.0 °C rise, 202.0 °C limit): Reached at crossing time 130.94 min (rounded to 131 min).\n"
        "• Average rise (139.0 °C rise, 160.0 °C limit): Reached at crossing time 176.10 min (rounded to 176 min).\n"
        "The single-point criterion governs the simulation endurance: Simulation Prediction S = 131 min.\n\n"
        "7.4 ASME V&V 20 Model-Error Rollup\n"
        "• Model Error: E = S − D = 131 min − 118 min = +13 min (+11.0% of D).\n"
        "• Acceptance Criterion: |E| ≤ 0.10 × D = 11.8 min.\n"
        "• Validation Uncertainty: u_val = sqrt(u_num² + u_inp² + u_exp²) = sqrt(4² + 6² + 5²) = sqrt(77) = ±8.77 min ≈ ±9 min.\n"
        "• Comparison & Outcome: |E| = 13 min > 11.8 min criterion (exceeds tolerance by 1.2 min); |E| = 13 min > 9 min u_val (exceeds uncertainty by 4 min).\n"
        "• Finding: The companion simulation DOES NOT VALIDATE. Because |E| > u_val, the discrepancy is resolved as an actionable model error.\n"
        "• Largest Passing Prediction: S_max = D + 0.10 × D = 129.8 min (integer S = 129 min).\n\n"
        "7.5 Diagnostic Physical Assessment & Model Rework Allocation\n"
        "Diagnostic comparison indicates that the metallic tie thermal bridge is physically well-proportioned: the simulation reproduces the exact "
        "45 min temporal separation between single-point and average-rise governance observed in the test (163 min − 118 min = 45 min test; "
        "176 min − 131 min = 45 min run), and matches the temperature elevation of the tie above the mean (91.2 °C in run vs. 85.0 °C in test, "
        "a 6.2 °C delta). However, the model exhibits a uniform +13 min delay across both criteria. Rework belongs not in the tie mesh, but in the "
        "bulk concrete through-thickness thermal conductivity k(T), volumetric heat capacity (density and specific heat), moisture desorption enthalpy, "
        "and furnace-side radiative/convective heat flux. As of 10/10/2025, no model rework has been initiated.\n\n"
        "7.6 Scope Limitation: ASTM E119 vs. WUI Wildfire\n"
        "Validation against ASTM E119 evaluates model performance under a standard building compartment fire curve. It does NOT establish or validate "
        "Ocotillo's marketing claim of wildfire outperformance or 2-hour wildfire survival. A wildland-urban interface (WUI) fire is a wind-driven, "
        "radiation-dominated, transient fire front (Sonoran buffelgrass) with rapid flame passage, severe flame tilt, and high localized heat fluxes. "
        "E119 endurance ratings cannot be converted to wildfire survival times. Wildfire performance validation requires physical test data from the "
        "confirmatory testing window scheduled at Red Butte on 10/27/2025, reported strictly as E ± u_val per ASME V&V 20.\n\n"
        "7.7 Rating Certification & Stamp Boundary\n"
        "Certification of assembly fire-resistance ratings is reserved exclusively to the fire-protection engineer of record (Marla Kettering, PE, "
        "AZ PE #45106, Ironwood Fire Protection Engineering). If Red Butte ever formally substantiated Bianca Rennert's 129 min figure in a reissued "
        "report, the endurance would clear the 120 min rung, enabling Ironwood to upgrade the certified rating from 1-hour to 2-hour. Neither Ocotillo "
        "nor The CFD ME has authority to alter ratings. The CFD ME stamps CFD thermal analysis only."
    )
    r_body = s7_p.add_run(s7_body)
    r_body.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------------------------
    # SECTION 11
    # ---------------------------------------------------------------------------
    add_h1("11. Professional Engineer Signatures & Stamp Block")

    p = doc.add_paragraph()
    p.add_run(
        "This memorandum has been prepared, verified, and stamped in full compliance with the professional bylaws of The CFD Mechanical Engineer, LLC, "
        "ASME V&V 20-2009, and the engineering registration statutes of the State of Arizona.\n"
    )

    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_gordon, cell_falk = tbl_sig.rows[0].cells[0], tbl_sig.rows[0].cells[1]
    cell_gordon.width = Inches(3.25)
    cell_falk.width = Inches(3.25)
    set_table_borders(tbl_sig, color="003366", sz="4", val="single")

    p_g = cell_gordon.paragraphs[0]
    p_g.paragraph_format.space_after = Pt(2)
    r = p_g.add_run("ORIGINATING ENGINEER:\n")
    r.bold = True
    p_g.add_run("_________________________________________\n")
    r = p_g.add_run("Gordon Selby, PE\n")
    r.bold = True
    p_g.add_run("Owner & Principal Engineer, The CFD ME\n")
    p_g.add_run("Arizona Professional Engineer (Mechanical)\nRegistration No.: AZ PE #48213\nDate: 10/10/2025\n\n")
    r = p_g.add_run("PROFESSIONAL STAMP BLOCK:\n")
    r.bold = True
    r = p_g.add_run("CFD thermal analysis only. Fire-resistance rating certified separately by others.")
    r.italic = True

    p_f = cell_falk.paragraphs[0]
    p_f.paragraph_format.space_after = Pt(2)
    r = p_f.add_run("REVIEWING ENGINEER:\n")
    r.bold = True
    p_f.add_run("_________________________________________\n")
    r = p_f.add_run("Marguerite Falk, PE\n")
    r.bold = True
    p_f.add_run("Technical Director & Reviewing Engineer, The CFD ME\n")
    p_f.add_run("Arizona Professional Engineer (Mechanical)\nRegistration No.: AZ PE #42798\nDate: 10/10/2025\n\n")
    r = p_f.add_run("CHECKLIST DISPOSITION CONCURRENCE:\n")
    r.bold = True
    r = p_f.add_run("Item 6 CLOSED. Items 2, 3, 4, 5, 7, 9, and 10 remain OPEN pending technical remediation.")
    r.italic = True

    set_cell_background(cell_gordon, "FAFAFA")
    set_cell_background(cell_falk, "FAFAFA")
    set_cell_margins(cell_gordon, top=80, bottom=80, left=100, right=100)
    set_cell_margins(cell_falk, top=80, bottom=80, left=100, right=100)

    # Save document
    out_path = "output/CFDME-2025-041_validation_memo.docx"
    doc.save(out_path)
    print(f"Successfully generated validation memo at {out_path}")

if __name__ == "__main__":
    build_memo()
