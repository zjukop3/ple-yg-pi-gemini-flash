I have completed the technical investigation and compiled the deliverable note as requested. It is saved on the file server as:

**/filesystem/CFDME-2025-041_resolution_note_revA.docx**

Below is a summary of the technical findings and the basis for settling Peer-Review Checklist Item 4 with Marguerite Falk, PE, using strictly the data already on the file server.

---

### Executive Summary of Key Findings

| Question / Parameter | Value of Record / Status | Governing Standard Basis | Resolution Impact |
| :--- | :--- | :--- | :--- |
| **Plume Resolution Index ($D^*/dx$)** | **$D^*/dx = 7.52$ (reported as $7.5$)**<br>Fine grid $dx = 0.5\text{ m}$<br>Plume scale $D^* = 3.76\text{ m}$ ($Q = 30.1\text{ MW}$) | QA Verification Standard rev 3 §5.1<br>Required band: **$5\text{ to }10$** | **Band is met** (+50.4% margin above minimum; sitting at the optimal center of the band). |
| **Pope Resolved-TKE Fraction** | **$k_{\text{res}} / (k_{\text{res}} + k_{\text{sgs}}) = 84\%$ (0.84)**<br>Plume centerline probe at $z = 0.75\cdot D^*$ ($2.82\text{ m}$)<br>Sampled at $t = 40.0\text{ s}$ ($>20$ puffing cycles) | QA Verification Standard rev 3 §5.2<br>Minimum threshold: **$\ge 80\%$** | **Criterion is met** (+4% margin). |
| **Acceptance Basis** | Dual compliance with both §5.1 ($D^*/dx \in [5, 10]$) and §5.2 (Pope TKE $\ge 80\%$) | QA Verification Standard rev 3 §5 | **No decision required from Marguerite.** Criteria are strictly met numerically with no waivers or variances. Marguerite already co-signed this exact basis in the Scoping Memo (10/08/2025). |
| **Resolved-Energy Sampling Location** | Plume centerline axis, $z = 0.75\cdot D^* = 2.82\text{ m}$ above source | QA Verification Standard rev 3 §5.2 | **Inside the buoyancy-dominated region.** Sited directly in the core continuous flaming / necking zone ($L_{\text{flame}} = 5.4\text{ m}$), well away from boundaries. |
| **Ambient Values behind $D^*$ vs. Site** | **Reference:** $20^\circ\text{C}$, $1.204\text{ kg/m}^3$, $101.325\text{ kPa}$<br>**Site:** $35\text{–}42^\circ\text{C}$, $\sim 750\text{ m}$ elevation ($92.6\text{ kPa}$), $\rho \approx 1.02\text{–}1.05\text{ kg/m}^3$ | Thermodynamic check on $D^*$ formulation ($\rho_\infty \cdot T_\infty = P_\infty / R$) | Reference air does **not** represent site, but site conditions **increase** $D^*$ to $\sim 3.88\text{ m}$ and $D^*/dx$ to **$7.75$**, remaining well inside the $5\text{–}10$ band. Reference air is conservative. |
| **Checklist Item 4 Closure Status** | **Cannot close on rev B as drafted.**<br>**Settles immediately upon Section 6 text relocation.** | QA Verification Standard rev 3 §§3 & 6 | Formatting defect: rev B pointed to Appendix C and carried a RANS table. Moving existing data into Section 6 body settles the item with **no new runs**. |

---

### Detailed Breakdown

#### 1. Plume Resolution Index, Cell Size, and Band Compliance
* **Reporting Grid of Record:** The Phase 1 Report rev B thermal analysis rests on the **Fine Grid** ($11{,}196{,}000\text{ cells}$ fluid verification / $11{,}214{,}862\text{ cells}$ production conjugate mesh), with a background cell edge length of **$dx = 0.5\text{ m}$** across the wildfire sub-domain. (The near-source cylinder carries two additional snappy levels down to $dx = 0.125\text{ m}$).
* **Plume Length Scale ($D^*$):** Sourced from the $3.0\text{ m}$ front segment at Byram fireline intensity $I = 10{,}040\text{ kW/m}$, yielding total heat release rate $Q = 30.1\text{ MW}$ ($30{,}120\text{ kW}$). Evaluated under standard reference air ($\rho_\infty = 1.204\text{ kg/m}^3$, $c_p = 1005\text{ J/(kg}\cdot\text{K)}$, $T_\infty = 293.15\text{ K}$, $g = 9.81\text{ m/s}^2$):
  $$D^* = \left(\frac{Q}{\rho_\infty c_p T_\infty \sqrt{g}}\right)^{2/5} = 3.76\text{ m}$$
* **Plume Resolution Index:**
  $$D^*/dx = \frac{3.76\text{ m}}{0.5\text{ m}} = 7.52 \quad (\text{reported as } 7.5)$$
