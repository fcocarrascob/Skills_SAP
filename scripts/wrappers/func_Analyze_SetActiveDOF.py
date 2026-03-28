# ============================================================
# Wrapper: SapModel.Analyze.SetActiveDOF
# Category: Analyze
# Description: Set active/inactive global degrees of freedom for model
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets which global DOFs are active (solved) in the analysis model.
       Essential for 2D models (deactivate out-of-plane DOFs) or specialty analyses.

API Signature:
  SapModel.Analyze.SetActiveDOF(DOF) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  DOF : bool[6] — [UX, UY, UZ, RX, RY, RZ] — True=active
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: set 2D frame DOFs (XZ plane) ---
# UX, UZ, RY active; UY, RX, RZ inactive
# Note: SetActiveDOF returns [DOF_echo[], ret_code] — use raw[-1]
dof_2d = [True, False, True, False, True, False]
raw_set = SapModel.Analyze.SetActiveDOF(dof_2d)
ret_set = raw_set[-1] if isinstance(raw_set, (list, tuple)) else raw_set
assert ret_set == 0, f"SetActiveDOF(2D) failed: {ret_set}"

# --- Verification via GetActiveDOF ---
raw = SapModel.Analyze.GetActiveDOF([])
ret_code = raw[-1]
assert ret_code == 0, f"GetActiveDOF failed: {ret_code}"
read_dof = list(raw[0])
assert read_dof == dof_2d, f"DOFs mismatch: expected {dof_2d}, got {read_dof}"

# --- Set back to full 3D ---
dof_3d = [True, True, True, True, True, True]
raw_set3d = SapModel.Analyze.SetActiveDOF(dof_3d)
ret_set3d = raw_set3d[-1] if isinstance(raw_set3d, (list, tuple)) else raw_set3d
assert ret_set3d == 0, f"SetActiveDOF(3D) failed: {ret_set3d}"

raw = SapModel.Analyze.GetActiveDOF([])
assert raw[-1] == 0
read_dof_3d = list(raw[0])
assert read_dof_3d == dof_3d, f"3D DOFs mismatch"

# --- Result ---
result["function"] = "SapModel.Analyze.SetActiveDOF"
result["dof_2d_set"] = dof_2d
result["dof_2d_read"] = read_dof
result["dof_3d_verified"] = True
result["status"] = "verified"
