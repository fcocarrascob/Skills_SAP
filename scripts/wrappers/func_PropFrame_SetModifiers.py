# ============================================================
# Wrapper: SapModel.PropFrame.SetModifiers
# Category: PropFrame
# Description: Set stiffness modifiers (cracked sections, etc.)
# Verified: 2026-03-21
# Prerequisites: Model open, frame section defined
# ============================================================
"""
Usage: Assigns section property modifiers to a frame section.
       Commonly used for cracked-section analysis of reinforced
       concrete (e.g., 0.5*Ig for beams, 0.7*Ig for columns).

API Signature:
  SapModel.PropFrame.SetModifiers(Name, Value)

ByRef Output:
  Returns tuple: (value_out, ret_code)
  ret_code is raw[-1] (0=success)

Parameters:
  Name  : str      — Frame section property name
  Value : float[8] — Modifier array:
                      [0]=Area, [1]=Shear-AS2, [2]=Shear-AS3,
                      [3]=Torsion, [4]=I22, [5]=I33,
                      [6]=Mass, [7]=Weight
                      1.0=no modification, 0.5=50% stiffness, etc.
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30x60", "CONC_TEST", 0.6, 0.3)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_50x50", "CONC_TEST", 0.5, 0.5)
assert ret == 0

# --- Target function: cracked beam (0.5*Ig) ---
# ACI 318: beams 0.35*Ig, columns 0.70*Ig
# SetModifiers returns ByRef: (value_out, ret_code)
beam_mods = [1.0, 1.0, 1.0, 1.0, 0.35, 0.35, 1.0, 1.0]
raw = SapModel.PropFrame.SetModifiers("BEAM_30x60", beam_mods)
ret_code = raw[-1]
assert ret_code == 0, f"SetModifiers(beam) failed with ret_code={ret_code}, raw={raw}"

# Cracked columns (0.70*Ig)
col_mods = [1.0, 1.0, 1.0, 1.0, 0.70, 0.70, 1.0, 1.0]
raw_col = SapModel.PropFrame.SetModifiers("COL_50x50", col_mods)
ret_code = raw_col[-1]
assert ret_code == 0, f"SetModifiers(col) failed with ret_code={ret_code}, raw={raw_col}"

# --- Verification ---
# Read back modifiers
raw = SapModel.PropFrame.GetModifiers("BEAM_30x60", [])
ret_code = raw[-1]
assert ret_code == 0, f"GetModifiers failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetModifiers"
result["beam_modifiers"] = beam_mods
result["col_modifiers"] = col_mods
result["status"] = "verified"
