# ============================================================
# Wrapper: SapModel.PropLink.SetLinear
# Category: Properties
# Description: Define a linear-type link property with stiffness and damping
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates or modifies a linear link property. Defines DOFs, fixities,
       stiffness (Ke), and damping (Ce) for 6 DOFs (U1-U3, R1-R3).
       Used for spring connections, elastic supports, and simple connectors.

API Signature:
  SapModel.PropLink.SetLinear(Name, DOF, Fixed, Ke, Ce,
      dj2, dj3, KeCoupled, CeCoupled, Notes, GUID) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str      — Link property name
  DOF       : bool[6]  — Active DOFs [U1,U2,U3,R1,R2,R3]
  Fixed     : bool[6]  — Fixed DOFs (if DOF is True)
  Ke        : float[6] — Stiffness values (uncoupled) [F/L or FL]
  Ce        : float[6] — Damping values (uncoupled) [F/L or FL]
  dj2       : float    — Distance to U2 shear spring from J-End [L]
  dj3       : float    — Distance to U3 shear spring from J-End [L]
  KeCoupled : bool     — True if stiffness is coupled (21 terms)
  CeCoupled : bool     — True if damping is coupled (21 terms)
  Notes     : str      — Optional notes
  GUID      : str      — Optional GUID
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Target function: create linear link with translational stiffness ---
dof = [True, True, True, False, False, False]  # Only translational DOFs
fixed = [False, False, False, False, False, False]  # None fixed
ke = [10000.0, 5000.0, 5000.0, 0.0, 0.0, 0.0]  # kN/m stiffness
ce = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # No damping

raw = SapModel.PropLink.SetLinear(
    "SPRING_V", dof, fixed, ke, ce, 0.0, 0.0, False, False
)
ret_code = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret_code == 0, f"SetLinear(SPRING_V) failed: {ret_code}"

# Create another with all 6 DOFs
dof_full = [True, True, True, True, True, True]
fixed_full = [False, False, False, False, False, False]
ke_full = [10000, 10000, 10000, 5000, 5000, 5000]
ce_full = [100, 100, 100, 50, 50, 50]

raw = SapModel.PropLink.SetLinear(
    "CONNECTOR_6DOF", dof_full, fixed_full, ke_full, ce_full, 0.0, 0.0
)
ret_code = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret_code == 0, f"SetLinear(CONNECTOR_6DOF) failed: {ret_code}"

# --- Verification via GetLinear ---
raw = SapModel.PropLink.GetLinear(
    "SPRING_V", [], [], [], [], 0.0, 0.0, False, False, "", ""
)
ret_code = raw[-1]
assert ret_code == 0, f"GetLinear failed: {ret_code}"

read_dof = list(raw[0])
read_ke = list(raw[2])
assert read_dof[0] == True, f"U1 DOF should be active"
assert abs(read_ke[0] - 10000.0) < 1, f"U1 stiffness mismatch: {read_ke[0]}"

# --- Result ---
result["function"] = "SapModel.PropLink.SetLinear"
result["links_defined"] = ["SPRING_V", "CONNECTOR_6DOF"]
result["dof_read"] = read_dof
result["ke_read"] = read_ke
result["status"] = "verified"
