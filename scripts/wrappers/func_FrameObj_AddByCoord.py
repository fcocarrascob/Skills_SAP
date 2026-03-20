# ============================================================
# Wrapper: SapModel.FrameObj.AddByCoord
# Category: Object_Model
# Description: Add a frame element defined by endpoint coordinates
# Verified: 2026-03-20
# Prerequisites: Model open, material and section defined
# ============================================================
"""
Usage: Creates a frame (beam/column) between two coordinate points.
       Returns the name assigned to the frame.

API Signature:
  SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name, PropName, UserName, CSys)

ByRef Output:
  raw[0] = Name (name assigned by SAP2000)
  raw[-1] = ret_code (0=success)

Parameters:
  x1,y1,z1 : float — Coordinates of point i [L]
  x2,y2,z2 : float — Coordinates of point j [L]
  Name     : str   — Name (empty="auto-assign")
  PropName : str   — Frame section property name
  UserName : str   — User-defined name (empty=use Name)
  CSys     : str   — Coordinate system (default="Global")
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material and section ---
MATERIAL_NAME = "MAT_TEST"
ret = SapModel.PropMaterial.SetMaterial(MATERIAL_NAME, 2)  # 2=Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

SECTION_NAME = "SEC_TEST"
ret = SapModel.PropFrame.SetRectangle(SECTION_NAME, MATERIAL_NAME, 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

# --- Target function ---
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", SECTION_NAME, "")
frame_name = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"AddByCoord failed: {ret_code}"

# --- Verification ---
count = SapModel.FrameObj.Count()
assert count >= 1, f"Expected at least 1 frame, got {count}"

# --- Result ---
result["function"] = "SapModel.FrameObj.AddByCoord"
result["frame_name"] = frame_name
result["frame_count"] = count
result["status"] = "verified"
