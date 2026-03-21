# Step 2: Load Assignment Wrappers (Frame, Point, Area Loads)

## Goal
Add 6 wrapper scripts for core load-application functions (`PointObj.SetLoadForce`, `FrameObj.SetLoadDistributed`, `FrameObj.SetLoadPoint`, `AreaObj.SetLoadUniform`, `AreaObj.SetLoadGravity`, `FrameObj.SetLoadTemperature`) and register them in `registry.json`.

## Prerequisites
Make sure you are on the `expand-wrappers-registry` branch and Step 1 is committed.

### Step-by-Step Instructions

#### Step 2.1: Create `func_PointObj_SetLoadForce.py`
- [x] Create file `scripts/wrappers/func_PointObj_SetLoadForce.py`
- [x] Copy and paste code below into `scripts/wrappers/func_PointObj_SetLoadForce.py`:

```python
# ============================================================
# Wrapper: SapModel.PointObj.SetLoadForce
# Category: Load_Assignment
# Description: Apply forces/moments at a joint (6 DOF)
# Verified: pending
# Prerequisites: Model open, point exists, load pattern defined
# ============================================================
"""
Usage: Assigns point loads (forces and moments) to a joint in a
       specified load pattern. The value array has 6 components
       corresponding to [F1, F2, F3, M1, M2, M3] in the specified
       coordinate system.

API Signature:
  SapModel.PointObj.SetLoadForce(Name, LoadPat, Value, Replace, CSys, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str      — Point object name
  LoadPat  : str      — Load pattern name
  Value    : float[6] — [F1, F2, F3, M1, M2, M3] forces and moments
  Replace  : bool     — True=replace existing loads (default=True)
  CSys     : str      — Coordinate system (default="Global")
  ItemType : int      — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, section, frame, load pattern ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Get top point
raw_pts = SapModel.FrameObj.GetPoints(raw[0], "", "")
pt_top = raw_pts[1]  # j-end (top)
pt_bot = raw_pts[0]  # i-end (base)
assert raw_pts[-1] == 0, f"GetPoints failed: {raw_pts[-1]}"

# Fix the base
ret_r = SapModel.PointObj.SetRestraint(pt_bot, [True, True, True, True, True, True])
assert ret_r[-1] == 0, f"SetRestraint failed: {ret_r[-1]}"

# Add load pattern
ret = SapModel.LoadPatterns.Add("POINT_LOAD", 8)  # 8=Other
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: apply lateral force at top ---
# 100 kN in X direction, 50 kN downward in Z
force_values = [100.0, 0.0, -50.0, 0.0, 0.0, 0.0]
ret = SapModel.PointObj.SetLoadForce(pt_top, "POINT_LOAD", force_values)
assert ret == 0, f"SetLoadForce failed: {ret}"

# --- Verification ---
# Read back the force
raw = SapModel.PointObj.GetLoadForce(pt_top, 0, [], [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadForce failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.PointObj.SetLoadForce"
result["point_name"] = pt_top
result["force_values"] = force_values
result["status"] = "verified"
```

