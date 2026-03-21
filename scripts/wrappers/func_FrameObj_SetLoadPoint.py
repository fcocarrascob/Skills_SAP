# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadPoint
# Category: Load_Assignment
# Description: Apply a concentrated point load along a frame element
# Verified: 2026-03-21
# Prerequisites: Model open, frame exists, load pattern defined
# ============================================================
"""
Usage: Assigns a concentrated (point) load at a specified location
       along a frame element.

API Signature:
  SapModel.FrameObj.SetLoadPoint(Name, LoadPat, MyType, Dir,
      Dist, Val, CSys, RelDist, Replace, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Frame object name
  LoadPat  : str   — Load pattern name
  MyType   : int   — 1=Force, 2=Moment
  Dir      : int   — Direction: 1=Local1, 2=Local2, 3=Local3,
                      4=X, 5=Y, 6=Z, 7=ProjX, 8=ProjY, 9=ProjZ,
                      10=Gravity, 11=ProjGravity
  Dist     : float — Distance to load location (relative or absolute)
  Val      : float — Load value [F] or [FL]
  CSys     : str   — Coordinate system (default="Global")
  RelDist  : bool  — True=relative (0-1), False=absolute (default=True)
  Replace  : bool  — True=replace existing loads (default=True)
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "SEC_TEST", "")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Supports
raw_pts = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i, pt_j = raw_pts[0], raw_pts[1]
ret_r = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert ret_r[-1] == 0
ret_r = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert ret_r[-1] == 0

# Load pattern
ret = SapModel.LoadPatterns.Add("PT_LOAD", 3, 0)  # Live
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: point load at mid-span ---
# -50 kN in gravity direction at 50% of span
ret = SapModel.FrameObj.SetLoadPoint(
    frame_name, "PT_LOAD",
    1,      # MyType: Force
    10,     # Dir: Gravity
    0.5,    # Dist: mid-span (relative)
    -50     # Val: -50 kN
)
assert ret == 0, f"SetLoadPoint(midspan) failed: {ret}"

# Point load at quarter-span
ret = SapModel.FrameObj.SetLoadPoint(
    frame_name, "PT_LOAD",
    1,      # Force
    10,     # Gravity
    0.25,   # Dist: quarter-span
    -25,    # Val: -25 kN
    "Global", True, False  # Don't replace — add to existing
)
assert ret == 0, f"SetLoadPoint(quarter) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadPoint"
result["frame_name"] = frame_name
result["loads_applied"] = ["-50 kN at mid-span", "-25 kN at quarter-span"]
result["status"] = "verified"
