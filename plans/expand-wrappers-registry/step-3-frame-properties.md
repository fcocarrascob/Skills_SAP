# Step 3: Frame Properties & Releases

## Goal
Add 7 wrapper scripts for missing cross-section types (`SetPipe`, `SetChannel`, `SetAngle`, `SetTee`) and critical frame-object assignment functions (`SetReleases`, `SetEndLengthOffset`, `SetModifiers`) and register them in `registry.json`.

## Prerequisites
Make sure you are on the `expand-wrappers-registry` branch and Steps 1-2 are committed.

### Step-by-Step Instructions

#### Step 3.1: Create `func_PropFrame_SetPipe.py`
- [ ] Create file `scripts/wrappers/func_PropFrame_SetPipe.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_PropFrame_SetPipe.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetPipe
# Category: PropFrame
# Description: Define a circular hollow section (pipe/HSS round)
# Verified: pending
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a circular hollow structural section (pipe/CHS).
       Common for columns, braces, and truss elements.

API Signature:
  SapModel.PropFrame.SetPipe(Name, MatProp, T3, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Outer diameter [L]
  TW      : float — Wall thickness [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# Pipe D=0.3m, t=0.010m
ret = SapModel.PropFrame.SetPipe("PIPE_D300x10", "STEEL_TEST", 0.300, 0.010)
assert ret == 0, f"SetPipe(PIPE_D300x10) failed: {ret}"

# Smaller pipe
ret = SapModel.PropFrame.SetPipe("PIPE_D168x8", "STEEL_TEST", 0.168, 0.008)
assert ret == 0, f"SetPipe(PIPE_D168x8) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "PIPE_D300x10" in section_names, f"PIPE_D300x10 not found in: {section_names}"
assert "PIPE_D168x8" in section_names, f"PIPE_D168x8 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetPipe"
result["sections_created"] = ["PIPE_D300x10", "PIPE_D168x8"]
result["section_count"] = raw[0]
result["status"] = "verified"
```

#### Step 3.2: Create `func_PropFrame_SetChannel.py`
- [ ] Create file `scripts/wrappers/func_PropFrame_SetChannel.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_PropFrame_SetChannel.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetChannel
# Category: PropFrame
# Description: Define a C-shape channel section
# Verified: pending
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a channel (C-shape) cross-section for frame elements.
       Common for purlins, girts, and light structural members.

API Signature:
  SapModel.PropFrame.SetChannel(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Overall depth [L]
  T2      : float — Flange width [L]
  TF      : float — Flange thickness [L]
  TW      : float — Web thickness [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# C250x30 equivalent (approximate dimensions in meters)
ret = SapModel.PropFrame.SetChannel(
    "C250x30", "STEEL_TEST",
    0.254,   # T3 — overall depth
    0.076,   # T2 — flange width
    0.011,   # TF — flange thickness
    0.006    # TW — web thickness
)
assert ret == 0, f"SetChannel(C250x30) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "C250x30" in section_names, f"C250x30 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetChannel"
result["sections_created"] = ["C250x30"]
result["section_count"] = raw[0]
result["status"] = "verified"
```

#### Step 3.3: Create `func_PropFrame_SetAngle.py`
- [ ] Create file `scripts/wrappers/func_PropFrame_SetAngle.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_PropFrame_SetAngle.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetAngle
# Category: PropFrame
# Description: Define an L-shape angle section
# Verified: pending
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates an angle (L-shape) cross-section for frame elements.
       Common for bracing, truss members, and connections.

API Signature:
  SapModel.PropFrame.SetAngle(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Vertical leg depth [L]
  T2      : float — Horizontal leg width [L]
  TF      : float — Flange (horizontal leg) thickness [L]
  TW      : float — Web (vertical leg) thickness [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# L100x100x10 equal angle
ret = SapModel.PropFrame.SetAngle(
    "L100x100x10", "STEEL_TEST",
    0.100,   # T3 — vertical leg
    0.100,   # T2 — horizontal leg
    0.010,   # TF — flange thickness
    0.010    # TW — web thickness
)
assert ret == 0, f"SetAngle(L100x100x10) failed: {ret}"

# L150x75x10 unequal angle
ret = SapModel.PropFrame.SetAngle(
    "L150x75x10", "STEEL_TEST",
    0.150,   # T3
    0.075,   # T2
    0.010,   # TF
    0.010    # TW
)
assert ret == 0, f"SetAngle(L150x75x10) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "L100x100x10" in section_names, f"L100x100x10 not found in: {section_names}"
assert "L150x75x10" in section_names, f"L150x75x10 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetAngle"
result["sections_created"] = ["L100x100x10", "L150x75x10"]
result["section_count"] = raw[0]
result["status"] = "verified"
```

