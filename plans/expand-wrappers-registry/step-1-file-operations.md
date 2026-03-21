# Step 1: File Operations & Model Templates

## Goal
Add 5 wrapper scripts for missing File operations (`OpenFile`, `New2DFrame`, `New3DFrame`, `NewBeam`, `NewWall`) and register them in `registry.json` with full metadata.

## Prerequisites
Make sure you are on the `expand-wrappers-registry` branch before beginning implementation.
If not, run:
```powershell
git checkout expand-wrappers-registry
```
If the branch does not exist, create it from main:
```powershell
git checkout main; git pull; git checkout -b expand-wrappers-registry
```

### Step-by-Step Instructions

#### Step 1.1: Create `func_File_OpenFile.py`
- [x] Create file `scripts/wrappers/func_File_OpenFile.py`
- [x] Copy and paste code below into `scripts/wrappers/func_File_OpenFile.py`:

```python
# ============================================================
# Wrapper: SapModel.File.OpenFile
# Category: File
# Description: Open an existing .sdb model file by path
# Verified: pending
# Prerequisites: Connected to SAP2000, valid .sdb file path
# ============================================================
"""
Usage: Opens an existing SAP2000 model file. The file must have an
       .sdb, .$2k, .s2k, .xlsx, .xls, or .mdb extension.

API Signature:
  SapModel.File.OpenFile(FileName)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  FileName : str — Full path to the model file
"""
import os
import tempfile

# --- Minimal setup: create a blank model, save it, then re-open ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Create a simple frame so the model isn't empty
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Save model to a temp file
temp_dir = tempfile.gettempdir()
temp_path = os.path.join(temp_dir, "test_open_file.sdb")
ret = SapModel.File.Save(temp_path)
assert ret == 0, f"Save failed: {ret}"

# Now re-initialize and open the saved file
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# --- Target function ---
ret = SapModel.File.OpenFile(temp_path)
assert ret == 0, f"OpenFile failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
assert frame_count >= 1, f"Expected at least 1 frame after open, got {frame_count}"

# --- Result ---
result["function"] = "SapModel.File.OpenFile"
result["file_path"] = temp_path
result["frame_count"] = frame_count
result["status"] = "verified"
```

#### Step 1.2: Create `func_File_New2DFrame.py`
- [x] Create file `scripts/wrappers/func_File_New2DFrame.py`
- [x] Copy and paste code below into `scripts/wrappers/func_File_New2DFrame.py`:

```python
# ============================================================
# Wrapper: SapModel.File.New2DFrame
# Category: File
# Description: Create a 2D portal/braced frame from template
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new 2D frame model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.New2DFrame(TempType, NumberStorys, StoryHeight,
      NumberBays, BayWidth, Restraint, Beam, Column, Brace)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  TempType      : int  — e2DFrameType: 0=PortalFrame, 1=ConcentricBraced, 2=EccentricBraced
  NumberStorys   : int  — Number of stories
  StoryHeight    : float — Height of each story [L]
  NumberBays     : int  — Number of bays
  BayWidth       : float — Width of each bay [L]
  Restraint      : bool — True=add base restraints (default=True)
  Beam           : str  — Beam section name ("Default" or defined section)
  Column         : str  — Column section name ("Default" or defined section)
  Brace          : str  — Brace section name ("Default" or defined section, not for portal)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: Portal frame ---
# 3 stories, 12 ft each, 3 bays, 28 ft each
ret = SapModel.File.New2DFrame(0, 3, 12, 3, 28)
assert ret == 0, f"New2DFrame(Portal) failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
point_count = SapModel.PointObj.Count()
assert frame_count > 0, f"Expected frames in 2D portal, got {frame_count}"
assert point_count > 0, f"Expected points in 2D portal, got {point_count}"

# --- Result ---
result["function"] = "SapModel.File.New2DFrame"
result["template_type"] = "PortalFrame"
result["frame_count"] = frame_count
result["point_count"] = point_count
result["status"] = "verified"
```

#### Step 1.3: Create `func_File_New3DFrame.py`
- [x] Create file `scripts/wrappers/func_File_New3DFrame.py`
- [x] Copy and paste code below into `scripts/wrappers/func_File_New3DFrame.py`:

