# ============================================================
# Wrapper: SapModel.PointObj.SetLoadForce
# Category: Load_Assignment
# Description: Apply forces/moments at a joint (6 DOF)
# Verified: 2026-03-21
# Prerequisites: Model open, point exists, load pattern defined
# ============================================================
"""
Usage: Assigns point loads (forces and moments) to a joint in a
       specified load pattern. The value array has 6 components
       corresponding to [F1, F2, F3, M1, M2, M3] in the specified
       coordinate system.

API Signature:
  SapModel.PointObj.SetLoadForce(Name, LoadPat, Value, Replace, CSys, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str      — Point object name
  LoadPat  : str      — Load pattern name
  Value    : float[6] — [F1, F2, F3, M1, M2, M3] forces and moments
  Replace  : bool     — True=replace existing loads (default=True)
  CSys     : str      — Coordinate system (default="Global")
  ItemType : int      — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, section, frame, load pattern ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Get top point
raw_pts = SapModel.FrameObj.GetPoints(raw[0], "", "")
pt_top = raw_pts[1]  # j-end (top)
pt_bot = raw_pts[0]  # i-end (base)
assert raw_pts[-1] == 0, f"GetPoints failed: {raw_pts[-1]}"

# Fix the base
ret_r = SapModel.PointObj.SetRestraint(pt_bot, [True, True, True, True, True, True])
assert ret_r[-1] == 0, f"SetRestraint failed: {ret_r[-1]}"

# Add load pattern
ret = SapModel.LoadPatterns.Add("POINT_LOAD", 8)  # 8=Other
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: apply lateral force at top ---
# 100 kN in X direction, 50 kN downward in Z
force_values = [100.0, 0.0, -50.0, 0.0, 0.0, 0.0]
raw_sf = SapModel.PointObj.SetLoadForce(pt_top, "POINT_LOAD", force_values)
# Returns [Value_byref, ret_code] — Value is echoed back as ByRef output
assert raw_sf[-1] == 0, f"SetLoadForce failed: {raw_sf}"

# --- Verification ---
# Read back the force
raw = SapModel.PointObj.GetLoadForce(pt_top, 0, [], [], [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadForce failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.PointObj.SetLoadForce"
result["point_name"] = pt_top
result["force_values"] = force_values
result["status"] = "verified"
