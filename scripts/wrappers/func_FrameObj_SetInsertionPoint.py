# ============================================================
# Wrapper: SapModel.FrameObj.SetInsertionPoint_1
# Category: Object_Model
# Description: Assign cardinal point and joint offsets to frame objects
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Assigns the frame section insertion point (cardinal point) and
       end joint offsets. Controls the relative position of the section
       with respect to the frame element line.

API Signature:
  SapModel.FrameObj.SetInsertionPoint_1(Name, CardinalPoint, Mirror2, Mirror3,
      StiffTransform, Offset1, Offset2, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name           : str      — Frame object name
  CardinalPoint  : int      — 1=BotLeft..9=TopRight, 10=Centroid, 11=ShearCenter
  Mirror2        : bool     — Mirror about local 2 axis
  Mirror3        : bool     — Mirror about local 3 axis
  StiffTransform : bool     — Transform stiffness for offsets
  Offset1        : float[3] — I-End offsets [L] in CSys directions
  Offset2        : float[3] — J-End offsets [L] in CSys directions
  CSys           : str      — "Local" or named coordinate system
  ItemType       : int      — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: Top-Center cardinal point (8) with offsets ---
offset1 = [0.0, 0.0, 0.0]
offset2 = [0.0, 0.0, 0.0]

raw_set = SapModel.FrameObj.SetInsertionPoint_1(
    beam_name, 8, False, False, True, offset1, offset2
)
# Returns [Offset1[], Offset2[], ret_code]
assert raw_set[-1] == 0, f"SetInsertionPoint_1 ret_code={raw_set[-1]}, raw={raw_set}"

# --- Verification via GetInsertionPoint_1 ---
raw = SapModel.FrameObj.GetInsertionPoint_1(
    beam_name, 0, False, False, False, [], [], ""
)
ret_code = raw[-1]
assert ret_code == 0, f"GetInsertionPoint_1 failed: {ret_code}"
cardinal = raw[0]
assert cardinal == 8, f"Expected cardinal=8 (TopCenter), got {cardinal}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetInsertionPoint_1"
result["beam_name"] = beam_name
result["cardinal_point"] = cardinal
result["status"] = "verified"
