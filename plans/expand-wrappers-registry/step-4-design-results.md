# Step 4: Design & Results Extraction

## Goal
Add 7 wrapper scripts for steel/concrete design startup functions (`DesignSteel.StartDesign`, `DesignConcrete.StartDesign`, `DesignSteel.SetCode`) and analysis results extraction (`Results.FrameForce`, `Results.JointDispl`, `Results.JointReact`, `Results.AreaForceShell`). Register all in `registry.json`.

## Prerequisites
Make sure you are on the `expand-wrappers-registry` branch and Steps 1-3 are committed.

### Step-by-Step Instructions

#### Step 4.1: Create `func_DesignSteel_StartDesign.py`
- [ ] Create file `scripts/wrappers/func_DesignSteel_StartDesign.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_DesignSteel_StartDesign.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.StartDesign
# Category: Design
# Description: Run steel frame design check
# Verified: pending
# Prerequisites: Model analyzed, steel design code set
# ============================================================
"""
Usage: Starts the steel frame design procedure. The model must
       be analyzed first. The steel design code should be set
       before calling this function.

API Signature:
  SapModel.DesignSteel.StartDesign() -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  (none)
"""

# --- Minimal setup (portal frame for design) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites: steel material & section ---
ret = SapModel.PropMaterial.SetMaterial("A992Fy50", 1)  # Steel
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("A992Fy50", 2.0e8, 0.3, 1.2e-5)
assert ret == 0
ret = SapModel.PropFrame.SetISection(
    "W310x97", "A992Fy50",
    0.308, 0.305, 0.0154, 0.00991, 0.305, 0.0154  # d, bf, tf, tw, bfb, tfb
)
assert ret == 0

# Simple portal: 2 columns + 1 beam
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 4, "", "W310x97", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(8, 0, 0, 8, 0, 4, "", "W310x97", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 4, 8, 0, 4, "", "W310x97", "")
assert beam[-1] == 0

# Supports: pin bases
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, True, True, True])
assert ret == 0

# Load pattern (dead already exists, add live)
ret = SapModel.LoadPatterns.Add("LIVE", 3)  # 3=Live
assert ret == 0

# Distributed load on beam
ret = SapModel.FrameObj.SetLoadDistributed(
    beam[0], "DEAD", 1, 10, 0, 1, -10, -10, "Global", True, True
)
assert ret == 0

# Set steel design code
ret = SapModel.DesignSteel.SetCode("AISC 360-16")
assert ret == 0

# Analyze model
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# --- Target function ---
ret = SapModel.DesignSteel.StartDesign()
assert ret == 0, f"DesignSteel.StartDesign failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.StartDesign"
result["design_code"] = "AISC 360-16"
result["status"] = "verified"
```

#### Step 4.2: Create `func_DesignConcrete_StartDesign.py`
- [ ] Create file `scripts/wrappers/func_DesignConcrete_StartDesign.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_DesignConcrete_StartDesign.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignConcrete.StartDesign
# Category: Design
# Description: Run concrete frame design check
# Verified: pending
# Prerequisites: Model analyzed, concrete design code set
# ============================================================
"""
Usage: Starts the concrete frame design procedure. The model must
       be analyzed first. The concrete design code should be set
       before calling this function.

API Signature:
  SapModel.DesignConcrete.StartDesign() -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  (none)
"""

# --- Minimal setup (portal frame for design) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites: concrete material & section ---
ret = SapModel.PropMaterial.SetMaterial("CONC28", 2)  # 2=Concrete
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC28", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("COL_40x40", "CONC28", 0.4, 0.4)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30x50", "CONC28", 0.5, 0.3)
assert ret == 0

# Simple portal: 2 columns + 1 beam
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "COL_40x40", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(5, 0, 0, 5, 0, 3, "", "COL_40x40", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30x50", "")
assert beam[-1] == 0

# Supports: fixed bases
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, True, True, True])
assert ret == 0

# Gravity load on beam
ret = SapModel.FrameObj.SetLoadDistributed(
    beam[0], "DEAD", 1, 10, 0, 1, -15, -15, "Global", True, True
)
assert ret == 0

# Set concrete design code
ret = SapModel.DesignConcrete.SetCode("ACI 318-19")
assert ret == 0

# Analyze model
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# --- Target function ---
ret = SapModel.DesignConcrete.StartDesign()
assert ret == 0, f"DesignConcrete.StartDesign failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignConcrete.StartDesign"
result["design_code"] = "ACI 318-19"
result["status"] = "verified"
```

