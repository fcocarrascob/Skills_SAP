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
2. **Check function registry** — Call `query_function_registry` with the function
   name or a keyword query to see if the needed functions have already been
   verified.
3. **Load wrapper scripts** — If a `wrapper_script` field exists in the registry
   entry, call `load_script("func_...")` and **copy the exact call signature,
   argument order, and ByRef pattern from the wrapper**. The wrapper is the
   authoritative source of truth — it has been tested against the live COM bridge.
4. **Search for existing full scripts** — Call `list_scripts` with a relevant
   query. If a matching script exists, use `load_script` to load it as a starting point.
5. **Search API docs (FALLBACK ONLY)** — Call `search_api_docs` ONLY for
   functions that have **no wrapper script** and are **not in the registry**.
   API documentation describes the VBA interface and may differ from the
   Python COM bridge behaviour (argument count, order, ByRef layout).
   **Never override a verified wrapper with an API doc signature.**
6. **Generate the script** — Write a complete Python script following the
   patterns described below. For every function that has a wrapper, copy the
   call exactly from the wrapper — do not invent or reorder arguments.

> ⚠️ **WRAPPER PRIORITY RULE — NON-NEGOTIABLE:**
> When a verified wrapper exists for a function, it is the ONLY valid
> reference for that function's argument list, order, and return-value layout.
> API documentation is a secondary fallback used exclusively for functions
> with no wrapper. Mixing API doc signatures with wrapper-verified calls
> will introduce argument-count or ordering bugs that are hard to diagnose.
6. **Execute** — Call `run_sap_script` with the script. On success, any new
   API functions used are automatically registered in the function registry.
7. **Verify** — Read the returned `result`, `stdout`, and `return_value`.
   If `success` is `false`, analyze the error, fix the script, and re-execute.
8. **Save** — When the script succeeds, re-run with `save_as` to store it
   in the script library for future reuse.
9. **Register new functions** — For any new API functions not yet in the
   registry, call `register_verified_function` to add full metadata
   (category, description, parameter notes). Auto-registration captures
   the function path, but manual registration adds richer documentation.

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
# AddByCoord returns [Name_out, ret_code] — Name is raw[0], ret_code is raw[-1]
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 120, "", "R1", "1")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Write results for verification
result["frame_name"] = frame_name
result["num_frames"] = SapModel.FrameObj.Count()
```

### Results Extraction Template

```python
# Select the load case for output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

# Get joint displacements — ByRef params come first, ret_code is LAST
raw = SapModel.Results.JointDispl(
    "1",      # Joint name
    0,        # eItemTypeElm_ObjectElm
    0, [], [], [], [], [], [], [], [], [], []
)
# raw layout: [NumberResults, Obj[], Elm[], LoadCase[], StepType[], StepNum[],
#              U1[], U2[], U3[], R1[], R2[], R3[], ret_code]
# ret_code is always raw[-1]
ret_code = raw[-1]
result["displacement_U3"] = raw[8][0] if ret_code == 0 and len(raw[8]) > 0 else None
```

## Function Registry

The function registry (`scripts/registry.json`) tracks which API functions
have been successfully tested. Use it to avoid re-discovering function
signatures and ByRef conventions from scratch.

### Querying the Registry

```python
# Check if a specific function has been verified:
query_function_registry(function_path="SapModel.FrameObj.AddByCoord")
# → {function_path, category, description, verified, wrapper_script, ...}

# Search by keyword:
query_function_registry(query="frame")
# → {count, functions: [{function_path, category, verified, ...}, ...]}

# List verified functions only:
query_function_registry(verified_only=True)

# Get registry summary:
query_function_registry()
# → {total_registered, total_verified, categories: {...}}
```

### Wrapper Scripts

Verified functions have wrapper scripts in `scripts/wrappers/` that demonstrate
correct usage. Each wrapper:
- Targets a single API function
- Is self-contained (initializes a fresh model)
- Documents the ByRef output layout
- Asserts success and writes to `result`

> **The wrapper is the single source of truth for that function.**
> The argument count, argument order, and return-value layout shown in the
> wrapper have been verified against the live SAP2000 COM bridge.
> API documentation describes the VBA interface and can differ — e.g.,
> `GetTCLimits` takes 5 args in Python (no `ItemType`), `EditArea.Divide`
> takes 18 args (no trailing `SubMesh`/`SubMeshSize`), and
> `SelectObj.CoordinateRange` takes coordinates first and `CSys` last.

**Workflow for using a wrapper:**
1. Call `query_function_registry(function_path="SapModel.X.Y")` — check `wrapper_script`.
2. If wrapper exists: call `load_script("func_X_Y")` and copy the call verbatim.
3. Only if no wrapper: consult `search_api_docs` and mark as unverified.

```
load_script("func_FrameObj_AddByCoord")
```

### Auto-Registration

When a script executes successfully via `run_sap_script`, all SAP2000 API
functions called in the script are automatically detected and registered
as verified in the registry. The response includes a `registered_functions`
list showing what was captured.

## SAP2000 API Conventions

### Return Codes
- **0** = Success
- **Nonzero** = Error — always check `ret` after each call

### ByRef Parameters
SAP2000 uses ByRef (output) parameters extensively. In Python via COM:
- Functions return a **list**: `[byref_output1, byref_output2, ..., return_code]`
- The **last element `[-1]` is ALWAYS the return code** (Long)
- All ByRef output parameters come **before** the return code

> **CRITICAL:** This is the opposite of what the VBA signature suggests.
> The COM bridge in Python always places the `Long` return code at the end.

```python
# Example: AddCartesian returns [Name_out, ret_code]
raw = SapModel.PointObj.AddCartesian(5, 3, 2, "", "PT1")
point_name = raw[0]   # ByRef Name output (first)
ret_code   = raw[-1]  # return code (last)
assert ret_code == 0, f"AddCartesian failed: {ret_code}"

# Example: GetCoordCartesian returns [x, y, z, ret_code]
coord = SapModel.PointObj.GetCoordCartesian(point_name, 0, 0, 0)
x, y, z = coord[0], coord[1], coord[2]
ret_code = coord[-1]

# Example: FrameObj.GetPoints returns [pt_i, pt_j, ret_code]
raw = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i = raw[0]
pt_j = raw[1]
ret_code = raw[-1]
```

**Safe pattern to always use:**
```python
raw = SapModel.SomeObj.SomeFunction(...)
ret_code = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret_code == 0, f"SomeFunction failed: {ret_code}"
```

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
    │   ├── GetPoints(name) → [point1, point2, ret_code]
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
    │   └── JointDispl(name, itemType, ...) → [NRes, Obj[], Elm[], LC[], StType[], StNum[], U1[], U2[], U3[], R1[], R2[], R3[], ret_code]
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
