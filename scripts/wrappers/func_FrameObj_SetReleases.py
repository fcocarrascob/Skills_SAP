# ============================================================
# Wrapper: SapModel.FrameObj.SetReleases
# Category: Object_Model
# Description: Set end releases (moment releases for hinges)
# Verified: 2026-03-21
# Prerequisites: Model open, frame element exists
# ============================================================
"""
Usage: Assigns end releases to a frame element. End releases
       convert fixed connections to pinned (moment-released) or
       partially restrained connections at the i-end and j-end.

API Signature:
  SapModel.FrameObj.SetReleases(Name, ii, jj, StartValue, EndValue, ItemType)

ByRef Output:
  Returns tuple: (ii_out, jj_out, start_out, end_out, ret_code)
  ret_code is raw[-1] (0=success)

Parameters:
  Name       : str      — Frame object name
  ii         : bool[6]  — i-end releases [P, V2, V3, T, M2, M3]
                           True=released, False=fixed
  jj         : bool[6]  — j-end releases [P, V2, V3, T, M2, M3]
  StartValue : float[6] — Partial fixity spring values at i-end
                           (0=fully released when ii[k]=True)
  EndValue   : float[6] — Partial fixity spring values at j-end
  ItemType   : int      — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.3)
assert ret == 0

# Portal frame: two columns and one beam
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_TEST", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(6, 0, 0, 6, 0, 3, "", "SEC_TEST", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3, 6, 0, 3, "", "SEC_TEST", "")
beam_name = beam[0]
assert beam[-1] == 0

# --- Target function: pin both ends of beam (release M3) ---
# Release: [P, V2, V3, T, M2, M3]
# Pin = release M3 only (index 5)
ii_release = [False, False, False, False, False, True]  # i-end: release M3
jj_release = [False, False, False, False, False, True]  # j-end: release M3
start_vals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # fully released (no partial fixity)
end_vals   = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# SetReleases returns ByRef: (ii_out, jj_out, start_out, end_out, ret_code)
raw = SapModel.FrameObj.SetReleases(
    beam_name, ii_release, jj_release, start_vals, end_vals
)
ret_code = raw[-1]
assert ret_code == 0, f"SetReleases failed with ret_code={ret_code}, raw={raw}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
assert frame_count == 3, f"Expected 3 frames, got {frame_count}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetReleases"
result["frame_name"] = beam_name
result["i_releases"] = ii_release
result["j_releases"] = jj_release
result["status"] = "verified"