#### Step 4.3: Create `func_DesignSteel_SetCode.py`
- [ ] Create file `scripts/wrappers/func_DesignSteel_SetCode.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_DesignSteel_SetCode.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.SetCode
# Category: Design
# Description: Set the steel design code for the model
# Verified: pending
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets the steel frame design code used for design checks.
       Must be called before running steel design (StartDesign).

API Signature:
  SapModel.DesignSteel.SetCode(CodeName) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  CodeName : str — Design code name (e.g., "AISC 360-16",
                   "EN 1993-1-1:2005", "BS 5950-2000", "CSA S16-19")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# --- Target function ---
# Set AISC 360-16
ret = SapModel.DesignSteel.SetCode("AISC 360-16")
assert ret == 0, f"SetCode(AISC 360-16) failed: {ret}"

# Verify: read back code
raw = SapModel.DesignSteel.GetCode("")
ret_code = raw[-1]
assert ret_code == 0, f"GetCode failed: {ret_code}"
code_name = raw[0]
assert "AISC" in code_name, f"Expected AISC code, got: {code_name}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetCode"
result["code_set"] = "AISC 360-16"
result["code_read_back"] = code_name
result["status"] = "verified"
```

#### Step 4.4: Create `func_Results_FrameForce.py`
- [ ] Create file `scripts/wrappers/func_Results_FrameForce.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_Results_FrameForce.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.FrameForce
# Category: Analysis_Results
# Description: Extract frame element internal forces
# Verified: pending
# Prerequisites: Model analyzed
# ============================================================
"""
Usage: Extracts internal forces (P, V2, V3, T, M2, M3) for a
       given frame element after analysis. Results are returned at
       multiple stations along the element length.

API Signature:
  SapModel.Results.FrameForce(Name, ItemTypeElm,
      NumberResults, Obj, ObjSta, Elm, ElmSta,
      LoadCase, StepType, StepNum,
      P, V2, V3, T, M2, M3) -> ret_code

ByRef Output (14 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — object names
  ObjSta[]      : float[] — station distances on object
  Elm[]         : str[]   — element names
  ElmSta[]      : float[] — station distances on element
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  P[]           : float[] — axial force
  V2[]          : float[] — shear in local-2
  V3[]          : float[] — shear in local-3
  T[]           : float[] — torsion
  M2[]          : float[] — moment about local-2
  M3[]          : float[] — moment about local-3

Parameters:
  Name        : str — Frame name (or "All" for all frames)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: simple beam with uniform load ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 6m span
beam = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = beam[0]
assert beam[-1] == 0

# Supports (pin-roller)
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret == 0

# Uniform load -10 kN/m on beam (gravity direction)
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -10, -10, "Global", True, True
)
assert ret == 0

# Analyze
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# Set results for DEAD case
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.FrameForce(
    beam_name, 0,     # ObjectElm
    0, [], [], [], [], [], [], [],   # ByRef placeholders
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"FrameForce failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No results returned"

obj_names   = list(raw[1])
obj_sta     = list(raw[2])
load_cases  = list(raw[5])
P_values    = list(raw[8])
V2_values   = list(raw[9])
M3_values   = list(raw[13])

# --- Result ---
result["function"] = "SapModel.Results.FrameForce"
result["frame_name"] = beam_name
result["num_results"] = num_results
result["sample_stations"] = obj_sta[:5]
result["sample_M3"] = M3_values[:5]
result["sample_V2"] = V2_values[:5]
result["status"] = "verified"
```

