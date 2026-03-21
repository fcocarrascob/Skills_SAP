# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadUniform
# Category: Load_Assignment
# Description: Apply uniform pressure on area elements (slab loads)
# Verified: pending
# Prerequisites: Model open, area exists, load pattern defined
# ============================================================
"""
Usage: Assigns a uniform surface load to an area element in a
       specified load pattern.

API Signature:
  SapModel.AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir,
      Replace, CSys, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Area object name
  LoadPat  : str   — Load pattern name
  Value    : float — Uniform load value [F/L^2]
  Dir      : int   — Direction: 1=Local1, 2=Local2, 3=Local3,
                      4=X, 5=Y, 6=Z, 7=ProjX, 8=ProjY, 9=ProjZ,
                      10=Gravity, 11=ProjGravity
  Replace  : bool  — True=replace existing loads (default=True)
  CSys     : str   — Coordinate system (default="Global")
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, shell section, area ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, True, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0, f"SetShell_1 failed: {ret}"

# Rectangular slab 6m x 4m at Z=3m
x = [0.0, 6.0, 6.0, 0.0]
y = [0.0, 0.0, 4.0, 4.0]
z = [3.0, 3.0, 3.0, 3.0]
raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "SLAB_20", "")
area_name = raw[3]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Load pattern
ret = SapModel.LoadPatterns.Add("SLAB_LL", 3, 0)  # Live
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

# --- Target function: uniform live load on slab ---
# -5 kN/m² in gravity direction
ret = SapModel.AreaObj.SetLoadUniform(area_name, "SLAB_LL", -5.0, 10)
assert ret == 0, f"SetLoadUniform failed: {ret}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadUniform"
result["area_name"] = area_name
result["load_value"] = -5.0
result["direction"] = "Gravity"
result["status"] = "verified"
