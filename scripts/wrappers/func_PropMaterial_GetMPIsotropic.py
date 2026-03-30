# ============================================================
# Wrapper: SapModel.PropMaterial.GetMPIsotropic
# Category: PropMaterial
# Description: Retrieve isotropic mechanical properties (E, Poisson, thermal)
# Verified: 2026-03-28
# Prerequisites: Model open, material defined with SetMPIsotropic
# ============================================================
"""
Usage: Reads back the isotropic mechanical properties assigned
       to an existing material. Useful for verification cycles.

API Signature:
  SapModel.PropMaterial.GetMPIsotropic(Name, E, U, A, Temp)

ByRef Output:
  [E, poisson, thermal, tempDep, ret_code]

Parameters:
  Name : str   — Existing material name
  E    : float — (ByRef out) Modulus of elasticity [F/L^2]
  U    : float — (ByRef out) Poisson ratio
  A    : float — (ByRef out) Thermal expansion coeff [1/T]
  Temp : float — (ByRef out) Temperature dependency flag
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create material with known properties ---
ret = SapModel.PropMaterial.SetMaterial("MAT_VERIFY", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

E_set = 2.0e8
U_set = 0.3
A_set = 1.2e-5
ret = SapModel.PropMaterial.SetMPIsotropic("MAT_VERIFY", E_set, U_set, A_set)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function: get isotropic properties ---
raw = SapModel.PropMaterial.GetMPIsotropic("MAT_VERIFY", 0, 0, 0, 0)
ret_code = raw[-1]
assert ret_code == 0, f"GetMPIsotropic failed: {ret_code}"

E_got = raw[0]
U_got = raw[1]
A_got = raw[2]

# Verify values match (within floating-point tolerance)
assert abs(E_got - E_set) < 1000, f"E mismatch: set={E_set}, got={E_got}"
assert abs(U_got - U_set) < 0.01, f"U mismatch: set={U_set}, got={U_got}"
assert abs(A_got - A_set) < 1e-7, f"A mismatch: set={A_set}, got={A_got}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.GetMPIsotropic"
result["E"] = E_got
result["poisson"] = U_got
result["thermal"] = A_got
result["byref_layout"] = "[E, poisson, thermal, tempDep, ret_code]"
result["status"] = "verified"
