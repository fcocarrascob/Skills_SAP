# ============================================================
# Wrapper: SapModel.PropMaterial.SetMaterial
# Category: PropMaterial
# Description: Define or modify a material by name and type
# Verified: 2026-03-20
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a new material definition with the given name and type.
       The type determines design behavior (steel, concrete, rebar, etc.).

API Signature:
  SapModel.PropMaterial.SetMaterial(Name, MatType, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str — Material name
  MatType : int — eMatType enum:
                   1=Steel, 2=Concrete, 3=NoDesign, 4=Aluminum,
                   5=ColdFormed, 6=Rebar, 7=Tendon
  Color   : int — Display color (optional, -1=default)
  Notes   : str — Notes (optional, ""=none)
  GUID    : str — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: create multiple material types ---
# Steel material
ret = SapModel.PropMaterial.SetMaterial("STEEL_A992", 1)
assert ret == 0, f"SetMaterial(Steel) failed: {ret}"

# Concrete material
ret = SapModel.PropMaterial.SetMaterial("CONC_FC28", 2)
assert ret == 0, f"SetMaterial(Concrete) failed: {ret}"

# Rebar material
ret = SapModel.PropMaterial.SetMaterial("REBAR_A630", 6)
assert ret == 0, f"SetMaterial(Rebar) failed: {ret}"

# --- Verification ---
# Check materials exist via GetNameList
raw = SapModel.PropMaterial.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
mat_names = list(raw[1])

assert "STEEL_A992" in mat_names, f"STEEL_A992 not found in: {mat_names}"
assert "CONC_FC28" in mat_names, f"CONC_FC28 not found in: {mat_names}"
assert "REBAR_A630" in mat_names, f"REBAR_A630 not found in: {mat_names}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.SetMaterial"
result["materials_created"] = ["STEEL_A992", "CONC_FC28", "REBAR_A630"]
result["material_count"] = raw[0]
result["all_materials"] = mat_names
result["status"] = "verified"
