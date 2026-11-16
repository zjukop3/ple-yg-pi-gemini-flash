# Pacific Crest Space Force Annex — 13.8 kV Site Distribution Conveyance Study
**Solicitation FA4610-26-R-0031 | Project PCSFA 24-0117**  
**Deliverable:** `/filesystem/final_batch4__electrical_task12_conveyance_study__blind/output/submission.zip`  
Containing at the zip root:
1. `conveyance_study.xlsx`
2. `conveyance_study_report.md`

---

### Executive Summary of Deliverables & Recommendations

| Item | Feeder | Description | Recommended Conveyance | Cable Size / Sets | Overhead Conductor | Design Current | Governing Ampacity | Route Length | Total Project Cost | Cost / LF |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **C01** | F1 | SS-1 Bus A to MB-1 MSG-A | **CEDB** | 500 kcmil (2 sets) | — | 640 A | 350.0 A/set (700 A) | 835 ft | $256,913.24 | $307.68 |
| **C02** | F2 | SS-1 Bus B to MB-1 MSG-B | **CEDB** | 350 kcmil (2 sets) | — | 560 A | 292.0 A/set (584 A) | 1,051 ft | $294,943.83 | $280.63 |
| **C03** | F3 | SS-1 Bus A to CUP-1 SWG-C1 | **CEDB** | 500 kcmil (1 set) | — | 400 A | 448.0 A | 476 ft | $100,647.61 | $211.44 |
| **C04** | CF-2 | CUP-1 to Lift Station LS-2 | **CEDB** | 250 kcmil (1 set) | — | 60 A | 321.0 A | 1,204 ft | $227,737.02 | $189.15 |
| **C05** | A-3 | MB-1 MSG-A to USS-A1 (Interior) | **RMC** | 500 kcmil (1 set) | — | 200 A | 245.0 A | 414 ft | $112,724.58 | $272.28 |
| **C06** | F4 | SS-1 Bus B to Gate House GH-1 | **OH** | 250 kcmil (risers) | 1/0 ACSR (Raven) | 40 A | 196.0 A | 1,917 ft | $116,507.80 | $60.78 |
| **C07** | CF-1 | CUP-1 to Warehouse W-3 | **CEDB** | 250 kcmil (1 set) | — | 120 A | 321.0 A | 643 ft | $235,792.14 | $366.71 |

---

### Admissibility and Engineering Basis Highlights

1. **Admissibility Determinations**:
   - **CEDB (Concrete-Encased Ductbank)**: Permitted for all site items (C01, C02, C03, C04, C06, C07) per UFC 3-550-01 ¶ 3-11.2.1 and PCSFA-IEDS Rev 3 ¶ 4.2.
   - **UEDB & DBC**: Prohibited for all primary distribution circuits by PCSFA-IEDS Rev 3 ¶ 4.2 and UFC 3-550-01 ¶ 3-11.3.1.
   - **HDD as Predominant Run Method**: Prohibited by UFC 3-550-01 ¶ 3-11.4.1 and IEDS ¶ 4.3 (authorized only for short crossing segments <=50 ft beyond pavement/channel edges).
   - **OH (Overhead Lines)**: Prohibited inside the congested industrial area (C01, C02, C03, C04, C07) per IEDS ¶ 4.1 and UFC 3-550-01 ¶ 3-11.1.1. Permitted outside the industrial area south of y=300 for **C06**, where it provides substantial cost savings ($60.78/LF vs. $115+/LF for CEDB).
   - **Interior MB-1 (C05)**: EMT is prohibited for >600 V by UFGS 26 20 00 ¶ 3.1.6.7. Cable tray (TRAY-EN and TRAY-LD) requires 18 inches vertical space (6 in tray + 12 in headroom per UFC 3-520-01 Table 3-1 and IEDS ¶ 5.1), but corridor COR-1D provides only 14 inches and MR-2 provides 16 inches. RMC requires only 6 inches vertical space and is the **only admissible conveyance** for C05.

2. **Electrical & Cable Sizing Basis**:
   - **Short-Circuit Withstand (IEDS ¶ 2.4)**: With 16.5 kA (SS-1) and 14.2 kA (SWG-C1) available fault currents at 0.5 s clearing time, minimum conductor size is **250 kcmil Al** (16.6 kA capability; 4/0 AWG fails at 14.1 kA).
   - **Feeder F1 (C01)**: Design current = 640 A at 100% load factor. Requires **2 parallel sets of 500 kcmil Al** (350 A/set = 700 A capacity).
   - **Feeder F2 (C02)**: Design current = 560 A at 100% load factor. Designed with **2 parallel sets of 350 kcmil Al** (292 A/set = 584 A capacity) in standard 5-inch conduits, avoiding 6-inch conduits and jamming issues of 1000 kcmil.
   - **Feeder A-3 (C05)**: Design current = 200 A in RMC at 40 °C ambient requires **500 kcmil Al** (245 A ampacity).

3. **Cost Estimating & Live Formulas**:
   - Bottom-up takeoffs across 324 priced lines covering all 34 alternatives.
   - Labor loaded rates: Wage Determination CA20260022 Mod 2 base and fringe plus statutory burden (11.65%) and Workers' Compensation (Line 8.74%, Inside 4.12%, Earthwork/Laborers 7.35%).
   - Equipment rates: USACE EP 1110-1-8 Region VII adjusted for jobsite bulk fuel prices ($5.12/gal gasoline, $4.38/gal off-road diesel) per paragraphs 3.9 and 3.10; bare rental rates per Rental Quote RQ-26-0419.
   - Materials adjusted by BLS PPI WPU102603 (factor 1.0238 for indexed items) plus recommended waste and 9.5% sales tax.
   - Markups: JOOH 9.5%, HOOH 4.5%, Profit 7.9714% (weighted guidelines), Surety Bond 1.2932% (graduated Class B schedule with 3% time surcharge on recommended designs sum), Escalation 1.019388 (UFS 3-701-01 Table 4-2 linear daily interpolation), Contingency 5.0%, SIOH 5.7%, Area Cost Factor = 1.0 (per UFS 3-701-01 p. 16).
   - Live Excel formulas implemented for all roll-up columns (`direct_cost_usd` through `cost_per_lf_usd`) in **Alternatives** and for `loaded_rate_usd` in **LaborRates**.

4. **Government-Furnished Document Findings (Discrepancy Log)**:
   - **FIND-01**: Government Estimate Template Line 2 applied ACF (1.16) to bottom-up direct cost; corrected to ACF = 1.0 per UFS 3-701-01 p. 16 and RFP 3.1.
   - **FIND-02**: C-101 showed W-12 water main top of pipe at ~72 in; corrected to 56 in per SUE survey QLA/QLB vacuum test holes TH-1 and TH-2 (IEDS 1.3 order of precedence item 5).
   - **FIND-03**: E-001 showed F1 phase pickup as 560 A; corrected to 640 A per Protective Device Settings Schedule Rev D (IEDS 1.3 order of precedence item 4).
   - **FIND-04**: Geotechnical Report GEO-24-0117 Table 2 classified all borings as OSHA Type B; corrected B-07 and B-10 to OSHA Type C (SP/SM granular soils and submerged below groundwater) per 29 CFR 1926 Subpart P and IEDS 1.3 / 4.12.
   - **FIND-05**: Documented conflict between solicitation Attachment J-3 Mod 2 and Wage Determination Mod 5 published 2026-08-06 under 29 CFR 1.6(c)(2)(ii)(A).