```python
# ============================================================
# Wrapper: SapModel.File.New3DFrame
# Category: File
# Description: Create a 3D building frame from template
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new 3D frame model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.New3DFrame(TempType, NumberStorys, StoryHeight,
      NumberBaysX, BayWidthX, NumberBaysY, BayWidthY, Restraint,
      Beam, Column, Area, NumberXDivisions, NumberYDivisions)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  TempType        : int  — e3DFrameType: 0=OpenFrame, 1=PerimeterFrame, 2=BeamSlab, 3=FlatPlate
  NumberStorys     : int  — Number of stories
  StoryHeight      : float — Height per story [L]
  NumberBaysX      : int  — Bays in X direction
  BayWidthX        : float — Bay width in X [L]
  NumberBaysY      : int  — Bays in Y direction
  BayWidthY        : float — Bay width in Y [L]
  Restraint        : bool — True=base restraints (default=True)
  Beam             : str  — Beam section ("Default" or defined)
  Column           : str  — Column section ("Default" or defined)
  Area             : str  — Slab shell section ("Default" or defined, for BeamSlab/FlatPlate)
  NumberXDivisions : int  — Slab mesh in X (default=4, for BeamSlab/FlatPlate)
  NumberYDivisions : int  — Slab mesh in Y (default=4, for BeamSlab/FlatPlate)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: BeamSlab 3D frame ---
# 3 stories at 12 ft, 3 bays @ 28 ft in X, 2 bays @ 36 ft in Y
ret = SapModel.File.New3DFrame(2, 3, 12, 3, 28, 2, 36)
assert ret == 0, f"New3DFrame(BeamSlab) failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
point_count = SapModel.PointObj.Count()
area_count = SapModel.AreaObj.Count()
assert frame_count > 0, f"Expected frames in 3D frame, got {frame_count}"
assert point_count > 0, f"Expected points in 3D frame, got {point_count}"
assert area_count > 0, f"Expected areas in BeamSlab, got {area_count}"

# --- Result ---
result["function"] = "SapModel.File.New3DFrame"
result["template_type"] = "BeamSlab"
result["frame_count"] = frame_count
result["point_count"] = point_count
result["area_count"] = area_count
result["status"] = "verified"
```

#### Step 1.4: Create `func_File_NewBeam.py`
- [x] Create file `scripts/wrappers/func_File_NewBeam.py`
- [x] Copy and paste code below into `scripts/wrappers/func_File_NewBeam.py`:

```python
# ============================================================
# Wrapper: SapModel.File.NewBeam
# Category: File
# Description: Create a simply-supported beam template
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new beam model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.NewBeam(NumberSpans, SpanLength, Restraint, Beam)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  NumberSpans : int   — Number of spans
  SpanLength  : float — Length of each span [L]
  Restraint   : bool  — True=add support restraints at span ends (default=True)
  Beam        : str   — Frame section name ("Default" or defined)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: 3-span beam ---
ret = SapModel.File.NewBeam(3, 30)
assert ret == 0, f"NewBeam failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
point_count = SapModel.PointObj.Count()
assert frame_count == 3, f"Expected 3 frames (spans), got {frame_count}"
assert point_count == 4, f"Expected 4 points (supports), got {point_count}"

# --- Result ---
result["function"] = "SapModel.File.NewBeam"
result["num_spans"] = 3
result["frame_count"] = frame_count
result["point_count"] = point_count
result["status"] = "verified"
```

#### Step 1.5: Create `func_File_NewWall.py`
- [x] Create file `scripts/wrappers/func_File_NewWall.py`
- [x] Copy and paste code below into `scripts/wrappers/func_File_NewWall.py`:

```python
# ============================================================
# Wrapper: SapModel.File.NewWall
# Category: File
# Description: Create a shear wall template
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new wall model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.NewWall(NumberXDivisions, DivisionWidthX,
      NumberZDivisions, DivisionWidthZ, Restraint, Area)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  NumberXDivisions : int   — Number of area elements in global X
  DivisionWidthX   : float — Width of each area element in X [L]
  NumberZDivisions : int   — Number of area elements in global Z (height)
  DivisionWidthZ   : float — Height of each area element in Z [L]
  Restraint        : bool  — True=base restraints (default=True)
  Area             : str   — Shell section name ("Default" or defined)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: 6x6 wall ---
ret = SapModel.File.NewWall(6, 4, 6, 4)
assert ret == 0, f"NewWall failed: {ret}"

# --- Verification ---
area_count = SapModel.AreaObj.Count()
point_count = SapModel.PointObj.Count()
assert area_count == 36, f"Expected 36 areas (6x6 grid), got {area_count}"
assert point_count > 0, f"Expected points in wall, got {point_count}"

# --- Result ---
result["function"] = "SapModel.File.NewWall"
result["area_count"] = area_count
result["point_count"] = point_count
result["status"] = "verified"
```

#### Step 1.6: Execute & Verify All Wrappers
- [x] Connect to SAP2000 using `connect_sap2000`
- [x] Execute each wrapper via `run_sap_script` and verify `ret_code == 0`:
  - `run_sap_script` with the content of `func_File_OpenFile.py` → save as `func_File_OpenFile`
  - `run_sap_script` with the content of `func_File_New2DFrame.py` → save as `func_File_New2DFrame`
  - `run_sap_script` with the content of `func_File_New3DFrame.py` → save as `func_File_New3DFrame`
  - `run_sap_script` with the content of `func_File_NewBeam.py` → save as `func_File_NewBeam`
  - `run_sap_script` with the content of `func_File_NewWall.py` → save as `func_File_NewWall`
