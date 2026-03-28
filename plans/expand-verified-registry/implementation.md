# Expansión del Registry Verificado de Funciones SAP2000

## Goal
Ampliar el registry verificado (`scripts/registry.json` + `scripts/wrappers/`) con ~45 funciones API esenciales organizadas en 8 steps independientes, pasando de ~133 a ~178 funciones verificadas.

## Prerequisites
Make sure that the user is currently on the `expand-verified-registry` branch before beginning implementation.
If not, move them to the correct branch. If the branch does not exist, create it from main.

### Convenciones del Proyecto
- **Wrapper pattern:** Header con metadata → docstring → fresh model init → prerequisites → target function → verification → result dict
- **Registry schema:** `category`, `description`, `signature`, `verified: true`, `first_verified`, `last_verified`, `verification_count`, `wrapper_script`, `used_in_scripts`, `parameter_notes`, `known_errors`, `notes`
- **Date format:** ISO8601 con microsegundos `YYYY-MM-DDTHH:MM:SS.000000+00:00`
- **Units:** Siempre `SetPresentUnits(6)` (kN_m_C)
- **Return code check:** `assert ret == 0` para directo, `assert raw[-1] == 0` para ByRef
- **File naming:** `func_{Category}_{Function}.py` → `SapModel.{Category}.{Function}`
- **Execution:** Cada wrapper se ejecuta vía MCP tool `run_sap_script` para verificación
- **Registration:** Tras verificación, se registra vía `register_verified_function` o se agrega manualmente a `registry.json`

---

### Step-by-Step Instructions

---

#### Step 1: Material Design Properties (Tier 1 — Producción)

4 wrappers: `SetOSteel_1`, `SetOConcrete_1`, `GetMaterial`, `GetMPIsotropic`

- [x] Create file `scripts/wrappers/func_PropMaterial_SetOSteel_1.py`:

```python
# ============================================================
# Wrapper: SapModel.PropMaterial.SetOSteel_1
# Category: PropMaterial
# Description: Set steel design properties (ASTM/EN overstrength)
# Verified: 2026-03-28
# Prerequisites: Model open, steel material defined via SetMaterial
# ============================================================
"""
Usage: Assigns steel design properties to an existing steel material.
       Defines yield/ultimate strengths all needed for steel design checks.

API Signature:
  SapModel.PropMaterial.SetOSteel_1(Name, Fy, Fu, EFy, EFu,
    SSType, SSHysType, StrainAtHardening, StrainAtMaxStress,
    StrainAtRupture, FinalSlope)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name              : str   — Existing steel material name
  Fy                : float — Minimum yield stress [F/L^2]
  Fu                : float — Minimum tensile stress [F/L^2]
  EFy               : float — Expected yield stress [F/L^2]
  EFu               : float — Expected tensile stress [F/L^2]
  SSType            : int   — Stress-strain curve type (0=User, 1=Parametric-Simple)
  SSHysType         : int   — Stress-strain hysteresis type (0=Elastic, 1=Kinematic, 2=Takeda, 3=Pivot)
  StrainAtHardening : float — Strain at onset of strain hardening
  StrainAtMaxStress : float — Strain at maximum stress
  StrainAtRupture   : float — Strain at rupture
  FinalSlope        : float — Final slope of stress-strain curve (negative for softening)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create steel material ---
ret = SapModel.PropMaterial.SetMaterial("A992_TEST", 1)  # 1=Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("A992_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function: set steel design properties ---
# A992 Fy=345 MPa = 345000 kN/m2, Fu=450 MPa = 450000 kN/m2
ret = SapModel.PropMaterial.SetOSteel_1(
    "A992_TEST",
    345000,    # Fy  [kN/m^2]
    450000,    # Fu  [kN/m^2]
    379500,    # EFy (1.1 × Fy)
    495000,    # EFu (1.1 × Fu)
    1,         # SSType — Parametric-Simple
    1,         # SSHysType — Kinematic
    0.02,      # StrainAtHardening
    0.10,      # StrainAtMaxStress
    0.20,      # StrainAtRupture
    -0.10      # FinalSlope
)
assert ret == 0, f"SetOSteel_1 failed: {ret}"

# Second steel: A36
ret = SapModel.PropMaterial.SetMaterial("A36_TEST", 1)
assert ret == 0, f"SetMaterial(A36) failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("A36_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetOSteel_1(
    "A36_TEST",
    250000,    # Fy  [kN/m^2]
    400000,    # Fu  [kN/m^2]
    275000,    # EFy
    440000,    # EFu
    1, 1, 0.02, 0.10, 0.20, -0.10
)
assert ret == 0, f"SetOSteel_1(A36) failed: {ret}"

# --- Verification: material exists ---
raw = SapModel.PropMaterial.GetNameList(0, [])
assert raw[-1] == 0, f"GetNameList failed: {raw[-1]}"
mat_names = list(raw[1])
assert "A992_TEST" in mat_names, f"A992_TEST not found in: {mat_names}"
assert "A36_TEST" in mat_names, f"A36_TEST not found in: {mat_names}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.SetOSteel_1"
result["materials_configured"] = ["A992_TEST", "A36_TEST"]
result["material_count"] = raw[0]
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_PropMaterial_SetOConcrete_1.py`:

```python
# ============================================================
# Wrapper: SapModel.PropMaterial.SetOConcrete_1
# Category: PropMaterial
# Description: Set concrete design properties (fc, strain model)
# Verified: 2026-03-28
# Prerequisites: Model open, concrete material defined via SetMaterial
# ============================================================
"""
Usage: Assigns concrete design properties to an existing concrete material.
       Defines compressive strength and stress-strain model for design checks.

API Signature:
  SapModel.PropMaterial.SetOConcrete_1(Name, fc, IsLightweight,
    FcsFactor, SSType, SSHysType, StrainAtfc,
    StrainUltimate, FinalSlope, FrictionAngle, DilatationalAngle)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name              : str   — Existing concrete material name
  fc                : float — Concrete compressive strength [F/L^2]
  IsLightweight     : bool  — True if lightweight concrete
  FcsFactor         : float — Concrete stress-strain factor (typically 0 for confined)
  SSType            : int   — Stress-strain type (0=User, 1=Parametric-Simple)
  SSHysType         : int   — Hysteresis type (0=Elastic, 1=Kinematic, 2=Takeda, 3=Pivot)
  StrainAtfc        : float — Strain at fc
  StrainUltimate    : float — Ultimate strain capacity
  FinalSlope        : float — Final slope (negative for softening)
  FrictionAngle     : float — Friction angle [deg] (default 0)
  DilatationalAngle : float — Dilatational angle [deg] (default 0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create concrete material ---
ret = SapModel.PropMaterial.SetMaterial("CONC_28", 2)  # 2=Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_28", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function: set concrete design properties ---
# fc=28 MPa = 28000 kN/m2
ret = SapModel.PropMaterial.SetOConcrete_1(
    "CONC_28",
    28000,     # fc [kN/m^2]
    False,     # IsLightweight
    0,         # FcsFactor
    1,         # SSType — Parametric-Simple
    1,         # SSHysType — Kinematic
    0.002,     # StrainAtfc
    0.005,     # StrainUltimate
    -0.10,     # FinalSlope
    0,         # FrictionAngle
    0          # DilatationalAngle
)
assert ret == 0, f"SetOConcrete_1 failed: {ret}"

# Second concrete: H30
ret = SapModel.PropMaterial.SetMaterial("CONC_H30", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_H30", 2.65e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetOConcrete_1(
    "CONC_H30",
    25000, False, 0, 1, 1, 0.002, 0.005, -0.10, 0, 0
)
assert ret == 0, f"SetOConcrete_1(H30) failed: {ret}"

# --- Verification ---
raw = SapModel.PropMaterial.GetNameList(0, [])
assert raw[-1] == 0, f"GetNameList failed: {raw[-1]}"
mat_names = list(raw[1])
assert "CONC_28" in mat_names, f"CONC_28 not found in: {mat_names}"
assert "CONC_H30" in mat_names, f"CONC_H30 not found in: {mat_names}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.SetOConcrete_1"
result["materials_configured"] = ["CONC_28", "CONC_H30"]
result["material_count"] = raw[0]
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_PropMaterial_GetMaterial.py`:

```python
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
```

- [x] Create file `scripts/wrappers/func_PropMaterial_GetMPIsotropic.py`:

