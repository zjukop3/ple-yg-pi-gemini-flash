### Deliverable Summary

I have completed the formal validation memorandum from Gordon Selby, PE to Marguerite Falk, PE and saved the primary deliverables under `output/`:

* **`output/CFDME-2025-041_validation_memo.docx`** — The complete, professional Word validation memorandum with all required ASME V&V 20 rollups, diagnostic evaluations, checklist dispositions, and the ready-to-send paragraph for Bianca.
* **`output/CFDME-2025-041_validation_memo.pdf`** — High-fidelity PDF export of the Word validation memorandum.
* **`output/validation_memo.docx`** and **`output/CFDME-2025-041_E119_validation_memo.docx`** — Reviewer convenience copies.
* **`output/CFDME-2025-041_Phase1_report_revB_with_Section7.docx`** — Phase 1 Draft Report rev B with Section 7 fully populated from the memo text.
* Copies of the memo have also been filed to the project record at `/Projects/CFDME-2025-041_Ocotillo_WUI/Reports/CFDME-2025-041_validation_memo_20251010.docx` and `/Projects/CFDME-2025-041_Ocotillo_WUI/Validation/CFDME-2025-041_validation_memo_20251010.docx`.

---

### Key Technical Determinations

1. **Assembly Identity & Basis of Record:**
   * **Settlement:** The assembly modeled in the companion run **is identical** to the assembly covered by the Ironwood certification memo (`IWFPE-CERT-25-0374`) and tested in Red Butte Report No. `RBFMT-25-0918`.
   * **Evidentiary Basis:** Perfect dimensional and material convergence across Ironwood §1.2, Red Butte §2, the dimensioned architectural drawing (`OAS_wall_assembly_section.png` / `OAS-WA-305mm-DW` rev A), and engineering CAD geometry `OAS-WUI-01_revC.FCStd`: two 50 mm siliceous-aggregate printed concrete leaves, a 205 mm open-air unfilled cavity (no insulation), 305 mm overall thickness, and continuous 9-gauge (3.8 mm) galvanized steel truss-type wire ties at 600 mm on-center vertical spacing with 25 mm embedment into each leaf.
   * **Revision Audit:** The meshed run was built on the morning of 10/09/2025 from `OAS-WUI-01_revC` (3.05 m × 3.05 m planar specimen). The client's subsequent revD transmittal (received 10/09/2025 afternoon) added a 610 mm hollow parapet, which is not part of the certified E119 test panel and was correctly excluded from the run.

2. **Governing Criterion, Crossing Times & Section 7 Stub:**
   * **Criteria (above initial ambient $T_{\text{amb}} = 21.0\text{ }^\circ\text{C}$):** Average unexposed rise limit = $139.0\text{ }^\circ\text{C}$ ($160.0\text{ }^\circ\text{C}$ absolute); Single-point rise limit = $181.0\text{ }^\circ\text{C}$ ($202.0\text{ }^\circ\text{C}$ absolute).
   * **Continuous Crossing Times (linear interpolation):**
     * Single-point rise: crosses at **$130.94\text{ min}$** $\rightarrow$ **$131\text{ min}$** to the nearest minute (tripping sample is also $131\text{ min}$).
     * Average rise: crosses at **$176.10\text{ min}$** $\rightarrow$ **$176\text{ min}$** to the nearest minute (tripping discrete sample would be $177\text{ min}$).
   * **Governance:** The single-point rise criterion governs because it is reached earlier ($131\text{ min} < 176\text{ min}$).
   * **Section 7 Stub:** The prediction of $S = 131\text{ min}$ in the Section 7 stub **stands confirmed**.

3. **Experimental Value ($D$) & Disposition on Bianca's Figure:**
   * **Certified Value Adopted:** **$D = 118\text{ min}$**, taken directly from Red Butte Report No. `RBFMT-25-0918` §5.2–§5.3 (single-point limit at TC-6, located directly over a 3.8 mm steel tie).
   * **Disposition on Bianca's Figure ($129\text{ min}$):** **Formally REJECTED**. Under `CFDME-QA-VAL-002` rev 2 §6, client-amended figures are strictly inadmissible without (i) a reissued lab report bearing an amendment sequence (e.g., `RBFMT-25-0918-R1`) signed by lab management, (ii) an accredited calibration certificate for TC-6, and (iii) an explicit supersession statement from the lab. Red Butte’s certified report already includes in-force NIST-traceable calibration certificates; informal post-test vendor adjustments cannot move the validation anchor.

