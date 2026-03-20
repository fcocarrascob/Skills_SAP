# ============================================================
# Wrapper: SapModel.PropArea.SetShell_1
# Category: PropArea
# Description: Create a shell (area) section property
# Verified: 2026-03-20
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a shell section property for area elements (slabs, walls,
       footings). The _1 suffix indicates the simplified interface with
       uniform thickness.

API Signature:
  SapModel.PropArea.SetShell_1(Name, ShellType, IncludeDrillingDOF,
      MatProp, MatAng, Thickness, Bending, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name              : str   — Section name
  ShellType         : int   — 1=Shell-Thin, 2=Shell-Thick, 3=Plate-Thin,
                               4=Plate-Thick, 5=Membrane, 6=ShellLayered
  IncludeDrillingDOF: bool  — Include drilling DOF (default=True)
  MatProp           : str   — Material property name
  MatAng            : float — Material angle [degrees] (default=0)
  Thickness         : float — Shell thickness [L]
  Bending           : float — Bending thickness [L] (default=same as Thickness)
  Color             : int   — Display color (optional, -1=default)
  Notes             : str   — Notes (optional, ""=none)
  GUID              : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define material ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)  # Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# Slab shell: 0.20m thick, Shell-Thin
ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, True, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0, f"SetShell_1(SLAB_20) failed: {ret}"

# Footing shell: 0.60m thick, Shell-Thick
ret = SapModel.PropArea.SetShell_1("FOOTING_60", 2, True, "CONC_TEST", 0, 0.60, 0.60)
assert ret == 0, f"SetShell_1(FOOTING_60) failed: {ret}"

# Wall membrane: 0.15m thick, Membrane
ret = SapModel.PropArea.SetShell_1("WALL_15", 5, False, "CONC_TEST", 0, 0.15, 0.15)
assert ret == 0, f"SetShell_1(WALL_15) failed: {ret}"

# --- Verification ---
raw = SapModel.PropArea.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
shell_names = list(raw[1])

assert "SLAB_20" in shell_names, f"SLAB_20 not found in: {shell_names}"
assert "FOOTING_60" in shell_names, f"FOOTING_60 not found in: {shell_names}"
assert "WALL_15" in shell_names, f"WALL_15 not found in: {shell_names}"

# --- Result ---
result["function"] = "SapModel.PropArea.SetShell_1"
result["shells_created"] = ["SLAB_20", "FOOTING_60", "WALL_15"]
result["shell_count"] = raw[0]
result["status"] = "verified"