```python
# ============================================================
# Wrapper: SapModel.PropMaterial.GetMPIsotropic
# Category: PropMaterial
# Description: Retrieve isotropic mechanical properties (E, Poisson, thermal)
# Verified: 2026-03-28
# Prerequisites: Model open, material defined with SetMPIsotropic
# ============================================================
"""
Usage: Reads back the isotropic mechanical properties assigned
       to an existing material. Useful for verification cycles.

API Signature:
  SapModel.PropMaterial.GetMPIsotropic(Name, E, U, A, Temp)

ByRef Output:
  [E, poisson, thermal, tempDep, ret_code]

Parameters:
  Name : str   — Existing material name
  E    : float — (ByRef out) Modulus of elasticity [F/L^2]
  U    : float — (ByRef out) Poisson ratio
  A    : float — (ByRef out) Thermal expansion coeff [1/T]
  Temp : float — (ByRef out) Temperature dependency flag
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create material with known properties ---
ret = SapModel.PropMaterial.SetMaterial("MAT_VERIFY", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

E_set = 2.0e8
U_set = 0.3
A_set = 1.2e-5
ret = SapModel.PropMaterial.SetMPIsotropic("MAT_VERIFY", E_set, U_set, A_set)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function: get isotropic properties ---
raw = SapModel.PropMaterial.GetMPIsotropic("MAT_VERIFY", 0, 0, 0, 0)
ret_code = raw[-1]
assert ret_code == 0, f"GetMPIsotropic failed: {ret_code}"

E_got = raw[0]
U_got = raw[1]
A_got = raw[2]

# Verify values match (within floating-point tolerance)
assert abs(E_got - E_set) < 1000, f"E mismatch: set={E_set}, got={E_got}"
assert abs(U_got - U_set) < 0.01, f"U mismatch: set={U_set}, got={U_got}"
assert abs(A_got - A_set) < 1e-7, f"A mismatch: set={A_set}, got={A_got}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.GetMPIsotropic"
result["E"] = E_got
result["poisson"] = U_got
result["thermal"] = A_got
result["byref_layout"] = "[E, poisson, thermal, tempDep, ret_code]"
result["status"] = "verified"
```

- [x] Register all 4 functions in `scripts/registry.json` — add entries under `"functions"` with the following keys (each with `verified: true`, `wrapper_script`, appropriate `category: "PropMaterial"`, `first_verified` and `last_verified` set to execution timestamp):
  - `SapModel.PropMaterial.SetOSteel_1`
  - `SapModel.PropMaterial.SetOConcrete_1`
  - `SapModel.PropMaterial.GetMaterial`
  - `SapModel.PropMaterial.GetMPIsotropic`
- [x] Execute each wrapper via MCP `run_sap_script` tool and verify `ret_code == 0`

##### Step 1 Verification Checklist
- [x] All 4 wrappers execute without assertion errors
- [x] `GetMaterial` returns correct `MatType` (1=Steel, 2=Concrete)
- [x] `GetMPIsotropic` returns values matching what was set
- [x] All 4 functions appear in `registry.json` with `verified: true`
- [x] `registry.json` summary `total_registered` count incremented by 4

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 2: Section Property Getters + New Types (Tier 1)

6 wrappers: `SetAngle`, `SetChannel`, `SetPipe`, `GetRectangle`, `GetCircle`, `GetISection`

- [ ] Create file `scripts/wrappers/func_PropFrame_SetAngle.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetAngle
# Category: PropFrame
# Description: Define an angle (L-shape) frame section
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates an angle (L) cross-section for frame elements.
       Common for bracing and secondary structural members.

API Signature:
  SapModel.PropFrame.SetAngle(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Vertical leg depth [L]
  T2      : float — Horizontal leg width [L]
  TF      : float — Flange thickness (horizontal leg) [L]
  TW      : float — Web thickness (vertical leg) [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_ANG", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_ANG", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# L75x75x6 (in meters)
ret = SapModel.PropFrame.SetAngle(
    "L75x75x6", "STEEL_ANG",
    0.075,   # T3 — vertical leg
    0.075,   # T2 — horizontal leg
    0.006,   # TF — flange thickness
    0.006,   # TW — web thickness
    -1, "", ""
)
assert ret == 0, f"SetAngle(L75x75x6) failed: {ret}"

# L100x75x8 (unequal legs)
ret = SapModel.PropFrame.SetAngle(
    "L100x75x8", "STEEL_ANG",
    0.100,   # T3
    0.075,   # T2
    0.008,   # TF
    0.008,   # TW
    -1, "", ""
)
assert ret == 0, f"SetAngle(L100x75x8) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])
assert "L75x75x6" in section_names, f"L75x75x6 not found in: {section_names}"
assert "L100x75x8" in section_names, f"L100x75x8 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetAngle"
result["sections_created"] = ["L75x75x6", "L100x75x8"]
result["section_count"] = raw[0]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropFrame_SetChannel.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetChannel
# Category: PropFrame
# Description: Define a channel (C-shape) frame section
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a channel (C) cross-section for frame elements.
       Common for purlins, girts, and secondary framing.

API Signature:
  SapModel.PropFrame.SetChannel(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Overall depth [L]
  T2      : float — Flange width [L]
  TF      : float — Flange thickness [L]
  TW      : float — Web thickness [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_CH", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_CH", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# C200x75 (in meters)
ret = SapModel.PropFrame.SetChannel(
    "C200x75", "STEEL_CH",
    0.200,   # T3 — depth
    0.075,   # T2 — flange width
    0.0109,  # TF — flange thickness
    0.0059,  # TW — web thickness
    -1, "", ""
)
assert ret == 0, f"SetChannel(C200x75) failed: {ret}"

# C150x50
ret = SapModel.PropFrame.SetChannel(
    "C150x50", "STEEL_CH",
    0.150, 0.050, 0.009, 0.005,
    -1, "", ""
)
assert ret == 0, f"SetChannel(C150x50) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])
assert "C200x75" in section_names, f"C200x75 not found in: {section_names}"
assert "C150x50" in section_names, f"C150x50 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetChannel"
result["sections_created"] = ["C200x75", "C150x50"]
result["section_count"] = raw[0]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropFrame_SetPipe.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.SetPipe
# Category: PropFrame
# Description: Define a circular pipe (hollow) frame section
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a circular pipe (hollow tube) section.
       Common for columns, braces, and truss elements.

API Signature:
  SapModel.PropFrame.SetPipe(Name, MatProp, T3, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Outer diameter [L]
  TW      : float — Wall thickness [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_PIPE", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_PIPE", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# Pipe 200x8 (OD=200mm, t=8mm)
ret = SapModel.PropFrame.SetPipe(
    "PIPE_200x8", "STEEL_PIPE",
    0.200,   # T3 — outer diameter
    0.008    # TW — wall thickness
)
assert ret == 0, f"SetPipe(200x8) failed: {ret}"

# Pipe 300x10
ret = SapModel.PropFrame.SetPipe(
    "PIPE_300x10", "STEEL_PIPE",
    0.300,   # T3
    0.010    # TW
)
assert ret == 0, f"SetPipe(300x10) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])
assert "PIPE_200x8" in section_names, f"PIPE_200x8 not found in: {section_names}"
assert "PIPE_300x10" in section_names, f"PIPE_300x10 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetPipe"
result["sections_created"] = ["PIPE_200x8", "PIPE_300x10"]
result["section_count"] = raw[0]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropFrame_GetRectangle.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.GetRectangle
# Category: PropFrame
# Description: Retrieve rectangular section properties
# Verified: 2026-03-28
# Prerequisites: Model open, rectangular section defined
# ============================================================
"""
Usage: Reads back the properties of an existing rectangular frame section.

API Signature:
  SapModel.PropFrame.GetRectangle(Name, FileName, MatProp, T3, T2, Color, Notes, GUID)

ByRef Output:
  [FileName, MatProp, T3, T2, Color, Notes, GUID, ret_code]

Parameters:
  Name     : str   — Existing section name
  FileName : str   — (ByRef out) Section file name
  MatProp  : str   — (ByRef out) Material property name
  T3       : float — (ByRef out) Section depth [L]
  T2       : float — (ByRef out) Section width [L]
  Color    : int   — (ByRef out) Display color
  Notes    : str   — (ByRef out) Notes
  GUID     : str   — (ByRef out) GUID
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: create material and rectangular section ---
ret = SapModel.PropMaterial.SetMaterial("CONC_R", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_R", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

T3_set = 0.6
T2_set = 0.3
ret = SapModel.PropFrame.SetRectangle("BEAM_30x60", "CONC_R", T3_set, T2_set)
assert ret == 0, f"SetRectangle failed: {ret}"

# --- Target function ---
raw = SapModel.PropFrame.GetRectangle("BEAM_30x60", "", "", 0, 0, 0, "", "")
ret_code = raw[-1]
assert ret_code == 0, f"GetRectangle failed: {ret_code}"

file_name = raw[0]
mat_prop = raw[1]
T3_got = raw[2]
T2_got = raw[3]

assert mat_prop == "CONC_R", f"Material mismatch: expected CONC_R, got {mat_prop}"
assert abs(T3_got - T3_set) < 0.001, f"T3 mismatch: set={T3_set}, got={T3_got}"
assert abs(T2_got - T2_set) < 0.001, f"T2 mismatch: set={T2_set}, got={T2_got}"

# --- Result ---
result["function"] = "SapModel.PropFrame.GetRectangle"
result["section_name"] = "BEAM_30x60"
result["material"] = mat_prop
result["T3"] = T3_got
result["T2"] = T2_got
result["byref_layout"] = "[FileName, MatProp, T3, T2, Color, Notes, GUID, ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropFrame_GetCircle.py`:

```python
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
```