- [x] Verify all 5 return `"status": "verified"` in the result

#### Step 1.7: Register Functions in Registry
- [x] Call `register_verified_function` for each of the 5 new functions with full metadata:

**SapModel.File.OpenFile:**
```json
{
  "function_path": "SapModel.File.OpenFile",
  "category": "File",
  "description": "Open an existing .sdb model file by path",
  "signature": "(FileName) -> ret_code",
  "parameter_notes": "FileName: str (full path to .sdb, .$2k, .s2k, .xlsx, .xls, or .mdb file)",
  "wrapper_script": "func_File_OpenFile",
  "notes": "Returns ret_code directly (0=success). No ByRef outputs. Only use from external API — not VBA inside SAP2000."
}
```

**SapModel.File.New2DFrame:**
```json
{
  "function_path": "SapModel.File.New2DFrame",
  "category": "File",
  "description": "Create a 2D portal/braced frame from parametric template",
  "signature": "(TempType, NumberStorys, StoryHeight, NumberBays, BayWidth, Restraint, Beam, Column, Brace) -> ret_code",
  "parameter_notes": "TempType: int (0=PortalFrame, 1=ConcentricBraced, 2=EccentricBraced); NumberStorys: int; StoryHeight: float [L]; NumberBays: int; BayWidth: float [L]; Restraint: bool (default=True); Beam: str ('Default' or section name); Column: str ('Default' or section name); Brace: str ('Default' or section name, portal only)",
  "wrapper_script": "func_File_New2DFrame",
  "notes": "Creates new model — do not use to add to existing model. Call InitializeNewModel() first."
}
```

**SapModel.File.New3DFrame:**
```json
{
  "function_path": "SapModel.File.New3DFrame",
  "category": "File",
  "description": "Create a 3D building frame from parametric template",
  "signature": "(TempType, NumberStorys, StoryHeight, NumberBaysX, BayWidthX, NumberBaysY, BayWidthY, Restraint, Beam, Column, Area, NumberXDivisions, NumberYDivisions) -> ret_code",
  "parameter_notes": "TempType: int (0=OpenFrame, 1=PerimeterFrame, 2=BeamSlab, 3=FlatPlate); NumberStorys: int; StoryHeight: float [L]; NumberBaysX: int; BayWidthX: float [L]; NumberBaysY: int; BayWidthY: float [L]; Restraint: bool (True); Beam/Column/Area: str ('Default'); NumberXDivisions/NumberYDivisions: int (4, for BeamSlab/FlatPlate)",
  "wrapper_script": "func_File_New3DFrame",
  "notes": "Creates new model — do not use to add to existing model. Area/Divisions only apply to BeamSlab and FlatPlate types."
}
```

**SapModel.File.NewBeam:**
```json
{
  "function_path": "SapModel.File.NewBeam",
  "category": "File",
  "description": "Create a simply-supported beam template",
  "signature": "(NumberSpans, SpanLength, Restraint, Beam) -> ret_code",
  "parameter_notes": "NumberSpans: int; SpanLength: float [L]; Restraint: bool (default=True); Beam: str ('Default' or section name)",
  "wrapper_script": "func_File_NewBeam",
  "notes": "Creates new model — do not use to add to existing model. Restraints at each span end."
}
```

**SapModel.File.NewWall:**
```json
{
  "function_path": "SapModel.File.NewWall",
  "category": "File",
  "description": "Create a shear wall template from area element grid",
  "signature": "(NumberXDivisions, DivisionWidthX, NumberZDivisions, DivisionWidthZ, Restraint, Area) -> ret_code",
  "parameter_notes": "NumberXDivisions: int; DivisionWidthX: float [L]; NumberZDivisions: int; DivisionWidthZ: float [L]; Restraint: bool (default=True); Area: str ('Default' or shell section name)",
  "wrapper_script": "func_File_NewWall",
  "notes": "Creates new model — do not use to add to existing model. Wall is built as a grid of area elements."
}
```

##### Step 1 Verification Checklist
- [x] All 5 wrappers exist in `scripts/wrappers/`
- [x] All 5 wrappers executed successfully via `run_sap_script` (status=verified)
- [x] All 5 functions registered in `registry.json` with full metadata (category, description, signature, parameter_notes, wrapper_script)
- [x] Registry count increased from 58 to ~63

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
```powershell
git add scripts/wrappers/func_File_OpenFile.py scripts/wrappers/func_File_New2DFrame.py scripts/wrappers/func_File_New3DFrame.py scripts/wrappers/func_File_NewBeam.py scripts/wrappers/func_File_NewWall.py scripts/registry.json
git commit -m "feat: add file operations & model template wrappers (OpenFile, New2DFrame, New3DFrame, NewBeam, NewWall)"
```
