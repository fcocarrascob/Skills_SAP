# Expand Verified Registry — Implementation

## Goal
Add ~33 verified SAP2000 API wrapper functions to the registry, covering critical gaps in loading, releases, groups, constraints, results (including modal), analysis control, and linear links — raising workflow coverage from ~60% to ~90%.

## Prerequisites
Make sure that the user is currently on the `expand-verified-registry` branch before beginning implementation.
If not, move them to the correct branch. If the branch does not exist, create it from main.

---

### Step-by-Step Instructions

---

#### Step 1: Cargas en Objetos — Core Loading (6 wrappers)

##### 1.1 — `FrameObj.SetLoadDistributed`

- [x] Create file `scripts/wrappers/func_FrameObj_SetLoadDistributed.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadDistributed
# Category: Object_Model
# Description: Assign distributed loads (force/moment per unit length) to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists, load pattern defined
# ============================================================
"""
Usage: Assigns distributed loads along the length of frame objects.
       Supports uniform and trapezoidal distributions, in any direction.

API Signature:
  SapModel.FrameObj.SetLoadDistributed(Name, LoadPat, MyType, Dir,
      Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Frame object name (or group name if ItemType=1)
  LoadPat : str   — Load pattern name
  MyType  : int   — 1=Force/length, 2=Moment/length
  Dir     : int   — Direction: 1-3=Local, 4-6=Global XYZ, 10=Gravity, 11=Projected Gravity
  Dist1   : float — Start distance (relative 0-1 or absolute [L])
  Dist2   : float — End distance (relative 0-1 or absolute [L])
  Val1    : float — Load value at start [F/L] or [FL/L]
  Val2    : float — Load value at end [F/L] or [FL/L]
  CSys    : str   — "Global" or "Local" or named coordinate system
  RelDist : bool  — True=relative distances, False=absolute
  Replace : bool  — True=replace previous loads in pattern
  ItemType: int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0, f"SetRectangle failed: {ret}"

# Create simply supported beam, 8m span
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Supports
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

# --- Target function: uniform load ---
# Full-length uniform downward load: -15 kN/m (gravity direction)
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -15, -15, "Global", True, True
)
assert ret == 0, f"SetLoadDistributed(uniform) failed: {ret}"

# --- Target function: trapezoidal load ---
# Add LIVE pattern
ret = SapModel.LoadPatterns.Add("LIVE", 3, 0, False)
assert ret == 0, f"LoadPatterns.Add(LIVE) failed: {ret}"

# Trapezoidal load from 0 to midspan: 0 kN/m -> -20 kN/m
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "LIVE", 1, 10, 0, 0.5, 0, -20, "Global", True, True
)
assert ret == 0, f"SetLoadDistributed(trapezoidal) failed: {ret}"

# --- Verification: query back via GetLoadDistributed ---
raw = SapModel.FrameObj.GetLoadDistributed(
    beam_name, 0, [], [], [], [], [], [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadDistributed failed: {ret_code}"
num_loads = raw[0]
assert num_loads >= 2, f"Expected >=2 loads, got {num_loads}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadDistributed"
result["beam_name"] = beam_name
result["num_loads_assigned"] = num_loads
result["status"] = "verified"
```

- [x] Execute via `run_sap_script` and verify `ret_code == 0` and `num_loads_assigned >= 2`.
- [x] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.SetLoadDistributed`
  - `category`: `Object_Model`
  - `description`: `Assign distributed loads (force/moment per unit length) to frame objects`
  - `signature`: `(Name, LoadPat, MyType, Dir, Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType) -> ret_code`
  - `wrapper_script`: `func_FrameObj_SetLoadDistributed`

---

##### 1.2 — `FrameObj.SetLoadPoint`

- [x] Create file `scripts/wrappers/func_FrameObj_SetLoadPoint.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadPoint
# Category: Object_Model
# Description: Assign point loads (force/moment) to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists, load pattern defined
# ============================================================
"""
Usage: Assigns a concentrated load at a specified distance along a frame.

API Signature:
  SapModel.FrameObj.SetLoadPoint(Name, LoadPat, MyType, Dir,
      Dist, Val, CSys, RelDist, Replace, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str   — Frame object name
  LoadPat : str   — Load pattern name
  MyType  : int   — 1=Force, 2=Moment
  Dir     : int   — 1-3=Local, 4-6=Global XYZ, 10=Gravity
  Dist    : float — Distance from I-End (relative 0-1 or absolute [L])
  Val     : float — Load value [F] or [FL]
  CSys    : str   — "Global" or "Local"
  RelDist : bool  — True=relative, False=absolute
  Replace : bool  — True=replace previous point loads in pattern
  ItemType: int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 6m
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

# --- Target function: point load at midspan ---
# 50 kN downward at midspan (relative distance 0.5)
ret = SapModel.FrameObj.SetLoadPoint(
    beam_name, "DEAD", 1, 10, 0.5, -50, "Global", True, True
)
assert ret == 0, f"SetLoadPoint(midspan) failed: {ret}"

# Add second point load at quarter span
ret = SapModel.FrameObj.SetLoadPoint(
    beam_name, "DEAD", 1, 10, 0.25, -25, "Global", True, False
)
assert ret == 0, f"SetLoadPoint(quarter) failed: {ret}"

# --- Verification via analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_frameobj_setloadpoint.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# Check reactions sum to total applied load (50 + 25 = 75 kN)
raw = SapModel.Results.JointReact(
    "1", 0, 0, [], [], [], [], [], [], [], [], [], [], []
)
assert raw[-1] == 0
F3_1 = raw[8][0]

raw = SapModel.Results.JointReact(
    "2", 0, 0, [], [], [], [], [], [], [], [], [], [], []
)
assert raw[-1] == 0
F3_2 = raw[8][0]

total_reaction = F3_1 + F3_2

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadPoint"
result["beam_name"] = beam_name
result["total_reaction"] = total_reaction
result["expected_total"] = 75.0
result["status"] = "verified"
```

- [x] Execute via `run_sap_script` and verify total reaction ≈ 75 kN.
- [x] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.SetLoadPoint`
  - `category`: `Object_Model`
  - `description`: `Assign point loads (force/moment) to frame objects at specified distance`
  - `signature`: `(Name, LoadPat, MyType, Dir, Dist, Val, CSys, RelDist, Replace, ItemType) -> ret_code`
  - `wrapper_script`: `func_FrameObj_SetLoadPoint`

---

##### 1.3 — `FrameObj.GetLoadDistributed`

- [x] Create file `scripts/wrappers/func_FrameObj_GetLoadDistributed.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.GetLoadDistributed
# Category: Object_Model
# Description: Retrieve distributed load assignments from frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame with distributed loads assigned
# ============================================================
"""
Usage: Retrieves all distributed load assignments for a frame object.

API Signature:
  SapModel.FrameObj.GetLoadDistributed(Name, NumberItems,
      FrameName, LoadPat, MyType, CSys, Dir,
      RD1, RD2, Dist1, Dist2, Val1, Val2, ItemType) -> ret_code

ByRef Output (12 values):
  NumberItems : int     — number of load assignments
  FrameName[] : str[]   — frame names
  LoadPat[]   : str[]   — load pattern names
  MyType[]    : int[]   — 1=Force, 2=Moment
  CSys[]      : str[]   — coordinate systems
  Dir[]       : int[]   — directions
  RD1[]       : float[] — relative start distances
  RD2[]       : float[] — relative end distances
  Dist1[]     : float[] — absolute start distances [L]
  Dist2[]     : float[] — absolute end distances [L]
  Val1[]      : float[] — start load values
  Val2[]      : float[] — end load values

Parameters:
  Name     : str — Frame name (or group/selection)
  ItemType : int — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# Assign known loads
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -12, -12, "Global", True, True
)
assert ret == 0

ret = SapModel.LoadPatterns.Add("LIVE", 3, 0, False)
assert ret == 0
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "LIVE", 1, 10, 0, 0.5, -5, -10, "Global", True, True
)
assert ret == 0