#### Step 4.5: Create `func_Results_JointDispl.py`
- [ ] Create file `scripts/wrappers/func_Results_JointDispl.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_Results_JointDispl.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.JointDispl
# Category: Analysis_Results
# Description: Extract joint displacements (translations/rotations)
# Verified: pending
# Prerequisites: Model analyzed
# ============================================================
"""
Usage: Extracts joint displacement results (U1, U2, U3, R1, R2, R3)
       after analysis. Returns translations and rotations for each
       joint and load case.

API Signature:
  SapModel.Results.JointDispl(Name, ItemTypeElm,
      NumberResults, Obj, Elm,
      LoadCase, StepType, StepNum,
      U1, U2, U3, R1, R2, R3) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — joint object names
  Elm[]         : str[]   — joint element names
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  U1[]          : float[] — translation in global-X [L]
  U2[]          : float[] — translation in global-Y [L]
  U3[]          : float[] — translation in global-Z [L]
  R1[]          : float[] — rotation about global-X [rad]
  R2[]          : float[] — rotation about global-Y [rad]
  R3[]          : float[] — rotation about global-Z [rad]

Parameters:
  Name        : str — Joint name ("All" for all joints)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: cantilever with point load ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("CANT_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Cantilever beam, 4m long
beam = SapModel.FrameObj.AddByCoord(0, 0, 0, 4, 0, 0, "", "CANT_SEC", "")
assert beam[-1] == 0

# Fixed support at node 1
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret == 0

# Point load at free end (node 2): -50 kN in Z
ret = SapModel.PointObj.SetLoadForce("2", "DEAD", [0, 0, -50, 0, 0, 0])
assert ret == 0

# Analyze
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# Set output selection
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.JointDispl(
    "All", 0,    # All joints, ObjectElm
    0, [], [],   # ByRef: NumberResults, Obj, Elm
    [], [], [],  # ByRef: LoadCase, StepType, StepNum
    [], [], [], [], [], []  # ByRef: U1..R3
)
ret_code = raw[-1]
assert ret_code == 0, f"JointDispl failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No displacement results"

obj_names  = list(raw[1])
load_cases = list(raw[3])
U1_values  = list(raw[6])
U2_values  = list(raw[7])
U3_values  = list(raw[8])

# --- Result ---
result["function"] = "SapModel.Results.JointDispl"
result["num_results"] = num_results
result["joint_names"] = obj_names
result["U3_values"] = U3_values
result["status"] = "verified"
```

#### Step 4.6: Create `func_Results_JointReact.py`
- [ ] Create file `scripts/wrappers/func_Results_JointReact.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_Results_JointReact.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.JointReact
# Category: Analysis_Results
# Description: Extract joint reactions (forces/moments at supports)
# Verified: pending
# Prerequisites: Model analyzed, joints with restraints
# ============================================================
"""
Usage: Extracts joint reaction forces and moments (F1, F2, F3, M1, M2, M3)
       at restrained joints after analysis.

API Signature:
  SapModel.Results.JointReact(Name, ItemTypeElm,
      NumberResults, Obj, Elm,
      LoadCase, StepType, StepNum,
      F1, F2, F3, M1, M2, M3) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — joint object names
  Elm[]         : str[]   — joint element names
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  F1[]          : float[] — reaction force global-X [F]
  F2[]          : float[] — reaction force global-Y [F]
  F3[]          : float[] — reaction force global-Z [F]
  M1[]          : float[] — reaction moment about global-X [F·L]
  M2[]          : float[] — reaction moment about global-Y [F·L]
  M3[]          : float[] — reaction moment about global-Z [F·L]

Parameters:
  Name        : str — Joint name ("All" for all restrained joints)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: simply supported beam ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SS_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 8m span
beam = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "SS_SEC", "")
assert beam[-1] == 0

# Pin-roller supports
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret == 0

# Uniform downward load -20 kN/m
ret = SapModel.FrameObj.SetLoadDistributed(
    beam[0], "DEAD", 1, 10, 0, 1, -20, -20, "Global", True, True
)
assert ret == 0

# Analyze
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# Set output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.JointReact(
    "All", 0,
    0, [], [],
    [], [], [],
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"JointReact failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No reaction results"

obj_names  = list(raw[1])
load_cases = list(raw[3])
F1_values  = list(raw[6])
F2_values  = list(raw[7])
F3_values  = list(raw[8])

# Sanity check: total vertical reaction ≈ w*L = 20*8 = 160 kN
total_F3 = sum(F3_values)

# --- Result ---
result["function"] = "SapModel.Results.JointReact"
result["num_results"] = num_results
result["joint_names"] = obj_names
result["F3_values"] = F3_values
result["total_vertical_reaction"] = total_F3
result["expected_total"] = 160.0
result["status"] = "verified"
```

#### Step 4.7: Create `func_Results_AreaForceShell.py`
- [ ] Create file `scripts/wrappers/func_Results_AreaForceShell.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_Results_AreaForceShell.py`:

```python
# ============================================================
# Wrapper: SapModel.Results.AreaForceShell
# Category: Analysis_Results
# Description: Extract shell element forces and moments
# Verified: pending
# Prerequisites: Model analyzed, area (shell) elements exist
# ============================================================
"""
Usage: Extracts shell forces and moments (F11, F22, F12, M11, M22, M12,
       V13, V23, etc.) for area elements. Results are per unit width.

API Signature:
  SapModel.Results.AreaForceShell(Name, ItemTypeElm,
      NumberResults, Obj, Elm,
      PointElm, LoadCase, StepType, StepNum,
      F11, F22, F12, FMax, FMin, FAngle, FVM,
      M11, M22, M12, MMax, MMin, MAngle,
      V13, V23, VMax, VAngle) -> ret_code

ByRef Output (25 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — area object names
  Elm[]         : str[]   — area element names
  PointElm[]    : str[]   — point element names at corners
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  F11[]..VAngle[]: float[] — force/moment result arrays

Parameters:
  Name        : str — Area name ("All" for all)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: simple slab ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material
ret = SapModel.PropMaterial.SetMaterial("CONC_SLAB", 2)  # Concrete
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_SLAB", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

# Shell section (150mm slab)
ret = SapModel.PropArea.SetShell_1("SLAB_150", 1, False, "CONC_SLAB", 0, 0.150, 0.150)
assert ret == 0

# Create a 4x4m slab (single area)
area = SapModel.AreaObj.AddByCoord(
    4,  # NumPoints
    [0, 4, 4, 0],   # X
    [0, 0, 4, 4],   # Y
    [0, 0, 0, 0],   # Z
    "", "SLAB_150"
)
assert area[-1] == 0

# Restraints at all four corners (supported slab)
for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret == 0, f"Restraint at node {i} failed: {ret}"

# Uniform area load
ret = SapModel.AreaObj.SetLoadUniform(area[0], "DEAD", -5, 10, True, "Global")
assert ret == 0

# Analyze
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# Set output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.AreaForceShell(
    "All", 0,
    0, [], [], [],     # NumberResults, Obj, Elm, PointElm
    [], [], [],        # LoadCase, StepType, StepNum
    [], [], [], [], [], [], [],   # F11..FVM
    [], [], [], [], [], [],       # M11..MAngle
    [], [], [], []                # V13, V23, VMax, VAngle
)
ret_code = raw[-1]
assert ret_code == 0, f"AreaForceShell failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No shell results returned"

# --- Result ---
result["function"] = "SapModel.Results.AreaForceShell"
result["num_results"] = num_results
result["status"] = "verified"
```

#### Step 4.8: Execute & Verify All Wrappers
- [ ] Ensure SAP2000 is connected (`connect_sap2000`)
- [ ] Execute each wrapper via `run_sap_script` and verify success:
  - `func_DesignSteel_StartDesign` → save as `func_DesignSteel_StartDesign`
  - `func_DesignConcrete_StartDesign` → save as `func_DesignConcrete_StartDesign`
  - `func_DesignSteel_SetCode` → save as `func_DesignSteel_SetCode`
  - `func_Results_FrameForce` → save as `func_Results_FrameForce`
  - `func_Results_JointDispl` → save as `func_Results_JointDispl`
  - `func_Results_JointReact` → save as `func_Results_JointReact`
  - `func_Results_AreaForceShell` → save as `func_Results_AreaForceShell`

#### Step 4.9: Register Functions in Registry
- [ ] Call `register_verified_function` for each of the 7 functions:

**SapModel.DesignSteel.StartDesign:**
```json
{
  "function_path": "SapModel.DesignSteel.StartDesign",
  "category": "Design",
  "description": "Run steel frame design check",
  "signature": "() -> ret_code",
  "parameter_notes": "No parameters. Model must be analyzed first and steel code set.",
  "wrapper_script": "func_DesignSteel_StartDesign",
  "notes": "Returns ret_code (0=success). Requires Analyze.RunAnalysis first. Set code with DesignSteel.SetCode before calling."
}
```

**SapModel.DesignConcrete.StartDesign:**
```json
{
  "function_path": "SapModel.DesignConcrete.StartDesign",
  "category": "Design",
  "description": "Run concrete frame design check",
  "signature": "() -> ret_code",
  "parameter_notes": "No parameters. Model must be analyzed first and concrete code set.",
  "wrapper_script": "func_DesignConcrete_StartDesign",
  "notes": "Returns ret_code (0=success). Requires Analyze.RunAnalysis first. Set code with DesignConcrete.SetCode before calling."
}
```

**SapModel.DesignSteel.SetCode:**
```json
{
  "function_path": "SapModel.DesignSteel.SetCode",
  "category": "Design",
  "description": "Set the steel design code for the model",
  "signature": "(CodeName) -> ret_code",
  "parameter_notes": "CodeName: str — e.g., 'AISC 360-16', 'EN 1993-1-1:2005', 'BS 5950-2000', 'CSA S16-19'",
  "wrapper_script": "func_DesignSteel_SetCode",
  "notes": "Returns ret_code (0=success). Use GetCode to verify. Pair with: DesignSteel.StartDesign."
}
```