#### Step 3.4: Create `func_PropFrame_SetTee.py`
- [ ] Create file `scripts/wrappers/func_PropFrame_SetTee.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_PropFrame_SetTee.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetTee
# Category: PropFrame
# Description: Define a T-shape section
# Verified: pending
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a T-shape cross-section for frame elements.
       Common for cut W-shapes and composite construction.

API Signature:
  SapModel.PropFrame.SetTee(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Overall depth (stem + flange) [L]
  T2      : float — Flange width [L]
  TF      : float — Flange thickness [L]
  TW      : float — Stem (web) thickness [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# WT155x33 equivalent (cut from W310)
ret = SapModel.PropFrame.SetTee(
    "WT155x33", "STEEL_TEST",
    0.154,   # T3 — overall depth
    0.205,   # T2 — flange width
    0.0154,  # TF — flange thickness
    0.00991  # TW — stem thickness
)
assert ret == 0, f"SetTee(WT155x33) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "WT155x33" in section_names, f"WT155x33 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetTee"
result["sections_created"] = ["WT155x33"]
result["section_count"] = raw[0]
result["status"] = "verified"
```

#### Step 3.5: Create `func_FrameObj_SetReleases.py`
- [ ] Create file `scripts/wrappers/func_FrameObj_SetReleases.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_FrameObj_SetReleases.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetReleases
# Category: Object_Model
# Description: Set end releases (moment releases for hinges)
# Verified: pending
# Prerequisites: Model open, frame element exists
# ============================================================
"""
Usage: Assigns end releases to a frame element. End releases
       convert fixed connections to pinned (moment-released) or
       partially restrained connections at the i-end and j-end.

API Signature:
  SapModel.FrameObj.SetReleases(Name, ii, jj, StartValue, EndValue, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name       : str      — Frame object name
  ii         : bool[6]  — i-end releases [P, V2, V3, T, M2, M3]
                           True=released, False=fixed
  jj         : bool[6]  — j-end releases [P, V2, V3, T, M2, M3]
  StartValue : float[6] — Partial fixity spring values at i-end
                           (0=fully released when ii[k]=True)
  EndValue   : float[6] — Partial fixity spring values at j-end
  ItemType   : int      — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.3)
assert ret == 0

# Portal frame: two columns and one beam
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_TEST", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(6, 0, 0, 6, 0, 3, "", "SEC_TEST", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3, 6, 0, 3, "", "SEC_TEST", "")
beam_name = beam[0]
assert beam[-1] == 0

# --- Target function: pin both ends of beam (release M3) ---
# Release: [P, V2, V3, T, M2, M3]
# Pin = release M3 only (index 5)
ii_release = [False, False, False, False, False, True]  # i-end: release M3
jj_release = [False, False, False, False, False, True]  # j-end: release M3
start_vals = [0, 0, 0, 0, 0, 0]  # fully released (no partial fixity)
end_vals   = [0, 0, 0, 0, 0, 0]

ret = SapModel.FrameObj.SetReleases(
    beam_name, ii_release, jj_release, start_vals, end_vals
)
assert ret == 0, f"SetReleases failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
assert frame_count == 3, f"Expected 3 frames, got {frame_count}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetReleases"
result["frame_name"] = beam_name
result["i_releases"] = ii_release
result["j_releases"] = jj_release
result["status"] = "verified"
```