- [ ] Create file `scripts/wrappers/func_PropFrame_GetISection.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.GetISection
# Category: PropFrame
# Description: Retrieve I-section properties
# Verified: 2026-03-28
# Prerequisites: Model open, I-section defined
# ============================================================
"""
Usage: Reads back the properties of an existing I/H frame section.

API Signature:
  SapModel.PropFrame.GetISection(Name, FileName, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID)

ByRef Output:
  [FileName, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID, ret_code]

Parameters:
  Name     : str   — Existing section name
  FileName : str   — (ByRef out) Section file name
  MatProp  : str   — (ByRef out) Material property name
  T3       : float — (ByRef out) Overall depth [L]
  T2       : float — (ByRef out) Top flange width [L]
  TF       : float — (ByRef out) Top flange thickness [L]
  TW       : float — (ByRef out) Web thickness [L]
  T2B      : float — (ByRef out) Bottom flange width [L]
  TFB      : float — (ByRef out) Bottom flange thickness [L]
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
ret = SapModel.PropMaterial.SetMaterial("STEEL_I", 1)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_I", 2.0e8, 0.3, 1.2e-5)
assert ret == 0

T3_set = 0.308
T2_set = 0.305
TF_set = 0.0154
TW_set = 0.00991
ret = SapModel.PropFrame.SetISection(
    "W310x97", "STEEL_I", T3_set, T2_set, TF_set, TW_set, T2_set, TF_set
)
assert ret == 0, f"SetISection failed: {ret}"

# --- Target function ---
raw = SapModel.PropFrame.GetISection("W310x97", "", "", 0, 0, 0, 0, 0, 0, 0, "", "")
ret_code = raw[-1]
assert ret_code == 0, f"GetISection failed: {ret_code}"

mat_prop = raw[1]
T3_got = raw[2]
T2_got = raw[3]
TF_got = raw[4]
TW_got = raw[5]

assert mat_prop == "STEEL_I", f"Material mismatch: expected STEEL_I, got {mat_prop}"
assert abs(T3_got - T3_set) < 0.001, f"T3 mismatch: set={T3_set}, got={T3_got}"
assert abs(T2_got - T2_set) < 0.001, f"T2 mismatch: set={T2_set}, got={T2_got}"
assert abs(TF_got - TF_set) < 0.001, f"TF mismatch: set={TF_set}, got={TF_got}"
assert abs(TW_got - TW_set) < 0.001, f"TW mismatch: set={TW_set}, got={TW_got}"

# --- Result ---
result["function"] = "SapModel.PropFrame.GetISection"
result["section_name"] = "W310x97"
result["material"] = mat_prop
result["T3"] = T3_got
result["T2"] = T2_got
result["TF"] = TF_got
result["TW"] = TW_got
result["byref_layout"] = "[FileName, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID, ret_code]"
result["status"] = "verified"
```

- [ ] Register all 6 functions in `scripts/registry.json`
- [ ] Execute each wrapper via MCP `run_sap_script` and verify `ret_code == 0`

##### Step 2 Verification Checklist
- [ ] All 6 wrappers execute without assertion errors
- [ ] Getter wrappers return values matching what was set
- [ ] SetAngle/SetChannel/SetPipe sections appear in `GetNameList`
- [ ] All 6 functions appear in `registry.json` with `verified: true`

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 3: Design Workflow Functions (Tier 1 — Producción)

9 wrappers: `DesignSteel.SetComboStrength`, `.GetComboStrength`, `.SetComboDeflection`, `.GetCode`, `.SetCode`, `.DeleteResults`, `DesignConcrete.SetComboStrength`, `.GetCode`, `.SetCode`

- [ ] Create file `scripts/wrappers/func_DesignSteel_SetComboStrength.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.SetComboStrength
# Category: Design
# Description: Select/deselect a combo for steel strength design
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Selects or deselects a load combination for steel strength
       design. Must be called after creating combinations.

API Signature:
  SapModel.DesignSteel.SetComboStrength(Name, Selected)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str  — Existing load combination name
  Selected : bool — True=select for strength design, False=deselect
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites: create combos ---
ret = SapModel.RespCombo.Add("LRFD_1", 0)
assert ret == 0, f"RespCombo.Add(LRFD_1) failed: {ret}"
ret = SapModel.RespCombo.Add("LRFD_2", 0)
assert ret == 0, f"RespCombo.Add(LRFD_2) failed: {ret}"

# --- Target function: select combos for strength design ---
ret = SapModel.DesignSteel.SetComboStrength("LRFD_1", True)
assert ret == 0, f"SetComboStrength(LRFD_1, True) failed: {ret}"

ret = SapModel.DesignSteel.SetComboStrength("LRFD_2", True)
assert ret == 0, f"SetComboStrength(LRFD_2, True) failed: {ret}"

# Deselect one
ret = SapModel.DesignSteel.SetComboStrength("LRFD_2", False)
assert ret == 0, f"SetComboStrength(LRFD_2, False) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetComboStrength"
result["combos_selected"] = ["LRFD_1"]
result["combos_deselected"] = ["LRFD_2"]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignSteel_GetComboStrength.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.GetComboStrength
# Category: Design
# Description: Retrieve combos selected for steel strength design
# Verified: 2026-03-28
# Prerequisites: Model open, combos selected via SetComboStrength
# ============================================================
"""
Usage: Returns the list of load combinations currently selected
       for steel strength design.

API Signature:
  SapModel.DesignSteel.GetComboStrength(NumberItems, MyName[])

ByRef Output:
  [NumberItems, MyName[], ret_code]

Parameters:
  NumberItems : int    — (ByRef out) Number of selected combos
  MyName      : str[]  — (ByRef out) Names of selected combos
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("STR_1", 0)
assert ret == 0
ret = SapModel.RespCombo.Add("STR_2", 0)
assert ret == 0

ret = SapModel.DesignSteel.SetComboStrength("STR_1", True)
assert ret == 0
ret = SapModel.DesignSteel.SetComboStrength("STR_2", True)
assert ret == 0

# --- Target function ---
raw = SapModel.DesignSteel.GetComboStrength(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetComboStrength failed: {ret_code}"

num_items = raw[0]
combo_names = list(raw[1]) if isinstance(raw[1], (list, tuple)) else [raw[1]]

assert num_items >= 2, f"Expected at least 2 combos, got {num_items}"
assert "STR_1" in combo_names, f"STR_1 not in strength combos: {combo_names}"
assert "STR_2" in combo_names, f"STR_2 not in strength combos: {combo_names}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.GetComboStrength"
result["num_items"] = num_items
result["combo_names"] = combo_names
result["byref_layout"] = "[NumberItems, MyName[], ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignSteel_SetComboDeflection.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.SetComboDeflection
# Category: Design
# Description: Select/deselect a combo for steel deflection design
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Selects or deselects a load combination for steel deflection
       design (serviceability check).

API Signature:
  SapModel.DesignSteel.SetComboDeflection(Name, Selected)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str  — Existing load combination name
  Selected : bool — True=select for deflection design, False=deselect
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("DEFL_SERV", 0)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignSteel.SetComboDeflection("DEFL_SERV", True)
assert ret == 0, f"SetComboDeflection(True) failed: {ret}"

ret = SapModel.DesignSteel.SetComboDeflection("DEFL_SERV", False)
assert ret == 0, f"SetComboDeflection(False) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetComboDeflection"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignSteel_GetCode.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.GetCode
# Category: Design
# Description: Retrieve current steel design code
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the currently set steel design code name.

API Signature:
  SapModel.DesignSteel.GetCode(CodeName)

ByRef Output:
  [CodeName, ret_code]

Parameters:
  CodeName : str — (ByRef out) Steel design code name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
raw = SapModel.DesignSteel.GetCode("")
ret_code = raw[-1]
assert ret_code == 0, f"GetCode failed: {ret_code}"
code_name = raw[0]

# --- Result ---
result["function"] = "SapModel.DesignSteel.GetCode"
result["code_name"] = code_name
result["byref_layout"] = "[CodeName, ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignSteel_SetCode.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.SetCode
# Category: Design
# Description: Set the steel design code
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets the steel design code for the model. Valid code names
       include AISC 360-10, AISC-LRFD93, AISC-ASD89, EN 1993-1-1:2005, etc.

API Signature:
  SapModel.DesignSteel.SetCode(CodeName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  CodeName : str — Steel design code name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: set and verify code ---
ret = SapModel.DesignSteel.SetCode("AISC 360-10")
assert ret == 0, f"SetCode('AISC 360-10') failed: {ret}"

# Verify via GetCode
raw = SapModel.DesignSteel.GetCode("")
assert raw[-1] == 0, f"GetCode failed: {raw[-1]}"
assert raw[0] == "AISC 360-10", f"Code mismatch: expected 'AISC 360-10', got '{raw[0]}'"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetCode"
result["code_set"] = "AISC 360-10"
result["code_verified"] = raw[0]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignSteel_DeleteResults.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignSteel.DeleteResults
# Category: Design
# Description: Delete all steel frame design results
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Deletes all steel frame design results from the model.
       Useful before re-running design with updated parameters.

API Signature:
  SapModel.DesignSteel.DeleteResults()

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignSteel.DeleteResults()
assert ret == 0, f"DeleteResults failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.DeleteResults"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignConcrete_SetComboStrength.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignConcrete.SetComboStrength
# Category: Design
# Description: Select/deselect a combo for concrete strength design
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Selects or deselects a load combination for concrete strength
       design. Similar to DesignSteel.SetComboStrength but for concrete.

API Signature:
  SapModel.DesignConcrete.SetComboStrength(Name, Selected)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str  — Existing load combination name
  Selected : bool — True=select for concrete strength design
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("CONC_STR1", 0)
assert ret == 0
ret = SapModel.RespCombo.Add("CONC_STR2", 0)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignConcrete.SetComboStrength("CONC_STR1", True)
assert ret == 0, f"SetComboStrength(CONC_STR1) failed: {ret}"

ret = SapModel.DesignConcrete.SetComboStrength("CONC_STR2", True)
assert ret == 0, f"SetComboStrength(CONC_STR2) failed: {ret}"

# Deselect
ret = SapModel.DesignConcrete.SetComboStrength("CONC_STR2", False)
assert ret == 0, f"SetComboStrength(deselect) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignConcrete.SetComboStrength"
result["combos_selected"] = ["CONC_STR1"]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignConcrete_GetCode.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignConcrete.GetCode
# Category: Design
# Description: Retrieve current concrete design code
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the currently set concrete design code name.

API Signature:
  SapModel.DesignConcrete.GetCode(CodeName)

ByRef Output:
  [CodeName, ret_code]

Parameters:
  CodeName : str — (ByRef out) Concrete design code name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
raw = SapModel.DesignConcrete.GetCode("")
ret_code = raw[-1]
assert ret_code == 0, f"GetCode failed: {ret_code}"
code_name = raw[0]

# --- Result ---
result["function"] = "SapModel.DesignConcrete.GetCode"
result["code_name"] = code_name
result["byref_layout"] = "[CodeName, ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_DesignConcrete_SetCode.py`:

