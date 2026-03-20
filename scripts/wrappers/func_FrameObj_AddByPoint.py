# ============================================================
# Wrapper: SapModel.FrameObj.AddByPoint
# Category: Object_Model
# Description: Create a frame element between two existing points
# Verified: 2026-03-20
# Prerequisites: Model open, material/section defined, points exist
# ============================================================
"""
Usage: Creates a frame (beam/column/brace) between two existing point
       objects. Unlike AddByCoord, this reuses existing points to avoid
       duplicate joints and ensures connectivity.

API Signature:
  SapModel.FrameObj.AddByPoint(Point1, Point2, Name, PropName, UserName)

ByRef Output:
  raw[0]  = Name (name assigned by SAP2000)
  raw[-1] = ret_code (0=success)

Parameters:
  Point1   : str — Start point name (point i)
  Point2   : str — End point name (point j)
  Name     : str — Output: assigned frame name (""=auto-assign)
  PropName : str — Frame section property name
  UserName : str — User-defined name (optional)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, section, and points ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

# Create 3 points: base-left, base-right, top
raw = SapModel.PointObj.AddCartesian(0, 0, 0, "", "BASE_L")
pt_bl = raw[0]
assert raw[-1] == 0, f"AddCartesian(BASE_L) failed: {raw[-1]}"

raw = SapModel.PointObj.AddCartesian(6.0, 0, 0, "", "BASE_R")
pt_br = raw[0]
assert raw[-1] == 0, f"AddCartesian(BASE_R) failed: {raw[-1]}"

raw = SapModel.PointObj.AddCartesian(0, 0, 4.0, "", "TOP_L")
pt_tl = raw[0]
assert raw[-1] == 0, f"AddCartesian(TOP_L) failed: {raw[-1]}"

# --- Target function: create frames between points ---
# Column: base-left to top-left
raw = SapModel.FrameObj.AddByPoint(pt_bl, pt_tl, "", "SEC_TEST", "COL_1")
col_name = raw[0]
assert raw[-1] == 0, f"AddByPoint(COL_1) failed: {raw[-1]}"

# Beam: base-left to base-right
raw = SapModel.FrameObj.AddByPoint(pt_bl, pt_br, "", "SEC_TEST", "BEAM_1")
beam_name = raw[0]
assert raw[-1] == 0, f"AddByPoint(BEAM_1) failed: {raw[-1]}"

# --- Verification ---
count = SapModel.FrameObj.Count()
assert count == 2, f"Expected 2 frames, got {count}"

# Verify frame endpoints match input points
raw = SapModel.FrameObj.GetPoints(col_name, "", "")
assert raw[-1] == 0, f"GetPoints failed: {raw[-1]}"
assert raw[0] == pt_bl or raw[1] == pt_tl, f"Column endpoints mismatch"

# --- Result ---
result["function"] = "SapModel.FrameObj.AddByPoint"
result["frames_created"] = [col_name, beam_name]
result["frame_count"] = count
result["status"] = "verified"