#### Step 3.6: Create `func_FrameObj_SetEndLengthOffset.py`
- [ ] Create file `scripts/wrappers/func_FrameObj_SetEndLengthOffset.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_FrameObj_SetEndLengthOffset.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetEndLengthOffset
# Category: Object_Model
# Description: Set rigid-zone offsets at beam-column joints
# Verified: pending
# Prerequisites: Model open, frame element exists
# ============================================================
"""
Usage: Assigns rigid-end zone offsets to a frame element. This
       simulates the rigid zone at beam-column intersections where
       the actual flexible length is shorter than the centerline length.

API Signature:
  SapModel.FrameObj.SetEndLengthOffset(Name, AutoOffset, Length1,
      Length2, RzFactor, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name       : str   — Frame object name
  AutoOffset : bool  — True=auto-calculate offsets from connected objects
  Length1    : float — Rigid-zone length at i-end [L] (ignored if AutoOffset=True)
  Length2    : float — Rigid-zone length at j-end [L] (ignored if AutoOffset=True)
  RzFactor   : float — Rigid-zone factor (0-1, typically 0.5 for half-rigid)
  ItemType   : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_50", "CONC_TEST", 0.5, 0.5)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30x60", "CONC_TEST", 0.6, 0.3)
assert ret == 0

# Simple portal
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3.5, "", "COL_50", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(6, 0, 0, 6, 0, 3.5, "", "COL_50", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3.5, 6, 0, 3.5, "", "BEAM_30x60", "")
beam_name = beam[0]
assert beam[-1] == 0

# --- Target function: manual rigid-end offsets ---
# Offset = half column depth = 0.25m at each end, RzFactor=1 (fully rigid)
ret = SapModel.FrameObj.SetEndLengthOffset(
    beam_name, False,  # Not auto
    0.25,   # Length1 (i-end offset)
    0.25,   # Length2 (j-end offset)
    1.0     # RzFactor (fully rigid)
)
assert ret == 0, f"SetEndLengthOffset(manual) failed: {ret}"

# --- Target function: auto offset on column ---
ret = SapModel.FrameObj.SetEndLengthOffset(
    col1[0], True, 0, 0, 0.5  # Auto, half-rigid
)
assert ret == 0, f"SetEndLengthOffset(auto) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetEndLengthOffset"
result["beam_name"] = beam_name
result["manual_offsets"] = [0.25, 0.25]
result["rz_factor"] = 1.0
result["status"] = "verified"
```

#### Step 3.7: Create `func_PropFrame_SetModifiers.py`
- [ ] Create file `scripts/wrappers/func_PropFrame_SetModifiers.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_PropFrame_SetModifiers.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetModifiers
# Category: PropFrame
# Description: Set stiffness modifiers (cracked sections, etc.)
# Verified: pending
# Prerequisites: Model open, frame section defined
# ============================================================
"""
Usage: Assigns section property modifiers to a frame section.
       Commonly used for cracked-section analysis of reinforced
       concrete (e.g., 0.5*Ig for beams, 0.7*Ig for columns).

API Signature:
  SapModel.PropFrame.SetModifiers(Name, Value)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name  : str      — Frame section property name
  Value : float[8] — Modifier array:
                      [0]=Area, [1]=Shear-AS2, [2]=Shear-AS3,
                      [3]=Torsion, [4]=I22, [5]=I33,
                      [6]=Mass, [7]=Weight
                      1.0=no modification, 0.5=50% stiffness, etc.
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30x60", "CONC_TEST", 0.6, 0.3)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_50x50", "CONC_TEST", 0.5, 0.5)
assert ret == 0

# --- Target function: cracked beam (0.5*Ig) ---
# ACI 318: beams 0.35*Ig, columns 0.70*Ig
beam_mods = [1.0, 1.0, 1.0, 1.0, 0.35, 0.35, 1.0, 1.0]
ret = SapModel.PropFrame.SetModifiers("BEAM_30x60", beam_mods)
assert ret == 0, f"SetModifiers(beam) failed: {ret}"

# Cracked columns (0.70*Ig)
col_mods = [1.0, 1.0, 1.0, 1.0, 0.70, 0.70, 1.0, 1.0]
ret = SapModel.PropFrame.SetModifiers("COL_50x50", col_mods)
assert ret == 0, f"SetModifiers(col) failed: {ret}"

# --- Verification ---
# Read back modifiers
raw = SapModel.PropFrame.GetModifiers("BEAM_30x60", [])
ret_code = raw[-1]
assert ret_code == 0, f"GetModifiers failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetModifiers"
result["beam_modifiers"] = beam_mods
result["col_modifiers"] = col_mods
result["status"] = "verified"
```