4. **ASME V&V 20 Model Error, Acceptance Criterion & Uncertainty:**
   * **Model Error:** $E = S - D = 131\text{ min} - 118\text{ min} = \mathbf{+13\text{ min}}$ ($+11.0\%$ of $D$). (Raw crossing: $130.94\text{ min} - 118.00\text{ min} = +12.94\text{ min}$).
   * **Primary Acceptance Criterion:** $|E| \le 10\%\text{ of }D = \mathbf{11.8\text{ min}}$ (limit as it falls).
   * **Validation Uncertainty:** $u_{\text{val}} = \sqrt{u_{\text{num}}^2 + u_{\text{inp}}^2 + u_{\text{exp}}^2} = \sqrt{4^2 + 6^2 + 5^2} = \sqrt{77} = \pm 8.77\text{ min} \rightarrow \mathbf{\pm 9\text{ min}}$.
   * **Comparison & Validation Finding:**
     * Against Acceptance Criterion: $|E| = 13\text{ min} > 11.8\text{ min}$ (FAILS by $1.2\text{ min}$).
     * Against Validation Uncertainty: $|E| = 13\text{ min} > 9\text{ min}$ (exceeds $u_{\text{val}}$ by $4\text{ min}$).
     * **Conclusion:** The companion simulation **DOES NOT VALIDATE**. Because $|E| > u_{\text{val}}$, the discrepancy is resolved as an **actionable model error**, not experimental or numerical noise.
   * **Largest Passing Prediction:** $S_{\text{max}} = D + 0.10 \times D = \mathbf{129.8\text{ min}}$ (limit as it falls); largest whole-minute integer prediction is **$129\text{ min}$**.

5. **Diagnostic Physics Comparisons & Rework Allocation:**
   * **Separation Between Criteria:** $163\text{ min} - 118\text{ min} = \mathbf{45\text{ min}}$ in test vs. $176\text{ min} - 131\text{ min} = \mathbf{45\text{ min}}$ in run ($176.10\text{ min} - 130.94\text{ min} = 45.16\text{ min}$) $\rightarrow$ **Exact match ($0\text{ min}$ delta)**.
   * **Governing Point Elevation Above 9-TC Mean:** At governance, TC-6 sits $181.0\text{ }^\circ\text{C} - 96.0\text{ }^\circ\text{C} = \mathbf{85.0\text{ }^\circ\text{C}}$ ($85.0\text{ K}$) above the mean in the test, while in the simulation it sits $181.0\text{ }^\circ\text{C} - 89.83\text{ }^\circ\text{C} = \mathbf{91.2\text{ }^\circ\text{C}}$ ($91.2\text{ K}$) above the mean ($202.1\text{ }^\circ\text{C} - 110.9\text{ }^\circ\text{C} = 91.2\text{ }^\circ\text{C}$ at integer $131\text{ min}$) $\rightarrow$ **Delta of only $6.2\text{ }^\circ\text{C}$ ($6.2\text{ K}$)**.
   * **Physics Inferred:** The 3D conjugate thermal bridging across the 3.8 mm steel ties is accurately captured in proportion, intensity, and timing relative to the bulk wall. However, the *entire* thermal response exhibits a uniform $+13\text{ min}$ delay across both failure modes.
   * **Where Rework Belongs:** Rework does not belong in the tie mesh or tie conduction model. It belongs in the bulk printed concrete through-thickness thermal response: (1) temperature-dependent thermal conductivity $k(T)$ (underestimating high-temperature conductivity), (2) volumetric heat capacity ($\rho \cdot c_p$) and moisture desorption / vaporization latent heat (overestimating thermal inertia), and (3) furnace-side radiative/convective heat flux boundary conditions.
   * **Rework Status:** **No rework has been started** on the file server as of 10/10/2025. Subcontractor logs show Mulshi Simulation Labs was improperly attempting steady RANS aerodynamic solves.
   * **Implications for Phase 1:** Phase 1 cannot issue an unqualified validation claim. Because the model over-predicts thermal endurance by $+13\text{ min}$ ($+11\%$), unexposed-face thermal predictions under wildfire exposure are non-conservative (overestimating survival time). Section 7 must document this as an actionable finding, launch materials cannot claim validation, and a technical remediation plan must be scoped.