#### Step 2.2: Create `func_FrameObj_SetLoadDistributed.py`
- [x] Create file `scripts/wrappers/func_FrameObj_SetLoadDistributed.py`
- [x] Copy and paste code below into `scripts/wrappers/func_FrameObj_SetLoadDistributed.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadDistributed
# Category: Load_Assignment
# Description: Apply uniform/trapezoidal distributed loads on frames
# Verified: pending
# Prerequisites: Model open, frame exists, load pattern defined
# ============================================================
"""
Usage: Assigns distributed loads (uniform or trapezoidal) along a
       frame element in a specified load pattern.

API Signature:
  SapModel.FrameObj.SetLoadDistributed(Name, LoadPat, MyType, Dir,
      Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Frame object name
  LoadPat  : str   — Load pattern name
  MyType   : int   — 1=Force per unit length, 2=Moment per unit length
  Dir      : int   — Direction: 1=Local1, 2=Local2, 3=Local3,
                      4=X, 5=Y, 6=Z, 7=ProjX, 8=ProjY, 9=ProjZ,
                      10=Gravity, 11=ProjGravity
  Dist1    : float — Start distance (relative or absolute)
  Dist2    : float — End distance (relative or absolute)
  Val1     : float — Load value at start [F/L] or [FL/L]
  Val2     : float — Load value at end [F/L] or [FL/L]
  CSys     : str   — Coordinate system (default="Global")
  RelDist  : bool  — True=distances are relative (0-1), False=absolute (default=True)
  Replace  : bool  — True=replace existing loads (default=True)
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

# Simply supported beam
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "SEC_TEST", "")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Supports
raw_pts = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i, pt_j = raw_pts[0], raw_pts[1]
ret_r = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert ret_r[-1] == 0
ret_r = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert ret_r[-1] == 0

# Load pattern
ret = SapModel.LoadPatterns.Add("DL_DIST", 1, 0)  # Dead
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: uniform load over full span ---
# -10 kN/m in gravity direction (full span, relative distances 0 to 1)
ret = SapModel.FrameObj.SetLoadDistributed(
    frame_name, "DL_DIST",
    1,     # MyType: Force per unit length
    10,    # Dir: Gravity direction
    0, 1,  # Dist1, Dist2 (relative: start to end)
    -10, -10  # Val1, Val2 (uniform -10 kN/m)
)
assert ret == 0, f"SetLoadDistributed(uniform) failed: {ret}"

# --- Target function: trapezoidal load ---
ret = SapModel.LoadPatterns.Add("LL_TRAP", 3, 0)  # Live
assert ret == 0
ret = SapModel.FrameObj.SetLoadDistributed(
    frame_name, "LL_TRAP",
    1,     # Force
    10,    # Gravity
    0, 1,
    -5, -15  # Trapezoidal: 5 kN/m at start, 15 kN/m at end
)
assert ret == 0, f"SetLoadDistributed(trapezoidal) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadDistributed"
result["frame_name"] = frame_name
result["loads_applied"] = ["DL_DIST (uniform -10 kN/m)", "LL_TRAP (trapezoidal -5 to -15 kN/m)"]
result["status"] = "verified"
```

#### Step 2.3: Create `func_FrameObj_SetLoadPoint.py`
- [x] Create file `scripts/wrappers/func_FrameObj_SetLoadPoint.py`
- [x] Copy and paste code below into `scripts/wrappers/func_FrameObj_SetLoadPoint.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadPoint
# Category: Load_Assignment
# Description: Apply a concentrated point load along a frame element
# Verified: pending
# Prerequisites: Model open, frame exists, load pattern defined
# ============================================================
"""
Usage: Assigns a concentrated (point) load at a specified location
       along a frame element.

API Signature:
  SapModel.FrameObj.SetLoadPoint(Name, LoadPat, MyType, Dir,
      Dist, Val, CSys, RelDist, Replace, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Frame object name
  LoadPat  : str   — Load pattern name
  MyType   : int   — 1=Force, 2=Moment
  Dir      : int   — Direction: 1=Local1, 2=Local2, 3=Local3,
                      4=X, 5=Y, 6=Z, 7=ProjX, 8=ProjY, 9=ProjZ,
                      10=Gravity, 11=ProjGravity
  Dist     : float — Distance to load location (relative or absolute)
  Val      : float — Load value [F] or [FL]
  CSys     : str   — Coordinate system (default="Global")
  RelDist  : bool  — True=relative (0-1), False=absolute (default=True)
  Replace  : bool  — True=replace existing loads (default=True)
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "SEC_TEST", "")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Supports
raw_pts = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i, pt_j = raw_pts[0], raw_pts[1]
ret_r = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert ret_r[-1] == 0
ret_r = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert ret_r[-1] == 0

# Load pattern
ret = SapModel.LoadPatterns.Add("PT_LOAD", 3, 0)  # Live
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: point load at mid-span ---
# -50 kN in gravity direction at 50% of span
ret = SapModel.FrameObj.SetLoadPoint(
    frame_name, "PT_LOAD",
    1,      # MyType: Force
    10,     # Dir: Gravity
    0.5,    # Dist: mid-span (relative)
    -50     # Val: -50 kN
)
assert ret == 0, f"SetLoadPoint(midspan) failed: {ret}"

# Point load at quarter-span
ret = SapModel.FrameObj.SetLoadPoint(
    frame_name, "PT_LOAD",
    1,      # Force
    10,     # Gravity
    0.25,   # Dist: quarter-span
    -25,    # Val: -25 kN
    "Global", True, False  # Don't replace — add to existing
)
assert ret == 0, f"SetLoadPoint(quarter) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadPoint"
result["frame_name"] = frame_name
result["loads_applied"] = ["-50 kN at mid-span", "-25 kN at quarter-span"]
result["status"] = "verified"
```

