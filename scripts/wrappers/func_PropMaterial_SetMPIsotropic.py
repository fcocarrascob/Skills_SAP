# ============================================================
# Wrapper: SapModel.PropMaterial.SetMPIsotropic
# Category: PropMaterial
# Description: Set isotropic mechanical properties for a material
# Verified: 2026-03-20
# Prerequisites: Model open, material already defined via SetMaterial
# ============================================================
"""
Usage: Assigns isotropic material properties (E, Poisson, thermal coeff)
       to an existing material definition. Call after SetMaterial.

API Signature:
  SapModel.PropMaterial.SetMPIsotropic(Name, E, U, A, Temp)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name : str   — Name of existing material
  E    : float — Modulus of elasticity [F/L^2]
  U    : float — Poisson's ratio (dimensionless)
  A    : float — Coefficient of thermal expansion [1/T]
  Temp : float — Temperature at which props are defined (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define materials first ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial(Steel) failed: {ret}"

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)  # Concrete
assert ret == 0, f"SetMaterial(Concrete) failed: {ret}"

# --- Target function: set isotropic properties ---
# Steel: E=200000 MPa (200 GPa), U=0.3, A=1.2e-5 /°C
# In kN_m_C: E = 2.0e8 kN/m², U = 0.3, A = 1.2e-5
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic(Steel) failed: {ret}"

# Concrete: E=25000 MPa (25 GPa), U=0.2, A=1.0e-5 /°C
# In kN_m_C: E = 2.5e7 kN/m², U = 0.2, A = 1.0e-5
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic(Concrete) failed: {ret}"

# --- Verification ---
# Read back properties to confirm they were set
raw = SapModel.PropMaterial.GetMPIsotropic("STEEL_TEST", 0, 0, 0, 0)
ret_code = raw[-1]
assert ret_code == 0, f"GetMPIsotropic(Steel) failed: {ret_code}"
e_steel = raw[0]
u_steel = raw[1]
a_steel = raw[2]

raw = SapModel.PropMaterial.GetMPIsotropic("CONC_TEST", 0, 0, 0, 0)
ret_code = raw[-1]
assert ret_code == 0, f"GetMPIsotropic(Concrete) failed: {ret_code}"
e_conc = raw[0]

# --- Result ---
result["function"] = "SapModel.PropMaterial.SetMPIsotropic"
result["steel_E"] = e_steel
result["steel_U"] = u_steel
result["steel_A"] = a_steel
result["concrete_E"] = e_conc
result["status"] = "verified"
