# ============================================================
# Wrapper: SapModel.FrameObj.GetModifiers
# Category: FrameObj
# Description: Retrieve stiffness modifiers for a frame object
# Verified: 2026-03-28
# Prerequisites: Model open, frame with modifiers
# ============================================================
"""
Usage: Reads back the stiffness modification factors from a frame.

API Signature:
  SapModel.FrameObj.GetModifiers(Name, Value)

ByRef Output:
  [Value[8], ret_code]

Parameters:
  Name  : str      — Frame object name
  Value : float[8] — (ByRef out) Modifier array
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_GM", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_GM", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_GM", "CONC_GM", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_GM", "")
frame_name = raw[0]
assert raw[-1] == 0

# Set known modifiers
set_mods = [1.0, 1.0, 1.0, 0.5, 0.35, 0.35, 1.0, 1.0]
raw_sm = SapModel.FrameObj.SetModifiers(frame_name, set_mods)
assert (raw_sm[-1] if isinstance(raw_sm, (list, tuple)) else raw_sm) == 0

# --- Target function ---
raw = SapModel.FrameObj.GetModifiers(frame_name, [0.0]*8)
ret_code = raw[-1]
assert ret_code == 0, f"GetModifiers failed: {ret_code}"

got_mods = list(raw[0])
# Verify I22 and I33 modifiers
assert abs(got_mods[4] - 0.35) < 0.01, f"I22 mismatch: expected 0.35, got {got_mods[4]}"
assert abs(got_mods[5] - 0.35) < 0.01, f"I33 mismatch: expected 0.35, got {got_mods[5]}"

# --- Result ---
result["function"] = "SapModel.FrameObj.GetModifiers"
result["frame_name"] = frame_name
result["modifiers"] = got_mods
result["byref_layout"] = "[Value[8], ret_code]"
result["status"] = "verified"
