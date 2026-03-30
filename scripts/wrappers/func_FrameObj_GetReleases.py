# ============================================================
# Wrapper: SapModel.FrameObj.GetReleases
# Category: Object_Model
# Description: Retrieve end release and partial fixity assignments from frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Retrieves the I-End and J-End release assignments and partial fixity
       spring values for a frame object.

API Signature:
  SapModel.FrameObj.GetReleases(Name, ii, jj,
      StartValue, EndValue) -> [ii[], jj[], StartValue[], EndValue[], ret_code]

ByRef Output (4 arrays):
  ii[]         : bool[6]  — I-End releases
  jj[]         : bool[6]  — J-End releases
  StartValue[] : float[6] — I-End partial fixity springs
  EndValue[]   : float[6] — J-End partial fixity springs

Parameters:
  Name : str — Frame object name
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

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# Assign known releases: both-end moment releases (R2 and R3)
ii_set = [False, False, False, False, True, False]   # R2 at I-End
jj_set = [False, False, False, False, False, True]   # R3 at J-End
start_v = [0, 0, 0, 0, 0, 0]
end_v = [0, 0, 0, 0, 0, 0]
ret = SapModel.FrameObj.SetReleases(beam_name, ii_set, jj_set, start_v, end_v)
assert ret == 0

# --- Target function ---
raw = SapModel.FrameObj.GetReleases(beam_name, [], [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetReleases failed: {ret_code}"

read_ii = list(raw[0])
read_jj = list(raw[1])
read_sv = list(raw[2])
read_ev = list(raw[3])

assert read_ii[4] == True, f"Expected R2 released at I-End"
assert read_jj[5] == True, f"Expected R3 released at J-End"

# --- Result ---
result["function"] = "SapModel.FrameObj.GetReleases"
result["ii_releases"] = read_ii
result["jj_releases"] = read_jj
result["start_values"] = read_sv
result["end_values"] = read_ev
result["status"] = "verified"
