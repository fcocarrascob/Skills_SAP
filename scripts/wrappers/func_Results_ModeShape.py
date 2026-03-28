# ============================================================
# Wrapper: SapModel.Results.ModeShape
# Category: Analysis_Results
# Description: Extract modal displacements (mode shapes) per joint
# Verified: 2026-03-28
# Prerequisites: Model analyzed with modal case
# ============================================================
"""
Usage: Reports the modal displacements (eigenvectors) at point elements
       for selected modal analysis cases.

API Signature:
  SapModel.Results.ModeShape(Name, ItemTypeElm,
      NumberResults, Obj, Elm, LoadCase, StepType, StepNum,
      U1, U2, U3, R1, R2, R3) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — point object names
  Elm[]         : str[]   — point element names
  LoadCase[]    : str[]   — modal case names
  StepType[]    : str[]   — always "Mode"
  StepNum[]     : float[] — mode numbers
  U1..U3[]      : float[] — translational displacements [L]
  R1..R3[]      : float[] — rotational displacements [rad]

Parameters:
  Name        : str — Point name, or group name for all points
  ItemTypeElm : int — 0=ObjectElm, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Setup: same 2-story portal ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_M", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_M", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 1, 24.0)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_M", 2, 2.4)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("COL_40", "CONC_M", 0.4, 0.4)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30", "CONC_M", 0.3, 0.2)
assert ret == 0

for x in [0, 5]:
    raw = SapModel.FrameObj.AddByCoord(x, 0, 0, x, 0, 3, "", "COL_40", "")
    assert raw[-1] == 0
    raw = SapModel.FrameObj.AddByCoord(x, 0, 3, x, 0, 6, "", "COL_40", "")
    assert raw[-1] == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "BEAM_30", "")
assert raw[-1] == 0
raw = SapModel.FrameObj.AddByCoord(0, 0, 6, 5, 0, 6, "", "BEAM_30", "")
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("4", [True, True, True, True, True, True])
assert ret[-1] == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_modeshape.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("MODAL")
assert ret == 0

# --- Target function: get mode shapes for ALL points ---
raw = SapModel.Results.ModeShape(
    "ALL", 2,  # GroupElm — "ALL" is a built-in group
    0, [], [], [], [], [],
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"ModeShape failed: {ret_code}"

num_results = raw[0]
obj_names = list(raw[1])   # point object names
# raw[2]=Elm[], raw[3]=LoadCase[], raw[4]=StepType[]
step_nums = list(raw[5])   # mode numbers
U1 = list(raw[6])          # U1 modal displacement
U2 = list(raw[7])          # U2 modal displacement
U3 = list(raw[8])          # U3 modal displacement

assert num_results > 0, f"No mode shape results"

# --- Result ---
result["function"] = "SapModel.Results.ModeShape"
result["num_results"] = num_results
result["unique_points"] = list(set(obj_names))
result["unique_modes"] = list(set(step_nums))
result["U1_sample"] = U1[:6]
result["status"] = "verified"