```python
# ============================================================
# Wrapper: SapModel.DesignConcrete.SetCode
# Category: Design
# Description: Set the concrete design code
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets the concrete design code for the model. Valid codes
       include ACI 318-14, ACI 318-11, EN 2-2004, CSA A23.3-14, etc.

API Signature:
  SapModel.DesignConcrete.SetCode(CodeName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  CodeName : str — Concrete design code name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignConcrete.SetCode("ACI 318-14")
assert ret == 0, f"SetCode('ACI 318-14') failed: {ret}"

# Verify via GetCode
raw = SapModel.DesignConcrete.GetCode("")
assert raw[-1] == 0, f"GetCode failed: {raw[-1]}"
assert raw[0] == "ACI 318-14", f"Code mismatch: expected 'ACI 318-14', got '{raw[0]}'"

# --- Result ---
result["function"] = "SapModel.DesignConcrete.SetCode"
result["code_set"] = "ACI 318-14"
result["code_verified"] = raw[0]
result["status"] = "verified"
```

- [ ] Register all 9 functions in `scripts/registry.json`
- [ ] Execute each wrapper via MCP `run_sap_script` and verify `ret_code == 0`

##### Step 3 Verification Checklist
- [ ] All 9 wrappers execute without assertion errors
- [ ] `GetComboStrength` returns combos set via `SetComboStrength`
- [ ] `SetCode` → `GetCode` round-trip matches for both steel and concrete
- [ ] All 9 functions appear in `registry.json` with `verified: true`

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 4: Combo Management Completo (Tier 1)

7 wrappers: `RespCombo.Delete`, `.ChangeName`, `.Count`, `.SetTypeOAPI`, `.GetTypeOAPI`, `.DeleteCase`, `.AddDesignDefaultCombos`

- [ ] Create file `scripts/wrappers/func_RespCombo_Delete.py`:

```python
# ============================================================
# Wrapper: SapModel.RespCombo.Delete
# Category: RespCombo
# Description: Delete an existing load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Deletes a specified load combination from the model.

API Signature:
  SapModel.RespCombo.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of existing load combination to delete
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("TEMP_COMBO", 0)
assert ret == 0

# Verify it exists
raw = SapModel.RespCombo.GetNameList(0, [])
assert raw[-1] == 0
assert "TEMP_COMBO" in list(raw[1])

# --- Target function ---
ret = SapModel.RespCombo.Delete("TEMP_COMBO")
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"Delete failed: {ret_code}"

# Verify it's gone
raw2 = SapModel.RespCombo.GetNameList(0, [])
if raw2[-1] == 0 and raw2[0] > 0:
    combo_names = list(raw2[1])
    assert "TEMP_COMBO" not in combo_names, f"TEMP_COMBO still exists after delete"

# --- Result ---
result["function"] = "SapModel.RespCombo.Delete"
result["deleted"] = "TEMP_COMBO"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_RespCombo_ChangeName.py`:

```python
# ============================================================
# Wrapper: SapModel.RespCombo.ChangeName
# Category: RespCombo
# Description: Rename an existing load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Changes the name of an existing load combination.
       The new name must be unique across all combos and load cases.

API Signature:
  SapModel.RespCombo.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing load combination name
  NewName : str — New name for the combination
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("OLD_NAME", 0)
assert ret == 0

# --- Target function ---
ret = SapModel.RespCombo.ChangeName("OLD_NAME", "NEW_NAME")
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"ChangeName failed: {ret_code}"

# Verify
raw = SapModel.RespCombo.GetNameList(0, [])
assert raw[-1] == 0
combo_names = list(raw[1])
assert "NEW_NAME" in combo_names, f"NEW_NAME not found in: {combo_names}"
assert "OLD_NAME" not in combo_names, f"OLD_NAME still exists in: {combo_names}"

# --- Result ---
result["function"] = "SapModel.RespCombo.ChangeName"
result["old_name"] = "OLD_NAME"
result["new_name"] = "NEW_NAME"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_RespCombo_Count.py`:

```python
# ============================================================
# Wrapper: SapModel.RespCombo.Count
# Category: RespCombo
# Description: Get total number of load combinations
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of load combinations defined in the model.

API Signature:
  SapModel.RespCombo.Count()

ByRef Output:
  count (direct return, integer)

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Count before adding ---
count_before = SapModel.RespCombo.Count()

# --- Add combos ---
ret = SapModel.RespCombo.Add("COUNT_TEST_1", 0)
assert ret == 0
ret = SapModel.RespCombo.Add("COUNT_TEST_2", 1)
assert ret == 0

# --- Target function ---
count_after = SapModel.RespCombo.Count()
assert count_after == count_before + 2, f"Expected {count_before + 2}, got {count_after}"

# --- Result ---
result["function"] = "SapModel.RespCombo.Count"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_RespCombo_SetTypeOAPI.py`:

```python
# ============================================================
# Wrapper: SapModel.RespCombo.SetTypeOAPI
# Category: RespCombo
# Description: Set the type of a load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Sets or changes the type of an existing load combination.
       Types: 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS, 4=RangeAdd.

API Signature:
  SapModel.RespCombo.SetTypeOAPI(Name, ComboType)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str — Existing load combination name
  ComboType : int — 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS, 4=RangeAdd
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create combo as linear ---
ret = SapModel.RespCombo.Add("TYPE_TEST", 0)  # LinearAdd
assert ret == 0

# --- Target function: change type to Envelope ---
ret = SapModel.RespCombo.SetTypeOAPI("TYPE_TEST", 1)  # Envelope
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"SetTypeOAPI failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.RespCombo.SetTypeOAPI"
result["combo"] = "TYPE_TEST"
result["new_type"] = 1
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_RespCombo_GetTypeOAPI.py`:

```python
# ============================================================
# Wrapper: SapModel.RespCombo.GetTypeOAPI
# Category: RespCombo
# Description: Get the type of a load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Retrieves the type of an existing load combination.
       Types: 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS, 4=RangeAdd.

API Signature:
  SapModel.RespCombo.GetTypeOAPI(Name)

ByRef Output:
  [ComboType, ret_code]

Parameters:
  Name : str — Existing load combination name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create combo as envelope ---
ret = SapModel.RespCombo.Add("GTYPE_TEST", 1)  # 1=Envelope
assert ret == 0

# --- Target function ---
raw = SapModel.RespCombo.GetTypeOAPI("GTYPE_TEST")
ret_code = raw[-1]
assert ret_code == 0, f"GetTypeOAPI failed: {ret_code}"
combo_type = raw[0]
assert combo_type == 1, f"Expected type=1 (Envelope), got {combo_type}"

# Change type and verify
ret = SapModel.RespCombo.SetTypeOAPI("GTYPE_TEST", 3)  # SRSS
ret_code2 = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code2 == 0

raw2 = SapModel.RespCombo.GetTypeOAPI("GTYPE_TEST")
assert raw2[-1] == 0
assert raw2[0] == 3, f"Expected type=3 (SRSS), got {raw2[0]}"

# --- Result ---
result["function"] = "SapModel.RespCombo.GetTypeOAPI"
result["initial_type"] = combo_type
result["changed_type"] = raw2[0]
result["byref_layout"] = "[ComboType, ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_RespCombo_DeleteCase.py`:

