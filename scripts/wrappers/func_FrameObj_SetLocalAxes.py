# ============================================================
# Wrapper: SapModel.FrameObj.SetLocalAxes
# Category: Object_Model
# Description: Assign local axis rotation angle to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Rotates the local 2 and 3 axes of a frame object about its local 1 axis.
       Used for orienting non-symmetric sections (I-beams, channels, angles).

API Signature:
  SapModel.FrameObj.SetLocalAxes(Name, Ang, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str   — Frame object name
  Ang      : float — Rotation angle [deg], positive = CCW about local 1
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: rotate 45 degrees ---
ret = SapModel.FrameObj.SetLocalAxes(beam_name, 45.0)
assert ret == 0, f"SetLocalAxes failed: {ret}"

# --- Verification via GetLocalAxes ---
raw = SapModel.FrameObj.GetLocalAxes(beam_name, 0.0)
ret_code = raw[-1]
assert ret_code == 0, f"GetLocalAxes failed: {ret_code}"
angle = raw[0]
assert abs(angle - 45.0) < 0.01, f"Expected 45°, got {angle}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLocalAxes"
result["beam_name"] = beam_name
result["angle_set"] = 45.0
result["angle_read"] = angle
result["status"] = "verified"
