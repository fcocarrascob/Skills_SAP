# ============================================================
# Wrapper: SapModel.PropArea.GetModifiers
# Category: PropArea
# Description: Retrieve stiffness modifiers for an area property
# Verified: 2026-03-28
# Prerequisites: Model open, area property with modifiers
# ============================================================
"""
Usage: Reads back the stiffness modification factors for an area property.

API Signature:
  SapModel.PropArea.GetModifiers(Name, Value)

ByRef Output:
  [Value[10], ret_code]

Parameters:
  Name  : str       — Area section property name
  Value : float[10] — (ByRef out) Modifier array
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_AGM", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_AGM", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("WALL_MOD", 1, True, "CONC_AGM", 0, 0.25, 0.25)
assert ret == 0

# Set known modifiers
set_mods = [1.0, 1.0, 1.0, 0.70, 0.70, 0.70, 1.0, 1.0, 1.0, 1.0]
raw_sm = SapModel.PropArea.SetModifiers("WALL_MOD", set_mods)
assert (raw_sm[-1] if isinstance(raw_sm, (list, tuple)) else raw_sm) == 0

# --- Target function ---
raw = SapModel.PropArea.GetModifiers("WALL_MOD", [0.0]*10)
ret_code = raw[-1]
assert ret_code == 0, f"GetModifiers failed: {ret_code}"

got_mods = list(raw[0])
assert abs(got_mods[3] - 0.70) < 0.01, f"m11 mismatch: expected 0.70, got {got_mods[3]}"

# --- Result ---
result["function"] = "SapModel.PropArea.GetModifiers"
result["section"] = "WALL_MOD"
result["modifiers"] = got_mods
result["byref_layout"] = "[Value[10], ret_code]"
result["status"] = "verified"
