# ============================================================
# Wrapper: SapModel.File.NewWall
# Category: File
# Description: Create a shear wall template
# Verified: 2026-03-21
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Creates a new wall model from a parametric template.
       This replaces any current model — do not use to add to
       an existing model.

API Signature:
  SapModel.File.NewWall(NumberXDivisions, DivisionWidthX,
      NumberZDivisions, DivisionWidthZ, Restraint, Area)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  NumberXDivisions : int   — Number of area elements in global X
  DivisionWidthX   : float — Width of each area element in X [L]
  NumberZDivisions : int   — Number of area elements in global Z (height)
  DivisionWidthZ   : float — Height of each area element in Z [L]
  Restraint        : bool  — True=base restraints (default=True)
  Area             : str   — Shell section name ("Default" or defined)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: 6x6 wall ---
ret = SapModel.File.NewWall(6, 4, 6, 4)
assert ret == 0, f"NewWall failed: {ret}"

# --- Verification ---
area_count = SapModel.AreaObj.Count()
point_count = SapModel.PointObj.Count()
assert area_count == 36, f"Expected 36 areas (6x6 grid), got {area_count}"
assert point_count > 0, f"Expected points in wall, got {point_count}"

# --- Result ---
result["function"] = "SapModel.File.NewWall"
result["area_count"] = area_count
result["point_count"] = point_count
result["status"] = "verified"
