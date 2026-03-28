# ============================================================
# Wrapper: SapModel.FrameObj.SetLoadDistributed
# Category: Object_Model
# Description: Assign distributed loads (force/moment per unit length) to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists, load pattern defined
# ============================================================
"""
Usage: Assigns distributed loads along the length of frame objects.
       Supports uniform and trapezoidal distributions, in any direction.

API Signature:
  SapModel.FrameObj.SetLoadDistributed(Name, LoadPat, MyType, Dir,
      Dist1, Dist2, Val1, Val2, CSys, RelDist, Replace, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Frame object name (or group name if ItemType=1)
  LoadPat : str   — Load pattern name
  MyType  : int   — 1=Force/length, 2=Moment/length
  Dir     : int   — Direction: 1-3=Local, 4-6=Global XYZ, 10=Gravity, 11=Projected Gravity
  Dist1   : float — Start distance (relative 0-1 or absolute [L])
  Dist2   : float — End distance (relative 0-1 or absolute [L])
  Val1    : float — Load value at start [F/L] or [FL/L]
  Val2    : float — Load value at end [F/L] or [FL/L]
  CSys    : str   — "Global" or "Local" or named coordinate system
  RelDist : bool  — True=relative distances, False=absolute
  Replace : bool  — True=replace previous loads in pattern
  ItemType: int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0, f"SetRectangle failed: {ret}"

# Create simply supported beam, 8m span
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Supports
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

# --- Target function: uniform load ---
# Full-length uniform downward load: -15 kN/m (gravity direction)
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -15, -15, "Global", True, True
)
assert ret == 0, f"SetLoadDistributed(uniform) failed: {ret}"

# --- Target function: trapezoidal load ---
# Add LIVE pattern
ret = SapModel.LoadPatterns.Add("LIVE", 3, 0, False)
assert ret == 0, f"LoadPatterns.Add(LIVE) failed: {ret}"

# Trapezoidal load from 0 to midspan: 0 kN/m -> -20 kN/m
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "LIVE", 1, 10, 0, 0.5, 0, -20, "Global", True, True
)
assert ret == 0, f"SetLoadDistributed(trapezoidal) failed: {ret}"

# --- Verification: query back via GetLoadDistributed ---
raw = SapModel.FrameObj.GetLoadDistributed(
    beam_name, 0, [], [], [], [], [], [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadDistributed failed: {ret_code}"
num_loads = raw[0]
assert num_loads >= 2, f"Expected >=2 loads, got {num_loads}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetLoadDistributed"
result["beam_name"] = beam_name
result["num_loads_assigned"] = num_loads
result["status"] = "verified"