# --- Target function ---
raw = SapModel.FrameObj.GetLoadDistributed(
    beam_name, 0, [], [], [], [], [], [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadDistributed failed: {ret_code}"

num_loads = raw[0]
frame_names = list(raw[1])
load_pats = list(raw[2])
val1_arr = list(raw[10])
val2_arr = list(raw[11])

assert num_loads == 2, f"Expected 2 loads, got {num_loads}"

# --- Result ---
result["function"] = "SapModel.FrameObj.GetLoadDistributed"
result["num_loads"] = num_loads
result["load_patterns"] = load_pats
result["val1"] = val1_arr
result["val2"] = val2_arr
result["status"] = "verified"
```

- [x] Execute via `run_sap_script` and verify `num_loads == 2`.
- [x] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.GetLoadDistributed`
  - `category`: `Object_Model`
  - `description`: `Retrieve distributed load assignments from frame objects`
  - `signature`: `(Name, NumberItems, FrameName[], LoadPat[], MyType[], CSys[], Dir[], RD1[], RD2[], Dist1[], Dist2[], Val1[], Val2[], ItemType) -> [NumberItems, FrameName[], LoadPat[], MyType[], CSys[], Dir[], RD1[], RD2[], Dist1[], Dist2[], Val1[], Val2[], ret_code]`
  - `wrapper_script`: `func_FrameObj_GetLoadDistributed`

---

##### 1.4 — `PointObj.SetLoadForce`

- [x] Create file `scripts/wrappers/func_PointObj_SetLoadForce.py`:

```python
# ============================================================
# Wrapper: SapModel.PointObj.SetLoadForce
# Category: Object_Model
# Description: Assign point load forces/moments to point objects
# Verified: 2026-03-28
# Prerequisites: Model open, point object exists, load pattern defined
# ============================================================
"""
Usage: Assigns concentrated forces and moments to point (joint) objects.

API Signature:
  SapModel.PointObj.SetLoadForce(Name, LoadPat, Value,
      Replace, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str      — Point object name
  LoadPat : str      — Load pattern name
  Value   : float[6] — [F1, F2, F3, M1, M2, M3] in specified CSys
  Replace : bool     — True=replace previous force loads
  CSys    : str      — "Global" or "Local" or named system
  ItemType: int      — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_SEC", "STEEL_TEST", 0.4, 0.4)
assert ret == 0

# Cantilever column (vertical)
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 5, "", "COL_SEC", "")
col_name = raw[0]
assert raw[-1] == 0

# Fixed base
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0

# --- Target function: apply lateral force at top ---
# 100 kN in X direction, 50 kN downward (Z), 20 kN-m moment about Y
load_values = [100.0, 0.0, -50.0, 0.0, 20.0, 0.0]
ret = SapModel.PointObj.SetLoadForce("2", "DEAD", load_values, True, "Global")
assert ret == 0, f"SetLoadForce failed: {ret}"

# --- Verification via analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_pointobj_setloadforce.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# Check base reactions
raw = SapModel.Results.JointReact(
    "1", 0, 0, [], [], [], [], [], [], [], [], [], [], []
)
assert raw[-1] == 0
F1_base = raw[6][0]  # Should be ≈ -100 kN (reaction opposes applied)
F3_base = raw[8][0]  # Should be ≈ 50 kN (reaction opposes applied)

# --- Result ---
result["function"] = "SapModel.PointObj.SetLoadForce"
result["applied_forces"] = load_values
result["base_reaction_F1"] = F1_base
result["base_reaction_F3"] = F3_base
result["status"] = "verified"
```

- [x] Execute via `run_sap_script` and verify base reactions oppose applied loads.
- [x] Register via `register_verified_function` (update existing entry with `wrapper_script`):
  - `function_path`: `SapModel.PointObj.SetLoadForce`
  - `category`: `Object_Model`
  - `description`: `Assign point load forces and moments to point objects`
  - `signature`: `(Name, LoadPat, Value[6], Replace, CSys, ItemType) -> ret_code`
  - `wrapper_script`: `func_PointObj_SetLoadForce`

---

##### 1.5 — `AreaObj.SetLoadUniform`

- [x] Create file `scripts/wrappers/func_AreaObj_SetLoadUniform.py`:

```python
# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadUniform
# Category: Object_Model
# Description: Assign uniform distributed loads to area objects
# Verified: 2026-03-28
# Prerequisites: Model open, area object exists, load pattern defined
# ============================================================
"""
Usage: Assigns a uniform pressure load [F/L²] to area (shell/plate/membrane)
       objects over their entire surface.

API Signature:
  SapModel.AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir,
      Replace, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str   — Area object name (or group)
  LoadPat : str   — Load pattern name
  Value   : float — Uniform load value [F/L²]
  Dir     : int   — 1-3=Local, 4-6=Global XYZ, 10=Gravity, 11=Proj. Gravity
  Replace : bool  — True=replace previous uniform loads
  CSys    : str   — "Global" or "Local"
  ItemType: int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, False, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

# Create 5m x 4m slab
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 5, 5, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
area_name = raw[3]
assert raw[-1] == 0

# Pin all corners
for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret == 0

# --- Target function: uniform downward load ---
# -5 kN/m² gravity direction
ret = SapModel.AreaObj.SetLoadUniform(
    area_name, "DEAD", -5.0, 10, True, "Global"
)
assert ret == 0, f"SetLoadUniform failed: {ret}"

# --- Verification via analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_areaobj_setloaduniform.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# Total applied = 5 * 5 * 4 = 100 kN (but self-weight adds more)
# Check base reactions exist and are nonzero
raw = SapModel.Results.BaseReact(
    0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
)
assert raw[-1] == 0
Fz = list(raw[5])
total_Fz = sum(Fz)

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadUniform"
result["area_name"] = area_name
result["total_base_Fz"] = total_Fz
result["status"] = "verified"
```

- [x] Execute via `run_sap_script` and verify `ret_code == 0`, `total_base_Fz != 0`.
- [x] Register via `register_verified_function`:
  - `function_path`: `SapModel.AreaObj.SetLoadUniform`
  - `category`: `Object_Model`
  - `description`: `Assign uniform distributed loads [F/L²] to area objects`
  - `signature`: `(Name, LoadPat, Value, Dir, Replace, CSys, ItemType) -> ret_code`
  - `wrapper_script`: `func_AreaObj_SetLoadUniform`

---

##### 1.6 — `AreaObj.SetLoadGravity`

- [x] Create file `scripts/wrappers/func_AreaObj_SetLoadGravity.py`:

```python
# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadGravity
# Category: Object_Model
# Description: Assign gravity load multipliers to area objects
# Verified: 2026-03-28
# Prerequisites: Model open, area object exists, load pattern defined
# ============================================================
"""
Usage: Assigns gravity load multipliers (x, y, z) to area objects.
       Multiplier of -1 in Z means full self-weight downward.

API Signature:
  SapModel.AreaObj.SetLoadGravity(Name, LoadPat, x, y, z,
      Replace, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str   — Area object name (or group)
  LoadPat : str   — Load pattern name
  x, y, z : float — Gravity multipliers in specified CSys
  Replace : bool  — True=replace previous gravity loads
  CSys    : str   — Coordinate system (default "Global")
  ItemType: int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_TEST", 1, 24.0)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_15", 1, False, "CONC_TEST", 0, 0.15, 0.15)
assert ret == 0

# Create 3m x 3m slab
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 3, 3, 0], [0, 0, 3, 3], [0, 0, 0, 0], "", "SLAB_15"
)
area_name = raw[3]
assert raw[-1] == 0

for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret == 0

# --- Target function ---
# Full self-weight: z = -1
ret = SapModel.AreaObj.SetLoadGravity(area_name, "DEAD", 0, 0, -1)
assert ret == 0, f"SetLoadGravity failed: {ret}"

# --- Verification ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_areaobj_setloadgravity.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

raw = SapModel.Results.BaseReact(
    0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
)
assert raw[-1] == 0
total_Fz = sum(list(raw[5]))

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadGravity"
result["area_name"] = area_name
result["total_base_Fz"] = total_Fz
result["status"] = "verified"
```

- [x] Execute via `run_sap_script` and verify `ret_code == 0`, non-zero Fz.
- [x] Register via `register_verified_function`:
  - `function_path`: `SapModel.AreaObj.SetLoadGravity`
  - `category`: `Object_Model`
  - `description`: `Assign gravity load multipliers to area objects`
  - `signature`: `(Name, LoadPat, x, y, z, Replace, CSys, ItemType) -> ret_code`
  - `wrapper_script`: `func_AreaObj_SetLoadGravity`

##### Step 1 Verification Checklist
- [x] All 6 wrappers execute with `ret_code == 0`
- [x] `FrameObj.SetLoadDistributed` — `num_loads_assigned >= 2`
- [x] `FrameObj.SetLoadPoint` — total reaction ≈ 75 kN
- [x] `FrameObj.GetLoadDistributed` — `num_loads == 2` with correct values
- [x] `PointObj.SetLoadForce` — base reactions oppose applied forces
- [x] `AreaObj.SetLoadUniform` — non-zero base reactions
- [x] `AreaObj.SetLoadGravity` — non-zero base reactions from self-weight
- [x] All 6 functions registered in `scripts/registry.json`

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 2: Releases y Propiedades de Frame Avanzadas (4 wrappers)

##### 2.1 — `FrameObj.SetReleases`

- [ ] Create file `scripts/wrappers/func_FrameObj_SetReleases.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetReleases
# Category: Object_Model
# Description: Assign end release (hinge/partial fixity) to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Assigns moment releases (hinges) and partial fixity springs at the
       I-End and J-End of frame objects. Essential for modeling pinned
       connections, simply-supported beams, and semi-rigid joints.

API Signature:
  SapModel.FrameObj.SetReleases(Name, ii, jj, StartValue, EndValue,
      ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name       : str      — Frame object name
  ii         : bool[6]  — I-End releases [U1, U2, U3, R1, R2, R3]
  jj         : bool[6]  — J-End releases [U1, U2, U3, R1, R2, R3]
  StartValue : float[6] — I-End partial fixity springs [F/L or FL/rad]
  EndValue   : float[6] — J-End partial fixity springs [F/L or FL/rad]
  ItemType   : int      — 0=Object, 1=Group, 2=SelectedObjects

Note: Unstable combinations are rejected (e.g., U1 released at both ends).
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Create beam
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: release M3 (major bending) at J-End ---
# This creates a pin at the J-End (simple support for bending)
ii_releases = [False, False, False, False, False, False]
jj_releases = [False, False, False, False, False, True]  # Release R3 (M33)
start_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
end_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

ret = SapModel.FrameObj.SetReleases(
    beam_name, ii_releases, jj_releases, start_values, end_values
)
assert ret == 0, f"SetReleases failed: {ret}"

# --- Verification via GetReleases ---
raw = SapModel.FrameObj.GetReleases(beam_name, [], [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetReleases failed: {ret_code}"

read_ii = list(raw[0])
read_jj = list(raw[1])

assert read_jj[5] == True, f"Expected R3 released at J-End, got {read_jj[5]}"
assert read_ii[5] == False, f"I-End R3 should be fixed, got {read_ii[5]}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetReleases"
result["beam_name"] = beam_name
result["ii_releases"] = read_ii
result["jj_releases"] = read_jj
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify J-End R3 is released.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.SetReleases`
  - `category`: `Object_Model`
  - `description`: `Assign end releases (hinges/partial fixity) to frame objects`
  - `signature`: `(Name, ii[6], jj[6], StartValue[6], EndValue[6], ItemType) -> ret_code`
  - `wrapper_script`: `func_FrameObj_SetReleases`

---

##### 2.2 — `FrameObj.GetReleases`

- [ ] Create file `scripts/wrappers/func_FrameObj_GetReleases.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.GetReleases
# Category: Object_Model
# Description: Retrieve end release and partial fixity assignments from frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Retrieves the I-End and J-End release assignments and partial fixity
       spring values for a frame object.

API Signature:
  SapModel.FrameObj.GetReleases(Name, ii, jj,
      StartValue, EndValue) -> [ii[], jj[], StartValue[], EndValue[], ret_code]

ByRef Output (4 arrays):
  ii[]         : bool[6]  — I-End releases
  jj[]         : bool[6]  — J-End releases
  StartValue[] : float[6] — I-End partial fixity springs
  EndValue[]   : float[6] — J-End partial fixity springs

Parameters:
  Name : str — Frame object name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# Assign known releases: both-end moment releases (R2 and R3)
ii_set = [False, False, False, False, True, False]   # R2 at I-End
jj_set = [False, False, False, False, False, True]   # R3 at J-End
start_v = [0, 0, 0, 0, 0, 0]
end_v = [0, 0, 0, 0, 0, 0]
ret = SapModel.FrameObj.SetReleases(beam_name, ii_set, jj_set, start_v, end_v)
assert ret == 0

# --- Target function ---
raw = SapModel.FrameObj.GetReleases(beam_name, [], [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetReleases failed: {ret_code}"

read_ii = list(raw[0])
read_jj = list(raw[1])
read_sv = list(raw[2])
read_ev = list(raw[3])

assert read_ii[4] == True, f"Expected R2 released at I-End"
assert read_jj[5] == True, f"Expected R3 released at J-End"

# --- Result ---
result["function"] = "SapModel.FrameObj.GetReleases"
result["ii_releases"] = read_ii
result["jj_releases"] = read_jj
result["start_values"] = read_sv
result["end_values"] = read_ev
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify releases match what was set.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.GetReleases`
  - `category`: `Object_Model`
  - `description`: `Retrieve end release and partial fixity assignments from frame objects`
  - `signature`: `(Name, ii[], jj[], StartValue[], EndValue[]) -> [ii[], jj[], StartValue[], EndValue[], ret_code]`
  - `wrapper_script`: `func_FrameObj_GetReleases`

---

##### 2.3 — `FrameObj.SetInsertionPoint`

- [ ] Create file `scripts/wrappers/func_FrameObj_SetInsertionPoint.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetInsertionPoint_1
# Category: Object_Model
# Description: Assign cardinal point and joint offsets to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Assigns the frame section insertion point (cardinal point) and
       end joint offsets. Controls the relative position of the section
       with respect to the frame element line.

API Signature:
  SapModel.FrameObj.SetInsertionPoint_1(Name, CardinalPoint, Mirror2, Mirror3,
      StiffTransform, Offset1, Offset2, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name           : str      — Frame object name
  CardinalPoint  : int      — 1=BotLeft..9=TopRight, 10=Centroid, 11=ShearCenter
  Mirror2        : bool     — Mirror about local 2 axis
  Mirror3        : bool     — Mirror about local 3 axis
  StiffTransform : bool     — Transform stiffness for offsets
  Offset1        : float[3] — I-End offsets [L] in CSys directions
  Offset2        : float[3] — J-End offsets [L] in CSys directions
  CSys           : str      — "Local" or named coordinate system
  ItemType       : int      — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: Top-Center cardinal point (8) with offsets ---
offset1 = [0.0, 0.0, 0.0]
offset2 = [0.0, 0.0, 0.0]

ret = SapModel.FrameObj.SetInsertionPoint_1(
    beam_name, 8, False, False, True, offset1, offset2
)
assert ret == 0, f"SetInsertionPoint_1 failed: {ret}"

# --- Verification via GetInsertionPoint_1 ---
raw = SapModel.FrameObj.GetInsertionPoint_1(
    beam_name, 0, False, False, False, [], [], ""
)
ret_code = raw[-1]
assert ret_code == 0, f"GetInsertionPoint_1 failed: {ret_code}"
cardinal = raw[0]
assert cardinal == 8, f"Expected cardinal=8 (TopCenter), got {cardinal}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetInsertionPoint_1"
result["beam_name"] = beam_name
result["cardinal_point"] = cardinal
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `cardinal_point == 8`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.SetInsertionPoint_1`
  - `category`: `Object_Model`
  - `description`: `Assign cardinal point and joint offsets to frame objects`
  - `signature`: `(Name, CardinalPoint, Mirror2, Mirror3, StiffTransform, Offset1[3], Offset2[3], CSys, ItemType) -> ret_code`
  - `wrapper_script`: `func_FrameObj_SetInsertionPoint`

---

##### 2.4 — `FrameObj.SetLocalAxes`

- [ ] Create file `scripts/wrappers/func_FrameObj_SetLocalAxes.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetLocalAxes
# Category: Object_Model
# Description: Assign local axis rotation angle to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Rotates the local 2 and 3 axes of a frame object about its local 1 axis.
       Used for orienting non-symmetric sections (I-beams, channels, angles).

API Signature:
  SapModel.FrameObj.SetLocalAxes(Name, Ang, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str   — Frame object name
  Ang      : float — Rotation angle [deg], positive = CCW about local 1
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: rotate 45 degrees ---
ret = SapModel.FrameObj.SetLocalAxes(beam_name, 45.0)
assert ret == 0, f"SetLocalAxes failed: {ret}"

# --- Verification via GetLocalAxes ---
raw = SapModel.FrameObj.GetLocalAxes(beam_name, 0.0)
ret_code = raw[-1]
assert ret_code == 0, f"GetLocalAxes failed: {ret_code}"
angle = raw[0]
assert abs(angle - 45.0) < 0.01, f"Expected 45°, got {angle}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLocalAxes"
result["beam_name"] = beam_name
result["angle_set"] = 45.0
result["angle_read"] = angle
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `angle_read ≈ 45°`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.SetLocalAxes`
  - `category`: `Object_Model`
  - `description`: `Assign local axis rotation angle to frame objects`
  - `signature`: `(Name, Ang, ItemType) -> ret_code`
  - `wrapper_script`: `func_FrameObj_SetLocalAxes`

##### Step 2 Verification Checklist
- [ ] All 4 wrappers execute with `ret_code == 0`
- [ ] `SetReleases` — J-End R3 confirmed released via `GetReleases`
- [ ] `GetReleases` — I-End R2 and J-End R3 match assigned values
- [ ] `SetInsertionPoint_1` — cardinal point reads back as 8
- [ ] `SetLocalAxes` — angle reads back as 45°
- [ ] All 4 functions registered in `scripts/registry.json`

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 3: Grupos y Asignaciones Masivas (4 wrappers)

##### 3.1 — `GroupDef.SetGroup`

- [ ] Create file `scripts/wrappers/func_GroupDef_SetGroup.py`:

```python
# ============================================================
# Wrapper: SapModel.GroupDef.SetGroup
# Category: Groups
# Description: Create or modify a group definition with properties
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a new group or modifies an existing group. Groups are used for
       selection, design, output reporting, and batch operations.

API Signature:
  SapModel.GroupDef.SetGroup(Name, Color, SpecifiedForSelection,
      SpecifiedForSectionCutDefinition, SpecifiedForSteelDesign,
      SpecifiedForConcreteDesign, SpecifiedForAluminumDesign,
      SpecifiedForColdFormedDesign, SpecifiedForStaticNLActiveStage,
      SpecifiedForBridgeResponseOutput, SpecifiedForAutoSeismicOutput,
      SpecifiedForAutoWindOutput, SpecifiedForMassAndWeight) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Group name. New group created if doesn't exist; modified if exists.
  Color: int — Display color (-1=auto)
  SpecifiedFor* : bool — 12 optional booleans controlling group usage
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: create groups ---
# Basic group with defaults
ret = SapModel.GroupDef.SetGroup("COLUMNS")
assert ret == 0, f"SetGroup(COLUMNS) failed: {ret}"

# Group with specific properties: for selection and concrete design only
ret = SapModel.GroupDef.SetGroup(
    "BEAMS_LEVEL1", -1, True, False, False, True, False, False, False, False, False, False, True
)
assert ret == 0, f"SetGroup(BEAMS_LEVEL1) failed: {ret}"

# --- Verification via GetNameList ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

num_groups = raw[0]
group_names = list(raw[1])
assert "COLUMNS" in group_names, f"COLUMNS not in groups: {group_names}"
assert "BEAMS_LEVEL1" in group_names, f"BEAMS_LEVEL1 not in groups: {group_names}"

# --- Result ---
result["function"] = "SapModel.GroupDef.SetGroup"
result["groups_created"] = ["COLUMNS", "BEAMS_LEVEL1"]
result["total_groups"] = num_groups
result["all_group_names"] = group_names
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify both groups appear in name list.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.GroupDef.SetGroup`
  - `category`: `Groups`
  - `description`: `Create or modify a group definition with properties`
  - `signature`: `(Name, Color, SpecifiedForSelection, ..., SpecifiedForMassAndWeight) -> ret_code`
  - `wrapper_script`: `func_GroupDef_SetGroup`

---

##### 3.2 — `GroupDef.GetNameList`

- [ ] Create file `scripts/wrappers/func_GroupDef_GetNameList.py`:

```python
# ============================================================
# Wrapper: SapModel.GroupDef.GetNameList
# Category: Groups
# Description: Retrieve names of all defined groups
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns a list of all group names defined in the model.
       Every model has at minimum the "ALL" group.

API Signature:
  SapModel.GroupDef.GetNameList(NumberNames, MyName) ->
      [NumberNames, MyName[], ret_code]

ByRef Output:
  NumberNames : int   — number of groups
  MyName[]    : str[] — group names

Parameters: None (all are ByRef outputs)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Create some groups
ret = SapModel.GroupDef.SetGroup("GROUP_A")
assert ret == 0
ret = SapModel.GroupDef.SetGroup("GROUP_B")
assert ret == 0

# --- Target function ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

num_groups = raw[0]
group_names = list(raw[1])

assert num_groups >= 3, f"Expected >=3 groups (ALL + 2), got {num_groups}"
assert "ALL" in group_names, "ALL group missing"
assert "GROUP_A" in group_names, "GROUP_A missing"
assert "GROUP_B" in group_names, "GROUP_B missing"

# --- Result ---
result["function"] = "SapModel.GroupDef.GetNameList"
result["num_groups"] = num_groups
result["group_names"] = group_names
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `num_groups >= 3`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.GroupDef.GetNameList`
  - `category`: `Groups`
  - `description`: `Retrieve names of all defined groups`
  - `signature`: `(NumberNames, MyName[]) -> [NumberNames, MyName[], ret_code]`
  - `wrapper_script`: `func_GroupDef_GetNameList`

---

##### 3.3 — `FrameObj.SetGroupAssign`

- [ ] Create file `scripts/wrappers/func_FrameObj_SetGroupAssign.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetGroupAssign
# Category: Object_Model
# Description: Add or remove frame objects from a group
# Verified: 2026-03-28
# Prerequisites: Model open, frame and group exist
# ============================================================
"""
Usage: Adds frame objects to (or removes from) a specified group.
       Groups must exist before objects can be assigned to them.

API Signature:
  SapModel.FrameObj.SetGroupAssign(Name, GroupName, Remove,
      ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str  — Frame object name
  GroupName : str  — Target group name (must exist)
  Remove    : bool — False=add, True=remove from group
  ItemType  : int  — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_SEC", "STEEL_TEST", 0.4, 0.4)
assert ret == 0

# Create some frames
raw1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "COL_SEC", "")
f1 = raw1[0]
assert raw1[-1] == 0
raw2 = SapModel.FrameObj.AddByCoord(5, 0, 0, 5, 0, 3, "", "COL_SEC", "")
f2 = raw2[0]
assert raw2[-1] == 0
raw3 = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "COL_SEC", "")
f3 = raw3[0]
assert raw3[-1] == 0

# Create group
ret = SapModel.GroupDef.SetGroup("COLUMNS")
assert ret == 0

# --- Target function ---
ret = SapModel.FrameObj.SetGroupAssign(f1, "COLUMNS")
assert ret == 0, f"SetGroupAssign(f1) failed: {ret}"

ret = SapModel.FrameObj.SetGroupAssign(f2, "COLUMNS")
assert ret == 0, f"SetGroupAssign(f2) failed: {ret}"

# --- Verification via GetAssignments ---
raw = SapModel.GroupDef.GetAssignments("COLUMNS", 0, [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetAssignments failed: {ret_code}"

num_items = raw[0]
obj_types = list(raw[1])
obj_names = list(raw[2])
assert num_items == 2, f"Expected 2 items in group, got {num_items}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetGroupAssign"
result["group_name"] = "COLUMNS"
result["items_in_group"] = num_items
result["object_names"] = obj_names
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `items_in_group == 2`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.FrameObj.SetGroupAssign`
  - `category`: `Object_Model`
  - `description`: `Add or remove frame objects from a group`
  - `signature`: `(Name, GroupName, Remove, ItemType) -> ret_code`
  - `wrapper_script`: `func_FrameObj_SetGroupAssign`

---

##### 3.4 — `AreaObj.SetGroupAssign`

- [ ] Create file `scripts/wrappers/func_AreaObj_SetGroupAssign.py`:

```python
# ============================================================
# Wrapper: SapModel.AreaObj.SetGroupAssign
# Category: Object_Model
# Description: Add or remove area objects from a group
# Verified: 2026-03-28
# Prerequisites: Model open, area and group exist
# ============================================================
"""
Usage: Adds area objects to (or removes from) a specified group.

API Signature:
  SapModel.AreaObj.SetGroupAssign(Name, GroupName, Remove,
      ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str  — Area object name
  GroupName : str  — Target group name (must exist)
  Remove    : bool — False=add, True=remove
  ItemType  : int  — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, False, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

# Create two areas
raw1 = SapModel.AreaObj.AddByCoord(
    4, [0, 4, 4, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
a1 = raw1[3]
assert raw1[-1] == 0

raw2 = SapModel.AreaObj.AddByCoord(
    4, [4, 8, 8, 4], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
a2 = raw2[3]
assert raw2[-1] == 0

# Create group
ret = SapModel.GroupDef.SetGroup("SLABS_FLOOR1")
assert ret == 0

# --- Target function ---
ret = SapModel.AreaObj.SetGroupAssign(a1, "SLABS_FLOOR1")
assert ret == 0, f"SetGroupAssign(a1) failed: {ret}"

ret = SapModel.AreaObj.SetGroupAssign(a2, "SLABS_FLOOR1")
assert ret == 0, f"SetGroupAssign(a2) failed: {ret}"

# --- Verification ---
raw = SapModel.GroupDef.GetAssignments("SLABS_FLOOR1", 0, [], [])
ret_code = raw[-1]
assert ret_code == 0
num_items = raw[0]
obj_types = list(raw[1])
assert num_items == 2, f"Expected 2, got {num_items}"
# ObjectType 5 = Area object
assert all(t == 5 for t in obj_types), f"Expected all type=5(Area), got {obj_types}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetGroupAssign"
result["group_name"] = "SLABS_FLOOR1"
result["items_in_group"] = num_items
result["object_types"] = obj_types
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `items_in_group == 2`, all type=5.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.AreaObj.SetGroupAssign`
  - `category`: `Object_Model`
  - `description`: `Add or remove area objects from a group`
  - `signature`: `(Name, GroupName, Remove, ItemType) -> ret_code`
  - `wrapper_script`: `func_AreaObj_SetGroupAssign`

##### Step 3 Verification Checklist
- [ ] All 4 wrappers execute with `ret_code == 0`
- [ ] `SetGroup` — both groups appear in `GetNameList`
- [ ] `GetNameList` — returns ALL + custom groups
- [ ] `FrameObj.SetGroupAssign` — 2 frames confirmed in group via `GetAssignments`
- [ ] `AreaObj.SetGroupAssign` — 2 areas confirmed in group, type=5
- [ ] All 4 functions registered in `scripts/registry.json`

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 4: Constraints Avanzados — Diafragma (2 wrappers)

##### 4.1 — `ConstraintDef.SetDiaphragm`

- [ ] Create file `scripts/wrappers/func_ConstraintDef_SetDiaphragm.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.SetDiaphragm
# Category: Constraints
# Description: Define a diaphragm constraint (rigid floor)
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates or modifies a diaphragm constraint. Diaphragms model rigid
       floor slabs where in-plane translations and rotation are coupled.
       Most common constraint for multi-story buildings.

API Signature:
  SapModel.ConstraintDef.SetDiaphragm(Name, Axis, CSys) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Constraint name (creates new if not exists)
  Axis : int — Perpendicular axis: 1=X, 2=Y, 3=Z, 4=AutoAxis (default)
  CSys : str — Coordinate system (default "Global")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: create diaphragm constraints ---
# Z-axis perpendicular = horizontal floor diaphragm (most common)
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_FLOOR1", 3, "Global")
assert ret == 0, f"SetDiaphragm(FLOOR1) failed: {ret}"

# Auto-axis (let SAP2000 determine from joint positions)
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_FLOOR2", 4, "Global")
assert ret == 0, f"SetDiaphragm(FLOOR2) failed: {ret}"

# --- Create points and assign diaphragm ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0

raw = SapModel.PointObj.AddCartesian(0, 0, 3, "", "PT1")
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(5, 0, 3, "", "PT2")
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(5, 5, 3, "", "PT3")
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(0, 5, 3, "", "PT4")
assert raw[-1] == 0

for pt in ["PT1", "PT2", "PT3", "PT4"]:
    ret = SapModel.PointObj.SetConstraint(pt, "DIAPH_FLOOR1")
    assert ret[-1] == 0, f"SetConstraint({pt}) failed: {ret[-1]}"

# --- Verification via GetDiaphragm ---
raw = SapModel.ConstraintDef.GetDiaphragm("DIAPH_FLOOR1", 0, "")
ret_code = raw[-1]
assert ret_code == 0, f"GetDiaphragm failed: {ret_code}"
axis = raw[0]
csys = raw[1]

# --- Result ---
result["function"] = "SapModel.ConstraintDef.SetDiaphragm"
result["constraints"] = ["DIAPH_FLOOR1", "DIAPH_FLOOR2"]
result["axis_read"] = axis
result["csys_read"] = csys
result["points_assigned"] = ["PT1", "PT2", "PT3", "PT4"]
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `axis_read == 3` (Z-axis).
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.ConstraintDef.SetDiaphragm`
  - `category`: `Constraints`
  - `description`: `Define a diaphragm constraint (rigid floor)`
  - `signature`: `(Name, Axis, CSys) -> ret_code`
  - `wrapper_script`: `func_ConstraintDef_SetDiaphragm`

---

##### 4.2 — `ConstraintDef.GetDiaphragm`

- [ ] Create file `scripts/wrappers/func_ConstraintDef_GetDiaphragm.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.GetDiaphragm
# Category: Constraints
# Description: Retrieve diaphragm constraint definition
# Verified: 2026-03-28
# Prerequisites: Model open, diaphragm constraint defined
# ============================================================
"""
Usage: Retrieves the axis and coordinate system for a diaphragm constraint.

API Signature:
  SapModel.ConstraintDef.GetDiaphragm(Name, Axis, CSys) ->
      [Axis, CSys, ret_code]

ByRef Output:
  Axis : int — 1=X, 2=Y, 3=Z, 4=AutoAxis
  CSys : str — Coordinate system name

Parameters:
  Name : str — Name of existing diaphragm constraint
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Create diaphragms with known axes
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_Z", 3, "Global")
assert ret == 0
ret = SapModel.ConstraintDef.SetDiaphragm("DIAPH_AUTO", 4, "Global")
assert ret == 0

# --- Target function ---
raw = SapModel.ConstraintDef.GetDiaphragm("DIAPH_Z", 0, "")
ret_code = raw[-1]
assert ret_code == 0, f"GetDiaphragm(Z) failed: {ret_code}"
axis_z = raw[0]
csys_z = raw[1]
assert axis_z == 3, f"Expected axis=3(Z), got {axis_z}"

raw = SapModel.ConstraintDef.GetDiaphragm("DIAPH_AUTO", 0, "")
ret_code = raw[-1]
assert ret_code == 0, f"GetDiaphragm(AUTO) failed: {ret_code}"
axis_auto = raw[0]
assert axis_auto == 4, f"Expected axis=4(Auto), got {axis_auto}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.GetDiaphragm"
result["diaph_z_axis"] = axis_z
result["diaph_z_csys"] = csys_z
result["diaph_auto_axis"] = axis_auto
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `axis == 3` and `axis == 4`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.ConstraintDef.GetDiaphragm`
  - `category`: `Constraints`
  - `description`: `Retrieve diaphragm constraint definition (axis and coordinate system)`
  - `signature`: `(Name, Axis, CSys) -> [Axis, CSys, ret_code]`
  - `wrapper_script`: `func_ConstraintDef_GetDiaphragm`

##### Step 4 Verification Checklist
- [ ] Both wrappers execute with `ret_code == 0`
- [ ] `SetDiaphragm` — Z-axis constraint reads back axis=3
- [ ] `GetDiaphragm` — both Z and Auto axes verified
- [ ] Both functions registered in `scripts/registry.json`

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 5a: Resultados Generales (2 wrappers)

##### 5a.1 — `Results.BaseReact`

- [ ] Create file `scripts/wrappers/func_Results_BaseReact.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.BaseReact
# Category: Analysis_Results
# Description: Extract total base reactions (forces and moments)
# Verified: 2026-03-28
# Prerequisites: Model analyzed
# ============================================================
"""
Usage: Reports the total base reactions (summed at a specified point)
       for selected load cases/combos. Essential for equilibrium checks.

API Signature:
  SapModel.Results.BaseReact(NumberResults, LoadCase, StepType,
      StepNum, Fx, Fy, Fz, Mx, My, Mz, gx, gy, gz) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  Fx[]          : float[] — base reaction force global-X [F]
  Fy[]          : float[] — base reaction force global-Y [F]
  Fz[]          : float[] — base reaction force global-Z [F]
  Mx[]          : float[] — base reaction moment about X [FL]
  My[]          : float[] — base reaction moment about Y [FL]
  Mz[]          : float[] — base reaction moment about Z [FL]
  gx, gy, gz    : float   — reporting point coordinates [L]

Parameters: None (all are ByRef outputs)
"""

# --- Minimal setup: beam with known load ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 10m, with -20 kN/m uniform load
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -20, -20, "Global", True, True
)
assert ret == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_basereact.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.BaseReact(
    0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
)
ret_code = raw[-1]
assert ret_code == 0, f"BaseReact failed: {ret_code}"

num_results = raw[0]
load_cases = list(raw[1])
Fx = list(raw[3])
Fy = list(raw[4])
Fz = list(raw[5])
Mx = list(raw[6])
My = list(raw[7])
Mz = list(raw[8])

total_Fz = sum(Fz)
# Expected: 20 kN/m * 10m = 200 kN total vertical reaction (positive upward)

# --- Result ---
result["function"] = "SapModel.Results.BaseReact"
result["num_results"] = num_results
result["load_cases"] = load_cases
result["total_Fz"] = total_Fz
result["expected_Fz"] = 200.0
result["Mx"] = Mx
result["My"] = My
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `total_Fz ≈ 200 kN`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Results.BaseReact`
  - `category`: `Analysis_Results`
  - `description`: `Extract total base reactions (forces and moments at reporting point)`
  - `signature`: `(NumberResults, LoadCase[], StepType[], StepNum[], Fx[], Fy[], Fz[], Mx[], My[], Mz[], gx, gy, gz) -> [NumberResults, LoadCase[], StepType[], StepNum[], Fx[], Fy[], Fz[], Mx[], My[], Mz[], gx, gy, gz, ret_code]`
  - `wrapper_script`: `func_Results_BaseReact`

---

##### 5a.2 — `Results.AreaStressShell`

- [ ] Create file `scripts/wrappers/func_Results_AreaStressShell.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.AreaStressShell
# Category: Analysis_Results
# Description: Extract shell element stresses (S11, S22, S12, etc.)
# Verified: 2026-03-28
# Prerequisites: Model analyzed, shell area elements exist
# ============================================================
"""
Usage: Reports area element stresses at top/bottom faces and average
       out-of-plane shear. Only applies to shell-type properties.

API Signature:
  SapModel.Results.AreaStressShell(Name, ItemTypeElm,
      NumberResults, Obj, Elm, PointElm,
      LoadCase, StepType, StepNum,
      S11Top, S22Top, S12Top, SMaxTop, SMinTop, SAngleTop, SVMTop,
      S11Bot, S22Bot, S12Bot, SMaxBot, SMinBot, SAngleBot, SVMBot,
      S13Avg, S23Avg, SMaxAvg, SAngleAvg) -> ret_code

ByRef Output (26 values):
  NumberResults : int   — number of result rows
  Obj..StepNum  : arrays — identification arrays
  S11Top..SVMTop: float[] — top fiber stresses [F/L²]
  S11Bot..SVMBot: float[] — bottom fiber stresses [F/L²]
  S13Avg..SAngleAvg: float[] — average out-of-plane shear [F/L²]

Parameters:
  Name        : str — Area name
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: loaded slab ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, False, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

# 4x4m supported slab
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 4, 4, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
area_name = raw[3]
assert raw[-1] == 0

for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret == 0

ret = SapModel.AreaObj.SetLoadUniform(area_name, "DEAD", -10, 10, True, "Global")
assert ret == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_areastressshell.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.AreaStressShell(
    area_name, 0,
    0, [], [], [],
    [], [], [],
    [], [], [], [], [], [], [],
    [], [], [], [], [], [], [],
    [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"AreaStressShell failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No stress results returned"

S11Top = list(raw[6])
S22Top = list(raw[7])

# --- Result ---
result["function"] = "SapModel.Results.AreaStressShell"
result["area_name"] = area_name
result["num_results"] = num_results
result["S11Top_sample"] = S11Top[:4] if len(S11Top) >= 4 else S11Top
result["S22Top_sample"] = S22Top[:4] if len(S22Top) >= 4 else S22Top
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `num_results > 0`, stress arrays non-empty.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Results.AreaStressShell`
  - `category`: `Analysis_Results`
  - `description`: `Extract shell element stresses (S11, S22, S12 at top/bottom, principal, Von Mises)`
  - `signature`: `(Name, ItemTypeElm, ..., SAngleAvg[]) -> [..., ret_code]`
  - `wrapper_script`: `func_Results_AreaStressShell`

##### Step 5a Verification Checklist
- [ ] Both wrappers execute with `ret_code == 0`
- [ ] `BaseReact` — `total_Fz ≈ 200 kN`
- [ ] `AreaStressShell` — non-empty stress arrays
- [ ] Both functions registered in `scripts/registry.json`

#### Step 5a STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 5b: Suite de Resultados Modales (3 wrappers)

##### 5b.1 — `Results.ModalPeriod`

- [ ] Create file `scripts/wrappers/func_Results_ModalPeriod.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.ModalPeriod
# Category: Analysis_Results
# Description: Extract modal periods, frequencies, and eigenvalues
# Verified: 2026-03-28
# Prerequisites: Model analyzed with modal case
# ============================================================
"""
Usage: Reports the modal period, cyclic frequency, circular frequency, and
       eigenvalue for each mode in selected modal load cases.

API Signature:
  SapModel.Results.ModalPeriod(NumberResults, LoadCase, StepType,
      StepNum, Period, Frequency, CircFreq, EigenValue) -> ret_code

ByRef Output (7 values):
  NumberResults : int     — number of modes
  LoadCase[]    : str[]   — modal case names
  StepType[]    : str[]   — always "Mode"
  StepNum[]     : float[] — mode numbers (1, 2, 3, ...)
  Period[]      : float[] — period per mode [s]
  Frequency[]   : float[] — cyclic frequency [1/s]
  CircFreq[]    : float[] — circular frequency [rad/s]
  EigenValue[]  : float[] — eigenvalue [rad²/s²]

Parameters: None (all are ByRef outputs)
"""

# --- Build a simple 3D frame for modal analysis ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material with weight/mass for modal analysis
ret = SapModel.PropMaterial.SetMaterial("CONC_M", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_M", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 1, 24.0)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 2, 2.4)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("COL_40", "CONC_M", 0.4, 0.4)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30", "CONC_M", 0.3, 0.2)
assert ret == 0

# 2-story portal frame
# Columns
for x in [0, 5]:
    raw = SapModel.FrameObj.AddByCoord(x, 0, 0, x, 0, 3, "", "COL_40", "")
    assert raw[-1] == 0
    raw = SapModel.FrameObj.AddByCoord(x, 0, 3, x, 0, 6, "", "COL_40", "")
    assert raw[-1] == 0

# Beams
raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30", "")
assert raw[-1] == 0
raw = SapModel.FrameObj.AddByCoord(0, 0, 6, 5, 0, 6, "", "BEAM_30", "")
assert raw[-1] == 0

# Fixed bases
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("3", [True, True, True, True, True, True])
assert ret[-1] == 0

# MODAL case exists by default in SAP2000 — just run analysis
ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_modalperiod.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

# Select MODAL case for output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.ModalPeriod(
    0, [], [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"ModalPeriod failed: {ret_code}"

num_modes = raw[0]
load_cases = list(raw[1])
step_nums = list(raw[2])
periods = list(raw[3])
frequencies = list(raw[4])
circ_freqs = list(raw[5])
eigenvalues = list(raw[6])

assert num_modes > 0, f"No modal results"
assert periods[0] > 0, f"First period should be positive, got {periods[0]}"

# --- Result ---
result["function"] = "SapModel.Results.ModalPeriod"
result["num_modes"] = num_modes
result["periods"] = periods
result["frequencies"] = frequencies
result["T1"] = periods[0]
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `num_modes > 0`, `T1 > 0`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Results.ModalPeriod`
  - `category`: `Analysis_Results`
  - `description`: `Extract modal periods, frequencies, circular frequencies, and eigenvalues`
  - `signature`: `(NumberResults, LoadCase[], StepType[], StepNum[], Period[], Frequency[], CircFreq[], EigenValue[]) -> [..., ret_code]`
  - `wrapper_script`: `func_Results_ModalPeriod`

---

##### 5b.2 — `Results.ModalParticipatingMassRatios`

- [ ] Create file `scripts/wrappers/func_Results_ModalParticipatingMassRatios.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.ModalParticipatingMassRatios
# Category: Analysis_Results
# Description: Extract modal participating mass ratios per mode
# Verified: 2026-03-28
# Prerequisites: Model analyzed with modal case
# ============================================================
"""
Usage: Reports the modal participating mass ratios for each mode.
       Critical for seismic design (ASCE 7, NSR-10 require ≥90% mass).

API Signature:
  SapModel.Results.ModalParticipatingMassRatios(NumberResults,
      LoadCase, StepType, StepNum, Period,
      Ux, Uy, Uz, SumUx, SumUy, SumUz,
      Rx, Ry, Rz, SumRx, SumRy, SumRz) -> ret_code

ByRef Output (16 values):
  NumberResults : int     — number of modes
  LoadCase[]    : str[]   — modal case names
  StepType[]    : str[]   — always "Mode"
  StepNum[]     : float[] — mode numbers
  Period[]      : float[] — period per mode [s]
  Ux..Uz[]      : float[] — mass ratio per mode per DOF
  SumUx..SumUz[]: float[] — cumulative mass ratios
  Rx..Rz[]      : float[] — rotational mass ratios
  SumRx..SumRz[]: float[] — cumulative rotational ratios

Parameters: None (all are ByRef outputs)
"""

# --- Use same 2-story frame as ModalPeriod ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_M", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_M", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 1, 24.0)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 2, 2.4)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("COL_40", "CONC_M", 0.4, 0.4)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30", "CONC_M", 0.3, 0.2)
assert ret == 0

for x in [0, 5]:
    raw = SapModel.FrameObj.AddByCoord(x, 0, 0, x, 0, 3, "", "COL_40", "")
    assert raw[-1] == 0
    raw = SapModel.FrameObj.AddByCoord(x, 0, 3, x, 0, 6, "", "COL_40", "")
    assert raw[-1] == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30", "")
assert raw[-1] == 0
raw = SapModel.FrameObj.AddByCoord(0, 0, 6, 5, 0, 6, "", "BEAM_30", "")
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("3", [True, True, True, True, True, True])
assert ret[-1] == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_modalmass.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.ModalParticipatingMassRatios(
    0, [], [], [], [],
    [], [], [], [], [], [],
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"ModalParticipatingMassRatios failed: {ret_code}"

num_modes = raw[0]
periods = list(raw[3])
Ux = list(raw[4])
Uy = list(raw[5])
Uz = list(raw[6])
SumUx = list(raw[7])
SumUy = list(raw[8])
SumUz = list(raw[9])

assert num_modes > 0, f"No modal results"
# Last SumUx should be close to 1.0 if enough modes captured
last_SumUx = SumUx[-1] if SumUx else 0

# --- Result ---
result["function"] = "SapModel.Results.ModalParticipatingMassRatios"
result["num_modes"] = num_modes
result["Ux_per_mode"] = Ux
result["SumUx"] = SumUx
result["SumUy"] = SumUy
result["final_SumUx"] = last_SumUx
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `num_modes > 0`, `SumUx` array populated.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Results.ModalParticipatingMassRatios`
  - `category`: `Analysis_Results`
  - `description`: `Extract modal participating mass ratios (individual and cumulative per DOF)`
  - `signature`: `(...) -> [..., ret_code]`
  - `wrapper_script`: `func_Results_ModalParticipatingMassRatios`

---

##### 5b.3 — `Results.ModeShape`

- [ ] Create file `scripts/wrappers/func_Results_ModeShape.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.ModeShape
# Category: Analysis_Results
# Description: Extract modal displacements (mode shapes) per joint
# Verified: 2026-03-28
# Prerequisites: Model analyzed with modal case
# ============================================================
"""
Usage: Reports the modal displacements (eigenvectors) at point elements
       for selected modal analysis cases.

API Signature:
  SapModel.Results.ModeShape(Name, ItemTypeElm,
      NumberResults, Obj, Elm, LoadCase, StepType, StepNum,
      U1, U2, U3, R1, R2, R3) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — point object names
  Elm[]         : str[]   — point element names
  LoadCase[]    : str[]   — modal case names
  StepType[]    : str[]   — always "Mode"
  StepNum[]     : float[] — mode numbers
  U1..U3[]      : float[] — translational displacements [L]
  R1..R3[]      : float[] — rotational displacements [rad]

Parameters:
  Name        : str — Point name, or group name for all points
  ItemTypeElm : int — 0=ObjectElm, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Setup: same 2-story portal ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_M", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_M", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 1, 24.0)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 2, 2.4)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("COL_40", "CONC_M", 0.4, 0.4)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30", "CONC_M", 0.3, 0.2)
assert ret == 0

for x in [0, 5]:
    raw = SapModel.FrameObj.AddByCoord(x, 0, 0, x, 0, 3, "", "COL_40", "")
    assert raw[-1] == 0
    raw = SapModel.FrameObj.AddByCoord(x, 0, 3, x, 0, 6, "", "COL_40", "")
    assert raw[-1] == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30", "")
assert raw[-1] == 0
raw = SapModel.FrameObj.AddByCoord(0, 0, 6, 5, 0, 6, "", "BEAM_30", "")
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("3", [True, True, True, True, True, True])
assert ret[-1] == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_modeshape.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")
assert ret == 0

# --- Target function: get mode shapes for ALL points ---
raw = SapModel.Results.ModeShape(
    "ALL", 2,  # GroupElm — "ALL" is a built-in group
    0, [], [], [], [], [],
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"ModeShape failed: {ret_code}"

num_results = raw[0]
obj_names = list(raw[1])
step_nums = list(raw[3])
U1 = list(raw[5])
U2 = list(raw[6])
U3 = list(raw[7])

assert num_results > 0, f"No mode shape results"

# --- Result ---
result["function"] = "SapModel.Results.ModeShape"
result["num_results"] = num_results
result["unique_points"] = list(set(obj_names))
result["unique_modes"] = list(set(step_nums))
result["U1_sample"] = U1[:6]
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `num_results > 0`, arrays populated.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Results.ModeShape`
  - `category`: `Analysis_Results`
  - `description`: `Extract modal displacements (mode shapes) at point elements`
  - `signature`: `(Name, ItemTypeElm, NumberResults, Obj[], Elm[], LoadCase[], StepType[], StepNum[], U1[], U2[], U3[], R1[], R2[], R3[]) -> [..., ret_code]`
  - `wrapper_script`: `func_Results_ModeShape`

##### Step 5b Verification Checklist
- [ ] All 3 wrappers execute with `ret_code == 0`
- [ ] `ModalPeriod` — `T1 > 0`, all periods positive
- [ ] `ModalParticipatingMassRatios` — `SumUx` populated, increasing
- [ ] `ModeShape` — non-empty displacement arrays with multiple modes
- [ ] All 3 functions registered in `scripts/registry.json`

#### Step 5b STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 6: Análisis y Control de Modelo (4 wrappers)

##### 6.1 — `Analyze.SetActiveDOF`

- [ ] Create file `scripts/wrappers/func_Analyze_SetActiveDOF.py`:

```python
# ============================================================
# Wrapper: SapModel.Analyze.SetActiveDOF
# Category: Analyze
# Description: Set active/inactive global degrees of freedom for model
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets which global DOFs are active (solved) in the analysis model.
       Essential for 2D models (deactivate out-of-plane DOFs) or specialty analyses.

API Signature:
  SapModel.Analyze.SetActiveDOF(DOF) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  DOF : bool[6] — [UX, UY, UZ, RX, RY, RZ] — True=active
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: set 2D frame DOFs (XZ plane) ---
# UX, UZ, RY active; UY, RX, RZ inactive
dof_2d = [True, False, True, False, True, False]
ret = SapModel.Analyze.SetActiveDOF(dof_2d)
assert ret == 0, f"SetActiveDOF(2D) failed: {ret}"

# --- Verification via GetActiveDOF ---
raw = SapModel.Analyze.GetActiveDOF([])
ret_code = raw[-1]
assert ret_code == 0, f"GetActiveDOF failed: {ret_code}"
read_dof = list(raw[0])
assert read_dof == dof_2d, f"DOFs mismatch: expected {dof_2d}, got {read_dof}"

# --- Set back to full 3D ---
dof_3d = [True, True, True, True, True, True]
ret = SapModel.Analyze.SetActiveDOF(dof_3d)
assert ret == 0, f"SetActiveDOF(3D) failed: {ret}"

raw = SapModel.Analyze.GetActiveDOF([])
assert raw[-1] == 0
read_dof_3d = list(raw[0])
assert read_dof_3d == dof_3d, f"3D DOFs mismatch"

# --- Result ---
result["function"] = "SapModel.Analyze.SetActiveDOF"
result["dof_2d_set"] = dof_2d
result["dof_2d_read"] = read_dof
result["dof_3d_verified"] = True
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify DOFs match.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Analyze.SetActiveDOF`
  - `category`: `Analyze`
  - `description`: `Set active/inactive global degrees of freedom for analysis model`
  - `signature`: `(DOF[6]) -> ret_code`
  - `wrapper_script`: `func_Analyze_SetActiveDOF`

---

##### 6.2 — `Analyze.GetActiveDOF`

- [ ] Create file `scripts/wrappers/func_Analyze_GetActiveDOF.py`:

```python
# ============================================================
# Wrapper: SapModel.Analyze.GetActiveDOF
# Category: Analyze
# Description: Retrieve active global degrees of freedom
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Gets the current active DOFs for the analysis model.

API Signature:
  SapModel.Analyze.GetActiveDOF(DOF) -> [DOF[], ret_code]

ByRef Output:
  DOF[] : bool[6] — [UX, UY, UZ, RX, RY, RZ]

Parameters: None (DOF is ByRef output)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Default for a new model should be all 6 DOFs active
raw = SapModel.Analyze.GetActiveDOF([])
ret_code = raw[-1]
assert ret_code == 0, f"GetActiveDOF failed: {ret_code}"

default_dof = list(raw[0])
# By default, all DOFs should be True
assert all(d == True for d in default_dof), f"Expected all True, got {default_dof}"

# Set to 2D and verify
dof_2d = [True, False, True, False, True, False]
ret = SapModel.Analyze.SetActiveDOF(dof_2d)
assert ret == 0

raw = SapModel.Analyze.GetActiveDOF([])
assert raw[-1] == 0
read_2d = list(raw[0])
assert read_2d == dof_2d, f"2D DOF mismatch: {read_2d}"

# --- Result ---
result["function"] = "SapModel.Analyze.GetActiveDOF"
result["default_dof"] = default_dof
result["after_set_2d"] = read_2d
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify default DOFs and 2D DOFs.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Analyze.GetActiveDOF`
  - `category`: `Analyze`
  - `description`: `Retrieve active global degrees of freedom for analysis model`
  - `signature`: `(DOF[]) -> [DOF[], ret_code]`
  - `wrapper_script`: `func_Analyze_GetActiveDOF`

---

##### 6.3 — `Analyze.GetCaseStatus`

- [ ] Create file `scripts/wrappers/func_Analyze_GetCaseStatus.py`:

```python
# ============================================================
# Wrapper: SapModel.Analyze.GetCaseStatus
# Category: Analyze
# Description: Retrieve run status for all load cases
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Reports whether each load case has been run, is pending, or failed.
       Status: 1=Not run, 2=Could not start, 3=Not finished, 4=Finished.

API Signature:
  SapModel.Analyze.GetCaseStatus(NumberItems, CaseName, Status) ->
      [NumberItems, CaseName[], Status[], ret_code]

ByRef Output:
  NumberItems : int   — number of load cases
  CaseName[]  : str[] — load case names
  Status[]    : int[] — 1=Not run, 2=Could not start, 3=Not finished, 4=Finished

Parameters: None (all are ByRef outputs)
"""

# --- Setup with a model that can be analyzed ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "SEC", "")
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, True, True, True])
assert ret[-1] == 0

# --- Check status BEFORE analysis (should be "Not run") ---
raw = SapModel.Analyze.GetCaseStatus(0, [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetCaseStatus(before) failed: {ret_code}"

num_before = raw[0]
names_before = list(raw[1])
status_before = list(raw[2])

# All should be 1 (Not run)
assert all(s == 1 for s in status_before), f"Expected all status=1, got {status_before}"

# --- Run analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_analyze_casestatus.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

# --- Check status AFTER analysis ---
raw = SapModel.Analyze.GetCaseStatus(0, [], [])
assert raw[-1] == 0

num_after = raw[0]
names_after = list(raw[1])
status_after = list(raw[2])

# Cases that ran should be 4 (Finished)
finished_cases = [n for n, s in zip(names_after, status_after) if s == 4]

# --- Result ---
result["function"] = "SapModel.Analyze.GetCaseStatus"
result["cases_before"] = names_before
result["status_before"] = status_before
result["cases_after"] = names_after
result["status_after"] = status_after
result["finished_cases"] = finished_cases
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify status changes from 1 to 4.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.Analyze.GetCaseStatus`
  - `category`: `Analyze`
  - `description`: `Retrieve run status for all load cases (1=Not run, 4=Finished)`
  - `signature`: `(NumberItems, CaseName[], Status[]) -> [NumberItems, CaseName[], Status[], ret_code]`
  - `wrapper_script`: `func_Analyze_GetCaseStatus`

---

##### 6.4 — `File.OpenFile` (verify/update existing)

- [ ] Verify existing wrapper `scripts/wrappers/func_File_OpenFile.py` is in registry.
- [ ] If not in registry, register via `register_verified_function`:
  - `function_path`: `SapModel.File.OpenFile`
  - `category`: `File`
  - `description`: `Open an existing SAP2000 model file (.sdb)`
  - `signature`: `(FileName) -> ret_code`
  - `wrapper_script`: `func_File_OpenFile`

##### Step 6 Verification Checklist
- [ ] `SetActiveDOF` — 2D DOF array matches set/get round-trip
- [ ] `GetActiveDOF` — default all-True, 2D setting confirmed
- [ ] `GetCaseStatus` — status transitions from 1→4 after RunAnalysis
- [ ] `File.OpenFile` — confirmed in registry
- [ ] All functions registered in `scripts/registry.json`

#### Step 6 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 7: Links Lineales y Propiedades Área (5 wrappers)

##### 7.1 — `PropLink.SetLinear`

- [ ] Create file `scripts/wrappers/func_PropLink_SetLinear.py`:

```python
# ============================================================
# Wrapper: SapModel.PropLink.SetLinear
# Category: Properties
# Description: Define a linear-type link property with stiffness and damping
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates or modifies a linear link property. Defines DOFs, fixities,
       stiffness (Ke), and damping (Ce) for 6 DOFs (U1-U3, R1-R3).
       Used for spring connections, elastic supports, and simple connectors.

API Signature:
  SapModel.PropLink.SetLinear(Name, DOF, Fixed, Ke, Ce,
      dj2, dj3, KeCoupled, CeCoupled, Notes, GUID) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str      — Link property name
  DOF       : bool[6]  — Active DOFs [U1,U2,U3,R1,R2,R3]
  Fixed     : bool[6]  — Fixed DOFs (if DOF is True)
  Ke        : float[6] — Stiffness values (uncoupled) [F/L or FL]
  Ce        : float[6] — Damping values (uncoupled) [F/L or FL]
  dj2       : float    — Distance to U2 shear spring from J-End [L]
  dj3       : float    — Distance to U3 shear spring from J-End [L]
  KeCoupled : bool     — True if stiffness is coupled (21 terms)
  CeCoupled : bool     — True if damping is coupled (21 terms)
  Notes     : str      — Optional notes
  GUID      : str      — Optional GUID
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Target function: create linear link with translational stiffness ---
dof = [True, True, True, False, False, False]  # Only translational DOFs
fixed = [False, False, False, False, False, False]  # None fixed
ke = [10000.0, 5000.0, 5000.0, 0.0, 0.0, 0.0]  # kN/m stiffness
ce = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # No damping

ret = SapModel.PropLink.SetLinear(
    "SPRING_V", dof, fixed, ke, ce, 0.0, 0.0, False, False
)
assert ret == 0, f"SetLinear(SPRING_V) failed: {ret}"

# Create another with all 6 DOFs
dof_full = [True, True, True, True, True, True]
fixed_full = [False, False, False, False, False, False]
ke_full = [10000, 10000, 10000, 5000, 5000, 5000]
ce_full = [100, 100, 100, 50, 50, 50]

ret = SapModel.PropLink.SetLinear(
    "CONNECTOR_6DOF", dof_full, fixed_full, ke_full, ce_full, 0.0, 0.0
)
assert ret == 0, f"SetLinear(CONNECTOR_6DOF) failed: {ret}"

# --- Verification via GetLinear ---
raw = SapModel.PropLink.GetLinear(
    "SPRING_V", [], [], [], [], 0.0, 0.0, False, False, "", ""
)
ret_code = raw[-1]
assert ret_code == 0, f"GetLinear failed: {ret_code}"

read_dof = list(raw[0])
read_ke = list(raw[2])
assert read_dof[0] == True, f"U1 DOF should be active"
assert abs(read_ke[0] - 10000.0) < 1, f"U1 stiffness mismatch: {read_ke[0]}"

# --- Result ---
result["function"] = "SapModel.PropLink.SetLinear"
result["links_defined"] = ["SPRING_V", "CONNECTOR_6DOF"]
result["dof_read"] = read_dof
result["ke_read"] = read_ke
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify stiffness values match.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.PropLink.SetLinear`
  - `category`: `Properties`
  - `description`: `Define a linear-type link property (stiffness, damping, DOFs)`
  - `signature`: `(Name, DOF[6], Fixed[6], Ke[6], Ce[6], dj2, dj3, KeCoupled, CeCoupled, Notes, GUID) -> ret_code`
  - `wrapper_script`: `func_PropLink_SetLinear`

---

##### 7.2 — `LinkObj.AddByPoint`

- [ ] Create file `scripts/wrappers/func_LinkObj_AddByPoint.py`:

```python
# ============================================================
# Wrapper: SapModel.LinkObj.AddByPoint
# Category: Object_Model
# Description: Create a link element between two existing points
# Verified: 2026-03-28
# Prerequisites: Model open, points and link property exist
# ============================================================
"""
Usage: Creates a 2-joint link element connecting two existing point objects,
       or a 1-joint grounded link. Used for spring connections, dampers,
       and simple connectors.

API Signature:
  SapModel.LinkObj.AddByPoint(Point1, Point2, Name,
      IsSingleJoint, PropName, UserName) -> [Name, ret_code]

ByRef Output:
  Name     : str — Assigned link name
  ret_code : int — 0=success

Parameters:
  Point1        : str  — I-End point name
  Point2        : str  — J-End point name (ignored if IsSingleJoint=True)
  Name          : str  — Output: assigned name
  IsSingleJoint : bool — True=1-joint grounded link
  PropName      : str  — Link property name ("Default" or defined)
  UserName      : str  — Optional user name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Create link property
dof = [True, True, True, False, False, False]
fixed = [False, False, False, False, False, False]
ke = [5000, 5000, 5000, 0, 0, 0]
ce = [0, 0, 0, 0, 0, 0]
ret = SapModel.PropLink.SetLinear("SPRING_TEST", dof, fixed, ke, ce, 0, 0)
assert ret == 0

# Create two points
raw = SapModel.PointObj.AddCartesian(0, 0, 0, "", "PT_I")
pt_i = raw[0]
assert raw[-1] == 0
raw = SapModel.PointObj.AddCartesian(0, 0, 0.5, "", "PT_J")
pt_j = raw[0]
assert raw[-1] == 0

# --- Target function: two-joint link ---
raw = SapModel.LinkObj.AddByPoint(pt_i, pt_j, "", False, "SPRING_TEST", "LINK_1")
link_name = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"AddByPoint(2-joint) failed: {ret_code}"

# --- Target function: single-joint (grounded) link ---
raw2 = SapModel.PointObj.AddCartesian(5, 0, 0, "", "PT_GROUND")
pt_g = raw2[0]
assert raw2[-1] == 0

raw = SapModel.LinkObj.AddByPoint(pt_g, "", "", True, "SPRING_TEST", "LINK_GND")
link_gnd = raw[0]
assert raw[-1] == 0, f"AddByPoint(1-joint) failed: {raw[-1]}"

# --- Verification ---
count = SapModel.LinkObj.Count()
assert count == 2, f"Expected 2 links, got {count}"

# --- Result ---
result["function"] = "SapModel.LinkObj.AddByPoint"
result["two_joint_link"] = link_name
result["single_joint_link"] = link_gnd
result["link_count"] = count
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `link_count == 2`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.LinkObj.AddByPoint`
  - `category`: `Object_Model`
  - `description`: `Create a link element between two existing points (or grounded single-joint)`
  - `signature`: `(Point1, Point2, Name, IsSingleJoint, PropName, UserName) -> [Name, ret_code]`
  - `wrapper_script`: `func_LinkObj_AddByPoint`

---

##### 7.3 — `LinkObj.AddByCoord`

- [ ] Create file `scripts/wrappers/func_LinkObj_AddByCoord.py`:

```python
# ============================================================
# Wrapper: SapModel.LinkObj.AddByCoord
# Category: Object_Model
# Description: Create a link element by specifying end-point coordinates
# Verified: 2026-03-28
# Prerequisites: Model open, link property exists
# ============================================================
"""
Usage: Creates a link between two coordinate locations. Points are
       auto-created if they don't exist at those coordinates.

API Signature:
  SapModel.LinkObj.AddByCoord(xi, yi, zi, xj, yj, zj, Name,
      IsSingleJoint, PropName, UserName, CSys) -> [Name, ret_code]

ByRef Output:
  Name     : str — Assigned link name
  ret_code : int — 0=success

Parameters:
  xi,yi,zi      : float — I-End coordinates
  xj,yj,zj      : float — J-End coordinates (ignored if single joint)
  Name           : str   — Output: assigned name
  IsSingleJoint  : bool  — True=1-joint grounded link
  PropName       : str   — Link property name
  UserName       : str   — Optional user name
  CSys           : str   — Coordinate system
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

dof = [True, True, True, True, True, True]
fixed = [False, False, False, False, False, False]
ke = [10000, 10000, 20000, 1000, 1000, 1000]
ce = [0, 0, 0, 0, 0, 0]
ret = SapModel.PropLink.SetLinear("CONN_TEST", dof, fixed, ke, ce, 0, 0)
assert ret == 0

# --- Target function: two-joint link by coordinates ---
raw = SapModel.LinkObj.AddByCoord(
    0, 0, 0,     # I-End
    0, 0, 0.3,   # J-End
    "", False, "CONN_TEST", "LINK_COORD1"
)
link1 = raw[0]
assert raw[-1] == 0, f"AddByCoord(2-joint) failed: {raw[-1]}"

# Single-joint grounded link
raw = SapModel.LinkObj.AddByCoord(
    5, 5, 0,     # I-End
    0, 0, 0,     # J-End (ignored)
    "", True, "CONN_TEST", "LINK_GRND"
)
link2 = raw[0]
assert raw[-1] == 0, f"AddByCoord(1-joint) failed: {raw[-1]}"

# --- Verification ---
count = SapModel.LinkObj.Count()
assert count == 2, f"Expected 2 links, got {count}"

# --- Result ---
result["function"] = "SapModel.LinkObj.AddByCoord"
result["link_2joint"] = link1
result["link_grounded"] = link2
result["link_count"] = count
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `link_count == 2`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.LinkObj.AddByCoord`
  - `category`: `Object_Model`
  - `description`: `Create a link element by specifying I-End and J-End coordinates`
  - `signature`: `(xi, yi, zi, xj, yj, zj, Name, IsSingleJoint, PropName, UserName, CSys) -> [Name, ret_code]`
  - `wrapper_script`: `func_LinkObj_AddByCoord`

---

##### 7.4 — `AreaObj.SetProperty`

- [ ] Create file `scripts/wrappers/func_AreaObj_SetProperty.py`:

```python
# ============================================================
# Wrapper: SapModel.AreaObj.SetProperty
# Category: Object_Model
# Description: Assign or change area section property on an area object
# Verified: 2026-03-28
# Prerequisites: Model open, area object and property exist
# ============================================================
"""
Usage: Assigns a shell/plate/membrane section property to an area object,
       or changes the property of an existing area.

API Signature:
  SapModel.AreaObj.SetProperty(Name, PropName, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str — Area object name
  PropName : str — Area property name (or "None" to clear)
  ItemType : int — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

# Two different shell sections
ret = SapModel.PropArea.SetShell_1("SLAB_15", 1, False, "CONC_TEST", 0, 0.15, 0.15)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_25", 1, False, "CONC_TEST", 0, 0.25, 0.25)
assert ret == 0

# Create area with SLAB_15
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 4, 4, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_15"
)
area_name = raw[3]
assert raw[-1] == 0

# Verify initial property
raw_get = SapModel.AreaObj.GetProperty(area_name, "", "")
assert raw_get[-1] == 0
initial_prop = raw_get[0]
assert initial_prop == "SLAB_15", f"Initial prop should be SLAB_15, got {initial_prop}"

# --- Target function: change property ---
ret = SapModel.AreaObj.SetProperty(area_name, "SLAB_25")
assert ret == 0, f"SetProperty failed: {ret}"

# --- Verification ---
raw_get = SapModel.AreaObj.GetProperty(area_name, "", "")
assert raw_get[-1] == 0
new_prop = raw_get[0]
assert new_prop == "SLAB_25", f"Expected SLAB_25, got {new_prop}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetProperty"
result["area_name"] = area_name
result["initial_property"] = initial_prop
result["new_property"] = new_prop
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify property changed from SLAB_15 to SLAB_25.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.AreaObj.SetProperty`
  - `category`: `Object_Model`
  - `description`: `Assign or change area section property on an area object`
  - `signature`: `(Name, PropName, ItemType) -> ret_code`
  - `wrapper_script`: `func_AreaObj_SetProperty`

---

##### 7.5 — `PropArea.GetShell_1`

- [ ] Create file `scripts/wrappers/func_PropArea_GetShell_1.py`:

```python
# ============================================================
# Wrapper: SapModel.PropArea.GetShell_1
# Category: Properties
# Description: Retrieve shell-type area section properties
# Verified: 2026-03-28
# Prerequisites: Model open, shell property defined
# ============================================================
"""
Usage: Reads back properties of a shell-type area section including
       shell type, material, thicknesses, and other attributes.

API Signature:
  SapModel.PropArea.GetShell_1(Name, ShellType, IncludeDrillingDOF,
      MatProp, MatAng, Thickness, Bending,
      Color, Notes, GUID) -> [..., ret_code]

ByRef Output (8 values):
  ShellType         : int  — 1=Shell-thin, 2=Shell-thick, 3=Plate-thin,
                             4=Plate-thick, 5=Membrane, 6=Layered
  IncludeDrillingDOF: bool — Drilling DOF in analysis
  MatProp           : str  — Material name
  MatAng            : float— Material angle [deg]
  Thickness         : float— Membrane thickness [L]
  Bending           : float— Bending thickness [L]
  Color             : int  — Display color
  Notes             : str  — Notes
  GUID              : str  — GUID

Parameters:
  Name : str — Shell-type area property name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

# Create shell with known properties
ret = SapModel.PropArea.SetShell_1("WALL_30", 2, True, "CONC_TEST", 0, 0.30, 0.30)
assert ret == 0

# --- Target function ---
raw = SapModel.PropArea.GetShell_1(
    "WALL_30", 0, False, "", 0.0, 0.0, 0.0, 0, "", ""
)
ret_code = raw[-1]
assert ret_code == 0, f"GetShell_1 failed: {ret_code}"

shell_type = raw[0]
include_drill = raw[1]
mat_prop = raw[2]
mat_ang = raw[3]
thickness = raw[4]
bending = raw[5]

assert shell_type == 2, f"Expected ShellType=2(thick), got {shell_type}"
assert mat_prop == "CONC_TEST", f"Expected CONC_TEST, got {mat_prop}"
assert abs(thickness - 0.30) < 0.001, f"Expected thickness=0.30, got {thickness}"
assert abs(bending - 0.30) < 0.001, f"Expected bending=0.30, got {bending}"

# --- Result ---
result["function"] = "SapModel.PropArea.GetShell_1"
result["shell_type"] = shell_type
result["material"] = mat_prop
result["thickness"] = thickness
result["bending"] = bending
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` and verify `shell_type == 2`, `thickness == 0.30`.
- [ ] Register via `register_verified_function`:
  - `function_path`: `SapModel.PropArea.GetShell_1`
  - `category`: `Properties`
  - `description`: `Retrieve shell-type area section properties (type, material, thicknesses)`
  - `signature`: `(Name, ShellType, IncludeDrillingDOF, MatProp, MatAng, Thickness, Bending, Color, Notes, GUID) -> [..., ret_code]`
  - `wrapper_script`: `func_PropArea_GetShell_1`

##### Step 7 Verification Checklist
- [ ] All 5 wrappers execute with `ret_code == 0`
- [ ] `PropLink.SetLinear` — stiffness values match on read-back
- [ ] `LinkObj.AddByPoint` — 2 links created (2-joint + grounded)
- [ ] `LinkObj.AddByCoord` — 2 links created
- [ ] `AreaObj.SetProperty` — property changed from SLAB_15 to SLAB_25
- [ ] `PropArea.GetShell_1` — `shell_type=2`, `thickness=0.30`, `material=CONC_TEST`
- [ ] All 5 functions registered in `scripts/registry.json`

#### Step 7 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

## Final Summary

| Step | Wrappers | Focus |
|------|----------|-------|
| 1 | 6 | Core loading (frame distributed/point, area uniform/gravity, point force) |
| 2 | 4 | Frame releases, insertion point, local axes |
| 3 | 4 | Groups (create, list, assign frames/areas) |
| 4 | 2 | Diaphragm constraints (set/get) |
| 5a | 2 | General results (base reactions, area stresses) |
| 5b | 3 | Modal results (period, mass ratios, mode shapes) |
| 6 | 4 | Analysis control (DOFs, case status, file open) |
| 7 | 5 | Linear links (property, add by point/coord), area property ops |
| **Total** | **30** | **+ 3 already existing (update registry only)** |

After all steps: registry should have ~130 functions, ~83 wrappers, ~90% daily workflow coverage.
