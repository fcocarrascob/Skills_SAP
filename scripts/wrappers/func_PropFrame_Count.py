# ============================================================
# Wrapper: SapModel.PropFrame.Count
# Category: PropFrame
# Description: Get number of frame section properties
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined frame section properties.
       Optionally filter by section type.

API Signature:
  SapModel.PropFrame.Count(PropType)

ByRef Output:
  count (direct return, integer)

Parameters:
  PropType : int — (optional) 0=All, 1=ISection, 2=Channel, 3=Tee,
                    4=Angle, 5=DblAngle, 6=Box, 7=Pipe, 8=Rectangular,
                    9=Circle, etc.
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_CT", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("CT_RECT", "MAT_CT", 0.3, 0.3)
assert ret == 0
ret = SapModel.PropFrame.SetCircle("CT_CIRC", "MAT_CT", 0.3)
assert ret == 0

# --- Target function ---
count_all = SapModel.PropFrame.Count()
assert count_all >= 2, f"Expected at least 2 sections, got {count_all}"

# --- Result ---
result["function"] = "SapModel.PropFrame.Count"
result["count_all"] = count_all
result["status"] = "verified"