6. **Wildfire Claims vs. ASTM E119 Scope Boundaries:**
   * **What it Establishes:** Model accuracy under a standardized, monotonically rising, fuel-continuous building compartment fire soak (ASTM E119), showing a $+13\text{ min}$ over-prediction.
   * **What it Does NOT Establish:** It does *not* validate Ocotillo's marketing claim of "outperforming conventional wood-frame construction in a Sonoran WUI wildfire" or surviving a wildfire for 2 hours.
   * **Physical Distinction:** An E119 furnace fire is an enclosed, continuous thermal soak. A Sonoran buffelgrass WUI wildfire is an open, wind-driven ($5\text{--}12\text{ m/s}$), radiation-dominated, highly turbulent flame front with severe flame tilt, high localized heat flux spikes, convective cooling cycles, firebrands, and a rapid passage time ($R = 0.9\text{ m/s}$, front clears in minutes, not hours). E119 ratings cannot be converted to wildfire survival times by any algebraic formula.
   * **Closing the Gap:** Physical testing under wildfire-representative thermal exposures (e.g., the Red Butte confirmatory testing window scheduled for 10/27/2025).
   * **Future Reporting Format:** Strictly ASME V&V 20 tabular format ($S$, $D$, $E = S - D$, $u_{\text{val}}$, $10\%$ criterion). Binary "yes/no" or "pass/fail" statements remain prohibited.

7. **Rating Authority, Stamp Boundary & Bianca's Figure:**
   * **Effect on Rating:** If Bianca's $129\text{ min}$ figure were ever substantiated by Red Butte in an authorized reissued report, the governing endurance would become $\min(129\text{ min}, 163\text{ min}) = 129\text{ min}$. Because $129\text{ min} \ge 120\text{ min}$, it would clear the 2-hour rung (by $9\text{ min}$), legally allowing the certifying engineer to upgrade the certified rating from 1-hour ($60\text{ min}$) to 2-hour ($120\text{ min}$).
   * **Sole Authority:** Exclusively Marla Kettering, PE (AZ PE #45106), Principal of Ironwood Fire Protection Engineering. Neither Ocotillo, Red Butte, nor The CFD ME has authority to issue or modify ratings.
   * **Mandatory Stamp Language:** `"CFD thermal analysis only. Fire-resistance rating certified separately by others."`

8. **Peer-Review Checklist Disposition (`CFDME-2025-041`):**
   * **Item 6 ("Validation reported as $E \pm u_{\text{val}}$ against acceptance criterion, NOT yes/no"):** **CLOSED [X]** by this memorandum and the ready-to-issue Section 7 text.
   * **Items Staying OPEN [ ]:**
     * *Item 2 (Regime selection):* Froude classification ($Fr \approx 0.92\text{--}2.21$) not yet compiled in case-setup record.
     * *Item 3 (Solver package):* Mulshi steady RANS attempt must be replaced and confirmed as fireFoam LES.
     * *Item 4 (LES resolution basis):* $D^*/dx = 7.5$ and Pope resolved-TKE fraction ($84\%$) must be placed in the report body (not just Appendix C).
     * *Item 5 (Through-wall CFD treatment):* Multi-region conjugate setup and tie interface refinement require case audit.
     * *Item 7 (Geometry revision tagged):* revC confirmed for test, but revD parapet transmittal must be formally fenced.
     * *Item 9 (Pressure sanity check):* Critical unit defect in interim wind-load extraction ($12.4\text{ Pa}$ reported instead of $594\text{ Pa}$ / $12.4\text{ psf}$); conversion table required.
     * *Item 10 (Reviewer sign-off):* Held open pending closure of Items 2, 3, 4, 5, 7, and 9.

---

### Verbatim Paragraph for Bianca Rennert (Ready to Transmit Today)

> "Bianca: Under our firm QA procedures and ASME V&V 20 guidelines, we cannot state that the E119 companion simulation has validated against the physical test for Ocotillo's launch materials, and the simulation results cannot be used to claim a validated 2-hour rating. Our validation procedure strictly requires that experimental reference data be drawn from the certified third-party laboratory report of record (Red Butte Report No. RBFMT-25-0918), which establishes the governing single-point endurance at 118 min. Informal post-test thermocouple calibration adjustments cannot be adopted without a formal amended test report and calibration certificate issued directly by Red Butte; substituting uncertified figures would invalidate our professional review. Against the certified 118 min test endurance, our simulation predicts a governing single-point endurance of 131 min, yielding a comparison error of +13 min (+11.0%). This exceeds our mandatory 10% acceptance tolerance (11.8 min) as well as our validation uncertainty (±9 min), establishing a resolved model error that requires technical remediation. Furthermore, professional engineering standards prohibit extrapolating an ASTM E119 furnace endurance rating to a wildland-urban interface (WUI) wildfire survival claim; E119 is a comparative building compartment fire exposure rather than a transient, wind-driven vegetation fire. Formal validation of wildfire performance must await physical test data from the confirmatory testing window scheduled at Red Butte on 10/27/2025. Finally, official certification or modification of assembly fire-resistance ratings remains reserved exclusively to the fire-protection professional engineer of record (Ironwood Fire Protection Engineering). Consequently, launch materials should rely solely on Ironwood's certified 1-hour rating and must avoid unsubstantiated claims of simulation validation or 2-hour performance."