### Coordinated 3D MEP Model Delivery Summary (`dc_model hall_seed000_d000`)

#### Deliverables Produced
- **Main Solution Script**: `output/solution.py`
  - Self-contained, deterministic Python script executing in ~0.8 seconds (well within the 300 s budget).
  - Uses `ifcopenshell==0.8.4` and `numpy`.
  - Generates the coordinated IFC4 model to `sys.argv[1]` (default `output/model.ifc`).
  - Passes schema validation with `express_rules=True` with 0 errors.
- **Generated Model**: `output/model.ifc` (346 KB)
- **Reconciliation Side File**: `output/reconciliation.json` (listing all parameters extracted from drawings A-101 through F-101 and how each was applied).

---

### Reconciled Background Elements
- **Room & Grid**: 27,000 × 21,000 mm overall dimension with a 600 mm access floor tile grid (origin at SW internal corner, tiles A..AS / 1..35).
- **Access Floor Slab**: 27,000 × 21,000 × 35 mm (`IfcSlab`/`FLOOR`/`"AccessFloor"`), top at ±0 mm (finished floor) over a 865 mm clear plenum void (slab at -900 mm).
- **Structural Columns (6)**: 600 × 600 mm full clear height from 0 to 3600 mm (`IfcColumn`/`COLUMN`/`"StructuralColumn"`) at structural grid intersections (8400, 8400), (16800, 8400), (25200, 8400), (8400, 16800), (16800, 16800), (25200, 16800).
- **Cabinets (128)**: Modelled as `IfcFurniture`/`USERDEFINED`/`"Rack"` with required `Pset_DCM_Rack` property sets, correct rotations (facing South in Rows A, C, E and North in Rows B, D, F) about footprint centres:
  - 119 server cabinets type C1 (600 × 1200 × 2000 mm).
  - 9 distributor cabinets type N1 (800 × 1200 × 2000 mm).
  - Bay sequence and cross-aisle break (common east edge at $x = 11,400\text{ mm}$) exactly matching A-601.
- **CRAH Units (22)**: `IfcUnitaryEquipment`/`USERDEFINED`/`"CRAH"` with `Pset_DCM_CRAH`:
  - 18 In-row CRAH units (600 × 1200 × 2000 mm, 50 kW) facing row direction.
  - 4 Perimeter CRAH gallery units (1200 × 900 × 2000 mm, 100 kW) at tiles B01, P01, AC01, AQ01 facing North.
- **PDUs (6)**: `IfcElectricDistributionBoard`/`USERDEFINED`/`"PDU"` with `Pset_DCM_PDU`:
  - 762 × 813 × 1959 mm at tiles AJ05, AK10, AJ14, AK19, AJ23, AK28, set flush with row front faces.
- **Cold-Aisle Containment**: `IfcCovering`/`CEILING`/`"ContainmentRoof"` and `IfcDoor`/`DOOR`/`"ContainmentDoor"` with `Pset_DCM_Containment`:
  - CAC-BC and CAC-DE roofs: 1400 mm wide (100 mm overhang each side), 55.5 mm thick, underside at +2000 mm. West panels ($x \in [1860, 9940]$) and East panels ($x \in [11460, 19740]$).
  - 8 End doors (60 × 1200 × 2055.5 mm) closing aisle ends and cross-aisle breaks.
- **Sprinkler Grid (79 heads)**: `IfcFireSuppressionTerminal`/`SPRINKLER`/`"SprinklerHead"` with `Pset_DCM_Sprinkler`:
  - 63 ceiling heads at $z = 3575\text{ mm}$ (deflectors) on 3000 × 3000 mm grid ($x \in [1500..25500]$, $y \in [1500..19500]$), with heads near column keep-outs relocated clear per F-101.
  - 16 in-aisle heads under containment roofs at $z = 1890\text{ mm}$ (deflector hanging from roof soffit).

---

### Coordinated MEP Routing & Tiers
1. **Chilled Water Pipe (`CHW-1`)**:
   - `IfcPipeSegment`/`RIGIDSEGMENT`/`"ChilledWaterPipe"` with `Pset_DCM_Pathway`.
   - Bare OD 114.3 mm + 25.4 mm insulation = 168.3 mm OD over insulation.
   - Overhead Tier 1 at $z_{\text{center}} = 2710.0\text{ mm}$ ($z \in [2625.85, 2794.15]\text{ mm}$).
   - Enters at $(0, 9900\text{ mm})$, connects to N-S trunk at $x = 250\text{ mm}$, and headers serve Rows A–F (100% length) and Perimeter CRAHs ($y = 1800\text{ mm}$).
   - Reaches within 1626–2061 mm of all 22 CRAHs ($\le 2500\text{ mm}$).
2. **Power Busway (`BW-1`)**:
   - `IfcCableSegment`/`BUSBARSEGMENT`/`"Busway"` with `Pset_DCM_Pathway`.
   - Section 128 mm (W) × 147 mm (H).
   - Overhead Tier 2 at $z_{\text{center}} = 2950.0\text{ mm}$ ($z \in [2876.5, 3023.5]\text{ mm}$).
   - Enters at $(0, 9450\text{ mm})$, connects to N-S trunk at $x = 600\text{ mm}$, and branch headers serve Rows A–F (100% length), offset around columns to ensure clearance.
3. **Telecom Cable Tray (`CT-1`)**:
   - `IfcCableCarrierSegment`/`CABLETRAYSEGMENT`/`"CableTray"` with `Pset_DCM_Pathway`.
   - Section 683 mm (W) × 127 mm (H).
   - Under-floor plenum route at $z_{\text{center}} = -163.5\text{ mm}$ ($z \in [-227.0, -100.0]\text{ mm}$), maintaining 65 mm clearance below floor panels ($> 20\text{ mm}$ ANSI/TIA-942 requirement).
   - Enters at $(0, 9900\text{ mm})$, connects to N-S trunk at $x = 1400\text{ mm}$, and branch headers serve Rows A–F (100% length).

---

### Mechanical Verification Against Constraints
- **Hard Clashes**: Tested pairwise across all 279 3D solids in the model. **0 hard clashes (> 2 mm)**.
- **Connectivity**: All 3 networks are 100% connected graphs originating from their respective entry points at $x = 0$.
- **Row Coverage**: Rows A, B, C, D, E, F are each 100.0% served by all three services within $\le 800\text{ mm}$ of row centrelines ($\le 2500\text{ mm}$ constraint).
- **CRAH Service**: All 22 CRAHs are within $2061\text{ mm}$ of CHW piping ($\le 2500\text{ mm}$ constraint).
- **Headroom**: Bottom of lowest overhead service is $z = 2625.85\text{ mm} \ge 2600\text{ mm}$.
- **Sprinkler Standoff**: Top of highest overhead service is $z = 3023.5\text{ mm}$, leaving $551.5\text{ mm}$ vertical clearance to ceiling deflectors ($z = 3575\text{ mm}$), exceeding the 460 mm standoff requirement.
- **Tray–Busway Separation**: Tray is under-floor ($z = -100\text{ mm}$) and Busway is overhead ($z = 2876.5\text{ mm}$), achieving $2976.5\text{ mm}$ vertical separation everywhere ($\ge 300\text{ mm}$ requirement).
- **PDU Dedicated Space**: Dedicated space (1800 mm above each PDU, up to ceiling slab soffit at 3600 mm) has zero piping penetration; all CHW runs remain west of $x = 20,200\text{ mm}$ while PDUs start at $x = 21,000\text{ mm}$.