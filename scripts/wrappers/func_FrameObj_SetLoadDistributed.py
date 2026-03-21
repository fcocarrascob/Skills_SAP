# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadDistributed
# Category: Load_Assignment
# Description: Apply uniform/trapezoidal distributed loads on frames
# Verified: 2026-03-21
# Prerequisites: Model open, frame exists, load pattern defined
# ============================================================
"""
Usage: Assigns distributed loads (uniform or trapezoidal) along a
       frame element in a specified load pattern.

API Signature:
  SapModel.FrameObj.SetLoadDistributed(Name, LoadPat, MyType, Dir,
      Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Frame object name
  LoadPat  : str   — Load pattern name
  MyType   : int   — 1=Force per unit length, 2=Moment per unit length
  Dir      : int   — Direction: 1=Local1, 2=Local2, 3=Local3,
                      4=X, 5=Y, 6=Z, 7=ProjX, 8=ProjY, 9=ProjZ,
                      10=Gravity, 11=ProjGravity
  Dist1    : float — Start distance (relative or absolute)
  Dist2    : float — End distance (relative or absolute)
  Val1     : float — Load value at start [F/L] or [FL/L]
  Val2     : float — Load value at end [F/L] or [FL/L]
  CSys     : str   — Coordinate system (default="Global")
  RelDist  : bool  — True=distances are relative (0-1), False=absolute (default=True)
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

# Simply supported beam
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "SEC_TEST", "")
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
ret = SapModel.LoadPatterns.Add("DL_DIST", 1, 0)  # Dead
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: uniform load over full span ---
# -10 kN/m in gravity direction (full span, relative distances 0 to 1)
ret = SapModel.FrameObj.SetLoadDistributed(
    frame_name, "DL_DIST",
    1,     # MyType: Force per unit length
    10,    # Dir: Gravity direction
    0, 1,  # Dist1, Dist2 (relative: start to end)
    -10, -10  # Val1, Val2 (uniform -10 kN/m)
)
assert ret == 0, f"SetLoadDistributed(uniform) failed: {ret}"

# --- Target function: trapezoidal load ---
ret = SapModel.LoadPatterns.Add("LL_TRAP", 3, 0)  # Live
assert ret == 0
ret = SapModel.FrameObj.SetLoadDistributed(
    frame_name, "LL_TRAP",
    1,     # Force
    10,    # Gravity
    0, 1,
    -5, -15  # Trapezoidal: 5 kN/m at start, 15 kN/m at end
)
assert ret == 0, f"SetLoadDistributed(trapezoidal) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadDistributed"
result["frame_name"] = frame_name
result["loads_applied"] = ["DL_DIST (uniform -10 kN/m)", "LL_TRAP (trapezoidal -5 to -15 kN/m)"]
result["status"] = "verified"
