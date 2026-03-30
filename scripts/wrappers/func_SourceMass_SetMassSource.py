# ============================================================
# Wrapper: SapModel.SourceMass.SetMassSource
# Category: Mass_Source
# Description: Add or reinitialize a mass source definition
# Verified: 2026-03-28
# Prerequisites: Model open, load patterns defined
# ============================================================
"""
Usage: Creates or reinitializes a mass source specifying which
       elements and load patterns contribute to the model mass.
       Essential for seismic and modal analysis workflows.

API Signature:
  SapModel.SourceMass.SetMassSource(Name, MassFromElements,
    MassFromMasses, MassFromLoads, IsDefault,
    NumberLoads, LoadPat[], SF[])

ByRef Output:
  [LoadPat[], SF[], ret_code]

Parameters:
  Name             : str    — Mass source name (creates if new)
  MassFromElements : bool   — Include element self mass
  MassFromMasses   : bool   — Include assigned masses
  MassFromLoads    : bool   — Include specified load patterns
  IsDefault        : bool   — Set as default mass source
  NumberLoads      : int    — Number of load patterns
  LoadPat          : str[]  — Load pattern names
  SF               : float[] — Scale factors for each pattern
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: ensure DEAD pattern exists ---
# DEAD is auto-created in blank model

# --- Target function: create mass source with DEAD×1.0 ---
raw = SapModel.SourceMass.SetMassSource(
    "MASS_SISMICO",  # Name
    True,            # MassFromElements
    True,            # MassFromMasses
    True,            # MassFromLoads
    True,            # IsDefault
    1,               # NumberLoads
    ["DEAD"],        # LoadPat
    [1.0]            # SF
)
ret_code = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret_code == 0, f"SetMassSource failed: {raw}"

# Create second mass source with multiple patterns
ret = SapModel.LoadPatterns.Add("LIVE", 3)
assert ret == 0

raw2 = SapModel.SourceMass.SetMassSource(
    "MASS_PLUS_LIVE",
    True, True, True,
    False,            # Not default
    2,                # NumberLoads
    ["DEAD", "LIVE"], # LoadPat
    [1.0, 0.25]       # SF (DEAD×1.0 + LIVE×0.25)
)
ret_code2 = raw2[-1] if isinstance(raw2, (list, tuple)) else raw2
assert ret_code2 == 0, f"SetMassSource(MASS_PLUS_LIVE) failed: {raw2}"

# --- Verification ---
count = SapModel.SourceMass.Count()
assert count >= 2, f"Expected at least 2 mass sources, got {count}"

# --- Result ---
result["function"] = "SapModel.SourceMass.SetMassSource"
result["mass_sources_created"] = ["MASS_SISMICO", "MASS_PLUS_LIVE"]
result["count"] = count
result["status"] = "verified"