**SapModel.Results.FrameForce:**
```json
{
  "function_path": "SapModel.Results.FrameForce",
  "category": "Analysis_Results",
  "description": "Extract frame element internal forces (P, V2, V3, T, M2, M3)",
  "signature": "(Name, ItemTypeElm, NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3) -> ret_code",
  "parameter_notes": "Name: str (frame name or 'All'); ItemTypeElm: int (0=Object); 14 ByRef arrays returned: NumberResults, Obj[], ObjSta[], Elm[], ElmSta[], LoadCase[], StepType[], StepNum[], P[], V2[], V3[], T[], M2[], M3[]",
  "wrapper_script": "func_Results_FrameForce",
  "notes": "Call Results.Setup.SetCaseSelectedForOutput before extracting. ret_code=raw[-1], num_results=raw[0], P=raw[8], V2=raw[9], V3=raw[10], T=raw[11], M2=raw[12], M3=raw[13]"
}
```

**SapModel.Results.JointDispl:**
```json
{
  "function_path": "SapModel.Results.JointDispl",
  "category": "Analysis_Results",
  "description": "Extract joint displacements (translations and rotations)",
  "signature": "(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3) -> ret_code",
  "parameter_notes": "Name: str (joint name or 'All'); ItemTypeElm: int (0=Object); 12 ByRef: NumberResults, Obj[], Elm[], LoadCase[], StepType[], StepNum[], U1[], U2[], U3[], R1[], R2[], R3[]",
  "wrapper_script": "func_Results_JointDispl",
  "notes": "Call Results.Setup.SetCaseSelectedForOutput first. ret_code=raw[-1], U1=raw[6], U2=raw[7], U3=raw[8], R1=raw[9], R2=raw[10], R3=raw[11]"
}
```

**SapModel.Results.JointReact:**
```json
{
  "function_path": "SapModel.Results.JointReact",
  "category": "Analysis_Results",
  "description": "Extract joint reactions at supports",
  "signature": "(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3) -> ret_code",
  "parameter_notes": "Name: str (joint name or 'All'); ItemTypeElm: int (0=Object); 12 ByRef: NumberResults, Obj[], Elm[], LoadCase[], StepType[], StepNum[], F1[], F2[], F3[], M1[], M2[], M3[]",
  "wrapper_script": "func_Results_JointReact",
  "notes": "Call Results.Setup.SetCaseSelectedForOutput first. ret_code=raw[-1], F1=raw[6], F2=raw[7], F3=raw[8], M1=raw[9], M2=raw[10], M3=raw[11]"
}
```

**SapModel.Results.AreaForceShell:**
```json
{
  "function_path": "SapModel.Results.AreaForceShell",
  "category": "Analysis_Results",
  "description": "Extract shell element forces and moments",
  "signature": "(Name, ItemTypeElm, NumberResults, Obj, Elm, PointElm, LoadCase, StepType, StepNum, F11, F22, F12, FMax, FMin, FAngle, FVM, M11, M22, M12, MMax, MMin, MAngle, V13, V23, VMax, VAngle) -> ret_code",
  "parameter_notes": "Name: str (area name or 'All'); ItemTypeElm: int (0=Object); 25 ByRef outputs including membrane forces (F11,F22,F12), bending moments (M11,M22,M12), shear (V13,V23), and principal values (FMax,FMin,MMax,MMin,VMax)",
  "wrapper_script": "func_Results_AreaForceShell",
  "notes": "Call Results.Setup.SetCaseSelectedForOutput first. ret_code=raw[-1], num_results=raw[0]. Results at each corner of each element."
}
```

##### Step 4 Verification Checklist
- [ ] All 7 wrappers exist in `scripts/wrappers/`
- [ ] All 7 wrappers executed successfully via `run_sap_script` (status=verified)
- [ ] All 7 functions registered in `registry.json` with full metadata
- [ ] Registry count increased from ~76 to ~83

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
```powershell
git add scripts/wrappers/func_DesignSteel_StartDesign.py scripts/wrappers/func_DesignConcrete_StartDesign.py scripts/wrappers/func_DesignSteel_SetCode.py scripts/wrappers/func_Results_FrameForce.py scripts/wrappers/func_Results_JointDispl.py scripts/wrappers/func_Results_JointReact.py scripts/wrappers/func_Results_AreaForceShell.py scripts/registry.json
git commit -m "feat: add design startup/code and analysis results extraction wrappers"
```
