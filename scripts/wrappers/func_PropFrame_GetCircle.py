# ============================================================
# Wrapper: SapModel.PropFrame.GetCircle
# Category: PropFrame
# Description: Retrieve circular (solid) section properties
# Verified: 2026-03-28
# Prerequisites: Model open, circular section defined
# ============================================================
"""
Usage: Reads back the properties of an existing circular frame section.

API Signature:
  SapModel.PropFrame.GetCircle(Name, FileName, MatProp, T3, Color, Notes, GUID)

ByRef Output:
  [FileName, MatProp, T3, Color, Notes, GUID, ret_code]

Parameters:
  Name     : str   — Existing section name
  FileName : str   — (ByRef out) Section file name
  MatProp  : str   — (ByRef out) Material property name
  T3       : float — (ByRef out) Diameter [L]
  Color    : int   — (ByRef out) Display color
  Notes    : str   — (ByRef out) Notes
  GUID     : str   — (ByRef out) GUID
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_C", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_C", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

T3_set = 0.5  # 500mm diameter
ret = SapModel.PropFrame.SetCircle("COL_D500", "CONC_C", T3_set)
assert ret == 0, f"SetCircle failed: {ret}"

# --- Target function ---
raw = SapModel.PropFrame.GetCircle("COL_D500", "", "", 0, 0, "", "")
ret_code = raw[-1]
assert ret_code == 0, f"GetCircle failed: {ret_code}"

mat_prop = raw[1]
T3_got = raw[2]

assert mat_prop == "CONC_C", f"Material mismatch: expected CONC_C, got {mat_prop}"
assert abs(T3_got - T3_set) < 0.001, f"T3 mismatch: set={T3_set}, got={T3_got}"

# --- Result ---
result["function"] = "SapModel.PropFrame.GetCircle"
result["section_name"] = "COL_D500"
result["material"] = mat_prop
result["T3_diameter"] = T3_got
result["byref_layout"] = "[FileName, MatProp, T3, Color, Notes, GUID, ret_code]"
result["status"] = "verified"
