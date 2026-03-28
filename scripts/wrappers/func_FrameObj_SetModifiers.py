# ============================================================
# Wrapper: SapModel.FrameObj.SetModifiers
# Category: FrameObj
# Description: Set stiffness modifiers for a frame object
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Assigns stiffness modification factors to a frame element.
       Essential for seismic design (cracked section analysis).
       Common values: beams 0.35×I, columns 0.70×I per ACI 318.

API Signature:
  SapModel.FrameObj.SetModifiers(Name, Value)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name  : str      — Frame object name
  Value : float[8] — Modifier array:
    [0]=Area, [1]=AS2(shear), [2]=AS3(shear),
    [3]=Torsion, [4]=I22, [5]=I33,
    [6]=Mass, [7]=Weight
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_MOD", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_MOD", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_MOD", "CONC_MOD", 0.6, 0.3)
assert ret == 0

# Create beam
raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 6, 0, 3, "", "BEAM_MOD", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: apply cracked section modifiers (beam) ---
# ACI 318: beams I = 0.35×Ig
beam_mods = [1.0, 1.0, 1.0, 1.0, 0.35, 0.35, 1.0, 1.0]
raw_bm = SapModel.FrameObj.SetModifiers(beam_name, beam_mods)
ret_bm = raw_bm[-1] if isinstance(raw_bm, (list, tuple)) else raw_bm
assert ret_bm == 0, f"SetModifiers(beam) failed: {ret_bm}"

# Create column with column modifiers
raw2 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "BEAM_MOD", "")
col_name = raw2[0]
assert raw2[-1] == 0

# ACI 318: columns I = 0.70×Ig
col_mods = [1.0, 1.0, 1.0, 1.0, 0.70, 0.70, 1.0, 1.0]
raw_cm = SapModel.FrameObj.SetModifiers(col_name, col_mods)
ret_cm = raw_cm[-1] if isinstance(raw_cm, (list, tuple)) else raw_cm
assert ret_cm == 0, f"SetModifiers(column) failed: {ret_cm}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetModifiers"
result["beam"] = beam_name
result["beam_modifiers"] = beam_mods
result["column"] = col_name
result["column_modifiers"] = col_mods
result["status"] = "verified"
