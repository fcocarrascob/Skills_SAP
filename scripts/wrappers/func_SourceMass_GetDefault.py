# ============================================================
# Wrapper: SapModel.SourceMass.GetDefault
# Category: Mass_Source
# Description: Retrieve the default mass source name
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the name of the default mass source.

API Signature:
  SapModel.SourceMass.GetDefault(Name)

ByRef Output:
  [Name, ret_code]

Parameters:
  Name : str — (ByRef out) Default mass source name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: get default mass source ---
raw = SapModel.SourceMass.GetDefault("")
ret_code = raw[-1]
assert ret_code == 0, f"GetDefault failed: {ret_code}"
default_name = raw[0]

# Create custom mass source as default, then verify
ret = SapModel.SourceMass.SetMassSource(
    "MY_DEFAULT", True, True, True, True, 1, ["DEAD"], [1.0]
)
assert ret == 0

raw2 = SapModel.SourceMass.GetDefault("")
assert raw2[-1] == 0
assert raw2[0] == "MY_DEFAULT", f"Expected MY_DEFAULT, got {raw2[0]}"

# --- Result ---
result["function"] = "SapModel.SourceMass.GetDefault"
result["initial_default"] = default_name
result["new_default"] = raw2[0]
result["byref_layout"] = "[Name, ret_code]"
result["status"] = "verified"
