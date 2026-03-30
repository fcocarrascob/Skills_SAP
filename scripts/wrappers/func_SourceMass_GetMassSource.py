# ============================================================
# Wrapper: SapModel.SourceMass.GetMassSource
# Category: Mass_Source
# Description: Retrieve mass source data
# Verified: 2026-03-28
# Prerequisites: Model open, mass source defined
# ============================================================
"""
Usage: Gets the mass source configuration including which elements,
       masses and load patterns contribute, plus scale factors.

API Signature:
  SapModel.SourceMass.GetMassSource(Name, MassFromElements,
    MassFromMasses, MassFromLoads, IsDefault,
    NumberLoads, LoadPat[], SF[])

ByRef Output:
  [MassFromElements, MassFromMasses, MassFromLoads, IsDefault,
   NumberLoads, LoadPat[], SF[], ret_code]

Parameters:
  Name : str — Existing mass source name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create mass source ---
ret = SapModel.SourceMass.SetMassSource(
    "MS_GET_TEST", True, True, True, True, 1, ["DEAD"], [1.0]
)
assert ret == 0

# --- Target function ---
raw = SapModel.SourceMass.GetMassSource(
    "MS_GET_TEST", False, False, False, False, 0, [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"GetMassSource failed: {ret_code}"

mass_from_elements = raw[0]
mass_from_masses = raw[1]
mass_from_loads = raw[2]
is_default = raw[3]
num_loads = raw[4]

assert mass_from_elements == True, f"MassFromElements mismatch: {mass_from_elements}"
assert mass_from_loads == True, f"MassFromLoads mismatch: {mass_from_loads}"
assert is_default == True, f"IsDefault mismatch: {is_default}"
assert num_loads >= 1, f"Expected NumberLoads >= 1, got {num_loads}"

# --- Result ---
result["function"] = "SapModel.SourceMass.GetMassSource"
result["mass_from_elements"] = mass_from_elements
result["mass_from_loads"] = mass_from_loads
result["is_default"] = is_default
result["num_loads"] = num_loads
result["byref_layout"] = "[MassFromElements, MassFromMasses, MassFromLoads, IsDefault, NumberLoads, LoadPat[], SF[], ret_code]"
result["status"] = "verified"
