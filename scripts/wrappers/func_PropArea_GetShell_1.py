# ============================================================
# Wrapper: SapModel.PropArea.GetShell_1
# Category: Properties
# Description: Retrieve shell-type area section properties
# Verified: 2026-03-28
# Prerequisites: Model open, shell property defined
# ============================================================
"""
Usage: Reads back properties of a shell-type area section including
       shell type, material, thicknesses, and other attributes.

API Signature:
  SapModel.PropArea.GetShell_1(Name, ShellType, IncludeDrillingDOF,
      MatProp, MatAng, Thickness, Bending,
      Color, Notes, GUID) -> [..., ret_code]

ByRef Output (8 values):
  ShellType         : int  — 1=Shell-thin, 2=Shell-thick, 3=Plate-thin,
                             4=Plate-thick, 5=Membrane, 6=Layered
  IncludeDrillingDOF: bool — Drilling DOF in analysis
  MatProp           : str  — Material name
  MatAng            : float— Material angle [deg]
  Thickness         : float— Membrane thickness [L]
  Bending           : float— Bending thickness [L]
  Color             : int  — Display color
  Notes             : str  — Notes
  GUID              : str  — GUID

Parameters:
  Name : str — Shell-type area property name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

# Create shell with known properties
ret = SapModel.PropArea.SetShell_1("WALL_30", 2, True, "CONC_TEST", 0, 0.30, 0.30)
assert ret == 0

# --- Target function ---
raw = SapModel.PropArea.GetShell_1(
    "WALL_30", 0, False, "", 0.0, 0.0, 0.0, 0, "", ""
)
ret_code = raw[-1]
assert ret_code == 0, f"GetShell_1 failed: {ret_code}"

shell_type = raw[0]
include_drill = raw[1]
mat_prop = raw[2]
mat_ang = raw[3]
thickness = raw[4]
bending = raw[5]

assert shell_type == 2, f"Expected ShellType=2(thick), got {shell_type}"
assert mat_prop == "CONC_TEST", f"Expected CONC_TEST, got {mat_prop}"
assert abs(thickness - 0.30) < 0.001, f"Expected thickness=0.30, got {thickness}"
assert abs(bending - 0.30) < 0.001, f"Expected bending=0.30, got {bending}"

# --- Result ---
result["function"] = "SapModel.PropArea.GetShell_1"
result["shell_type"] = shell_type
result["material"] = mat_prop
result["thickness"] = thickness
result["bending"] = bending
result["status"] = "verified"
