# ============================================================
# Wrapper: SapModel.File.NewBeam
# Category: File
# Description: Create a simply-supported beam template
# Verified: 2026-03-21
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new beam model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.NewBeam(NumberSpans, SpanLength, Restraint, Beam)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  NumberSpans : int   — Number of spans
  SpanLength  : float — Length of each span [L]
  Restraint   : bool  — True=add support restraints at span ends (default=True)
  Beam        : str   — Frame section name ("Default" or defined)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: 3-span beam ---
ret = SapModel.File.NewBeam(3, 30)
assert ret == 0, f"NewBeam failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
point_count = SapModel.PointObj.Count()
assert frame_count == 3, f"Expected 3 frames (spans), got {frame_count}"
assert point_count == 4, f"Expected 4 points (supports), got {point_count}"

# --- Result ---
result["function"] = "SapModel.File.NewBeam"
result["num_spans"] = 3
result["frame_count"] = frame_count
result["point_count"] = point_count
result["status"] = "verified"