```python
# ============================================================
# Wrapper: SapModel.RespCombo.DeleteCase
# Category: RespCombo
# Description: Remove a load case or combo from a combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo with cases assigned
# ============================================================
"""
Usage: Deletes one load case or load combination from the list
       of cases included in a specified load combination.

API Signature:
  SapModel.RespCombo.DeleteCase(Name, CType, CName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name  : str — Load combination name
  CType : int — 0=LoadCase, 1=LoadCombo
  CName : str — Name of the case/combo to remove
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create combo with cases ---
ret = SapModel.RespCombo.Add("DELCASE_TEST", 0)
assert ret == 0

# Add DEAD case to combo (DEAD is auto-created in blank model as a load case)
ret = SapModel.RespCombo.SetCaseList("DELCASE_TEST", 0, "DEAD", 1.4)
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"SetCaseList failed: {ret_code}"

# --- Target function: delete DEAD from combo ---
ret = SapModel.RespCombo.DeleteCase("DELCASE_TEST", 0, "DEAD")
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"DeleteCase failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.RespCombo.DeleteCase"
result["combo"] = "DELCASE_TEST"
result["deleted_case"] = "DEAD"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_RespCombo_AddDesignDefaultCombos.py`:

```python
# ============================================================
# Wrapper: SapModel.RespCombo.AddDesignDefaultCombos
# Category: RespCombo
# Description: Add default design combinations by material type
# Verified: 2026-03-28
# Prerequisites: Model open, load patterns defined
# ============================================================
"""
Usage: Adds code-default design load combinations to the model.
       Generates combos for the currently set design code.

API Signature:
  SapModel.RespCombo.AddDesignDefaultCombos(DesignSteel, DesignConcrete,
    DesignAluminum, DesignColdFormed)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  DesignSteel      : bool — Add default steel combos
  DesignConcrete   : bool — Add default concrete combos
  DesignAluminum   : bool — Add default aluminum combos
  DesignColdFormed : bool — Add default cold-formed combos
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: add typical load patterns ---
ret = SapModel.LoadPatterns.Add("LIVE", 3)  # 3=LTYPE_LIVE
assert ret == 0

count_before = SapModel.RespCombo.Count()

# --- Target function: add default steel design combos ---
ret = SapModel.RespCombo.AddDesignDefaultCombos(True, False, False, False)
assert ret == 0, f"AddDesignDefaultCombos failed: {ret}"

count_after = SapModel.RespCombo.Count()
assert count_after > count_before, f"No combos added: before={count_before}, after={count_after}"

# Get generated combo names
raw = SapModel.RespCombo.GetNameList(0, [])
assert raw[-1] == 0
combo_names = list(raw[1])

# --- Result ---
result["function"] = "SapModel.RespCombo.AddDesignDefaultCombos"
result["combos_before"] = count_before
result["combos_after"] = count_after
result["generated_combos"] = combo_names
result["status"] = "verified"
```

- [ ] Register all 7 functions in `scripts/registry.json`
- [ ] Execute each wrapper via MCP `run_sap_script` and verify `ret_code == 0`

##### Step 4 Verification Checklist
- [ ] All 7 wrappers execute without assertion errors
- [ ] `Delete` removes combo (confirmed by `GetNameList`)
- [ ] `ChangeName` renames combo (old gone, new present)
- [ ] `Count` returns correct count before/after adding
- [ ] `SetTypeOAPI` → `GetTypeOAPI` round-trip matches
- [ ] All 7 functions appear in `registry.json` with `verified: true`

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 5: LoadCases & LoadPatterns Admin (Tier 2)

7 wrappers: `LoadCases.ResponseSpectrum.SetDampConstant`, `LoadCases.Count`, `.Delete`, `.ChangeName`, `LoadPatterns.Count`, `.Delete`, `.ChangeName`

- [ ] Create file `scripts/wrappers/func_LoadCases_ResponseSpectrum_SetDampConstant.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadCases.ResponseSpectrum.SetDampConstant
# Category: Load_Cases
# Description: Set constant damping for a response spectrum case
# Verified: 2026-03-28
# Prerequisites: Model open, RS load case defined
# ============================================================
"""
Usage: Sets a constant modal damping ratio for a response spectrum
       load case. Common value: 0.05 (5% for steel/concrete).

API Signature:
  SapModel.LoadCases.ResponseSpectrum.SetDampConstant(Name, Damp)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str   — Response spectrum load case name
  Damp : float — Modal damping ratio (e.g. 0.05 = 5%)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create a response spectrum case ---
ret = SapModel.LoadCases.ResponseSpectrum.SetCase("RS_X")
assert ret == 0, f"SetCase(RS_X) failed: {ret}"

# --- Target function ---
ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant("RS_X", 0.05)
assert ret == 0, f"SetDampConstant failed: {ret}"

# --- Result ---
result["function"] = "SapModel.LoadCases.ResponseSpectrum.SetDampConstant"
result["case_name"] = "RS_X"
result["damping"] = 0.05
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_LoadCases_Count.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadCases.Count
# Category: Load_Cases
# Description: Get total number of load cases (optionally by type)
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined load cases in the model.
       Optionally filter by case type (1=LinearStatic, 3=Modal, 4=RS, etc.)

API Signature:
  SapModel.LoadCases.Count(CaseType)

ByRef Output:
  count (direct return, integer)

Parameters:
  CaseType : int — (optional) eLoadCaseType enum. Omit for all types.
                   1=LinearStatic, 2=NonlinearStatic, 3=Modal,
                   4=ResponseSpectrum, etc.
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: count all cases ---
count_all = SapModel.LoadCases.Count()
assert count_all >= 1, f"Expected at least 1 case (DEAD), got {count_all}"

# --- Result ---
result["function"] = "SapModel.LoadCases.Count"
result["count_all"] = count_all
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_LoadCases_Delete.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadCases.Delete
# Category: Load_Cases
# Description: Delete a load case
# Verified: 2026-03-28
# Prerequisites: Model open, load case exists
# ============================================================
"""
Usage: Deletes a specified load case from the model.

API Signature:
  SapModel.LoadCases.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of existing load case
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: add a load pattern → creates auto load case ---
ret = SapModel.LoadPatterns.Add("WIND_DEL", 7)  # 7=LTYPE_WIND
assert ret == 0

count_before = SapModel.LoadCases.Count()

# --- Target function ---
ret = SapModel.LoadCases.Delete("WIND_DEL")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.LoadCases.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.LoadCases.Delete"
result["deleted"] = "WIND_DEL"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_LoadCases_ChangeName.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadCases.ChangeName
# Category: Load_Cases
# Description: Rename a load case
# Verified: 2026-03-28
# Prerequisites: Model open, load case exists
# ============================================================
"""
Usage: Changes the name of an existing load case.

API Signature:
  SapModel.LoadCases.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing load case name
  NewName : str — New name for the load case
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.LoadPatterns.Add("RENAME_LC", 3)
assert ret == 0

# --- Target function ---
ret = SapModel.LoadCases.ChangeName("RENAME_LC", "RENAMED_LC")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify via GetNameList
raw = SapModel.LoadCases.GetNameList(0, [])
assert raw[-1] == 0
case_names = list(raw[1])
assert "RENAMED_LC" in case_names, f"RENAMED_LC not found in: {case_names}"
assert "RENAME_LC" not in case_names, f"RENAME_LC still exists in: {case_names}"

# --- Result ---
result["function"] = "SapModel.LoadCases.ChangeName"
result["old_name"] = "RENAME_LC"
result["new_name"] = "RENAMED_LC"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_LoadPatterns_Count.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadPatterns.Count
# Category: Load_Patterns
# Description: Get total number of load patterns
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined load patterns in the model.

API Signature:
  SapModel.LoadPatterns.Count()

ByRef Output:
  count (direct return, integer)

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
count_before = SapModel.LoadPatterns.Count()
assert count_before >= 1, f"Expected at least 1 (DEAD), got {count_before}"

# Add patterns and recount
ret = SapModel.LoadPatterns.Add("LIVE_C", 3)
assert ret == 0
ret = SapModel.LoadPatterns.Add("WIND_C", 7)
assert ret == 0

count_after = SapModel.LoadPatterns.Count()
assert count_after == count_before + 2, f"Expected {count_before + 2}, got {count_after}"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.Count"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_LoadPatterns_Delete.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadPatterns.Delete
# Category: Load_Patterns
# Description: Delete a load pattern
# Verified: 2026-03-28
# Prerequisites: Model open, load pattern exists, at least 2 patterns
# ============================================================
"""
Usage: Deletes a specified load pattern from the model.
       Cannot delete the last remaining load pattern.

API Signature:
  SapModel.LoadPatterns.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of existing load pattern
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: must have >1 pattern ---
ret = SapModel.LoadPatterns.Add("TEMP_LP", 3)
assert ret == 0

count_before = SapModel.LoadPatterns.Count()

# --- Target function ---
ret = SapModel.LoadPatterns.Delete("TEMP_LP")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.LoadPatterns.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.Delete"
result["deleted"] = "TEMP_LP"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_LoadPatterns_ChangeName.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadPatterns.ChangeName
# Category: Load_Patterns
# Description: Rename a load pattern
# Verified: 2026-03-28
# Prerequisites: Model open, load pattern exists
# ============================================================
"""
Usage: Changes the name of an existing load pattern.

API Signature:
  SapModel.LoadPatterns.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing load pattern name
  NewName : str — New name for the load pattern
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# DEAD pattern exists by default
# --- Target function ---
ret = SapModel.LoadPatterns.ChangeName("DEAD", "PP")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify
raw = SapModel.LoadPatterns.GetNameList(0, [])
assert raw[-1] == 0
pat_names = list(raw[1])
assert "PP" in pat_names, f"PP not found in: {pat_names}"
assert "DEAD" not in pat_names, f"DEAD still exists in: {pat_names}"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.ChangeName"
result["old_name"] = "DEAD"
result["new_name"] = "PP"
result["status"] = "verified"
```

