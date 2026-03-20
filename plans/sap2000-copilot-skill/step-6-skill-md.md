# Step 6: SKILL.md — Domain Knowledge

## Goal
Create the SKILL.md and supporting reference files that teach Copilot how to act as a SAP2000 API expert: the mandatory workflow (search docs → check library → generate script → execute → verify → save), script patterns, conventions, and error handling.

## Prerequisites
Steps 1–5 must be committed. All MCP tools must be in place.

### Step-by-Step Instructions

#### Step 6.1: Create the skill directory structure
- [x] Create the following directories:
  - `.github/skills/sap2000-api/`
  - `.github/skills/sap2000-api/references/`

#### Step 6.2: Create the SKILL.md
- [x] Copy and paste code below into `.github/skills/sap2000-api/SKILL.md`:

```markdown
---
name: sap2000-api
description: >-
  Create, execute, and verify SAP2000 API scripts via MCP bridge.
  Use when: writing SAP2000 scripts, creating structural models, assigning loads,
  running analysis, extracting results, debugging API errors, SAP2000 automation,
  structural engineering modeling, frame objects, area objects, load patterns,
  load cases, response combinations, design checks.
  Workflow: search API docs → check script library → generate Python script →
  execute via MCP → verify results → save script.
---

# SAP2000 API Assistant

You are an expert in the SAP2000 structural analysis API. You help users create,
execute, and verify scripts that automate SAP2000 operations via the local COM bridge.

## Mandatory Workflow

**ALWAYS follow this sequence for every SAP2000 task:**

1. **Check connection** — Call `get_model_info` to verify SAP2000 is connected.
   If not connected, call `connect_sap2000` first.
2. **Search for existing scripts** — Call `list_scripts` with a relevant query.
   If a matching script exists, use `load_script` to load it as a starting point.
3. **Search API docs** — Call `search_api_docs` to find the correct functions,
   parameter order, and return value conventions before writing any code.
4. **Generate the script** — Write a complete Python script following the
   patterns described below.
5. **Execute** — Call `run_sap_script` with the script.
6. **Verify** — Read the returned `result`, `stdout`, and `return_value`.
   If `success` is `false`, analyze the error, fix the script, and re-execute.
7. **Save** — When the script succeeds, re-run with `save_as` to store it
   in the script library for future reuse.

## Script Patterns

### Pre-injected Variables

Every script receives these variables automatically — do NOT create them:

```python
SapModel   # cSapModel — the active model reference
SapObject  # cOAPI — the SAP2000 application object
result     # dict — write output values here for verification
```

### Basic Script Template

```python
# Always work through SapModel — it's already connected
ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

# Define materials
ret = SapModel.PropMaterial.SetMaterial("CONC", 2)  # 2 = Concrete
ret = SapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2, 0.0000055)

# Define sections
ret = SapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12)

# Create geometry
ret = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 120, "", "R1", "1")

# Write results for verification
result["return_code"] = ret
result["num_frames"] = SapModel.FrameObj.Count()
```

### Results Extraction Template

```python
# Select the load case for output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

