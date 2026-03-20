# ============================================================
# Wrapper: SapModel.SelectObj.CoordinateRange
# Category: Select
# Description: Select objects within a coordinate bounding box
# Verified: 2026-03-20
# Prerequisites: Model open, objects exist in range
# ============================================================
"""
Usage: Selects all objects (points, frames, areas) within a rectangular
       coordinate range (bounding box). Useful for batch operations on
       geometric regions of a model.

API Signature:
  SapModel.SelectObj.CoordinateRange(XMin, XMax, YMin, YMax,
      ZMin, ZMax, Deselect, CSys, IncludeIntersections,
      IncludePoints, IncludeFrames, IncludeAreas, IncludeSolids,
      IncludeLinks)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  XMin, XMax : float — X range [L]
  YMin, YMax : float — Y range [L]
  ZMin, ZMax : float — Z range [L]
  Deselect   : bool  — False=select, True=deselect matching objects
  CSys       : str   — Coordinate system (default="Global")
  IncludeIntersections: bool — Include objects intersecting range (default=True)
  IncludePoints  : bool — Select points (default=True)
  IncludeFrames  : bool — Select frames (default=True)
  IncludeAreas   : bool — Select areas (default=True)
  IncludeSolids  : bool — Select solids (default=True)
  IncludeLinks   : bool — Select links (default=True)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, section, and 3 frames ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

# Frame 1: X = 0 to 5 (fully inside range)
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord(F1) failed: {raw[-1]}"

# Frame 2: X = 3 to 8 (partially inside range)
raw = SapModel.FrameObj.AddByCoord(3, 0, 0, 8, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord(F2) failed: {raw[-1]}"

# Frame 3: X = 10 to 15 (outside range)
raw = SapModel.FrameObj.AddByCoord(10, 0, 0, 15, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord(F3) failed: {raw[-1]}"

total_frames = SapModel.FrameObj.Count()
assert total_frames == 3, f"Expected 3 frames, got {total_frames}"

# Clear any selection first
ret = SapModel.SelectObj.ClearSelection()
assert ret == 0, f"ClearSelection failed: {ret}"

# --- Target function: select objects in X=[0, 6] ---
ret = SapModel.SelectObj.CoordinateRange(
    0.0, 6.0,    # XMin, XMax
    -1.0, 1.0,   # YMin, YMax
    -1.0, 1.0,   # ZMin, ZMax
    False,        # Deselect = False (select)
    "Global"      # CSys
)
assert ret == 0, f"CoordinateRange failed: {ret}"

# --- Verification ---
# Get selected frames
raw = SapModel.SelectObj.GetSelected(0, [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetSelected failed: {ret_code}"
num_selected = raw[0]

# Should have selected at least 2 frames and their points
# (Frame 1 fully inside, Frame 2 intersects range)
assert num_selected > 0, f"Expected some selected objects, got {num_selected}"

# --- Result ---
result["function"] = "SapModel.SelectObj.CoordinateRange"
result["total_frames"] = total_frames
result["num_selected_objects"] = num_selected
result["status"] = "verified"
