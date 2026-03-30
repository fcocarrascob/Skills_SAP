# ============================================================
# Wrapper: SapModel.FrameObj.SetReleases
# Category: Object_Model
# Description: Assign end release (hinge/partial fixity) to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Assigns moment releases (hinges) and partial fixity springs at the
       I-End and J-End of frame objects. Essential for modeling pinned
       connections, simply-supported beams, and semi-rigid joints.

API Signature:
  SapModel.FrameObj.SetReleases(Name, ii, jj, StartValue, EndValue,
      ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name       : str      — Frame object name
  ii         : bool[6]  — I-End releases [U1, U2, U3, R1, R2, R3]
  jj         : bool[6]  — J-End releases [U1, U2, U3, R1, R2, R3]
  StartValue : float[6] — I-End partial fixity springs [F/L or FL/rad]
  EndValue   : float[6] — J-End partial fixity springs [F/L or FL/rad]
  ItemType   : int      — 0=Object, 1=Group, 2=SelectedObjects

Note: Unstable combinations are rejected (e.g., U1 released at both ends).
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

# Create beam
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: release M3 (major bending) at J-End ---
# This creates a pin at the J-End (simple support for bending)
ii_releases = [False, False, False, False, False, False]
jj_releases = [False, False, False, False, False, True]  # Release R3 (M33)
start_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
end_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

raw_set = SapModel.FrameObj.SetReleases(
    beam_name, ii_releases, jj_releases, start_values, end_values
)
# SetReleases returns [ii, jj, StartValue, EndValue, ret_code]
assert raw_set[-1] == 0, f"SetReleases ret_code={raw_set[-1]}, raw={raw_set}"

# --- Verification via GetReleases ---
raw = SapModel.FrameObj.GetReleases(beam_name, [], [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetReleases failed: {ret_code}"

read_ii = list(raw[0])
read_jj = list(raw[1])

assert read_jj[5] == True, f"Expected R3 released at J-End, got {read_jj[5]}"
assert read_ii[5] == False, f"I-End R3 should be fixed, got {read_ii[5]}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetReleases"
result["beam_name"] = beam_name
result["ii_releases"] = read_ii
result["jj_releases"] = read_jj
result["status"] = "verified"