# Get joint displacements — ByRef params returned as tuple
ret = SapModel.Results.JointDispl(
    "1",      # Joint name
    0,        # eItemTypeElm_ObjectElm
    0, [], [], [], [], [], [], [], [], [], []
)
# ret is a tuple: (return_code, NumberResults, Obj[], Elm[], LoadCase[], ...)
result["displacement_U3"] = ret[8][0] if ret[0] == 0 else None
```

## SAP2000 API Conventions

### Return Codes
- **0** = Success
- **Nonzero** = Error — always check `ret` after each call

### ByRef Parameters
SAP2000 uses ByRef (output) parameters extensively. In Python via COM:
- Functions return a **tuple**: `(return_code, param1, param2, ...)`
- The first element is always the return code
- Subsequent elements are the ByRef output parameters

### Unit System
Set units BEFORE creating geometry:
```python
# Common unit enums (pass as integer):
# 1=lb_in_F, 2=lb_ft_F, 3=kip_in_F, 4=kip_ft_F,
# 5=kN_mm_C, 6=kN_m_C, 7=kgf_mm_C, 8=kgf_m_C,
# 9=N_mm_C, 10=N_m_C, 11=Ton_mm_C, 12=Ton_m_C
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
```

### Arrays
- **0-based** arrays in all cases
- When passing arrays to COM, use Python lists
- Dynamic arrays in output: COM fills and returns them in the tuple

### Frame Section Modifiers
Array of 8 values (indices 0–7):
```python
ModValue = [1000, 0, 0, 1, 1, 1, 1, 1]
# [0]=Area, [1]=AS2, [2]=AS3, [3]=Torsion, [4]=I22, [5]=I33, [6]=Mass, [7]=Weight
ret = SapModel.PropFrame.SetModifiers("R1", ModValue)
```

### Material Types (eMatType)
```
1 = Steel
2 = Concrete
3 = NoDesign
4 = Aluminum
5 = ColdFormed
6 = Rebar
7 = Tendon
```

### Load Pattern Types (eLoadPatternType)
```
1 = Dead,  2 = SuperDead,  3 = Live,  4 = ReduceLive
5 = Quake, 6 = Wind,       7 = Snow,  8 = Other
```

### 2D Frame Types (e2DFrameType)
```
0 = PortalFrame
1 = ConcentricBraced
2 = EccentricBraced
```

### 3D Frame Types (e3DFrameType)
```
0 = OpenFrame
1 = PerimeterFrame
2 = BeamSlab
3 = FlatPlate
```

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `return_code != 0` | Invalid parameters or wrong state | Check param types and order via `search_api_docs` |
| `AttributeError: 'NoneType'` | SapModel is None | Connection lost — call `connect_sap2000` |
| `COMError` | COM interface failure | SAP2000 may have crashed — reconnect |
| `Module blocked` | Importing os, subprocess, etc. | Use only allowed modules (math, json, datetime, etc.) |
| `Timeout after 120s` | Analysis taking too long | Simplify model or increase timeout |

## Object Hierarchy

The SAP2000 API is accessed through a hierarchy of objects:

```
SapObject (cOAPI)
├── ApplicationStart()
├── ApplicationExit(save)
├── GetOAPIVersionNumber()
└── SapModel (cSapModel)
    ├── InitializeNewModel()
    ├── SetPresentUnits(units)
    ├── GetPresentUnits()
    ├── File
    │   ├── NewBlank()
    │   ├── New2DFrame(type, stories, height, bays, width)
    │   ├── New3DFrame(type, stories, height, baysX, widthX, baysY, widthY)
    │   ├── Save(path)
    │   └── OpenFile(path)
    ├── PropMaterial
    │   ├── SetMaterial(name, type)
    │   └── SetMPIsotropic(name, E, poisson, thermal)
    ├── PropFrame
    │   ├── SetRectangle(name, material, depth, width)
    │   └── SetModifiers(name, value_array)
    ├── FrameObj
    │   ├── AddByCoord(x1,y1,z1, x2,y2,z2, name, section, group)
    │   ├── GetPoints(name) → (ret, point1, point2)
    │   ├── Count() → int
    │   ├── SetLoadDistributed(name, pattern, type, dir, dist1, dist2, val1, val2)
    │   └── SetLoadPoint(name, pattern, type, dir, dist, val)
    ├── AreaObj
    │   ├── AddByCoord(nPoints, x[], y[], z[], name, prop)
    │   ├── AddByPoint(nPoints, points[], name, prop)
    │   └── Count() → int
    ├── PointObj
    │   ├── SetRestraint(name, restraint_array)
    │   ├── SetLoadForce(name, pattern, value_array)
    │   └── Count() → int
    ├── LoadPatterns
    │   └── Add(name, type, selfMassMultiplier)
    ├── LoadCases
    │   └── ChangeName(old, new)
    ├── RespCombo
    │   └── Add(name, comboType)
    ├── Analyze
    │   ├── RunAnalysis()
    │   ├── CreateAnalysisModel()
    │   └── DeleteResults(name, all)
    ├── Results
    │   ├── Setup
    │   │   ├── DeselectAllCasesAndCombosForOutput()
    │   │   └── SetCaseSelectedForOutput(name)
    │   └── JointDispl(name, itemType, ...) → tuple
    ├── View
    │   └── RefreshView(window, zoom)
    └── SelectObj
        ├── All()
        └── ClearSelection()
```

## Reference Files

For detailed information, load these reference files on demand:
- [API Patterns](./references/api-patterns.md) — Detailed patterns for common operations
- [Common Workflows](./references/common-workflows.md) — Step-by-step workflows for typical tasks
- [Enum Reference](./references/enum-reference.md) — Complete enumeration values
```

#### Step 6.3: Create the API Patterns reference
- [x] Copy and paste code below into `.github/skills/sap2000-api/references/api-patterns.md`:

```markdown
# SAP2000 API Patterns

## Pattern 1: Create Model From Scratch

```python
# 1. Initialize
ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

# 2. Set units FIRST
ret = SapModel.SetPresentUnits(4)  # kip_ft_F

# 3. Define materials
ret = SapModel.PropMaterial.SetMaterial("CONC", 2)
ret = SapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2, 0.0000055)

# 4. Define sections
ret = SapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12)

# 5. Create geometry
ret = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, "", "R1", "1")

