# ============================================================
# Wrapper: SapModel.File.New2DFrame
# Category: File
# Description: Create a 2D portal/braced frame from template
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new 2D frame model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.New2DFrame(TempType, NumberStorys, StoryHeight,
      NumberBays, BayWidth, Restraint, Beam, Column, Brace)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  TempType      : int  — e2DFrameType: 0=PortalFrame, 1=ConcentricBraced, 2=EccentricBraced
  NumberStorys   : int  — Number of stories
  StoryHeight    : float — Height of each story [L]
  NumberBays     : int  — Number of bays
  BayWidth       : float — Width of each bay [L]
  Restraint      : bool — True=add base restraints (default=True)
  Beam           : str  — Beam section name ("Default" or defined section)
  Column         : str  — Column section name ("Default" or defined section)
  Brace          : str  — Brace section name ("Default" or defined section, not for portal)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: Portal frame ---
# 3 stories, 12 ft each, 3 bays, 28 ft each
ret = SapModel.File.New2DFrame(0, 3, 12, 3, 28)
assert ret == 0, f"New2DFrame(Portal) failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
point_count = SapModel.PointObj.Count()
assert frame_count > 0, f"Expected frames in 2D portal, got {frame_count}"
assert point_count > 0, f"Expected points in 2D portal, got {point_count}"

# --- Result ---
result["function"] = "SapModel.File.New2DFrame"
result["template_type"] = "PortalFrame"
result["frame_count"] = frame_count
result["point_count"] = point_count
result["status"] = "verified"
