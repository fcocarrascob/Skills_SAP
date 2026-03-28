# ============================================================
# Wrapper: SapModel.Analyze.GetActiveDOF
# Category: Analyze
# Description: Retrieve active global degrees of freedom
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Gets the current active DOFs for the analysis model.

API Signature:
  SapModel.Analyze.GetActiveDOF(DOF) -> [DOF[], ret_code]

ByRef Output:
  DOF[] : bool[6] — [UX, UY, UZ, RX, RY, RZ]

Parameters: None (DOF is ByRef output)

Note: SetActiveDOF also returns [DOF_echo[], ret_code] — use raw[-1] for ret_code.
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Default for a new model should be all 6 DOFs active
raw = SapModel.Analyze.GetActiveDOF([])
ret_code = raw[-1]
assert ret_code == 0, f"GetActiveDOF failed: {ret_code}"

default_dof = list(raw[0])
# By default, all DOFs should be True
assert all(d == True for d in default_dof), f"Expected all True, got {default_dof}"

# Set to 2D and verify
dof_2d = [True, False, True, False, True, False]
raw_set = SapModel.Analyze.SetActiveDOF(dof_2d)
ret_set = raw_set[-1] if isinstance(raw_set, (list, tuple)) else raw_set
assert ret_set == 0

raw = SapModel.Analyze.GetActiveDOF([])
assert raw[-1] == 0
read_2d = list(raw[0])
assert read_2d == dof_2d, f"2D DOF mismatch: {read_2d}"

# --- Result ---
result["function"] = "SapModel.Analyze.GetActiveDOF"
result["default_dof"] = default_dof
result["after_set_2d"] = read_2d
result["status"] = "verified"
