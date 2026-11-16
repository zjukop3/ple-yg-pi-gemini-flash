### Cattail Run Data Campus — Phase 1 Foundation Strategy Summary

As Structural Engineer of Record for Ardent Vale Infrastructure LLC, the Phase 1 foundation strategy evaluation and design have been completed across all six single-storey building pads (`CR-P1` … `CR-P6`) on the Cattail Run Data Campus in Loudoun County, Virginia.

The final deliverable has been written and verified at:
`/filesystem/dc_structural__foundation_strategy__blind/output/submission.zip`

The archive contains exactly the six required files at its root:

1. **`foundation_geometry.json`**:
   * Complete Revit foundation geometry parameter file conforming strictly to the owner's BIM Parameter Standard Rev. 2.
   * Covers all 36 foundation units (five isolated column footings and one continuous shear-wall footing per pad across all six pads).
   * All plan dimensions (`B_in`, `L_in`), thicknesses (`thickness_in`), and bearing depths (`bearing_depth_in`) are dimensioned to the owner's 3-inch grid; minimum footing thickness is 12 inches.
   * Uniform bearing depth of 42 inches below finished grade across all pads, founded in Stratum I, satisfying the frost protection requirement for a 100-year Air Freezing Index of 556 °F-days (> 500 °F-days) per Loudoun County AHJ Amendment 3 and NOAA NCEI 1981–2010 normals.
   * Shear-wall footings (`W1`) on all pads carry computed `sliding_fs` (≥ 1.5), `eccentricity_in` (≤ 48 in, within the kern/middle third `L/6`), and `uplift_fs` (≥ 1.5).

2. **`ground_improvement_plan.json`**:
   * Complete ground-improvement programme conforming to the BIM Parameter Standard:
     * `stress_concentration_ratio_ns`: 10.0 (per FHWA GEC 13 Vol 1 Section 4.2.2 and RFI-011 for structure foundation support under rigid footings).
     * `pier_diameter_in`: 30 inches (2.5 ft).
     * `rigs_mobilised`: 2 rigs.
     * `mobilisation_cost_usd`: $80,000.00 ($40,000 per rig, maximum 2 pads per rig).
     * `pads_improved`: `["CR-P1", "CR-P2", "CR-P4", "CR-P6"]`.
     * `rig_assignments`: `{"RIG-1": ["CR-P1", "CR-P2"], "RIG-2": ["CR-P4", "CR-P6"]}`.
     * `modulus_tests`: 1 production modulus test per improved pad ($9,500 each).
     * `pads`: Contains pad-level tested stiffness modulus (`stiffness_modulus_pci`), treatment depth (`treatment_depth_ft`), and total pier linear footage (`total_pier_lf`).

3. **`foundation_schedule.xlsx`**:
   * Formatted on the owner's template with all 19 columns and all 36 foundation rows.
   * Exactly agrees with `foundation_geometry.json` in dimensions, thickness, bearing depth, concrete strengths, w/cm ratios, reinforcement ratios, bar sizes and spacings, pier quantities, settlements, and governing constraints.

4. **`foundation_feasibility_matrix.md`**:
   * Comprehensive pad-by-pad evaluation matrix for all 36 foundations detailing service demands, bearing capacity checks, settlement predictions, shear-wall stability checks, governing constraints, foundation decisions, and comparative costs of both alternatives (spread footings alone vs. improved spread footings).

5. **`constraint_register.xlsx`**:
   * Formatted on the owner's template with all nine required columns: `req_id`, `document`, `clause`, `requirement`, `value`, `unit`, `kind`, `applies_to`, and `resolution`.
   * Exactly 48 rows (well under the 96-row parsing cutoff), placing live substantive requirements first (governing bearing capacity equations, factors of safety per occupancy from UFC 3-220-01 Table 2-3, groundwater correction, settlement limit 1.0 in, angular distortion limit 1/500, minimum footing widths, frost depth, sliding/overturning/uplift criteria, concrete durability limits per UFGS 03 30 00 and EM 1110-2-2000, aggregate pier bounds, and mobilisation limits), followed by cancelled and superseded documents explicitly identified as set aside.

6. **`design_basis.md`**:
   * Opens with the required fenced ```json block stating frost indices (100-yr AFI = 556 °F-days for 1981–2010 vs. superseded 416 °F-days for 1951–1980), pad decisions, comparative costs, campus totals, and rejected criteria.
   * Full engineering narrative detailing governing criteria and set-aside documents; bearing capacity (Meyerhof, Hansen, Vesic) and layered elastic settlement methods; factor of safety basis; tolerable movement criteria; ground improvement parameters; document conflict resolutions; and campus programme optimisation logic.

---

### Campus Programme Optimisation Rationale

* **`CR-P1`, `CR-P2`, `CR-P6` (Improved Spread Footings)**: Underlain by soft Stratum I residual soils ($E_s = 85\text{--}110\text{ ksf}$). Unimproved spread footings at the 42-in frost elevation exceed the 1.0-in settlement and 1/500 angular distortion limits even at excessive dimensions ($>25\text{ ft}$). Deepening to Stratum II requires costly dewatering below groundwater and massive excavations with side slopes. Rammed aggregate piers terminate into Stratum II (11 ft depth), controlling settlement to $\le 0.98\text{ in}$ and angular distortion to $< 1/500$. These three pads require two mobilised rigs.
* **`CR-P4` (Improved Spread Footings)**: Unimproved spread footings are technically feasible but require huge footings ($W1$ $B=22.25\text{ ft}$, $F3$ $B=19.0\text{ ft}$) costing $61,623. Because Rig 2 is already mobilised for `CR-P6` (and can serve up to 2 pads), it has capacity to serve `CR-P4` at zero additional mobilisation cost. Improving `CR-P4` costs $45,881, yielding a direct net savings of over $15,700.
* **`CR-P3` & `CR-P5` (Spread Footings Alone)**: Underlain by thin, stiff Stratum I soils ($E_s = 210\text{--}250\text{ ksf}$). Compact spread footings founded at 42 in are fully compliant with bearing capacity and settlement ($s \le 0.81\text{ in}$ on `CR-P5`, $s \le 0.995\text{ in}$ on `CR-P3`) and angular distortion ($< 0.0012$). Spread footings cost only $32,729 on `CR-P3` and $16,774 on `CR-P5`. Improving either pad would trigger mobilising a third rig ($40,000) and production testing ($9,500), adding over $50,000 in unnecessary cost.
* **Campus Total**: Exactly **2 rigs** mobilised, serving **4 improved pads** and **2 unimproved pads**, achieving an optimal, fully compliant total campus foundation cost of **$423,252.57**.