- [ ] Register all 7 functions in `scripts/registry.json`
- [ ] Execute each wrapper via MCP `run_sap_script` and verify `ret_code == 0`

##### Step 5 Verification Checklist
- [ ] All 7 wrappers execute without assertion errors
- [ ] `Count` reports correct totals before/after operations
- [ ] `Delete` and `ChangeName` confirmed via `GetNameList`
- [ ] `SetDampConstant` succeeds on RS case
- [ ] All 7 functions appear in `registry.json` with `verified: true`

#### Step 5 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 6: Mass Source (Tier 2 — Workflow sísmico)

4 wrappers: `SourceMass.SetMassSource`, `.GetMassSource`, `.GetDefault`, `.Count`

- [ ] Create file `scripts/wrappers/func_SourceMass_SetMassSource.py`:

```python
# ============================================================
# Wrapper: SapModel.SourceMass.SetMassSource
# Category: Mass_Source
# Description: Add or reinitialize a mass source definition
# Verified: 2026-03-28
# Prerequisites: Model open, load patterns defined
# ============================================================
"""
Usage: Creates or reinitializes a mass source specifying which
       elements and load patterns contribute to the model mass.
       Essential for seismic and modal analysis workflows.

API Signature:
  SapModel.SourceMass.SetMassSource(Name, MassFromElements,
    MassFromMasses, MassFromLoads, IsDefault,
    NumberLoads, LoadPat[], SF[])

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name             : str    — Mass source name (creates if new)
  MassFromElements : bool   — Include element self mass
  MassFromMasses   : bool   — Include assigned masses
  MassFromLoads    : bool   — Include specified load patterns
  IsDefault        : bool   — Set as default mass source
  NumberLoads      : int    — Number of load patterns
  LoadPat          : str[]  — Load pattern names
  SF               : float[] — Scale factors for each pattern
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: ensure DEAD pattern exists ---
# DEAD is auto-created in blank model

# --- Target function: create mass source with DEAD×1.0 ---
ret = SapModel.SourceMass.SetMassSource(
    "MASS_SISMICO",  # Name
    True,            # MassFromElements
    True,            # MassFromMasses
    True,            # MassFromLoads
    True,            # IsDefault
    1,               # NumberLoads
    ["DEAD"],        # LoadPat
    [1.0]            # SF
)
assert ret == 0, f"SetMassSource failed: {ret}"

# Create second mass source with multiple patterns
ret = SapModel.LoadPatterns.Add("LIVE", 3)
assert ret == 0

ret = SapModel.SourceMass.SetMassSource(
    "MASS_PLUS_LIVE",
    True, True, True,
    False,            # Not default
    2,                # NumberLoads
    ["DEAD", "LIVE"], # LoadPat
    [1.0, 0.25]       # SF (DEAD×1.0 + LIVE×0.25)
)
assert ret == 0, f"SetMassSource(MASS_PLUS_LIVE) failed: {ret}"

# --- Verification ---
count = SapModel.SourceMass.Count()
assert count >= 2, f"Expected at least 2 mass sources, got {count}"

# --- Result ---
result["function"] = "SapModel.SourceMass.SetMassSource"
result["mass_sources_created"] = ["MASS_SISMICO", "MASS_PLUS_LIVE"]
result["count"] = count
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_SourceMass_GetMassSource.py`:

```python
# ============================================================
# Wrapper: SapModel.SourceMass.GetMassSource
# Category: Mass_Source
# Description: Retrieve mass source data
# Verified: 2026-03-28
# Prerequisites: Model open, mass source defined
# ============================================================
"""
Usage: Gets the mass source configuration including which elements,
       masses and load patterns contribute, plus scale factors.

API Signature:
  SapModel.SourceMass.GetMassSource(Name, MassFromElements,
    MassFromMasses, MassFromLoads, IsDefault,
    NumberLoads, LoadPat[], SF[])

ByRef Output:
  [MassFromElements, MassFromMasses, MassFromLoads, IsDefault,
   NumberLoads, LoadPat[], SF[], ret_code]

Parameters:
  Name : str — Existing mass source name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create mass source ---
ret = SapModel.SourceMass.SetMassSource(
    "MS_GET_TEST", True, True, True, True, 1, ["DEAD"], [1.0]
)
assert ret == 0

# --- Target function ---
raw = SapModel.SourceMass.GetMassSource(
    "MS_GET_TEST", False, False, False, False, 0, [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"GetMassSource failed: {ret_code}"

mass_from_elements = raw[0]
mass_from_masses = raw[1]
mass_from_loads = raw[2]
is_default = raw[3]
num_loads = raw[4]

assert mass_from_elements == True, f"MassFromElements mismatch: {mass_from_elements}"
assert mass_from_loads == True, f"MassFromLoads mismatch: {mass_from_loads}"
assert is_default == True, f"IsDefault mismatch: {is_default}"
assert num_loads >= 1, f"Expected NumberLoads >= 1, got {num_loads}"

# --- Result ---
result["function"] = "SapModel.SourceMass.GetMassSource"
result["mass_from_elements"] = mass_from_elements
result["mass_from_loads"] = mass_from_loads
result["is_default"] = is_default
result["num_loads"] = num_loads
result["byref_layout"] = "[MassFromElements, MassFromMasses, MassFromLoads, IsDefault, NumberLoads, LoadPat[], SF[], ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_SourceMass_GetDefault.py`:

```python
# ============================================================
# Wrapper: SapModel.SourceMass.GetDefault
# Category: Mass_Source
# Description: Retrieve the default mass source name
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the name of the default mass source.

API Signature:
  SapModel.SourceMass.GetDefault(Name)

ByRef Output:
  [Name, ret_code]

Parameters:
  Name : str — (ByRef out) Default mass source name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: get default mass source ---
raw = SapModel.SourceMass.GetDefault("")
ret_code = raw[-1]
assert ret_code == 0, f"GetDefault failed: {ret_code}"
default_name = raw[0]

# Create custom mass source as default, then verify
ret = SapModel.SourceMass.SetMassSource(
    "MY_DEFAULT", True, True, True, True, 1, ["DEAD"], [1.0]
)
assert ret == 0

raw2 = SapModel.SourceMass.GetDefault("")
assert raw2[-1] == 0
assert raw2[0] == "MY_DEFAULT", f"Expected MY_DEFAULT, got {raw2[0]}"

# --- Result ---
result["function"] = "SapModel.SourceMass.GetDefault"
result["initial_default"] = default_name
result["new_default"] = raw2[0]
result["byref_layout"] = "[Name, ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_SourceMass_Count.py`:

```python
# ============================================================
# Wrapper: SapModel.SourceMass.Count
# Category: Mass_Source
# Description: Get total number of mass sources
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined mass sources.

API Signature:
  SapModel.SourceMass.Count()

ByRef Output:
  count (direct return, integer)

Parameters:
  (none)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
count_before = SapModel.SourceMass.Count()
assert count_before >= 1, f"Expected at least 1 default mass source, got {count_before}"

# Add a mass source
ret = SapModel.SourceMass.SetMassSource(
    "MS_COUNT_TEST", True, True, True, False, 1, ["DEAD"], [1.0]
)
assert ret == 0

count_after = SapModel.SourceMass.Count()
assert count_after == count_before + 1, f"Expected {count_before + 1}, got {count_after}"

# --- Result ---
result["function"] = "SapModel.SourceMass.Count"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Register all 4 functions in `scripts/registry.json`
- [ ] Execute each wrapper via MCP `run_sap_script` and verify `ret_code == 0`

##### Step 6 Verification Checklist
- [ ] All 4 wrappers execute without assertion errors
- [ ] `SetMassSource` → `GetMassSource` roundtrip produces matching flags/SFs
- [ ] `GetDefault` returns correct default after setting new default
- [ ] `Count` increments correctly after adding mass source
- [ ] All 4 functions appear in `registry.json` with `verified: true`

#### Step 6 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 7: Constraint Types + Admin (Tier 2)

6 wrappers: `ConstraintDef.SetBeam`, `.SetPlate`, `.SetEqual`, `.Count`, `.Delete`, `.GetNameList`

- [ ] Create file `scripts/wrappers/func_ConstraintDef_SetBeam.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.SetBeam
# Category: Constraints
# Description: Define a beam constraint for rigid beam connections
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a beam constraint that couples selected DOFs.
       Beam constraints are used for connecting elements where
       rotations are coupled in a beam-like manner.

API Signature:
  SapModel.ConstraintDef.SetBeam(Name, Value, CSys)

ByRef Output:
  ret_code — returned at raw[-1] (ByRef echo pattern)

Parameters:
  Name  : str     — Constraint name
  Value : bool[6] — DOF coupling [UX, UY, UZ, RX, RY, RZ]
  CSys  : str     — Coordinate system (default="Global")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
dof = [True, True, True, True, True, True]
raw = SapModel.ConstraintDef.SetBeam("BEAM_CONST", dof, "Global")
assert raw[-1] == 0, f"SetBeam failed: {raw[-1]}"