#### Step 2.4: Create `func_AreaObj_SetLoadUniform.py`
- [x] Create file `scripts/wrappers/func_AreaObj_SetLoadUniform.py`
- [x] Copy and paste code below into `scripts/wrappers/func_AreaObj_SetLoadUniform.py`:

```python
# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadUniform
# Category: Load_Assignment
# Description: Apply uniform pressure on area elements (slab loads)
# Verified: pending
# Prerequisites: Model open, area exists, load pattern defined
# ============================================================
"""
Usage: Assigns a uniform surface load to an area element in a
       specified load pattern.

API Signature:
  SapModel.AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir,
      Replace, CSys, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Area object name
  LoadPat  : str   — Load pattern name
  Value    : float — Uniform load value [F/L^2]
  Dir      : int   — Direction: 1=Local1, 2=Local2, 3=Local3,
                      4=X, 5=Y, 6=Z, 7=ProjX, 8=ProjY, 9=ProjZ,
                      10=Gravity, 11=ProjGravity
  Replace  : bool  — True=replace existing loads (default=True)
  CSys     : str   — Coordinate system (default="Global")
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, shell section, area ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, True, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0, f"SetShell_1 failed: {ret}"

# Rectangular slab 6m x 4m at Z=3m
x = [0.0, 6.0, 6.0, 0.0]
y = [0.0, 0.0, 4.0, 4.0]
z = [3.0, 3.0, 3.0, 3.0]
raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "SLAB_20", "")
area_name = raw[3]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Load pattern
ret = SapModel.LoadPatterns.Add("SLAB_LL", 3, 0)  # Live
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: uniform live load on slab ---
# -5 kN/m² in gravity direction
ret = SapModel.AreaObj.SetLoadUniform(area_name, "SLAB_LL", -5.0, 10)
assert ret == 0, f"SetLoadUniform failed: {ret}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadUniform"
result["area_name"] = area_name
result["load_value"] = -5.0
result["direction"] = "Gravity"
result["status"] = "verified"
```

#### Step 2.5: Create `func_AreaObj_SetLoadGravity.py`
- [x] Create file `scripts/wrappers/func_AreaObj_SetLoadGravity.py`
- [x] Copy and paste code below into `scripts/wrappers/func_AreaObj_SetLoadGravity.py`:

```python
# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadGravity
# Category: Load_Assignment
# Description: Apply gravity multiplier on area self-weight
# Verified: pending
# Prerequisites: Model open, area exists, load pattern defined
# ============================================================
"""
Usage: Assigns gravity load multipliers to an area element.
       This acts as a multiplier on the element's self-weight,
       applying loads in the specified global direction.

API Signature:
  SapModel.AreaObj.SetLoadGravity(Name, LoadPat, x, y, z,
      Replace, CSys, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Area object name
  LoadPat  : str   — Load pattern name
  x        : float — Gravity multiplier in global X
  y        : float — Gravity multiplier in global Y
  z        : float — Gravity multiplier in global Z
  Replace  : bool  — True=replace existing (default=True)
  CSys     : str   — Coordinate system (default="Global")
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_TEST", 1, 23.56)
assert ret == 0

ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, True, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

x = [0.0, 6.0, 6.0, 0.0]
y = [0.0, 0.0, 4.0, 4.0]
z = [3.0, 3.0, 3.0, 3.0]
raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "SLAB_20", "")
area_name = raw[3]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

ret = SapModel.LoadPatterns.Add("SW_GRAV", 1, 0)  # Dead
assert ret == 0

# --- Target function: gravity multiplier (1g downward) ---
ret = SapModel.AreaObj.SetLoadGravity(area_name, "SW_GRAV", 0, 0, -1)
assert ret == 0, f"SetLoadGravity failed: {ret}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadGravity"
result["area_name"] = area_name
result["gravity_multiplier"] = [0, 0, -1]
result["status"] = "verified"
```