#### Step 3.8: Execute & Verify All Wrappers
- [ ] Ensure SAP2000 is connected (`connect_sap2000`)
- [ ] Execute each wrapper via `run_sap_script` and verify success:
  - `func_PropFrame_SetPipe` → save as `func_PropFrame_SetPipe`
  - `func_PropFrame_SetChannel` → save as `func_PropFrame_SetChannel`
  - `func_PropFrame_SetAngle` → save as `func_PropFrame_SetAngle`
  - `func_PropFrame_SetTee` → save as `func_PropFrame_SetTee`
  - `func_FrameObj_SetReleases` → save as `func_FrameObj_SetReleases`
  - `func_FrameObj_SetEndLengthOffset` → save as `func_FrameObj_SetEndLengthOffset`
  - `func_PropFrame_SetModifiers` → save as `func_PropFrame_SetModifiers`

#### Step 3.9: Register Functions in Registry
- [ ] Call `register_verified_function` for each of the 7 functions:

**SapModel.PropFrame.SetPipe:**
```json
{
  "function_path": "SapModel.PropFrame.SetPipe",
  "category": "PropFrame",
  "description": "Define a circular hollow section (pipe/HSS round)",
  "signature": "(Name, MatProp, T3, TW, Color, Notes, GUID) -> ret_code",
  "parameter_notes": "Name: str; MatProp: str; T3: float (outer diameter [L]); TW: float (wall thickness [L]); Color: int (-1=default); Notes: str; GUID: str",
  "wrapper_script": "func_PropFrame_SetPipe",
  "notes": "Returns ret_code directly (0=success). Common for CHS columns, braces, and truss elements."
}
```

**SapModel.PropFrame.SetChannel:**
```json
{
  "function_path": "SapModel.PropFrame.SetChannel",
  "category": "PropFrame",
  "description": "Define a C-shape channel section",
  "signature": "(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID) -> ret_code",
  "parameter_notes": "Name: str; MatProp: str; T3: float (overall depth [L]); T2: float (flange width [L]); TF: float (flange thickness [L]); TW: float (web thickness [L]); Color: int; Notes: str; GUID: str",
  "wrapper_script": "func_PropFrame_SetChannel",
  "notes": "Returns ret_code directly (0=success). Common for purlins, girts, light structural members."
}
```

**SapModel.PropFrame.SetAngle:**
```json
{
  "function_path": "SapModel.PropFrame.SetAngle",
  "category": "PropFrame",
  "description": "Define an L-shape angle section",
  "signature": "(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID) -> ret_code",
  "parameter_notes": "Name: str; MatProp: str; T3: float (vertical leg depth [L]); T2: float (horizontal leg width [L]); TF: float (horizontal leg thickness [L]); TW: float (vertical leg thickness [L]); Color: int; Notes: str; GUID: str",
  "wrapper_script": "func_PropFrame_SetAngle",
  "notes": "Returns ret_code directly (0=success). Supports equal and unequal angles."
}
```

