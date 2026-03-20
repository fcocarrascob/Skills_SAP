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