# 6. Set restraints
Restraint = [True, True, True, True, False, False]  # Pin support
ret = SapModel.PointObj.SetRestraint("1", Restraint)
```

## Pattern 2: Create From Template

```python
ret = SapModel.InitializeNewModel()
# Portal frame: 3 stories, 12ft height, 3 bays, 28ft width
ret = SapModel.File.New2DFrame(0, 3, 12, 3, 28)  # 0 = PortalFrame
```

## Pattern 3: Assign Loads

```python
# Add load patterns
ret = SapModel.LoadPatterns.Add("DEAD", 1, 1)    # type=1 (Dead), selfweight=1
ret = SapModel.LoadPatterns.Add("LIVE", 3)         # type=3 (Live)

# Point load on a joint
PointLoadValue = [0, 0, -10, 0, 0, 0]   # Fx, Fy, Fz, Mx, My, Mz
ret = SapModel.PointObj.SetLoadForce("3", "LIVE", PointLoadValue)

# Distributed load on a frame
# SetLoadDistributed(name, pattern, myType, dir, dist1, dist2, val1, val2, csys)
# myType: 1=Force, 2=Moment
# dir: 1=Local1, 2=Local2, 3=Local3, ..., 10=GravityProject, 11=ProjectedGlobal
ret = SapModel.FrameObj.SetLoadDistributed("1", "DEAD", 1, 10, 0, 1, 1.8, 1.8)

# Point load on a frame
# SetLoadPoint(name, pattern, myType, dir, dist, val, csys)
ret = SapModel.FrameObj.SetLoadPoint("2", "LIVE", 1, 2, 0.5, -15, "Local")
```

## Pattern 4: Run Analysis & Extract Results

```python
# Save model (required before analysis)
ret = SapModel.File.Save("C:\\temp\\model.sdb")

# Run analysis
ret = SapModel.Analyze.RunAnalysis()

# Setup results output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

# Get joint displacements
ret = SapModel.Results.JointDispl(
    "3", 0,   # joint name, eItemTypeElm_ObjectElm
    0, [], [], [], [], [], [], [], [], [], []
)
# ret = (return_code, NumberResults, Obj[], Elm[], LoadCase[], StepType[],
#        StepNum[], U1[], U2[], U3[], R1[], R2[], R3[])
if ret[0] == 0:
    result["U1"] = ret[7][0]
    result["U2"] = ret[8][0]
    result["U3"] = ret[9][0]
```

## Pattern 5: Frame Object Points

```python
# Get the endpoint joint names of a frame
ret = SapModel.FrameObj.GetPoints("1", "", "")
# ret = (return_code, Point_i_name, Point_j_name)
point_i = ret[1]
point_j = ret[2]
```

## Pattern 6: Area Objects

```python
# Add area by coordinates
x = [0, 10, 10, 0]
y = [0, 0, 0, 0]
z = [0, 0, 10, 10]
ret = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "Default", "", "Global")
# name is returned in ret[1] if ByRef
```
```

#### Step 6.4: Create the Common Workflows reference
- [x] Copy and paste code below into `.github/skills/sap2000-api/references/common-workflows.md`:

```markdown
# Common SAP2000 Workflows

## Workflow 1: Simple Beam Analysis

1. Initialize model → `SapModel.InitializeNewModel()`
2. Create blank model → `SapModel.File.NewBlank()`
3. Set units → `SapModel.SetPresentUnits(4)` (kip_ft_F)
4. Define material → `PropMaterial.SetMaterial` + `SetMPIsotropic`
5. Define section → `PropFrame.SetRectangle`
6. Create beam → `FrameObj.AddByCoord` (one horizontal member)
7. Set supports → `PointObj.SetRestraint` on both ends
8. Add load pattern → `LoadPatterns.Add`
9. Assign loads → `FrameObj.SetLoadDistributed`
10. Save → `File.Save`
11. Run analysis → `Analyze.RunAnalysis`
12. Extract results → `Results.Setup` + `Results.JointDispl`

## Workflow 2: Portal Frame from Template

1. Initialize → `SapModel.InitializeNewModel()`
2. Create from template → `File.New2DFrame(0, stories, height, bays, width)`
3. Assign additional loads if needed
4. Save and run analysis
5. Extract results

## Workflow 3: Verification Problem (Example 1-001)

This is the standard SAP2000 verification problem:

1. Create blank model
2. Define concrete material (E=3600 ksi, ν=0.2, α=0.0000055)
3. Define rectangular frame section (12×12 in)
4. Set section modifiers: Area=1000, AS2=0, AS3=0
5. Switch to kip-ft units
6. Add three frame members by coordinates:
   - Column: (0,0,0) → (0,0,10)
   - Beam: (0,0,10) → (8,0,16)
   - Cantilever: (-4,0,10) → (0,0,10)
7. Set base restraint (fixed: Ux, Uy, Uz, Rx)
8. Set top restraint (roller: Ux, Uy)
9. Add 7 load patterns with various load types
10. Save and run analysis
11. Compare results with hand-calculated values

## Workflow 4: Design Check

1. Create/load model with analysis results
2. Select design code → `DesignSteel.SetCode` or `DesignConcrete.SetCode`
3. Start design → `DesignSteel.StartDesign`
4. Extract design results

## Workflow 5: Modify Existing Model

1. Connect to existing SAP2000 instance → `connect_sap2000(attach_to_existing=True)`
2. Check model state → `get_model_info`
3. Make modifications via script
4. Save → `File.Save`
5. Re-run analysis if needed
```

