# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadTemperature
# Category: Load_Assignment
# Description: Apply thermal loads on frame elements
# Verified: pending
# Prerequisites: Model open, frame exists, load pattern defined
# ============================================================
"""
Usage: Assigns temperature loads (uniform or gradient) to a frame
       element.

API Signature:
  SapModel.FrameObj.SetLoadTemperature(Name, LoadPat, MyType,
      Val, PatternName, Replace, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name        : str   — Frame object name
  LoadPat     : str   — Load pattern name
  MyType      : int   — 1=Temperature, 2=Temperature gradient 2-2,
                         3=Temperature gradient 3-3
  Val         : float — Temperature value [T] or gradient [T/L]
  PatternName : str   — Joint pattern name (""=none)
  Replace     : bool  — True=replace existing (default=True)
  ItemType    : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("MAT_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "SEC_TEST", "")
frame_name = raw[0]
assert raw[-1] == 0

# Supports
raw_pts = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i, pt_j = raw_pts[0], raw_pts[1]
ret_r = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert ret_r[-1] == 0
ret_r = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert ret_r[-1] == 0

# Load pattern for thermal
ret = SapModel.LoadPatterns.Add("TEMP", 8, 0)  # Other
assert ret == 0

# --- Target function: uniform temperature change ---
# +30°C uniform temperature increase
ret = SapModel.FrameObj.SetLoadTemperature(
    frame_name, "TEMP",
    1,      # MyType: Temperature
    30      # Val: +30°C
)
assert ret == 0, f"SetLoadTemperature(uniform) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadTemperature"
result["frame_name"] = frame_name
result["temperature_change"] = 30
result["status"] = "verified"
