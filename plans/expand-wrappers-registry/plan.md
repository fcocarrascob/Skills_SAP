# Expand Wrappers & Registry with Missing API Functions

**Branch:** `expand-wrappers-registry`
**Description:** Add ~30 new wrapper scripts and enrich registry.json with critical missing SAP2000 API functions across file operations, loading, sections, design, results, and groups.

## Goal
The current skill has 58 registered functions and 26 wrapper scripts, but ~50+ important API functions are missing — particularly in design, load assignment, frame releases, additional section types, results extraction, and groups. This plan fills the most impactful gaps in 5 commits, enabling complete modeling → analysis → design → results workflows.

## Current State
- **Registry:** 58 functions (all verified)
- **Wrappers:** 26 scripts in `scripts/wrappers/`
- **Key gaps:** File.Open, New2D/3DFrame, frame releases, point/distributed/area loads (wrappers), design start, area results, groups, additional section types (Pipe, Channel, Angle), database tables

---

## Implementation Steps

### Step 1: File Operations & Model Templates
**Files:** `scripts/wrappers/func_File_OpenFile.py`, `func_File_New2DFrame.py`, `func_File_New3DFrame.py`, `func_File_NewBeam.py`, `func_File_NewWall.py`, `scripts/registry.json`
**What:** Create wrapper scripts for the 5 missing File operations — these are the entry points for any workflow. `OpenFile` loads existing models, `New2DFrame`/`New3DFrame` generate parametric templates, `NewBeam` and `NewWall` add quick-start templates.
**Functions (5):**
| Function | Priority | Description |
|----------|----------|-------------|
| `SapModel.File.OpenFile` | Critical | Open existing .sdb model by path |
| `SapModel.File.New2DFrame` | Critical | Create 2D portal/braced frame from template |
| `SapModel.File.New3DFrame` | Critical | Create 3D building frame from template |
| `SapModel.File.NewBeam` | Important | Create simply-supported beam template |
| `SapModel.File.NewWall` | Important | Create shear wall template |
**Testing:** Execute each wrapper via `run_sap_script` in SAP2000 → verify `ret_code == 0` and model is created → auto-register in registry → manually enrich registry metadata (category, description, signature, parameter_notes)

---

### Step 2: Load Assignment Wrappers (Frame, Point, Area Loads)
**Files:** `scripts/wrappers/func_PointObj_SetLoadForce.py`, `func_FrameObj_SetLoadDistributed.py`, `func_FrameObj_SetLoadPoint.py`, `func_AreaObj_SetLoadUniform.py`, `func_AreaObj_SetLoadGravity.py`, `func_FrameObj_SetLoadTemperature.py`, `scripts/registry.json`
**What:** Create wrappers for the core load-application functions. `PointObj.SetLoadForce` already exists in registry but needs a wrapper. `FrameObj.SetLoadDistributed` is registered but needs a dedicated wrapper. Add `FrameObj.SetLoadPoint`, `AreaObj.SetLoadUniform`, `AreaObj.SetLoadGravity`, and `FrameObj.SetLoadTemperature`.
**Functions (6):**
| Function | Priority | Description |
|----------|----------|-------------|
| `SapModel.PointObj.SetLoadForce` | Critical | Apply forces/moments at joints (6 DOF) |
| `SapModel.FrameObj.SetLoadDistributed` | Critical | Uniform/trapezoidal distributed loads on frames |
| `SapModel.FrameObj.SetLoadPoint` | Critical | Concentrated load at a point along frame |
| `SapModel.AreaObj.SetLoadUniform` | Critical | Uniform pressure on area elements (slab loads) |
| `SapModel.AreaObj.SetLoadGravity` | Important | Gravity multiplier on area self-weight |
| `SapModel.FrameObj.SetLoadTemperature` | Important | Thermal loads on frame elements |
**Testing:** Each wrapper creates a minimal model, applies the load, verifies with a Get function or by checking return code → register in registry with full parameter_notes

---

