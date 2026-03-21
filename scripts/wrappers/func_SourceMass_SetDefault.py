# ============================================================
# Wrapper: SapModel.SourceMass.SetDefault
# Category: Mass_Source
# Description: Set the default mass source
# Verified: 2026-03-21
# Prerequisites: Model open, mass source defined
# ============================================================
"""
Usage: Sets a named mass source as the default for analysis.
       The default mass source is used by SAP2000 to calculate
       seismic weight, modal mass, and mass participation.

IMPORTANT: The API path is SapModel.SourceMass (NOT SapModel.MassSource).

API Signature:
  SapModel.SourceMass.SetDefault(Name) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Mass source name to set as default
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites: create a mass source ---
# SetMassSource(Name, MassFromElements, MassFromMasses, MassFromLoads,
#               IsDefault, NumberLoads, LoadPat, SF)
# NOTE: Returns [LoadPat_byref, SF_byref, ret_code] — use raw[-1]
raw_ms = SapModel.SourceMass.SetMassSource(
    "SEISMIC_MASS",  # Name
    True,            # MassFromElements
    True,            # MassFromMasses
    True,            # MassFromLoads
    False,           # IsDefault (not yet)
    1,               # NumberLoads
    ["DEAD"],        # LoadPat[]
    [1.0]            # SF[] (scale factors)
)
assert raw_ms[-1] == 0, f"SetMassSource failed: {raw_ms[-1]}"

# --- Target function: set as default ---
ret = SapModel.SourceMass.SetDefault("SEISMIC_MASS")
assert ret == 0, f"SetDefault(SEISMIC_MASS) failed: {ret}"

# --- Verification: read back default ---
raw = SapModel.SourceMass.GetDefault("")
ret_code = raw[-1]
assert ret_code == 0, f"GetDefault failed: {ret_code}"
default_name = raw[0]
assert default_name == "SEISMIC_MASS", f"Expected SEISMIC_MASS, got: {default_name}"

# --- Result ---
result["function"] = "SapModel.SourceMass.SetDefault"
result["default_mass_source"] = default_name
result["status"] = "verified"
