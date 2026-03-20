# ============================================================
# Wrapper: SapModel.PropMaterial.SetWeightAndMass
# Category: PropMaterial
# Description: Set weight per unit volume and mass per unit volume
# Verified: 2026-03-20
# Prerequisites: Model open, material already defined via SetMaterial
# ============================================================
"""
Usage: Sets the weight per unit volume and/or mass per unit volume
       for an existing material. Both are needed for self-weight and
       dynamic analysis respectively.

API Signature:
  SapModel.PropMaterial.SetWeightAndMass(Name, MyType, Value, Temp)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name   : str   — Name of existing material
  MyType : int   — 1=weight per unit volume [F/L^3]
                    2=mass per unit volume [M/L^3]
  Value  : float — The weight or mass per unit volume
  Temp   : float — Temperature (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define material ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)  # Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function: set weight and mass ---
# Concrete weight: 24 kN/m³ (typical reinforced concrete)
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_TEST", 1, 24.0)
assert ret == 0, f"SetWeightAndMass(weight) failed: {ret}"

# Concrete mass: ~2.4 ton/m³ ≈ 2447 kg/m³
# In kN_m_C: mass = weight / g = 24.0 / 9.81 ≈ 2.446 kN·s²/m⁴
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_TEST", 2, 2.4)
assert ret == 0, f"SetWeightAndMass(mass) failed: {ret}"

# --- Verification ---
# Read back weight and mass
raw = SapModel.PropMaterial.GetWeightAndMass("CONC_TEST", 0, 0, 0)
ret_code = raw[-1]
assert ret_code == 0, f"GetWeightAndMass failed: {ret_code}"
weight_value = raw[0]
mass_value = raw[1]

# --- Result ---
result["function"] = "SapModel.PropMaterial.SetWeightAndMass"
result["weight_per_volume"] = weight_value
result["mass_per_volume"] = mass_value
result["status"] = "verified"
