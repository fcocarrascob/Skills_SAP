# ============================================================
# Wrapper: SapModel.File.New3DFrame
# Category: File
# Description: Create a 3D building frame from template
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new 3D frame model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.New3DFrame(TempType, NumberStorys, StoryHeight,
      NumberBaysX, BayWidthX, NumberBaysY, BayWidthY, Restraint,
      Beam, Column, Area, NumberXDivisions, NumberYDivisions)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  TempType        : int  — e3DFrameType: 0=OpenFrame, 1=PerimeterFrame, 2=BeamSlab, 3=FlatPlate
  NumberStorys     : int  — Number of stories
  StoryHeight      : float — Height per story [L]
  NumberBaysX      : int  — Bays in X direction
  BayWidthX        : float — Bay width in X [L]
  NumberBaysY      : int  — Bays in Y direction
  BayWidthY        : float — Bay width in Y [L]
  Restraint        : bool — True=base restraints (default=True)
  Beam             : str  — Beam section ("Default" or defined)
  Column           : str  — Column section ("Default" or defined)
  Area             : str  — Slab shell section ("Default" or defined, for BeamSlab/FlatPlate)
  NumberXDivisions : int  — Slab mesh in X (default=4, for BeamSlab/FlatPlate)
  NumberYDivisions : int  — Slab mesh in Y (default=4, for BeamSlab/FlatPlate)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: BeamSlab 3D frame ---
# 3 stories at 12 ft, 3 bays @ 28 ft in X, 2 bays @ 36 ft in Y
ret = SapModel.File.New3DFrame(2, 3, 12, 3, 28, 2, 36)
assert ret == 0, f"New3DFrame(BeamSlab) failed: {ret}"

# --- Verification ---
frame_count = SapModel.FrameObj.Count()
point_count = SapModel.PointObj.Count()
area_count = SapModel.AreaObj.Count()
assert frame_count > 0, f"Expected frames in 3D frame, got {frame_count}"
assert point_count > 0, f"Expected points in 3D frame, got {point_count}"
assert area_count > 0, f"Expected areas in BeamSlab, got {area_count}"

# --- Result ---
result["function"] = "SapModel.File.New3DFrame"
result["template_type"] = "BeamSlab"
result["frame_count"] = frame_count
result["point_count"] = point_count
result["area_count"] = area_count
result["status"] = "verified"
