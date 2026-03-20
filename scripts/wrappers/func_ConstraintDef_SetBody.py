# ============================================================
# Wrapper: SapModel.ConstraintDef.SetBody
# Category: Constraints
# Description: Define a body constraint (rigid link) for DOF coupling
# Verified: 2026-03-20
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a body constraint that couples selected DOFs between
       assigned joints. Used for rigid diaphragms, rigid links, and
       master-slave connections in structural models.

API Signature:
  SapModel.ConstraintDef.SetBody(Name, Value, CSys)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name  : str     — Constraint name
  Value : bool[6] — DOF coupling [UX, UY, UZ, RX, RY, RZ]
                     True=constrained (coupled), False=free
  CSys  : str     — Coordinate system (default="Global")
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: create body constraints ---
# Full rigid body (all 6 DOF coupled)
dof_full = [True, True, True, True, True, True]
raw = SapModel.ConstraintDef.SetBody("RIGID_FULL", dof_full, "Global")
assert raw[-1] == 0, f"SetBody(RIGID_FULL) failed: {raw[-1]}"

# Rigid diaphragm (only in-plane: UX, UY, RZ)
dof_diaphragm = [True, True, False, False, False, True]
raw = SapModel.ConstraintDef.SetBody("RIGID_DIAPH", dof_diaphragm, "Global")
assert raw[-1] == 0, f"SetBody(RIGID_DIAPH) failed: {raw[-1]}"

# --- Prerequisites for assignment: create points and assign constraint ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

# Create two points
raw = SapModel.PointObj.AddCartesian(0, 0, 3, "", "PT_A")
pt_a = raw[0]
assert raw[-1] == 0, f"AddCartesian(A) failed: {raw[-1]}"

raw = SapModel.PointObj.AddCartesian(5, 0, 3, "", "PT_B")
pt_b = raw[0]
assert raw[-1] == 0, f"AddCartesian(B) failed: {raw[-1]}"

# Assign body constraint to points (returns tuple with ByRef constraint name)
raw_sc = SapModel.PointObj.SetConstraint(pt_a, "RIGID_DIAPH")
assert raw_sc[-1] == 0, f"SetConstraint(A) failed: {raw_sc[-1]}"

raw_sc = SapModel.PointObj.SetConstraint(pt_b, "RIGID_DIAPH")
assert raw_sc[-1] == 0, f"SetConstraint(B) failed: {raw_sc[-1]}"


# --- Verification ---
# Read back constraint definition
raw = SapModel.ConstraintDef.GetBody("RIGID_DIAPH", [], "")
ret_code = raw[-1]
assert ret_code == 0, f"GetBody failed: {ret_code}"
read_dof = list(raw[0])

# --- Result ---
result["function"] = "SapModel.ConstraintDef.SetBody"
result["constraints_created"] = ["RIGID_FULL", "RIGID_DIAPH"]
result["diaphragm_dof"] = read_dof
result["points_assigned"] = [pt_a, pt_b]
result["status"] = "verified"