#### Step 2.6: Create `func_FrameObj_SetLoadTemperature.py`
- [x] Create file `scripts/wrappers/func_FrameObj_SetLoadTemperature.py`
- [x] Copy and paste code below into `scripts/wrappers/func_FrameObj_SetLoadTemperature.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadTemperature
# Category: Load_Assignment
# Description: Apply thermal loads on frame elements
# Verified: pending
# Prerequisites: Model open, frame exists, load pattern defined
# ============================================================
"""
Usage: Assigns temperature loads (uniform or gradient) to a frame
       element.

API Signature:
  SapModel.FrameObj.SetLoadTemperature(Name, LoadPat, MyType,
      Val, PatternName, Replace, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name        : str   — Frame object name
  LoadPat     : str   — Load pattern name
  MyType      : int   — 1=Temperature, 2=Temperature gradient 2-2,
                         3=Temperature gradient 3-3
  Val         : float — Temperature value [T] or gradient [T/L]
  PatternName : str   — Joint pattern name (""=none)
  Replace     : bool  — True=replace existing (default=True)
  ItemType    : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("MAT_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "SEC_TEST", "")
frame_name = raw[0]
assert raw[-1] == 0

# Supports
raw_pts = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i, pt_j = raw_pts[0], raw_pts[1]
ret_r = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert ret_r[-1] == 0
ret_r = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert ret_r[-1] == 0

# Load pattern for thermal
ret = SapModel.LoadPatterns.Add("TEMP", 8, 0)  # Other
assert ret == 0

# --- Target function: uniform temperature change ---
# +30°C uniform temperature increase
ret = SapModel.FrameObj.SetLoadTemperature(
    frame_name, "TEMP",
    1,      # MyType: Temperature
    30      # Val: +30°C
)
assert ret == 0, f"SetLoadTemperature(uniform) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadTemperature"
result["frame_name"] = frame_name
result["temperature_change"] = 30
result["status"] = "verified"
```

#### Step 2.7: Execute & Verify All Wrappers
- [x] Ensure SAP2000 is connected (`connect_sap2000`)
- [x] Execute each wrapper via `run_sap_script` and verify success:
  - `func_PointObj_SetLoadForce` → save as `func_PointObj_SetLoadForce`
  - `func_FrameObj_SetLoadDistributed` → save as `func_FrameObj_SetLoadDistributed`
  - `func_FrameObj_SetLoadPoint` → save as `func_FrameObj_SetLoadPoint`
  - `func_AreaObj_SetLoadUniform` → save as `func_AreaObj_SetLoadUniform`
  - `func_AreaObj_SetLoadGravity` → save as `func_AreaObj_SetLoadGravity`
  - `func_FrameObj_SetLoadTemperature` → save as `func_FrameObj_SetLoadTemperature`

#### Step 2.8: Register Functions in Registry
- [x] Call `register_verified_function` for each of the 6 functions:

**SapModel.PointObj.SetLoadForce:**
```json
{
  "function_path": "SapModel.PointObj.SetLoadForce",
  "category": "Load_Assignment",
  "description": "Apply forces/moments at a joint (6 DOF)",
  "signature": "(Name, LoadPat, Value, Replace, CSys, ItemType) -> ret_code",
  "parameter_notes": "Name: str (point name); LoadPat: str (load pattern); Value: float[6] [F1,F2,F3,M1,M2,M3]; Replace: bool (True); CSys: str ('Global'); ItemType: int (0=Object)",
  "wrapper_script": "func_PointObj_SetLoadForce",
  "notes": "Returns ret_code directly (0=success). Value array in coordinate system directions."
}
```

**SapModel.FrameObj.SetLoadDistributed:**
```json
{
  "function_path": "SapModel.FrameObj.SetLoadDistributed",
  "category": "Load_Assignment",
  "description": "Apply uniform/trapezoidal distributed loads on frames",
  "signature": "(Name, LoadPat, MyType, Dir, Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType) -> ret_code",
  "parameter_notes": "Name: str; LoadPat: str; MyType: int (1=Force/L, 2=Moment/L); Dir: int (10=Gravity, 6=Z, etc.); Dist1/Dist2: float (relative 0-1 or absolute); Val1/Val2: float [F/L]; CSys: str ('Global'); RelDist: bool (True); Replace: bool (True); ItemType: int (0)",
  "wrapper_script": "func_FrameObj_SetLoadDistributed",
  "notes": "For uniform load set Val1=Val2. For trapezoidal use different Val1/Val2. Dir=10 for gravity."
}
```

