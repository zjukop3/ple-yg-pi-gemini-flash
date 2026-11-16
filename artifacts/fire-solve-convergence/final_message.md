# Formal Engineering Disposition & Technical Memorandum
**Project Number:** CFDME-2025-041 (Ocotillo WUI Wildfire, Phase 1)  
**Deliverable File:** `/filesystem/CFDME-2025-041_transient_solve_disposition_revA.docx`  
**Date of Record:** 10/10/2025  
**Certifying Engineer:** Gordon Selby, PE (Arizona PE Registration #48213), Owner & Principal Engineer, The CFD ME  
**Reviewing Engineer:** Marguerite Falk, PE (Arizona PE Registration #42798), Technical Director & Reviewing Engineer, The CFD ME  

---

### Executive Disposition Summary

1. **Attempt 3 Disposition:** The third steady-solve attempt executed by Mulshi Simulation Labs on 10/09/2025 (Job 41304 on cluster `borrego`, 64 cores) is **FORMALLY REJECTED** in its entirety. Mulshi’s recommendation to launch a fourth steady attempt with looser convergence tolerances or reduced under-relaxation is **EXPLICITLY FORBIDDEN**.
2. **Authorization:** Production **transient reacting Large-Eddy Simulation (LES)** is hereby authorized under the `fireFoam` solver family, strictly governed by `/filesystem/Firm/Standards/Reference_Cases/fireFoam_transient_controlDict.txt` and `CFDME_Modeling_Standards_Fire_rev4.pdf`.

---

### Key Technical Findings & Quantitative Determinations

#### 1. Residual Plateau & Plume Dynamics
* **Nature of the Plateau:** In Attempt 3, residuals initially dropped through iteration 400 (~3 orders on velocity, 4 orders on pressure), then entered a persistent limit-cycle plateau between iterations 400 and 800 ($U_x$ initial residual pegged in $3.00\times 10^{-4}$ to $8.00\times 10^{-4}$; $p$ residual in $2.00\times 10^{-5}$ to $3.00\times 10^{-5}$). Centerline probe 0 ($x = 1.50\text{ m}$, $y = 0.00\text{ m}$, $z = 8.00\text{ m}$) oscillated with a peak-to-peak amplitude of $40.00\text{ K}$ on temperature and $2.40\text{ m/s}$ on vertical velocity at a period of $\sim 1.15\text{ s}$.
* **Physical Phenomenon:** This plateau is **not** numerical noise or solver stalling; it is the physical **Cetegen–Ahmed buoyant puffing instability** of the $30.10\text{ MW}$, $D = 3.00\text{ m}$ fire plume.
* **Theoretical Frequency & Period:** Per `CFDME_Modeling_Standards_Fire_rev4.pdf` §4, $f = 1.50 \cdot D^{-1/2}\text{ Hz}$. For $D = 3.00\text{ m}$:
  * Frequency: $f = 1.50 \cdot (3.00)^{-1/2} = 0.8660\text{ Hz} \rightarrow \mathbf{0.87\text{ Hz}}$
  * Period: $T_p = 1 / f = (3.00)^{1/2} / 1.50 = 1.1547\text{ s} \rightarrow \mathbf{1.15\text{ s}}$
* **Run Observations:** Centerline probe 0 oscillated at $T_{p,\text{run}} = \mathbf{1.15\text{ s}}$ ($f_{\text{run}} = \mathbf{0.87\text{ Hz}}$).
* **Closeness / Percentage Agreement:** 
  * Unrounded period discrepancy: $|1.15\text{ s} - 1.1547\text{ s}| / 1.1547\text{ s} = \mathbf{0.41\%}$ discrepancy ($\mathbf{99.59\%}$ agreement).
  * Unrounded frequency discrepancy: $|0.8696\text{ Hz} - 0.8660\text{ Hz}| / 0.8660\text{ Hz} = \mathbf{0.41\%}\text{ to } \mathbf{0.46\%}$ discrepancy ($\mathbf{99.54\%}$ agreement).
  * Reported two-decimal precision: $\mathbf{1.15\text{ s}}$ vs. $\mathbf{1.15\text{ s}}$ and $\mathbf{0.87\text{ Hz}}$ vs. $\mathbf{0.87\text{ Hz}}$ represent an **exact $0.00\%$ numerical difference ($100.00\%$ match)**.
* **Existence of Steady Solution:** **ABSOLUTELY NOT.** Modeling Standard rev 4 Section 4 mandates: *"Because the plume oscillates at a finite, deterministic, physical frequency, no time-invariant flow field exists that any residual-tolerance schedule can converge to."* Chasing a steady solution is physically impossible and numerically invalid.

#### 2. Compliance Audit of Delivered Setup & Non-Conformances
* **Root Cause:** Mulshi delivered a setup (`OAS_case_setup_from_DWA.txt`) copied wholesale from `CFDME-2024-018 Dry Wash Aerospace` (`DWA_highaltitude_case_setup.txt`), an external aerodynamics case for high-altitude compressible flow ($p_\infty = 26,500\text{ Pa}$, $T_\infty = 223.00\text{ K} / -50.15\text{ }^\circ\text{C}$, $\rho_\infty = 0.40\text{ kg/m}^3$, $\text{Mach } 0.25$). This is a flagrant violation of Modeling Standard rev 4 Section 7 (*"Cross-Regime Transfer"*), which prohibits case reuse across physical envelopes without a complete first-principles rebuild.
* **Itemized Non-Conforming Items & Correct Requirements:**
  1. *Solver Selection:* Delivered steady `rhoSimpleFoam` / SIMPLE `fireFoam` loop $\rightarrow$ Must be transient reacting `fireFoam` LES (rev 4 §3.1).
  2. *Cross-Regime Transfer:* Inherited from aerospace high-altitude case $\rightarrow$ Must be rebuilt from first principles (rev 4 §7).
  3. *Ambient Thermodynamics:* Delivered $p_\infty = 26,500\text{ Pa}$, $T_\infty = 223.00\text{ K}$, $\rho_\infty = 0.40\text{ kg/m}^3$ $\rightarrow$ Must be ground-level Sonoran Desert WUI: $p = 101,325\text{ Pa}$, $T = 35.00\text{ }^\circ\text{C}$ to $42.00\text{ }^\circ\text{C}$, $\text{RH} = 10.00\%$ to $25.00\%$, $\rho = 1.14\text{ kg/m}^3$ to $1.17\text{ kg/m}^3$ (reference: $T_\infty = 293.15\text{ K}$, $\rho_\infty = 1.20\text{ kg/m}^3$).
  4. *Atmospheric Wind Inlet:* Delivered uniform aerospace inlet $\rightarrow$ Must be `atmBoundaryLayerInletVelocity` with matching turbulent $k$ and $\omega / \varepsilon$ profiles ($z_{\text{ref}} = 6.10\text{ m} / 20.00\text{ ft}$, $z_0 = 0.03\text{ m}$) per rev 4 §3.2.
  5. *Combustion Chemistry:* Delivered no chemistry / 1-in-5 SIMPLE sweeps $\rightarrow$ Continuous finite-rate Eddy Dissipation Concept (EDC) coupled to sub-grid strain on every LES time step (rev 4 §3.3).
  6. *Radiation Closure:* Delivered radiation off / arbitrary 32 rays $\rightarrow$ `fvDOM` with firm reference specification: 4 angular directions ($S_4$ quadrature), 2 wavelength bands split at $2.50\text{ }\mu\text{m}$ for $1200.00\text{ K}$ to $1700.00\text{ K}$ flame temperatures, participating media absorption/emission (rev 4 §3.4, Appendix A).
  7. *Turbulence Closure:* Delivered RAS $k$-$\omega$ SST $\rightarrow$ Large-Eddy Simulation (LES) using Dynamic Smagorinsky or WALE (rev 4 §5).
  8. *Wall Assembly & CHT:* Delivered single-region adiabatic wall $\rightarrow$ Multi-region conjugate heat transfer (`chtMultiRegionFoam`): outer leaf ($50.00\text{ mm}$ printed concrete), internal cavity ($205.00\text{ mm}$ air with participating radiation, emissivity $0.90$), inner leaf ($50.00\text{ mm}$ concrete), and discrete 9-gauge ($3.80\text{ mm}$) galvanized steel ties ($k = 45.00\text{ W/(m}\cdot\text{K)}$, emissivity $0.25$) embedded $25.00\text{ mm}$ with $4\times$ mesh refinement at tie-concrete interfaces (rev 4 §6).
  9. *Thermophysical Properties:* Delivered constant properties $\rightarrow$ Temperature-dependent $k(T)$, $\rho(T)$, $c_p(T)$ for concrete and steel, JANAF polynomials for gas species (rev 4 §3.5, Appendix A).
  10. *Time-Stepping Controls:* Delivered fixed $\Delta t = 0.01\text{ s}$, `adjustTimeStep no`, `writeControl timeStep` ($100$ steps) $\rightarrow$ Adaptive stepping (`adjustTimeStep yes`), $\text{maxCo} = 0.90$, $\text{maxDeltaT} = 0.01\text{ s}$, `writeControl adjustableRunTime` (rev 4 §4).

#### 3. Specifications of the Authorized Production Run
* **Governing Reference Dictionary:** `/filesystem/Firm/Standards/Reference_Cases/fireFoam_transient_controlDict.txt` (enforces mandatory ceilings: $\text{maxCo} = 0.90$, $\text{maxDeltaT} = 0.01\text{ s}$, `adjustTimeStep yes`).
* **Largest Permissible Write Interval:** Standard rev 4 §4 mandates $\ge 25$ samples per puffing period. With $T_p = 1.1547\text{ s}$, $\text{writeInterval} \le 1.1547 / 25 = 0.046188\text{ s} \rightarrow \mathbf{0.0461\text{ s}}$ (guarantees $25.05$ samples per physical cycle; if evaluated against rounded $1.15\text{ s}$, $0.0460\text{ s}$).
* **Shortest Permissible End Time:** Standard rev 4 §4 mandates a minimum of 20 puffing cycles past initial transient clearance ($8.00\text{ s}$ from fine-grid study log). 20 cycles $= 20 \cdot 1.1547\text{ s} = 23.09\text{ s}$. Shortest compliant end time $= 8.00\text{ s} + 23.09\text{ s} = \mathbf{31.09\text{ s}}$ (or $31.00\text{ s}$ on rounded cycles; reference dictionary ceiling is $60.00\text{ s}$).
* **Side-by-Side Time-Control Comparison (Every Differing Entry):**
  * `adjustTimeStep`: Authorized: `yes` | Delivered: `no`
  * `maxCo`: Authorized: `0.9` | Delivered: `[omitted]`
  * `maxDeltaT`: Authorized: `0.01` s | Delivered: `[omitted]`
  * `writeControl`: Authorized: `adjustableRunTime` | Delivered: `timeStep`
  * `writeInterval`: Authorized: `0.0461` s | Delivered: `100` (time steps, representing $1.00\text{ s}$)
  * `deltaT`: Authorized: `0.001` s (initial) | Delivered: `0.01` s (fixed)
  * `endTime`: Authorized: `31.09` s (or $60.00\text{ s}$) | Delivered: `2000` (outer iterations)
  * `startFrom`: Authorized: `startTime` (or `latestTime`) | Delivered: `startTime`
  * `writePrecision`: Authorized: `8` | Delivered: `6`
* **Mesh Identification:** Attempt 3 ran on production mesh `OAS-WUI-01_revC` ($11,214,862\text{ cells}$, domain top $z = 40.00\text{ m}$) meshed by Renata Ellsworth on 10/09/2025 morning (`log.snappyHexMesh_20251009.txt`).
* **Verification Scope:**
  * *What it covers:* Background $dx = 0.50\text{ m}$ sized against $D^* = 3.76\text{ m}$ yields $D^*/dx = \mathbf{7.52}$ (conforming to the mandatory $5.00\text{ to }10.00$ band per QA Verification Standard rev 3 §5.1); mesh quality checks passed with "Mesh OK" (non-orthogonality max $45.30^\circ \le 70.00^\circ$, skewness max $1.52 \le 4.00$, aspect ratio max $8.42 \le 20.00$); fluid-only three-grid LES study (`three_grid_study_outputs.txt`) demonstrated Pope resolved-TKE fraction $k_{\text{res}} / (k_{\text{res}} + k_{\text{sgs}}) = \mathbf{84.00\%} \ge 80.00\%$.
  * *What it does not cover:* Multi-region CHT discretization, cavity radiation, $4\times$ tie embedment refinement (rev 4 §6); domain height differs ($z = 40.00\text{ m}$ vs. $z = 60.00\text{ m}$), so raw cell counts ($11.21\text{M}$ vs. $11.20\text{M}$) are not directly comparable; does not cover client's revD geometry ($610.00\text{ mm}$ parapet transmitted 10/09/2025 without a signed change order).
* **Carried Forward vs. Rebuilt:** Only the `OAS-WUI-01_revC` polyMesh geometry and patch naming carry forward. All physics, boundary conditions, thermophysical tables, and initial fields are discarded and rebuilt new.
* **Inlet Defining Settings:** `atmBoundaryLayerInletVelocity` with matching $k$ and $\omega / \varepsilon$; $z_{\text{ref}} = 6.10\text{ m}$ ($20.00\text{ ft}$); $z_0 = 0.03\text{ m}$ (Exposure C desert scrub); $U_{\text{ref}} = 5.00\text{ m/s}$, $8.00\text{ m/s}$, $12.00\text{ m/s}$; wind directions $\theta = 240.00^\circ$ and $270.00^\circ$ (SOW §3.1).

#### 4. Computational Cost, Wall-Clock Projections & Usability Audit
* **Firm's Projection Basis:** Linear scaling in physical time on fixed mesh, solver stack, and core count ($0.14375\text{ h/s} = 8\text{ minutes and } 38\text{ seconds per simulated second}$, or $6.96\text{ simulated seconds per wall-clock hour}$ established from fine-grid study run of record: $40.00\text{ s}$ reached in $5\text{ hours and } 45\text{ minutes}$ on `borrego` + cloud burst).
* **Projected Solver Wall Clock:**
  * **One Authorized Case (at shortest standard $31.09\text{ s}$):** $\mathbf{4\text{ hours and } 28\text{ minutes}}$ ($4\text{h } 28\text{m} / 4.47\text{ h}$). *(At $31.00\text{ s}$: $4\text{h } 27\text{m}$; at $40.00\text{ s}$: $5\text{h } 45\text{m}$; at $60.00\text{ s}$ reference ceiling: $8\text{h } 38\text{m}$).*
  * **Full Wildfire Matrix ($6\text{ cases}$ per SOW §3.1):** $\mathbf{26\text{ hours and } 49\text{ minutes}}$ ($26\text{h } 49\text{m} / 26.82\text{ h}$). *(At $31.00\text{ s}$: $26\text{h } 44\text{m}$; at $40.00\text{ s}$: $34\text{h } 30\text{m}$; at $60.00\text{ s}$ reference ceiling: $51\text{h } 45\text{m}$).*
* **Can the Projection Basis Be Met?** **NO.** The basis cannot be strictly met on every condition it sets:
  1. *Mesh Mismatch:* Run of record was fluid-only; production mesh is a multi-region CHT case (solid conduction, cavity radiation, coupled interface iterations), adding heavy per-step overhead.
  2. *Core-Count Mismatch:* Run of record ran on `borrego` + cloud burst ($192\text{ to }256\text{ cores}$); running on Mulshi’s $64\text{ cores}$ cuts parallel throughput by $\sim 3\times\text{ to }4\times$.
  3. *Zero Courant Margin:* Fine-grid study ran at mean $\text{Co} = 0.47$ and max $\text{Co} = 0.90$ (pegged against the ceiling) with average $\Delta t = 2.20\times 10^{-3}\text{ s}$ ($0.0022\text{ s}$). Zero Courant headroom remains. Higher design winds ($12.00\text{ m/s}$) and local $4\times$ tie refinement will force $\Delta t$ down (to $0.0005\text{ s} - 0.0010\text{ s}$), doubling iteration counts and wall clock.
* **Valuation of the Figure:** Represents an **idealized lower-bound floor**. True operational wall clock on 64 cores with multi-region CHT will be **$2.5\times\text{ to }4.0\times$ higher** ($11\text{ to }18\text{ hours}$ per case, or $65\text{ to }105\text{ hours}$ for the matrix).
* **Attempt 3 Consumption:** Burned $\mathbf{6\text{ hours and } 41\text{ minutes}}$ ($6\text{h } 41\text{m} / 24,060.00\text{ s}$) across 64 cores ($424.30\text{ user CPU-hours}$) to reach iteration 800.
* **Comparison to Authorized Case:** Attempt 3 consumed **$149.63\%$ ($\sim 1.5\times$)** of the wall clock required to complete an entire authorized production transient run ($4\text{h } 28\text{m}$), while achieving **$0.00\text{ s}$ of valid simulated physical time**.
* **Downstream Usability:** **EXACTLY ZERO ($0.00\%$).** Completely unusable. Initializing from Attempt 3 would contaminate the transient LES with non-physical under-relaxation and limit-cycle residual distortions. The run must be discarded in its entirety.

---

### Verification of Deliverable File & Required Formatting

The deliverable has been written directly to:
`/filesystem/CFDME-2025-041_transient_solve_disposition_revA.docx`

* **Letterhead & Metadata:** Official firm header (`THE CFD ME | Tucson, Arizona | AZ PE #48213 | CFDME-2025-041 rev A`), title block, and complete memo table.
* **Reviewer & Stamp Block:** Completed dual sign-off table containing Gordon Selby, PE (AZ PE #48213) and Marguerite Falk, PE (AZ PE #42798), dated 10/10/2025.
* **Mandatory Stamp Boundary Language:** Embedded verbatim:  
  `"CFD thermal analysis only. Fire-resistance rating certified separately by others."`
* **Unit Discipline & Numeric Precision:** Fully compliant with Units SOP rev 2:
  * Strict internal SI units on every value.
  * Simulated physical times formatted to two decimal places (`xx.xx s`).
  * Computational wall clocks formatted in hours and minutes (`X hours and Y minutes` / `Xh Ym`).
  * Plume frequencies and periods formatted to two decimal places (`xx.xx Hz`, `xx.xx s`).
  * Solver write interval formatted to four decimal places (`x.xxxx s`).
  * Explicit 10-point project assumption register included in Section 6.