### Step 3: Frame Properties & Releases
**Files:** `scripts/wrappers/func_PropFrame_SetPipe.py`, `func_PropFrame_SetChannel.py`, `func_PropFrame_SetAngle.py`, `func_PropFrame_SetTee.py`, `func_FrameObj_SetReleases.py`, `func_FrameObj_SetEndLengthOffset.py`, `func_PropFrame_SetModifiers.py`, `scripts/registry.json`
**What:** Add 4 missing cross-section types (Pipe, Channel, Angle, Tee) and 3 critical frame-object assignment functions: end releases (pin/fixed), rigid-end offsets, and section property modifiers.
**Functions (7):**
| Function | Priority | Description |
|----------|----------|-------------|
| `SapModel.PropFrame.SetPipe` | Important | Circular hollow section (pipe/HSS round) |
| `SapModel.PropFrame.SetChannel` | Important | C-shape channel section |
| `SapModel.PropFrame.SetAngle` | Important | L-shape angle section |
| `SapModel.PropFrame.SetTee` | Nice-to-have | T-shape section |
| `SapModel.FrameObj.SetReleases` | Critical | End releases (moment releases for hinges) |
| `SapModel.FrameObj.SetEndLengthOffset` | Important | Rigid-zone offsets at beam-column joints |
| `SapModel.PropFrame.SetModifiers` | Important | Stiffness modifiers (cracked sections, etc.) |
**Testing:** Execute wrappers against live SAP2000 → verify section created with correct geometry → verify releases applied → register with full metadata

---

### Step 4: Design & Results Extraction
**Files:** `scripts/wrappers/func_DesignSteel_StartDesign.py`, `func_DesignConcrete_StartDesign.py`, `func_DesignSteel_SetCode.py`, `func_Results_FrameForce.py`, `func_Results_JointDispl.py`, `func_Results_JointReact.py`, `func_Results_AreaForce.py`, `scripts/registry.json`
**What:** Add design initiation wrappers (steel + concrete) and results extraction wrappers. `Results.FrameForce`, `Results.JointDispl`, and `Results.JointReact` are already in registry but lack wrappers — create them. Add `Results.AreaForce` for slab/wall forces.
**Functions (7):**
| Function | Priority | Description |
|----------|----------|-------------|
| `SapModel.DesignSteel.StartDesign` | Critical | Run steel frame design check |
| `SapModel.DesignConcrete.StartDesign` | Critical | Run concrete frame design check |
| `SapModel.DesignSteel.SetCode` | Important | Set steel design code (AISC 360, Eurocode, etc.) |
| `SapModel.Results.FrameForce` | Critical | Extract axial/shear/moment diagrams (needs wrapper) |
| `SapModel.Results.JointDispl` | Critical | Extract joint displacements (needs wrapper) |
| `SapModel.Results.JointReact` | Critical | Extract support reactions (needs wrapper) |
| `SapModel.Results.AreaForce` | Important | Extract membrane/plate forces from area elements |
**Testing:** Build a simple 2D frame → apply loads → run analysis → extract results with each wrapper → verify non-zero results returned → run design → verify design status returned → register all

---

### Step 5: Groups, Mass Source & Database Tables
**Files:** `scripts/wrappers/func_GroupDef_SetGroup_1.py`, `func_GroupDef_GetNameList.py`, `func_GroupDef_GetAssignments.py`, `func_MassSource_SetDefault.py`, `func_DatabaseTables_GetTableForDisplay.py`, `func_PointObj_SetLoadMass.py`, `scripts/registry.json`
**What:** Add group management (define groups, query members), mass source definition for modal analysis, database table extraction for flexible results, and point mass assignment.
**Functions (6):**
| Function | Priority | Description |
|----------|----------|-------------|
| `SapModel.GroupDef.SetGroup_1` | Important | Create or modify a named group |
| `SapModel.GroupDef.GetNameList` | Important | List all defined groups |
| `SapModel.GroupDef.GetAssignments` | Important | Get objects assigned to a group |
| `SapModel.MassSource.SetDefault` | Important | Define default mass source for analysis |
| `SapModel.DatabaseTables.GetTableForDisplay` | Important | General-purpose table extraction |
| `SapModel.PointObj.SetLoadMass` | Important | Add lumped mass at joints |
**Testing:** Create groups, assign objects, query back → define mass source → extract a table → register all with full metadata

---

## Summary

| Step | Functions | Wrappers | Focus Area |
|------|-----------|----------|------------|
| 1 | 5 | 5 | File operations & templates |
| 2 | 6 | 6 | Load assignments |
| 3 | 7 | 7 | Sections & frame releases |
| 4 | 7 | 7 | Design & results extraction |
| 5 | 6 | 6 | Groups, mass source, DB tables |
| **Total** | **31** | **31** | |

After all 5 steps: **~89 registered** functions, **~57 wrappers** — covering the full structural engineering workflow: model creation → geometry → properties → loads → analysis → results → design.

## Execution Notes
- Each wrapper must be **executed and verified** against live SAP2000 via `run_sap_script` before registering
- Follow the existing wrapper pattern: initialize model → define prerequisites → call target function → assert success → write to `result`
- Registry entries should include: category, description, signature, parameter_notes, wrapper_script name
- Wrappers naming convention: `func_{Object}_{Function}.py`
- Each step corresponds to one commit on the `expand-wrappers-registry` branch