# Partial DOF beam constraint
dof_partial = [True, True, True, False, False, False]
raw2 = SapModel.ConstraintDef.SetBeam("BEAM_TRANSL", dof_partial, "Global")
assert raw2[-1] == 0, f"SetBeam(partial) failed: {raw2[-1]}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.SetBeam"
result["constraints_created"] = ["BEAM_CONST", "BEAM_TRANSL"]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_ConstraintDef_SetPlate.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.SetPlate
# Category: Constraints
# Description: Define a plate constraint for slab connections
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a plate constraint. Plate constraints couple
       in-plane deformations (like a plate/membrane).

API Signature:
  SapModel.ConstraintDef.SetPlate(Name, Value, CSys)

ByRef Output:
  ret_code — returned at raw[-1]

Parameters:
  Name  : str     — Constraint name
  Value : bool[6] — DOF coupling [UX, UY, UZ, RX, RY, RZ]
  CSys  : str     — Coordinate system (default="Global")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
# In-plane: UX, UY, RZ
dof = [True, True, False, False, False, True]
raw = SapModel.ConstraintDef.SetPlate("PLATE_CONST", dof, "Global")
assert raw[-1] == 0, f"SetPlate failed: {raw[-1]}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.SetPlate"
result["constraints_created"] = ["PLATE_CONST"]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_ConstraintDef_SetEqual.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.SetEqual
# Category: Constraints
# Description: Define an equal constraint (equal displacements)
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates an equal constraint. Assigned joints will have
       equal displacements in the specified DOFs.

API Signature:
  SapModel.ConstraintDef.SetEqual(Name, Value, CSys)

ByRef Output:
  ret_code — returned at raw[-1]

Parameters:
  Name  : str     — Constraint name
  Value : bool[6] — DOF coupling [UX, UY, UZ, RX, RY, RZ]
  CSys  : str     — Coordinate system (default="Global")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
dof_all = [True, True, True, True, True, True]
raw = SapModel.ConstraintDef.SetEqual("EQUAL_ALL", dof_all, "Global")
assert raw[-1] == 0, f"SetEqual(all) failed: {raw[-1]}"

# Equal vertical displacement only
dof_uz = [False, False, True, False, False, False]
raw2 = SapModel.ConstraintDef.SetEqual("EQUAL_UZ", dof_uz, "Global")
assert raw2[-1] == 0, f"SetEqual(UZ) failed: {raw2[-1]}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.SetEqual"
result["constraints_created"] = ["EQUAL_ALL", "EQUAL_UZ"]
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_ConstraintDef_Count.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.Count
# Category: Constraints
# Description: Get total number of constraint definitions
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the total number of defined constraints, optionally
       filtered by constraint type.

API Signature:
  SapModel.ConstraintDef.Count(ConstraintType)

ByRef Output:
  count (direct return, integer)

Parameters:
  ConstraintType : int — (optional) 0=All, 1=Body, 2=Diaphragm,
                          3=Plate, 4=Rod, 5=Beam, 6=Equal, 7=Local,
                          8=Weld, 9=Line
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Create constraints ---
dof = [True, True, True, True, True, True]
raw = SapModel.ConstraintDef.SetBody("COUNT_BODY", dof, "Global")
assert raw[-1] == 0

raw = SapModel.ConstraintDef.SetBeam("COUNT_BEAM", dof, "Global")
assert raw[-1] == 0

# --- Target function ---
count_all = SapModel.ConstraintDef.Count(0)  # 0=All
assert count_all >= 2, f"Expected at least 2 constraints, got {count_all}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.Count"
result["count_all"] = count_all
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_ConstraintDef_Delete.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.Delete
# Category: Constraints
# Description: Delete a constraint definition
# Verified: 2026-03-28
# Prerequisites: Model open, constraint defined
# ============================================================
"""
Usage: Deletes a specified constraint definition.

API Signature:
  SapModel.ConstraintDef.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of existing constraint to delete
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
dof = [True, True, True, True, True, True]
raw = SapModel.ConstraintDef.SetBody("DEL_CONST", dof, "Global")
assert raw[-1] == 0

count_before = SapModel.ConstraintDef.Count(0)

# --- Target function ---
ret = SapModel.ConstraintDef.Delete("DEL_CONST")
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"Delete failed: {ret_code}"

count_after = SapModel.ConstraintDef.Count(0)
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.Delete"
result["deleted"] = "DEL_CONST"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_ConstraintDef_GetNameList.py`:

```python
# ============================================================
# Wrapper: SapModel.ConstraintDef.GetNameList
# Category: Constraints
# Description: Retrieve names of all constraint definitions
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the names of all defined constraints in the model.

API Signature:
  SapModel.ConstraintDef.GetNameList(NumberNames, MyName[])

ByRef Output:
  [NumberNames, MyName[], ret_code]

Parameters:
  NumberNames : int   — (ByRef out) Number of constraint names
  MyName      : str[] — (ByRef out) Array of constraint names
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
dof = [True, True, True, True, True, True]
raw = SapModel.ConstraintDef.SetBody("NL_BODY", dof, "Global")
assert raw[-1] == 0

ret = SapModel.ConstraintDef.SetDiaphragm("NL_DIAPH", 4)  # 4=Auto axis
assert ret == 0

# --- Target function ---
raw = SapModel.ConstraintDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

num_names = raw[0]
names = list(raw[1]) if isinstance(raw[1], (list, tuple)) else [raw[1]]

assert "NL_BODY" in names, f"NL_BODY not found in: {names}"
assert "NL_DIAPH" in names, f"NL_DIAPH not found in: {names}"

# --- Result ---
result["function"] = "SapModel.ConstraintDef.GetNameList"
result["num_constraints"] = num_names
result["constraint_names"] = names
result["byref_layout"] = "[NumberNames, MyName[], ret_code]"
result["status"] = "verified"
```

- [ ] Register all 6 functions in `scripts/registry.json`
- [ ] Execute each wrapper via MCP `run_sap_script` and verify `ret_code == 0`

##### Step 7 Verification Checklist
- [ ] All 6 wrappers execute without assertion errors
- [ ] `SetBeam`, `SetPlate`, `SetEqual` constraints created successfully
- [ ] `Count` returns correct total after creating constraints
- [ ] `Delete` removes constraint (count decrements)
- [ ] `GetNameList` contains all created constraint names
- [ ] All 6 functions appear in `registry.json` with `verified: true`

#### Step 7 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 8: Frame/Area Modifiers + Property Admin (Tier 2)

10 wrappers: `FrameObj.SetModifiers`, `.GetModifiers`, `PropArea.SetModifiers`, `.GetModifiers`, `PropFrame.ChangeName`, `.Delete`, `.Count`, `PropMaterial.ChangeName`, `.Delete`, `.Count`

- [ ] Create file `scripts/wrappers/func_FrameObj_SetModifiers.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.SetModifiers
# Category: FrameObj
# Description: Set stiffness modifiers for a frame object
# Verified: 2026-03-28
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Assigns stiffness modification factors to a frame element.
       Essential for seismic design (cracked section analysis).
       Common values: beams 0.35×I, columns 0.70×I per ACI 318.

API Signature:
  SapModel.FrameObj.SetModifiers(Name, Value)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name  : str      — Frame object name
  Value : float[8] — Modifier array:
    [0]=Area, [1]=AS2(shear), [2]=AS3(shear),
    [3]=Torsion, [4]=I22, [5]=I33,
    [6]=Mass, [7]=Weight
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_MOD", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_MOD", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_MOD", "CONC_MOD", 0.6, 0.3)
assert ret == 0

# Create beam
raw = SapModel.FrameObj.AddByCoord(0, 0, 3, 6, 0, 3, "", "BEAM_MOD", "")
beam_name = raw[0]
assert raw[-1] == 0

# --- Target function: apply cracked section modifiers (beam) ---
# ACI 318: beams I = 0.35×Ig
beam_mods = [1.0, 1.0, 1.0, 1.0, 0.35, 0.35, 1.0, 1.0]
ret = SapModel.FrameObj.SetModifiers(beam_name, beam_mods)
assert ret == 0, f"SetModifiers(beam) failed: {ret}"

# Create column with column modifiers
raw2 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "BEAM_MOD", "")
col_name = raw2[0]
assert raw2[-1] == 0

# ACI 318: columns I = 0.70×Ig
col_mods = [1.0, 1.0, 1.0, 1.0, 0.70, 0.70, 1.0, 1.0]
ret = SapModel.FrameObj.SetModifiers(col_name, col_mods)
assert ret == 0, f"SetModifiers(column) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetModifiers"
result["beam"] = beam_name
result["beam_modifiers"] = beam_mods
result["column"] = col_name
result["column_modifiers"] = col_mods
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_FrameObj_GetModifiers.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.GetModifiers
# Category: FrameObj
# Description: Retrieve stiffness modifiers for a frame object
# Verified: 2026-03-28
# Prerequisites: Model open, frame with modifiers
# ============================================================
"""
Usage: Reads back the stiffness modification factors from a frame.

API Signature:
  SapModel.FrameObj.GetModifiers(Name, Value)

ByRef Output:
  [Value[8], ret_code]

Parameters:
  Name  : str      — Frame object name
  Value : float[8] — (ByRef out) Modifier array
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_GM", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_GM", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_GM", "CONC_GM", 0.5, 0.3)
assert ret == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_GM", "")
frame_name = raw[0]
assert raw[-1] == 0