**SapModel.FrameObj.SetLoadPoint:**
```json
{
  "function_path": "SapModel.FrameObj.SetLoadPoint",
  "category": "Load_Assignment",
  "description": "Apply a concentrated point load along a frame element",
  "signature": "(Name, LoadPat, MyType, Dir, Dist, Val, CSys, RelDist, Replace, ItemType) -> ret_code",
  "parameter_notes": "Name: str; LoadPat: str; MyType: int (1=Force, 2=Moment); Dir: int (10=Gravity, etc.); Dist: float (0-1 relative or absolute); Val: float [F] or [FL]; CSys: str ('Global'); RelDist: bool (True); Replace: bool (True); ItemType: int (0)",
  "wrapper_script": "func_FrameObj_SetLoadPoint",
  "notes": "Returns ret_code directly (0=success). Set Replace=False to add multiple point loads."
}
```

**SapModel.AreaObj.SetLoadUniform:**
```json
{
  "function_path": "SapModel.AreaObj.SetLoadUniform",
  "category": "Load_Assignment",
  "description": "Apply uniform surface pressure on area elements (slab loads)",
  "signature": "(Name, LoadPat, Value, Dir, Replace, CSys, ItemType) -> ret_code",
  "parameter_notes": "Name: str; LoadPat: str; Value: float [F/L^2]; Dir: int (10=Gravity, 6=Z, etc.); Replace: bool (True); CSys: str ('Global'); ItemType: int (0)",
  "wrapper_script": "func_AreaObj_SetLoadUniform",
  "notes": "Returns ret_code directly (0=success). Negative value for downward pressure with gravity direction."
}
```

**SapModel.AreaObj.SetLoadGravity:**
```json
{
  "function_path": "SapModel.AreaObj.SetLoadGravity",
  "category": "Load_Assignment",
  "description": "Apply gravity multiplier on area element self-weight",
  "signature": "(Name, LoadPat, x, y, z, Replace, CSys, ItemType) -> ret_code",
  "parameter_notes": "Name: str; LoadPat: str; x/y/z: float (gravity multipliers in global directions); Replace: bool (True); CSys: str ('Global'); ItemType: int (0)",
  "wrapper_script": "func_AreaObj_SetLoadGravity",
  "notes": "Returns ret_code directly (0=success). Use z=-1 for standard 1g downward gravity."
}
```

**SapModel.FrameObj.SetLoadTemperature:**
```json
{
  "function_path": "SapModel.FrameObj.SetLoadTemperature",
  "category": "Load_Assignment",
  "description": "Apply thermal loads on frame elements",
  "signature": "(Name, LoadPat, MyType, Val, PatternName, Replace, ItemType) -> ret_code",
  "parameter_notes": "Name: str; LoadPat: str; MyType: int (1=Temperature, 2=Gradient2-2, 3=Gradient3-3); Val: float [T] or [T/L]; PatternName: str (''=none); Replace: bool (True); ItemType: int (0)",
  "wrapper_script": "func_FrameObj_SetLoadTemperature",
  "notes": "Returns ret_code directly (0=success). Requires material with thermal expansion coefficient defined."
}
```

##### Step 2 Verification Checklist
- [x] All 6 wrappers exist in `scripts/wrappers/`
- [x] All 6 wrappers executed successfully via `run_sap_script` (status=verified)
- [x] All 6 functions registered in `registry.json` with full metadata
- [x] Registry count increased from ~63 to ~69

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
```powershell
git add scripts/wrappers/func_PointObj_SetLoadForce.py scripts/wrappers/func_FrameObj_SetLoadDistributed.py scripts/wrappers/func_FrameObj_SetLoadPoint.py scripts/wrappers/func_AreaObj_SetLoadUniform.py scripts/wrappers/func_AreaObj_SetLoadGravity.py scripts/wrappers/func_FrameObj_SetLoadTemperature.py scripts/registry.json
git commit -m "feat: add load assignment wrappers (point force, distributed, point load, uniform area, gravity, temperature)"
```
