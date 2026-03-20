# ============================================================
# Wrapper: SapModel.File.NewBlank
# Category: File
# Description: Initialize a new blank model
# Verified: 2026-03-20
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new blank SAP2000 model. Use at the start of any
       scripting session to ensure a clean workspace.

API Signature:
  SapModel.File.NewBlank()

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()

# --- Target function ---
ret = SapModel.File.NewBlank()
assert ret == 0, f"File.NewBlank failed: {ret}"

# --- Verification ---
# Set units to confirm model is active
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed (model not active): {ret}"

# Verify model is empty
frame_count = SapModel.FrameObj.Count()
point_count = SapModel.PointObj.Count()
assert frame_count == 0, f"Expected 0 frames in blank model, got {frame_count}"
assert point_count == 0, f"Expected 0 points in blank model, got {point_count}"

# --- Result ---
result["function"] = "SapModel.File.NewBlank"
result["frame_count"] = frame_count
result["point_count"] = point_count
result["status"] = "verified"