* **Band Assessment:** QA Verification Standard rev 3 §5.1 requires $D^*/dx \in [5, 10]$. Our index $7.52$ lands directly in the center of the band ($+50.4\%$ margin above $5.0$, $-24.8\%$ below $10.0$). **The firm band is met.**

#### 2. Resolution Acceptance Basis & Reviewer Decision
* **What Acceptance Rests On:** QA Verification Standard rev 3 §5 accepts either criterion alone ($D^*/dx \in [5, 10]$ per §5.1, or Pope resolved-TKE fraction $\ge 80\%$ per §5.2), but prefers both for life-safety / AHJ deliverables. The fine reporting grid satisfies **both** criteria ($D^*/dx = 7.52$ and Pope fraction $= 84\%$), meeting the firm's highest standard of verification evidence.
* **Does It Need a Decision from Marguerite?** **No.** Both criteria are strictly met with positive margin; no discretionary waiver, variance, or "engineering judgement" substitution is requested. Furthermore, Marguerite reviewed and concurred with the exact $D^* = 3.76\text{ m}$ and $dx = 0.5\text{ m}$ sizing basis when she co-signed the Phase 1 Scoping Memo on 10/08/2025. Her only role on Item 4 is confirming that the report body carries the verified numbers.

#### 3. Resolved-Energy Probe Location & Site Ambient Conditions
* **Was the Resolved-Energy Figure Sampled Inside the Region the Index Describes?**
  * **Yes.** The probe was located on the plume centerline axis at $z = 0.75\cdot D^* = 2.82\text{ m}$ above the fuel bed, sampled at $t = 40.0\text{ s}$ over 28 puffing cycles ($T = 1.15\text{ s}$, $f = 0.87\text{ Hz}$ per Modeling Standards rev 4 §4).
  * $D^* = 3.76\text{ m}$ defines the buoyancy-dominated plume core. In this fire, solid flame length is $L = 5.4\text{ m}$ (wind-tilted Byram) and still-air flame height is $\sim 11.5\text{ m}$. At $z = 2.82\text{ m}$, the probe sits directly in the core continuous flaming / buoyant vortex necking region, far from domain boundaries, strictly fulfilling §5.2.
* **Do Ambient Values Represent the Site, and What Would Site Conditions Do?**
  * **No.** Standard sea-level air ($20^\circ\text{C}$, $1.204\text{ kg/m}^3$, $101.325\text{ kPa}$) was used in the formula, whereas the Avra Valley WUI site design envelope is $35\text{–}42^\circ\text{C}$, RH $10\text{–}25\%$, at $\sim 750\text{ m}$ elevation ($P_{\text{amb}} \approx 92.6\text{ kPa}$).
  * **Thermodynamic Impact:** Since air is an ideal gas, $\rho_\infty \cdot T_\infty = P_\infty / R$. At constant pressure, temperature rise lowers density inversely, leaving $\rho_\infty \cdot T_\infty$ virtually constant ($<0.1\%$ effect on $D^*$). However, the lower barometric pressure at $750\text{ m}$ elevation ($\sim 8.6\%$ below sea level, $\rho \approx 1.02\text{–}1.05\text{ kg/m}^3$) decreases the denominator, which **increases $D^*$ by $\sim 3.5\%$ from $3.76\text{ m}$ to $3.88\text{ m}$**.
  * On the $dx = 0.5\text{ m}$ mesh, $D^*/dx$ increases from **$7.52$ to $7.75$**.
  * Under all physical interpretations, $D^*/dx$ remains between $7.48$ and $7.75$, safely inside the $5\text{ to }10$ band. The standard-air formulation of record is slightly conservative.

#### 4. Checklist Item Closure Status & Settlement Path
* **Can Item 4 Close Now?** **No, not on the rev B draft as it currently stands.** Section 6 of rev B contains a non-compliant RANS-style three-grid monitor table (violating §6) and delegates the resolution numbers to Appendix C (violating §3 and §6). Marguerite’s checklist objection was procedurally correct.
* **What Would Settle It?** No new CFD runs or compute time are required. All necessary data is already verified in `three_grid_study_outputs.txt`. Item 4 is settled completely by:
  1. Moving the verified resolution figures ($Q = 30.1\text{ MW}$, $D^* = 3.76\text{ m}$, $dx = 0.5\text{ m}$, $D^*/dx = 7.5$, Pope fraction $= 84\%$ at $z = 0.75\cdot D^*$, and the single-sentence compliance statement per §3(d)) directly into **Section 6 body text and table**.
  2. Relegating the three-grid monitor comparison table to **Appendix C as an informational sensitivity study**.
* The Word document `/filesystem/CFDME-2025-041_resolution_note_revA.docx` includes the **exact ready-to-insert text for Section 6** and a completed Reviewer Sign-off / PE Stamp block for Marguerite Falk to close Item 4.