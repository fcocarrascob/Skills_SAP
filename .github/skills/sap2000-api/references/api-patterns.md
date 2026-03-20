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