**SapModel.PropFrame.SetTee:**
```json
{
  "function_path": "SapModel.PropFrame.SetTee",
  "category": "PropFrame",
  "description": "Define a T-shape section",
  "signature": "(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID) -> ret_code",
  "parameter_notes": "Name: str; MatProp: str; T3: float (overall depth [L]); T2: float (flange width [L]); TF: float (flange thickness [L]); TW: float (stem thickness [L]); Color: int; Notes: str; GUID: str",
  "wrapper_script": "func_PropFrame_SetTee",
  "notes": "Returns ret_code directly (0=success). Common for WT shapes (cut I-sections) and composite construction."
}
```

**SapModel.FrameObj.SetReleases:**
```json
{
  "function_path": "SapModel.FrameObj.SetReleases",
  "category": "Object_Model",
  "description": "Set end releases (moment releases for hinges)",
  "signature": "(Name, ii, jj, StartValue, EndValue, ItemType) -> ret_code",
  "parameter_notes": "Name: str; ii: bool[6] i-end [P,V2,V3,T,M2,M3] True=released; jj: bool[6] j-end; StartValue: float[6] partial fixity springs at i-end (0=fully released); EndValue: float[6] at j-end; ItemType: int (0)",
  "wrapper_script": "func_FrameObj_SetReleases",
  "notes": "Returns ret_code directly (0=success). For simple pin, release M3=[False,False,False,False,False,True]. Use StartValue/EndValue=0 for fully released."
}
```

**SapModel.FrameObj.SetEndLengthOffset:**
```json
{
  "function_path": "SapModel.FrameObj.SetEndLengthOffset",
  "category": "Object_Model",
  "description": "Set rigid-zone offsets at beam-column joints",
  "signature": "(Name, AutoOffset, Length1, Length2, RzFactor, ItemType) -> ret_code",
  "parameter_notes": "Name: str; AutoOffset: bool (True=auto from connected objects); Length1: float (i-end offset [L]); Length2: float (j-end offset [L]); RzFactor: float (0-1, rigid-zone factor, 1=fully rigid, 0.5=half-rigid); ItemType: int (0)",
  "wrapper_script": "func_FrameObj_SetEndLengthOffset",
  "notes": "Returns ret_code directly (0=success). Length1/Length2 ignored when AutoOffset=True."
}
```

**SapModel.PropFrame.SetModifiers:**
```json
{
  "function_path": "SapModel.PropFrame.SetModifiers",
  "category": "PropFrame",
  "description": "Set stiffness modifiers (cracked sections, etc.)",
  "signature": "(Name, Value) -> ret_code",
  "parameter_notes": "Name: str (section name); Value: float[8] [Area, AS2, AS3, Torsion, I22, I33, Mass, Weight] — 1.0=no mod, 0.35=ACI beam, 0.70=ACI column",
  "wrapper_script": "func_PropFrame_SetModifiers",
  "notes": "Returns ret_code directly (0=success). ACI 318: beams 0.35*Ig, columns 0.70*Ig. Array has 8 elements."
}
```

##### Step 3 Verification Checklist
- [ ] All 7 wrappers exist in `scripts/wrappers/`
- [ ] All 7 wrappers executed successfully via `run_sap_script` (status=verified)
- [ ] All 7 functions registered in `registry.json` with full metadata
- [ ] Registry count increased from ~69 to ~76

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
```powershell
git add scripts/wrappers/func_PropFrame_SetPipe.py scripts/wrappers/func_PropFrame_SetChannel.py scripts/wrappers/func_PropFrame_SetAngle.py scripts/wrappers/func_PropFrame_SetTee.py scripts/wrappers/func_FrameObj_SetReleases.py scripts/wrappers/func_FrameObj_SetEndLengthOffset.py scripts/wrappers/func_PropFrame_SetModifiers.py scripts/registry.json
git commit -m "feat: add frame section types (Pipe, Channel, Angle, Tee) and frame releases/offsets/modifiers"
```