# Set known modifiers
set_mods = [1.0, 1.0, 1.0, 0.5, 0.35, 0.35, 1.0, 1.0]
ret = SapModel.FrameObj.SetModifiers(frame_name, set_mods)
assert ret == 0

# --- Target function ---
raw = SapModel.FrameObj.GetModifiers(frame_name, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetModifiers failed: {ret_code}"

got_mods = list(raw[0])
# Verify I33 and I22 modifiers
assert abs(got_mods[4] - 0.35) < 0.01, f"I22 mismatch: expected 0.35, got {got_mods[4]}"
assert abs(got_mods[5] - 0.35) < 0.01, f"I33 mismatch: expected 0.35, got {got_mods[5]}"

# --- Result ---
result["function"] = "SapModel.FrameObj.GetModifiers"
result["frame_name"] = frame_name
result["modifiers"] = got_mods
result["byref_layout"] = "[Value[8], ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropArea_SetModifiers.py`:

```python
# ============================================================
# Wrapper: SapModel.PropArea.SetModifiers
# Category: PropArea
# Description: Set stiffness modifiers for an area property
# Verified: 2026-03-28
# Prerequisites: Model open, area property defined
# ============================================================
"""
Usage: Assigns stiffness modification factors to an area property.
       Applied to ALL area objects using this property.
       Array of 10 modifiers for shell elements.

API Signature:
  SapModel.PropArea.SetModifiers(Name, Value)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name  : str       — Area section property name
  Value : float[10] — Modifier array:
    [0]=f11, [1]=f22, [2]=f12, [3]=m11, [4]=m22,
    [5]=m12, [6]=v13, [7]=v23, [8]=mass, [9]=weight
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_AM", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_AM", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

ret = SapModel.PropArea.SetShell_1("SLAB_MOD", 1, True, "CONC_AM", 0, 0.2, 0.2)
assert ret == 0, f"SetShell_1 failed: {ret}"

# --- Target function ---
# Cracked slab modifiers: reduce bending stiffness
slab_mods = [1.0, 1.0, 1.0, 0.25, 0.25, 0.25, 1.0, 1.0, 1.0, 1.0]
ret = SapModel.PropArea.SetModifiers("SLAB_MOD", slab_mods)
assert ret == 0, f"SetModifiers failed: {ret}"

# --- Result ---
result["function"] = "SapModel.PropArea.SetModifiers"
result["section"] = "SLAB_MOD"
result["modifiers"] = slab_mods
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropArea_GetModifiers.py`:

```python
# ============================================================
# Wrapper: SapModel.PropArea.GetModifiers
# Category: PropArea
# Description: Retrieve stiffness modifiers for an area property
# Verified: 2026-03-28
# Prerequisites: Model open, area property with modifiers
# ============================================================
"""
Usage: Reads back the stiffness modification factors for an area property.

API Signature:
  SapModel.PropArea.GetModifiers(Name, Value)

ByRef Output:
  [Value[10], ret_code]

Parameters:
  Name  : str       — Area section property name
  Value : float[10] — (ByRef out) Modifier array
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_AGM", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_AGM", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("WALL_MOD", 1, True, "CONC_AGM", 0, 0.25, 0.25)
assert ret == 0

# Set known modifiers
set_mods = [1.0, 1.0, 1.0, 0.70, 0.70, 0.70, 1.0, 1.0, 1.0, 1.0]
ret = SapModel.PropArea.SetModifiers("WALL_MOD", set_mods)
assert ret == 0

# --- Target function ---
raw = SapModel.PropArea.GetModifiers("WALL_MOD", [])
ret_code = raw[-1]
assert ret_code == 0, f"GetModifiers failed: {ret_code}"

got_mods = list(raw[0])
assert abs(got_mods[3] - 0.70) < 0.01, f"m11 mismatch: expected 0.70, got {got_mods[3]}"

# --- Result ---
result["function"] = "SapModel.PropArea.GetModifiers"
result["section"] = "WALL_MOD"
result["modifiers"] = got_mods
result["byref_layout"] = "[Value[10], ret_code]"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropFrame_ChangeName.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.ChangeName
# Category: PropFrame
# Description: Rename a frame section property
# Verified: 2026-03-28
# Prerequisites: Model open, frame section defined
# ============================================================
"""
Usage: Changes the name of an existing frame section property.

API Signature:
  SapModel.PropFrame.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing frame section name
  NewName : str — New name for the section
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_CN", 2)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("OLD_SEC", "MAT_CN", 0.5, 0.3)
assert ret == 0

# --- Target function ---
ret = SapModel.PropFrame.ChangeName("OLD_SEC", "NEW_SEC")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify
raw = SapModel.PropFrame.GetNameList(0, [])
assert raw[-1] == 0
names = list(raw[1])
assert "NEW_SEC" in names, f"NEW_SEC not found in: {names}"
assert "OLD_SEC" not in names, f"OLD_SEC still exists in: {names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.ChangeName"
result["old_name"] = "OLD_SEC"
result["new_name"] = "NEW_SEC"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropFrame_Delete.py`:

```python
# ============================================================
# Wrapper: SapModel.PropFrame.Delete
# Category: PropFrame
# Description: Delete a frame section property
# Verified: 2026-03-28
# Prerequisites: Model open, frame section defined, not in use
# ============================================================
"""
Usage: Deletes a frame section property. Cannot delete if in use
       by any frame object.

API Signature:
  SapModel.PropFrame.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of frame section to delete
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_DEL", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TO_DEL", "MAT_DEL", 0.3, 0.3)
assert ret == 0

count_before = SapModel.PropFrame.Count()

# --- Target function ---
ret = SapModel.PropFrame.Delete("SEC_TO_DEL")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.PropFrame.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.PropFrame.Delete"
result["deleted"] = "SEC_TO_DEL"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropFrame_Count.py`:

```python
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
```

- [ ] Create file `scripts/wrappers/func_PropMaterial_ChangeName.py`:

```python
# ============================================================
# Wrapper: SapModel.PropMaterial.ChangeName
# Category: PropMaterial
# Description: Rename a material property
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Changes the name of an existing material property.

API Signature:
  SapModel.PropMaterial.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing material name
  NewName : str — New name for the material
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("OLD_MAT", 1)
assert ret == 0

# --- Target function ---
ret = SapModel.PropMaterial.ChangeName("OLD_MAT", "NEW_MAT")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify
raw = SapModel.PropMaterial.GetNameList(0, [])
assert raw[-1] == 0
mat_names = list(raw[1])
assert "NEW_MAT" in mat_names, f"NEW_MAT not found in: {mat_names}"
assert "OLD_MAT" not in mat_names, f"OLD_MAT still exists in: {mat_names}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.ChangeName"
result["old_name"] = "OLD_MAT"
result["new_name"] = "NEW_MAT"
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropMaterial_Delete.py`:

```python
# ============================================================
# Wrapper: SapModel.PropMaterial.Delete
# Category: PropMaterial
# Description: Delete a material property
# Verified: 2026-03-28
# Prerequisites: Model open, material defined, not in use
# ============================================================
"""
Usage: Deletes a material property. Cannot delete if in use
       by any section or element.

API Signature:
  SapModel.PropMaterial.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of material to delete
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TO_DEL", 1)
assert ret == 0

count_before = SapModel.PropMaterial.Count()

# --- Target function ---
ret = SapModel.PropMaterial.Delete("MAT_TO_DEL")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.PropMaterial.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.Delete"
result["deleted"] = "MAT_TO_DEL"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
```

- [ ] Create file `scripts/wrappers/func_PropMaterial_Count.py`:

```python
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
```

- [ ] Register all 10 functions in `scripts/registry.json`
- [ ] Execute each wrapper via MCP `run_sap_script` and verify `ret_code == 0`

##### Step 8 Verification Checklist
- [ ] All 10 wrappers execute without assertion errors
- [ ] `FrameObj.SetModifiers` → `GetModifiers` roundtrip matches (I22=0.35, I33=0.35)
- [ ] `PropArea.SetModifiers` → `GetModifiers` roundtrip matches
- [ ] `ChangeName` renames (old gone, new present) for both PropFrame and PropMaterial
- [ ] `Delete` removes property (count decrements) for both PropFrame and PropMaterial
- [ ] `Count` returns correct totals
- [ ] All 10 functions appear in `registry.json` with `verified: true`

#### Step 8 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

## Final Summary

| Step | Wrappers | Category | Priority |
|------|----------|----------|----------|
| 1 | 4 | PropMaterial (Design Props + Getters) | Tier 1 |
| 2 | 6 | PropFrame (New Types + Getters) | Tier 1 |
| 3 | 9 | Design (Steel + Concrete workflows) | Tier 1 |
| 4 | 7 | RespCombo (CRUD completo) | Tier 1 |
| 5 | 7 | LoadCases + LoadPatterns (Admin) | Tier 2 |
| 6 | 4 | SourceMass (Seismic workflow) | Tier 2 |
| 7 | 6 | ConstraintDef (New Types + Admin) | Tier 2 |
| 8 | 10 | Frame/Area Modifiers + Property Admin | Tier 2 |
| **Total** | **53** | | |

After all steps, the registry will have ~186 verified functions (133 + 53).
