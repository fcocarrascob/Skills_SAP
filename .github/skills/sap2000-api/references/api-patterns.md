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
# NOTE: RunAnalysis requires the model to be saved first.
# Save must be done manually or via File.Save before calling this.

# Run analysis
ret = SapModel.Analyze.RunAnalysis()

# Setup results output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

# Get joint displacements
# COM convention: ret_code is ALWAYS the LAST element raw[-1]
# ByRef outputs come FIRST
raw = SapModel.Results.JointDispl(
    "3", 0,   # joint name, eItemTypeElm_ObjectElm
    0, [], [], [], [], [], [], [], [], [], []
)
# raw layout (13 elements):
# [0]=NumberResults, [1]=Obj[], [2]=Elm[], [3]=LoadCase[], [4]=StepType[],
# [5]=StepNum[], [6]=U1[], [7]=U2[], [8]=U3[], [9]=R1[], [10]=R2[], [11]=R3[],
# [12]=ret_code  ← LAST element is always ret_code
if raw[-1] == 0 and raw[0] > 0:
    result["U1"] = raw[6][0]
    result["U2"] = raw[7][0]
    result["U3"] = raw[8][0]
```

## Pattern 5: Frame Object Points

```python
# Get the endpoint joint names of a frame
# COM convention: ByRef outputs first, ret_code LAST
raw = SapModel.FrameObj.GetPoints("1", "", "")
# raw = [Point_i_name, Point_j_name, ret_code]
point_i = raw[0]
point_j = raw[1]
assert raw[-1] == 0, f"GetPoints failed: {raw[-1]}"
```

## Pattern 6: Area Objects

```python
# Add area by coordinates
# COM convention: ByRef Name output is first, ret_code is LAST
x = [0, 10, 10, 0]
y = [0, 0, 0, 0]
z = [0, 0, 10, 10]
raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "Default", "", "Global")
# raw = [Name_out, ret_code]
area_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"
```

## Pattern 7: General ByRef Convention

```python
# CRITICAL: ALL SAP2000 COM functions follow this convention:
# raw = [byref_out1, byref_out2, ..., byref_outN, ret_code]
# ret_code is ALWAYS raw[-1] (the last element)
# This is the OPPOSITE of what the VBA signature implies.

# Verified with (len → layout):
# AddCartesian    (2)  → [Name, ret_code]
# GetCoordCart.   (4)  → [x, y, z, ret_code]
# GetPoints       (3)  → [pt_i, pt_j, ret_code]
# GetMPIsotropic  (5)  → [E, poisson, thermal, tempDep, ret_code]
# GetRestraint    (2)  → [restraints[], ret_code]
# GetRectangle    (8)  → [FileName, MatProp, t3, t2, Color, Notes, GUID, ret_code]
# JointDispl      (13) → [NRes, Obj[], Elm[], LC[], StType[], StNum[],
#                          U1[], U2[], U3[], R1[], R2[], R3[], ret_code]

# Safe universal pattern:
raw = SapModel.SomeObj.SomeFunction(...)
ret_code = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret_code == 0, f"SomeFunction failed: {ret_code}"
```
