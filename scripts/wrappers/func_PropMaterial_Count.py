# ============================================================
# Wrapper: SapModel.PropMaterial.Count
# Category: PropMaterial
# Description: Get number of material properties
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined material properties.
       Optionally filter by material type.

API Signature:
  SapModel.PropMaterial.Count(MatType)

ByRef Output:
  count (direct return, integer)

Parameters:
  MatType : int — (optional) 0=All, 1=Steel, 2=Concrete, etc.
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_CNT", 1)
assert ret == 0
ret = SapModel.PropMaterial.SetMaterial("CONC_CNT", 2)
assert ret == 0

# --- Target function ---
count_all = SapModel.PropMaterial.Count()
assert count_all >= 2, f"Expected at least 2 materials, got {count_all}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.Count"
result["count_all"] = count_all
result["status"] = "verified"
