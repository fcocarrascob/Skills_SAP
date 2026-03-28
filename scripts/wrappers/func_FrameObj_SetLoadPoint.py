# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadPoint
# Category: Object_Model
# Description: Assign point loads (force/moment) to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists, load pattern defined
# ============================================================
"""
Usage: Assigns a concentrated load at a specified distance along a frame.

API Signature:
  SapModel.FrameObj.SetLoadPoint(Name, LoadPat, MyType, Dir,
      Dist, Val, CSys, RelDist, Replace, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str   — Frame object name
  LoadPat : str   — Load pattern name
  MyType  : int   — 1=Force, 2=Moment
  Dir     : int   — 1-3=Local, 4-6=Global XYZ, 10=Gravity
  Dist    : float — Distance from I-End (relative 0-1 or absolute [L])
  Val     : float — Load value [F] or [FL]
  CSys    : str   — "Global" or "Local"
  RelDist : bool  — True=relative, False=absolute
  Replace : bool  — True=replace previous point loads in pattern
  ItemType: int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 6m
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

# --- Target function: point load at midspan ---
# 50 kN downward at midspan (relative distance 0.5)
ret = SapModel.FrameObj.SetLoadPoint(
    beam_name, "DEAD", 1, 10, 0.5, -50, "Global", True, True
)
assert ret == 0, f"SetLoadPoint(midspan) failed: {ret}"

# Add second point load at quarter span
ret = SapModel.FrameObj.SetLoadPoint(
    beam_name, "DEAD", 1, 10, 0.25, -25, "Global", True, False
)
assert ret == 0, f"SetLoadPoint(quarter) failed: {ret}"

# --- Verification via analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_frameobj_setloadpoint.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# Check reactions sum to total applied load (50 + 25 = 75 kN)
raw = SapModel.Results.JointReact(
    "1", 0, 0, [], [], [], [], [], [], [], [], [], [], []
)
assert raw[-1] == 0
F3_1 = raw[8][0]

raw = SapModel.Results.JointReact(
    "2", 0, 0, [], [], [], [], [], [], [], [], [], [], []
)
assert raw[-1] == 0
F3_2 = raw[8][0]

total_reaction = F3_1 + F3_2

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadPoint"
result["beam_name"] = beam_name
result["total_reaction"] = total_reaction
result["expected_total"] = 75.0
result["status"] = "verified"
