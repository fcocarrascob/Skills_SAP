# ============================================================
# Wrapper: SapModel.AreaObj.SetSpring
# Category: Object_Model
# Description: Assign area springs (Winkler foundation) to an area element
# Verified: 2026-03-20
# Prerequisites: Model open, area element exists
# ============================================================
"""
Usage: Assigns spring supports to an area element face. Commonly used
       for soil-structure interaction (Winkler foundation model) where
       a spring constant represents the soil modulus.

API Signature:
  SapModel.AreaObj.SetSpring(Name, MyType, S, SimpleSpringType,
      LinkProp, Face, SpringLocalOneType, Dir, Outward, Vec,
      Ang, Replace, CSys, ItemType)

ByRef Output:
  ret_code (0=success) — last element of return list [Vec_tuple, ret_code]

Parameters:
  Name              : str   — Area object name
  MyType            : int   — 1=Simple, 2=Link property
  S                 : float — Spring stiffness [F/L^3] for simple springs
  SimpleSpringType  : int   — 0=Compression+Tension, 1=Compression-only,
                               2=Tension-only
  LinkProp          : str   — Link property name (for MyType=2, ""=N/A)
  Face              : int   — -1=Bottom, -2=Top, 1-4=Side faces
  SpringLocalOneType: int   — 0=Parallel to 1-axis, 1=Normal to face,
                               2=User vector
  Dir               : int   — Direction: 1=Local-1, 2=Local-2, 3=Local-3
  Outward           : bool  — True=outward direction
  Vec               : float[3] — User direction vector (for type=2)
  Ang               : float — Rotation angle [degrees]
  Replace           : bool  — True=replace existing springs
  CSys              : str   — Coordinate system
  ItemType          : int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, shell, and an area element ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

ret = SapModel.PropArea.SetShell_1("FOOTING_60", 2, True, "CONC_TEST", 0, 0.60, 0.60)
assert ret == 0, f"SetShell_1 failed: {ret}"

# Create footing area (2m x 2m at Z=0)
x = [0.0, 2.0, 2.0, 0.0]
y = [0.0, 0.0, 2.0, 2.0]
z = [0.0, 0.0, 0.0, 0.0]
raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "FOOTING_60", "")
area_name = raw[3]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# --- Target function: assign soil spring to bottom face ---
# Soil modulus: 30000 kN/m³ (typical for dense sand)
# Compression-only spring on bottom face
raw_spring = SapModel.AreaObj.SetSpring(
    area_name,        # Name
    1,                # MyType = Simple
    30000.0,          # S = spring stiffness [kN/m³]
    1,                # SimpleSpringType = Compression-only
    "",               # LinkProp = N/A for simple
    -1,               # Face = Bottom
    1,                # SpringLocalOneType = Normal to face
    1,                # Dir = Local-1
    False,            # Outward = False
    [0, 0, 0],        # Vec = not used
    0,                # Ang = 0
    True,             # Replace = True
    "Global",         # CSys
    0                 # ItemType = Object
)
# SetSpring returns [Vec_tuple, ret_code] or just ret_code depending on version
if isinstance(raw_spring, (list, tuple)):
    ret = raw_spring[-1]
else:
    ret = raw_spring
assert ret == 0, f"SetSpring failed: {ret}"

# --- Verification ---
count = SapModel.AreaObj.Count()
assert count == 1, f"Expected 1 area, got {count}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetSpring"
result["area_name"] = area_name
result["spring_stiffness"] = 30000.0
result["spring_type"] = "compression-only"
result["face"] = "bottom"
result["status"] = "verified"