#### Step 6.5: Create the Enum Reference
- [x] Copy and paste code below into `.github/skills/sap2000-api/references/enum-reference.md`:

```markdown
# SAP2000 Enumeration Reference

## eUnits (Unit Systems)

| Value | Name | Description |
|-------|------|-------------|
| 1 | lb_in_F | Pound, Inch, Fahrenheit |
| 2 | lb_ft_F | Pound, Foot, Fahrenheit |
| 3 | kip_in_F | Kip, Inch, Fahrenheit |
| 4 | kip_ft_F | Kip, Foot, Fahrenheit |
| 5 | kN_mm_C | KiloNewton, Millimeter, Celsius |
| 6 | kN_m_C | KiloNewton, Meter, Celsius |
| 7 | kgf_mm_C | Kilogram-force, Millimeter, Celsius |
| 8 | kgf_m_C | Kilogram-force, Meter, Celsius |
| 9 | N_mm_C | Newton, Millimeter, Celsius |
| 10 | N_m_C | Newton, Meter, Celsius |
| 11 | Ton_mm_C | Metric Ton, Millimeter, Celsius |
| 12 | Ton_m_C | Metric Ton, Meter, Celsius |

## eMatType (Material Types)

| Value | Name |
|-------|------|
| 1 | Steel |
| 2 | Concrete |
| 3 | NoDesign |
| 4 | Aluminum |
| 5 | ColdFormed |
| 6 | Rebar |
| 7 | Tendon |

## eLoadPatternType

| Value | Name |
|-------|------|
| 1 | Dead |
| 2 | SuperDead |
| 3 | Live |
| 4 | ReduceLive |
| 5 | Quake |
| 6 | Wind |
| 7 | Snow |
| 8 | Other |
| 11 | Temperature |
| 12 | Roof Live |
| 13 | Notional |

## e2DFrameType

| Value | Name |
|-------|------|
| 0 | PortalFrame |
| 1 | ConcentricBraced |
| 2 | EccentricBraced |

## e3DFrameType

| Value | Name |
|-------|------|
| 0 | OpenFrame |
| 1 | PerimeterFrame |
| 2 | BeamSlab |
| 3 | FlatPlate |

## eLoadCaseType

| Value | Name |
|-------|------|
| 1 | LinearStatic |
| 2 | NonlinearStatic |
| 3 | Modal |
| 4 | ResponseSpectrum |
| 5 | LinearHistory |
| 6 | NonlinearHistory |
| 7 | LinearDynamic |
| 8 | NonlinearDynamic |
| 9 | MovingLoad |
| 10 | Buckling |
| 11 | SteadyState |
| 12 | PowerSpectralDensity |

## eItemTypeElm

| Value | Name |
|-------|------|
| 0 | ObjectElm |
| 1 | Element |
| 2 | GroupElm |
| 3 | SelectionElm |

## eConstraintType

| Value | Name |
|-------|------|
| 1 | Body |
| 2 | Diaphragm |
| 3 | Plate |
| 4 | Rod |
| 5 | Beam |
| 6 | Equal |
| 7 | Local |
| 13 | Weld |

## eCombType (Combination Types)

| Value | Name |
|-------|------|
| 0 | LinearAdd |
| 1 | Envelope |
| 2 | AbsoluteAdd |
| 3 | SRSS |
| 4 | RangeAdd |
```

##### Step 6 Verification Checklist
- [x] `.github/skills/sap2000-api/SKILL.md` exists with valid YAML frontmatter
- [x] `.github/skills/sap2000-api/references/api-patterns.md` exists
- [x] `.github/skills/sap2000-api/references/common-workflows.md` exists
- [x] `.github/skills/sap2000-api/references/enum-reference.md` exists
- [x] The SKILL.md `name` field matches the folder name: `sap2000-api`
- [x] The `description` field contains trigger keywords for discoverability
- [x] File is under 500 lines (progressive loading compliant)

#### Step 6 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
