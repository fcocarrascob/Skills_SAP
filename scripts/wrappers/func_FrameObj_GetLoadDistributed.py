# ============================================================
# Wrapper: SapModel.FrameObj.GetLoadDistributed
# Category: Object_Model
# Description: Retrieve distributed load assignments from frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame with distributed loads assigned
# ============================================================
"""
Usage: Retrieves all distributed load assignments for a frame object.

API Signature:
  SapModel.FrameObj.GetLoadDistributed(Name, NumberItems,
      FrameName, LoadPat, MyType, CSys, Dir,
      RD1, RD2, Dist1, Dist2, Val1, Val2, ItemType) -> ret_code

ByRef Output (12 values):
  NumberItems : int     — number of load assignments
  FrameName[] : str[]   — frame names
  LoadPat[]   : str[]   — load pattern names
  MyType[]    : int[]   — 1=Force, 2=Moment
  CSys[]      : str[]   — coordinate systems
  Dir[]       : int[]   — directions
  RD1[]       : float[] — relative start distances
  RD2[]       : float[] — relative end distances
  Dist1[]     : float[] — absolute start distances [L]
  Dist2[]     : float[] — absolute end distances [L]
  Val1[]      : float[] — start load values
  Val2[]      : float[] — end load values

Parameters:
  Name     : str — Frame name (or group/selection)
  ItemType : int — 0=Object, 1=Group, 2=SelectedObjects
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

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# Assign known loads
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -12, -12, "Global", True, True
)
assert ret == 0

ret = SapModel.LoadPatterns.Add("LIVE", 3, 0, False)
assert ret == 0
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "LIVE", 1, 10, 0, 0.5, -5, -10, "Global", True, True
)
assert ret == 0

# --- Target function ---
raw = SapModel.FrameObj.GetLoadDistributed(
    beam_name, 0, [], [], [], [], [], [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadDistributed failed: {ret_code}"

num_loads = raw[0]
frame_names = list(raw[1])
load_pats = list(raw[2])
val1_arr = list(raw[10])
val2_arr = list(raw[11])

assert num_loads == 2, f"Expected 2 loads, got {num_loads}"

# --- Result ---
result["function"] = "SapModel.FrameObj.GetLoadDistributed"
result["num_loads"] = num_loads
result["load_patterns"] = load_pats
result["val1"] = val1_arr
result["val2"] = val2_arr
result["status"] = "verified"
