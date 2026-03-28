# ============================================================
# Wrapper: SapModel.PropArea.SetModifiers
# Category: PropArea
# Description: Set stiffness modifiers for an area property
# Verified: 2026-03-28
# Prerequisites: Model open, area property defined
# ============================================================
"""
Usage: Assigns stiffness modification factors to an area property.
       Applied to ALL area objects using this property.
       Array of 10 modifiers for shell elements.

API Signature:
  SapModel.PropArea.SetModifiers(Name, Value)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name  : str       — Area section property name
  Value : float[10] — Modifier array:
    [0]=f11, [1]=f22, [2]=f12, [3]=m11, [4]=m22,
    [5]=m12, [6]=v13, [7]=v23, [8]=mass, [9]=weight
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_AM", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_AM", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

ret = SapModel.PropArea.SetShell_1("SLAB_MOD", 1, True, "CONC_AM", 0, 0.2, 0.2)
assert ret == 0, f"SetShell_1 failed: {ret}"

# --- Target function ---
# Cracked slab modifiers: reduce bending stiffness
slab_mods = [1.0, 1.0, 1.0, 0.25, 0.25, 0.25, 1.0, 1.0, 1.0, 1.0]
raw_sm = SapModel.PropArea.SetModifiers("SLAB_MOD", slab_mods)
ret_sm = raw_sm[-1] if isinstance(raw_sm, (list, tuple)) else raw_sm
assert ret_sm == 0, f"SetModifiers failed: {ret_sm}"

# --- Result ---
result["function"] = "SapModel.PropArea.SetModifiers"
result["section"] = "SLAB_MOD"
result["modifiers"] = slab_mods
result["status"] = "verified"
