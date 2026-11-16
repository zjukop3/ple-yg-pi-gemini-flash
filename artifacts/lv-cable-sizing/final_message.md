# Low-Voltage Wire Schedule & Conductor Engineering Package
**Building 4210, Consolidated Support Facility — Naval Support Activity Whitmore Ridge**
**Project P-4210 | Contract Sheet E-621**

The complete engineering submission has been compiled, audited against every code of record and project document, and published to:
`/filesystem/electrical__lv_cable_sizing__blind/output/submission.zip`

---

### Deliverable Package Summary (`submission.zip`)

The submission archive contains all five required contract and design deliverables at its root level:

1. **`wire_schedule.csv`**
   - Covers all 32 low-voltage circuits from `P-4210_connected_load_schedule.xlsx` across 27 exact audited columns:
     `circuit, description, from, to, install_class, length_ft, sets, size, material, egc_size, raceway_trade_in, duct_ids, design_current_a, corrected_ampacity_a, vd_load_a, vd_pct, cumulative_vd_pct, ambient_c, ccc, governing_constraint, ocpd_a, system_voltage_v, phases, power_factor, r_ohm_per_kft, x_ohm_per_kft, drop_v`
   - Circuit lengths incorporate plan right-angle routing, vertical riser heights from Sheet E-618, and the 16-foot total termination allowance (8 ft per end per EDS-26 Clause 4.2.4).
   - Conductor corrected ampacities were computed under engineering supervision (NFPA 70 310.14(B)) using Cascadia Wire Engineering Data Section 4, the Neher-McGrath method for duct banks, and free-air solar heat balance for cable tray CT-R1.
   - Sizing strictly adheres to terminal physical limits, 60°C lug limits (notably LP-1), and proportional circular-mil scaling of equipment grounding conductors under NFPA 70 250.122(B) where phase conductors were increased for voltage drop.

2. **`E-621_wire_schedule.dxf`**
   - Contract drawing sheet carrying standard G-TTLB title block naming Sheet **E-621** and Project **P-4210**.
   - Contains complete text entities (TEXT/MTEXT) for all 32 circuit lines, an abbreviation legend, and exact matching conductor sizes and designations.

3. **`calc_book.xlsx`**
   - **`front_sheet`**: Declares all project calculation parameters as numeric stored values:
     - `outdoor_design_dry_bulb_c` = 42.0°C (Yuma MCAS record max daily normal 106.8°F / 41.56°C rounded up).
     - `roof_ambient_c` = 46.0°C (outdoor dry-bulb + 4 K roof film allowance, coordinated with memo M-501-C).
     - `earth_ambient_c` = 27.45°C (NOAA annual mean daily normal 24.45°C + 3 K).
     - `soil_thermal_resistivity_k_m_w` = 0.60 K·m/W (specified fluidized thermal backfill per GEO-4210-T 2.2).
     - `soil_thermal_resistivity_rejected_native_k_m_w` = 0.95 K·m/W (considered and rejected native SP-SM).
     - `encasement_thermal_resistivity_k_m_w` = 0.55 K·m/W (red-dyed concrete encasement per GEO-4210-T 2.3).
     - `solar_irradiance_w_m2` = 1030.0 W/m² (EDS-26 5.4).
     - `load_factor` = 1.0 (100% per UFC 3-501-01 3-2.3.3).
     - `termination_allowance_ft` = 16.0 ft (EDS-26 4.2.4).
     - `vd_start_point` = T-1 secondary lugs (point of government ownership per WRPU service letter).
     - `vd_limit_feeder_pct` = 3.0%, `vd_limit_branch_pct` = 3.0%, `vd_limit_total_pct` = 5.0% (UFC 3-501-01 3-2.7).
     - `mutual_heating_rise_k` = 28.4 K (governing Neher-McGrath rise in DB-1).
     - `tray_sum_od_in` = 8.19 in (<= 16.2 in allowable width in 18 in tray CT-R1).
     - `distinct_large_sizes` = 4 (1/0 AWG, 300 kcmil, 350 kcmil, 500 kcmil; <= 5 permitted per EDS-26 3.4.2).
     - `ampacity_basis` = Calculated under engineering supervision (heat balance and Neher-McGrath), NFPA 70 310.14(B).
     - `total_usd` = $160,050.50.
   - **`duct_assignment`**: Line-by-line duct assignment for each parallel set in DB-1 (SE-1 sets in D1–D4, D7, D8; F-10 sets in D9, D10) and DB-2 (F-05 sets in E1, E2), respecting reserved ducts (D11, D12, E4).
   - **`cost_ledger`**: Complete unit-price breakdown across conductors, terminations, and interior rigid steel raceways, reconciling material ($113,661.14) and labor ($46,389.36) to the package total of $160,050.50.

4. **`design_basis.md`**
   - Opens with the required fenced JSON block (`codes_of_record`, `environment`, `sources`, `voltage_drop`, `cost`, `duct_assignment`, `mutual_heating_rise_k`).
   - Detailed engineering narrative detailing:
     - Adoption of IBC 2024 and NFPA 70 (2023 Edition) under UFC 1-200-01 Change 4, with most restrictive precedence and supersession of EDS-26 Rev 2.
     - Environmental parameters and derivation from NOAA station USW00003145, GEO-4210-T, and M-501-C.
     - Voltage-drop hierarchy: T-1 secondary starting point (0.00%), zero loss through transformer K-13 with no reset (secondary inherits 1.43% upstream drop per UFC 3-501-01 3-2.7.4.5.3), feeder chain drops <= 3.00%, branch circuit drops <= 3.00%, and cumulative end-of-circuit load drops <= 5.00%.
     - Service entrance sizing (2000 A main bus) and duct bank assignment minimizing mutual heating.
     - Standardization limiting large sizes (> #1 AWG) to 4 sizes, respecting all listed lug limits and terminal quantities.

5. **`constraint_register.xlsx`**
   - Criteria log workbook with columns: `req_id, document, clause, requirement, value, unit, kind, applies_to, resolution`.
   - Formulates 38 discrete criteria rows covering federal criteria (UFC 1-200-01, UFC 3-501-01, UFC 3-520-01), national codes (NFPA 70, IBC), installation standards (EDS-26 Rev 4), contract specifications (26 05 19, 26 05 33, 26 24 16), and site reports (GEO-4210-T, WRPU). Explicitly records superseded and non-governing materials (EDS-26 Rev 2, Meridian Cable) as non-governing to ensure high register precision.