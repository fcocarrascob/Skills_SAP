# ============================================================
# Wrapper: SapModel.PropMaterial.GetMaterial
# Category: PropMaterial
# Description: Get material type and metadata for an existing material
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Retrieves the material type, color, notes and GUID for an
       existing material definition.

API Signature:
  SapModel.PropMaterial.GetMaterial(Name, MatType, Color, Notes, GUID)

ByRef Output:
  [MatType, Color, Notes, GUID, ret_code]

Parameters:
  Name    : str — Existing material name
  MatType : int — (ByRef out) eMatType enum (1=Steel, 2=Concrete, etc.)
  Color   : int — (ByRef out) Display color
  Notes   : str — (ByRef out) Notes
  GUID    : str — (ByRef out) GUID
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create materials ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_GET", 1)
assert ret == 0, f"SetMaterial(Steel) failed: {ret}"

ret = SapModel.PropMaterial.SetMaterial("CONC_GET", 2)
assert ret == 0, f"SetMaterial(Concrete) failed: {ret}"

# --- Target function: get material info ---
raw = SapModel.PropMaterial.GetMaterial("STEEL_GET", 0, 0, "", "")
ret_code = raw[-1]
assert ret_code == 0, f"GetMaterial(Steel) failed: {ret_code}"
steel_type = raw[0]  # Should be 1 (Steel)
assert steel_type == 1, f"Expected MatType=1 (Steel), got {steel_type}"

raw2 = SapModel.PropMaterial.GetMaterial("CONC_GET", 0, 0, "", "")
ret_code2 = raw2[-1]
assert ret_code2 == 0, f"GetMaterial(Concrete) failed: {ret_code2}"
conc_type = raw2[0]  # Should be 2 (Concrete)
assert conc_type == 2, f"Expected MatType=2 (Concrete), got {conc_type}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.GetMaterial"
result["steel_mat_type"] = steel_type
result["conc_mat_type"] = conc_type
result["byref_layout"] = "[MatType, Color, Notes, GUID, ret_code]"
result["status"] = "verified"
