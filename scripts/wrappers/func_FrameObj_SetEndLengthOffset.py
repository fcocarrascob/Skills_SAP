# ============================================================
# Wrapper: SapModel.FrameObj.SetEndLengthOffset
# Category: Object_Model
# Description: Set rigid-zone offsets at beam-column joints
# Verified: 2026-03-21
# Prerequisites: Model open, frame element exists
# ============================================================
"""
Usage: Assigns rigid-end zone offsets to a frame element. This
       simulates the rigid zone at beam-column intersections where
       the actual flexible length is shorter than the centerline length.

API Signature:
  SapModel.FrameObj.SetEndLengthOffset(Name, AutoOffset, Length1,
      Length2, RzFactor, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name       : str   — Frame object name
  AutoOffset : bool  — True=auto-calculate offsets from connected objects
  Length1    : float — Rigid-zone length at i-end [L] (ignored if AutoOffset=True)
  Length2    : float — Rigid-zone length at j-end [L] (ignored if AutoOffset=True)
  RzFactor   : float — Rigid-zone factor (0-1, typically 0.5 for half-rigid)
  ItemType   : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("COL_50", "CONC_TEST", 0.5, 0.5)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_30x60", "CONC_TEST", 0.6, 0.3)
assert ret == 0

# Simple portal
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3.5, "", "COL_50", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(6, 0, 0, 6, 0, 3.5, "", "COL_50", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3.5, 6, 0, 3.5, "", "BEAM_30x60", "")
beam_name = beam[0]
assert beam[-1] == 0

# --- Target function: manual rigid-end offsets ---
# Offset = half column depth = 0.25m at each end, RzFactor=1 (fully rigid)
ret = SapModel.FrameObj.SetEndLengthOffset(
    beam_name, False,  # Not auto
    0.25,   # Length1 (i-end offset)
    0.25,   # Length2 (j-end offset)
    1.0     # RzFactor (fully rigid)
)
assert ret == 0, f"SetEndLengthOffset(manual) failed: {ret}"

# --- Target function: auto offset on column ---
ret = SapModel.FrameObj.SetEndLengthOffset(
    col1[0], True, 0, 0, 0.5  # Auto, half-rigid
)
assert ret == 0, f"SetEndLengthOffset(auto) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetEndLengthOffset"
result["beam_name"] = beam_name
result["manual_offsets"] = [0.25, 0.25]
result["rz_factor"] = 1.0
result["status"] = "verified"
