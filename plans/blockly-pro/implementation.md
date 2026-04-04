# Blockly Visual Scripter — Profesionalización

## Goal
Transformar el prototipo Blockly en un editor visual completo: reorganizar archivos en `scripts/blockly/`, generar bloques paramétricos desde el registry, transpilación data-driven, y GUI profesional con PySide6.

## Prerequisites
Make sure that the user is currently on the `feat/blockly-pro` branch before beginning implementation.
If not, move them to the correct branch. If the branch does not exist, create it from main.

```powershell
git checkout -b feat/blockly-pro main
```

### Step-by-Step Instructions

---

#### Step 0: Reorganizar archivos Blockly en `scripts/blockly/`

Mover los 4 módulos Python (`blockly_generator.py`, `blockly_transpiler.py`, `blockly_executor.py`, `blockly_gui.py`) a la carpeta `scripts/blockly/` para que todo lo relacionado con Blockly esté en un solo lugar.

- [x] Mover archivos Python al directorio `scripts/blockly/`:

```powershell
cd c:\Users\fcoca\Desktop\Ingenieria\Proyectos_Python\Skills_SAP
git mv scripts/blockly_generator.py scripts/blockly/blockly_generator.py
git mv scripts/blockly_transpiler.py scripts/blockly/blockly_transpiler.py
git mv scripts/blockly_executor.py scripts/blockly/blockly_executor.py
git mv scripts/blockly_gui.py scripts/blockly/blockly_gui.py
```

- [x] Crear `scripts/blockly/__init__.py`:

```python
"""
SAP2000 Visual Scripter — Blockly
==================================
Editor visual drag-and-drop para crear scripts de SAP2000.

Módulos:
  - blockly_generator: Genera block_definitions.js, generators.js, toolbox_structure.xml
  - blockly_transpiler: Convierte Blockly XML → Python
  - blockly_executor: Ejecuta Python contra SAP2000 vía COM
  - blockly_gui: Aplicación PySide6 con editor Blockly embebido

Uso:
    python -m scripts.blockly.blockly_gui
    # o directamente:
    python scripts/blockly/blockly_gui.py
"""
```

- [x] Actualizar imports en `scripts/blockly/blockly_gui.py` — cambiar imports relativos:

Reemplazar las líneas 31-32:
```python
from blockly_transpiler import BlocklyTranspiler
from blockly_executor import BlocklyScriptExecutor
```

Por:
```python
try:
    from blockly_transpiler import BlocklyTranspiler
    from blockly_executor import BlocklyScriptExecutor
except ImportError:
    from .blockly_transpiler import BlocklyTranspiler
    from .blockly_executor import BlocklyScriptExecutor
```

- [x] Actualizar default paths en `scripts/blockly/blockly_generator.py` — función `main()`:

Reemplazar:
```python
def main():
    """CLI entry point"""
    import sys
    
    registry_path = sys.argv[1] if len(sys.argv) > 1 else "scripts/registry.json"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "scripts/blockly"
```

Por:
```python
def main():
    """CLI entry point"""
    import sys
    
    # Detectar ubicación relativa al proyecto
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent  # scripts/blockly/ → scripts/ → project_root/
    
    registry_path = sys.argv[1] if len(sys.argv) > 1 else str(project_root / "scripts" / "registry.json")
    output_dir = sys.argv[2] if len(sys.argv) > 2 else str(script_dir)
```

- [x] Actualizar `scripts/blockly/README.md` con la nueva estructura de carpetas:

Reemplazar la sección de estructura:
```markdown
## 🛠️ Estructura de Carpetas

```
scripts/blockly/                    # Todo Blockly en un solo lugar
├── __init__.py                    # Package init
├── blockly_gui.py                 # 🚀 APP PRINCIPAL
├── blockly_executor.py            # Executor SAP2000 (COM bridge)
├── blockly_transpiler.py          # XML → Python translator
├── blockly_generator.py           # Genera bloques desde registry
├── index.html                     # HTML + Blockly CDN (standalone)
├── block_definitions.js           # AUTO-GENERADO
├── toolbox_structure.xml          # AUTO-GENERADO
├── generators.js                  # AUTO-GENERADO
└── README.md                      # Esta documentación
```
```

- [x] Actualizar comandos de ejecución en el README:

Reemplazar:
```markdown
### 2. Generar definiciones de bloques (desde registry.json)

```bash
python scripts/blockly/blockly_generator.py
```

### 3. Ejecutar modo demo (sin SAP2000)

```bash
python scripts/blockly/blockly_gui.py
```
```

##### Step 0 Verification Checklist
- [x] `python scripts/blockly/blockly_gui.py` abre la app sin errores de import
- [x] `python scripts/blockly/blockly_generator.py` genera los 3 archivos JS/XML
- [x] No quedan archivos `blockly_*.py` sueltos en `scripts/` (solo en `scripts/blockly/`)
- [x] `git status` muestra los renames correctamente

#### Step 0 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

```powershell
git add -A
git commit -m "refactor: move all blockly modules into scripts/blockly/"
```

---

#### Step 1: Reescribir `blockly_generator.py` — Motor de generación con parámetros

Reescribir el generador para que extraiga parámetros reales de cada función del registry y produzca bloques con campos editables, generadores Python completos, y toolbox con bloques listados.

- [x] Reemplazar el contenido completo de `scripts/blockly/blockly_generator.py` con el código siguiente:

```python
"""
Blockly Block Generator — Auto-genera definiciones de bloques desde registry.json
===============================================================================
Genera:
  1. block_definitions.js — Blockly block JSON con args0 poblados
  2. toolbox_structure.xml — Toolbox organizado por 9 fases con bloques listados
  3. generators.js — Generador Python para CADA bloque

Uso:
    python scripts/blockly/blockly_generator.py [registry_path] [output_dir]
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


# ─── Phase colors (Blockly hue 0-360) ───────────────────────────────────────

PHASE_COLORS = {
    1: 0,       # Rojo: Init (File)
    2: 30,      # Naranja: Materials
    3: 60,      # Amarillo: Sections
    4: 120,     # Verde: Geometry
    5: 160,     # Cian: Constraints/Groups
    6: 200,     # Azul claro: Loads
    7: 230,     # Azul: Analysis
    8: 270,     # Púrpura: Results
    9: 300,     # Magenta: Design
    999: 210,   # Gris-azul: Utility / Sin fase
}

PHASE_NAMES = {
    1: "Inicializar",
    2: "Materiales",
    3: "Secciones",
    4: "Geometría",
    5: "Restricciones / Grupos",
    6: "Cargas",
    7: "Análisis",
    8: "Resultados",
    9: "Diseño",
}

# ─── Category → Phase mapping ───────────────────────────────────────────────

CATEGORY_PHASE = {
    "File": 1,
    "PropMaterial": 2,
    "PropFrame": 3, "PropArea": 3, "Properties": 3,
    "Object_Model": 4, "FrameObj": 4, "AreaObj": 4, "Edit": 4,
    "Constraints": 5, "Groups": 5, "Select": 5,
    "Load_Patterns": 6, "Load_Cases": 6, "RespCombo": 6, "Mass_Source": 6,
    "Analyze": 7,
    "Analysis_Results": 8, "Database_Tables": 8,
    "Design": 9,
    "Functions": 999,
}

# ─── Known enum mappings (for dropdown generation) ──────────────────────────

ENUM_MAPS = {
    "MatType": {
        "Steel (1)": "1",
        "Concrete (2)": "2",
        "NoDesign (3)": "3",
        "Aluminum (4)": "4",
        "ColdFormed (5)": "5",
        "Rebar (6)": "6",
        "Tendon (7)": "7",
    },
    "eUnits": {
        "lb_in_F (1)": "1",
        "lb_ft_F (2)": "2",
        "kip_in_F (3)": "3",
        "kip_ft_F (4)": "4",
        "kN_mm_C (5)": "5",
        "kN_m_C (6)": "6",
        "kgf_mm_C (7)": "7",
        "kgf_m_C (8)": "8",
        "N_mm_C (9)": "9",
        "N_m_C (10)": "10",
        "Ton_mm_C (11)": "11",
        "Ton_m_C (12)": "12",
        "kN_cm_C (13)": "13",
        "kgf_cm_C (14)": "14",
        "N_cm_C (15)": "15",
        "Ton_cm_C (16)": "16",
    },
    "eLoadPatternType": {
        "Dead (1)": "1",
        "SuperDead (2)": "2",
        "Live (3)": "3",
        "ReduceLive (4)": "4",
        "Quake (5)": "5",
        "Wind (6)": "6",
        "Snow (7)": "7",
        "Other (8)": "8",
        "Move (9)": "9",
        "Temperature (10)": "10",
        "RoofLive (11)": "11",
        "Notional (12)": "12",
    },
    "eItemType": {
        "Object (0)": "0",
        "Group (1)": "1",
        "SelectedObjects (2)": "2",
    },
    "eFrameLoadDistType": {
        "Force (1)": "1",
        "Moment (2)": "2",
    },
    "eFrameLoadDir": {
        "Local1 (1)": "1",
        "Local2 (2)": "2",
        "Local3 (3)": "3",
        "X (4)": "4",
        "Y (5)": "5",
        "Z (6)": "6",
        "GravityProjected (10)": "10",
        "GravityFull (11)": "11",
    },
    "eDOF": {
        "UX": "True",
        "UY": "True",
        "UZ": "True",
        "RX": "True",
        "RY": "True",
        "RZ": "True",
    },
    "eShellType": {
        "ShellThin (1)": "1",
        "ShellThick (2)": "2",
        "Membrane (3)": "3",
        "Plate (4)": "4",
    },
    "eCombType": {
        "LinearAdd (0)": "0",
        "Envelope (1)": "1",
        "AbsAdd (2)": "2",
        "SRSS (3)": "3",
        "RangeAdd (4)": "4",
    },
}


@dataclass
class ParamDef:
    """Definición de un parámetro para un bloque Blockly."""
    name: str
    param_type: str  # "str", "float", "int", "bool", "enum", "list_bool"
    default: str = ""
    enum_key: str = ""  # Key en ENUM_MAPS si es dropdown
    description: str = ""
    required: bool = True


@dataclass
class BlockSpec:
    """Especificación completa de un bloque Blockly."""
    block_type: str          # e.g. "sap_File_NewBlank"
    func_path: str           # e.g. "SapModel.File.NewBlank"
    display_name: str        # e.g. "File.NewBlank"
    phase: int
    params: List[ParamDef] = field(default_factory=list)
    has_byref: bool = False
    byref_outputs: List[str] = field(default_factory=list)
    description: str = ""
    api_call: str = ""       # e.g. "SapModel.File.NewBlank()"


class BlocklyBlockGenerator:
    """Generador de bloques Blockly desde registry SAP2000."""

    def __init__(self, registry_path: str = "scripts/registry.json"):
        self.registry_path = Path(registry_path)
        self.registry = self._load_registry()
        self.output_dir: Optional[Path] = None
        self.block_specs: List[BlockSpec] = []

    def _load_registry(self) -> Dict[str, Any]:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry no encontrado: {self.registry_path}")
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ─── Main entry ──────────────────────────────────────────────────────

    def generate_all(self, output_dir: str = "scripts/blockly"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Parse registry → BlockSpecs
        self.block_specs = self._build_block_specs()
        print(f"📦 {len(self.block_specs)} bloques parseados del registry")

        # 2. Generate output files
        defs_js = self._generate_block_definitions_js()
        toolbox_xml = self._generate_toolbox_xml()
        gens_js = self._generate_generators_js()

        (self.output_dir / "block_definitions.js").write_text(defs_js, encoding="utf-8")
        (self.output_dir / "toolbox_structure.xml").write_text(toolbox_xml, encoding="utf-8")
        (self.output_dir / "generators.js").write_text(gens_js, encoding="utf-8")

        print(f"✅ Generados en {self.output_dir}:")
        print(f"   block_definitions.js  ({len(defs_js):,} bytes)")
        print(f"   toolbox_structure.xml ({len(toolbox_xml):,} bytes)")
        print(f"   generators.js         ({len(gens_js):,} bytes)")

    # ─── Registry → BlockSpec parsing ────────────────────────────────────

    def _build_block_specs(self) -> List[BlockSpec]:
        specs = []
        functions = self.registry.get("functions", {})

        for func_path, info in functions.items():
            if not func_path:
                continue

            # Derive block_type: SapModel.File.NewBlank → sap_File_NewBlank
            short_path = func_path.replace("SapModel.", "")
            block_type = "sap_" + short_path.replace(".", "_")
            display_name = short_path

            # Phase from category
            category = info.get("category", "")
            phase = CATEGORY_PHASE.get(category, 999)

            # Parse parameters
            params = self._parse_params(info)

            # ByRef detection
            notes = info.get("notes", "")
            has_byref = "ByRef" in notes or "Returns [" in notes or "ret_code]" in notes
            byref_outputs = self._parse_byref_outputs(notes)

            # API call path
            api_call = func_path

            spec = BlockSpec(
                block_type=block_type,
                func_path=func_path,
                display_name=display_name,
                phase=phase,
                params=params,
                has_byref=has_byref,
                byref_outputs=byref_outputs,
                description=info.get("description", ""),
                api_call=api_call,
            )
            specs.append(spec)

        return specs

    def _parse_params(self, info: Dict) -> List[ParamDef]:
        """Parse parameters from signature + parameter_notes."""
        params = []
        signature = info.get("signature", "")
        param_notes = info.get("parameter_notes", "")

        # Extract param names from signature: "(Name, MatType, ...) -> ret_code"
        sig_match = re.match(r"\(([^)]*)\)", signature)
        if not sig_match:
            return params

        raw_params = [p.strip() for p in sig_match.group(1).split(",") if p.strip()]

        for pname in raw_params:
            # Skip common optional/internal params
            if pname in ("Color", "Notes", "GUID", "CSys"):
                continue

            pdef = ParamDef(name=pname, param_type="str")

            # Detect type from parameter_notes
            pdef = self._infer_param_type(pdef, param_notes, pname)

            params.append(pdef)

        return params

    def _infer_param_type(self, pdef: ParamDef, notes: str, pname: str) -> ParamDef:
        """Infer field type from parameter notes and naming conventions."""
        name_lower = pname.lower()

        # Check for enum references in notes
        if "MatType" in pname or "eMatType" in notes:
            pdef.param_type = "enum"
            pdef.enum_key = "MatType"
            pdef.default = "2"
        elif "Units" in pname or "eUnits" in pname:
            pdef.param_type = "enum"
            pdef.enum_key = "eUnits"
            pdef.default = "6"
        elif "PatternType" in pname or "eLoadPatternType" in notes:
            pdef.param_type = "enum"
            pdef.enum_key = "eLoadPatternType"
            pdef.default = "1"
        elif "ItemType" in pname or "eItemType" in notes:
            pdef.param_type = "enum"
            pdef.enum_key = "eItemType"
            pdef.default = "0"
        elif "DistType" in pname:
            pdef.param_type = "enum"
            pdef.enum_key = "eFrameLoadDistType"
            pdef.default = "1"
        elif "Dir" == pname or "Dir" in pname and "load" in notes.lower():
            pdef.param_type = "enum"
            pdef.enum_key = "eFrameLoadDir"
            pdef.default = "10"
        elif "ShellType" in pname:
            pdef.param_type = "enum"
            pdef.enum_key = "eShellType"
            pdef.default = "1"
        elif "CombType" in pname or "ComboType" in pname:
            pdef.param_type = "enum"
            pdef.enum_key = "eCombType"
            pdef.default = "0"
        # Numeric fields by naming convention
        elif any(name_lower.startswith(prefix) for prefix in
                 ("x", "y", "z", "t2", "t3", "t", "e", "u", "r", "d",
                  "dist", "val", "sf", "weight", "mass", "load")):
            pdef.param_type = "float"
            pdef.default = "0"
        elif name_lower in ("tf", "tw", "bftop", "bfbot", "t2b", "hweb"):
            pdef.param_type = "float"
            pdef.default = "0"
        elif any(kw in notes.lower() for kw in ("[l]", "depth", "width", "thickness",
                                                  "height", "length", "radius")):
            if name_lower not in ("name", "matprop", "prop"):
                pdef.param_type = "float"
                pdef.default = "0"
        # Boolean fields
        elif name_lower in ("replace", "relative"):
            pdef.param_type = "bool"
            pdef.default = "true"
        # String fields (names, labels)
        elif any(kw in name_lower for kw in ("name", "prop", "mat", "label",
                                              "pattern", "case", "combo", "group")):
            pdef.param_type = "str"
            pdef.default = ""
        else:
            # Default to string for safety
            pdef.param_type = "str"
            pdef.default = ""

        return pdef

    def _parse_byref_outputs(self, notes: str) -> List[str]:
        """Extract ByRef output names from notes like 'Returns [Name, ret_code]'."""
        match = re.search(r"Returns?\s*\[([^\]]+)\]", notes)
        if not match:
            return []
        parts = [p.strip() for p in match.group(1).split(",")]
        # Exclude ret_code from outputs
        return [p for p in parts if p.lower() != "ret_code"]

    # ─── block_definitions.js ────────────────────────────────────────────

    def _generate_block_definitions_js(self) -> str:
        lines = [
            "// ═══════════════════════════════════════════════════════════",
            f"// Auto-generado por blockly_generator.py — {datetime.now():%Y-%m-%d %H:%M}",
            "// NO editar manualmente — regenerar con:",
            "//   python scripts/blockly/blockly_generator.py",
            "// ═══════════════════════════════════════════════════════════",
            "",
            "// Registrar todos los bloques SAP2000 en Blockly",
            "function registerSAP2000Blocks() {",
            "",
        ]

        for spec in self.block_specs:
            lines.append(self._block_definition_js(spec))

        lines.append("  console.log('✅ ' + Object.keys(Blockly.Blocks).filter(k => k.startsWith('sap_')).length + ' SAP2000 blocks registered');")
        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def _block_definition_js(self, spec: BlockSpec) -> str:
        """Generate Blockly.Blocks[type] = { init: ... } for one block."""
        colour = PHASE_COLORS.get(spec.phase, PHASE_COLORS[999])
        is_creator = any(kw in spec.display_name for kw in ("Add", "Create", "New"))

        parts = []
        parts.append(f"  // {spec.display_name}")
        parts.append(f"  Blockly.Blocks['{spec.block_type}'] = {{")
        parts.append(f"    init: function() {{")
        parts.append(f"      this.setColour({colour});")

        if spec.params:
            # First param gets the display name as label
            first = spec.params[0]
            parts.append(self._field_js(first, label_prefix=spec.display_name + " "))

            for param in spec.params[1:]:
                parts.append(self._field_js(param))
        else:
            parts.append(f"      this.appendDummyInput()")
            parts.append(f"          .appendField('{spec.display_name}()');")

        # Statement connections
        parts.append(f"      this.setPreviousStatement(true);")
        parts.append(f"      this.setNextStatement(true);")
        tooltip = spec.description.replace("'", "\\'")[:120]
        parts.append(f"      this.setTooltip('{tooltip}');")
        parts.append(f"    }}")
        parts.append(f"  }};")
        parts.append("")

        return "\n".join(parts)

    def _field_js(self, param: ParamDef, label_prefix: str = "") -> str:
        """Generate a single field/input for a block parameter."""
        label = label_prefix + param.name if label_prefix else param.name

        if param.param_type == "enum" and param.enum_key in ENUM_MAPS:
            options = ENUM_MAPS[param.enum_key]
            options_js = json.dumps([[k, v] for k, v in options.items()])
            return (
                f"      this.appendDummyInput('{param.name}')\n"
                f"          .appendField('{label}:')\n"
                f"          .appendField(new Blockly.FieldDropdown({options_js}), '{param.name}');"
            )
        elif param.param_type == "float":
            default_val = param.default or "0"
            return (
                f"      this.appendDummyInput('{param.name}')\n"
                f"          .appendField('{label}:')\n"
                f"          .appendField(new Blockly.FieldNumber({default_val}), '{param.name}');"
            )
        elif param.param_type == "int":
            default_val = param.default or "0"
            return (
                f"      this.appendDummyInput('{param.name}')\n"
                f"          .appendField('{label}:')\n"
                f"          .appendField(new Blockly.FieldNumber({default_val}, -Infinity, Infinity, 1), '{param.name}');"
            )
        elif param.param_type == "bool":
            default_val = param.default or "TRUE"
            return (
                f"      this.appendDummyInput('{param.name}')\n"
                f"          .appendField('{label}:')\n"
                f"          .appendField(new Blockly.FieldCheckbox('{default_val.upper()}'), '{param.name}');"
            )
        else:
            # String / default
            default_val = param.default or ""
            safe_default = default_val.replace("'", "\\'")
            return (
                f"      this.appendDummyInput('{param.name}')\n"
                f"          .appendField('{label}:')\n"
                f"          .appendField(new Blockly.FieldTextInput('{safe_default}'), '{param.name}');"
            )

    # ─── generators.js ───────────────────────────────────────────────────

    def _generate_generators_js(self) -> str:
        lines = [
            "// ═══════════════════════════════════════════════════════════",
            f"// Auto-generado por blockly_generator.py — {datetime.now():%Y-%m-%d %H:%M}",
            "// Generadores Python para cada bloque SAP2000",
            "// NO editar manualmente",
            "// ═══════════════════════════════════════════════════════════",
            "",
            "function registerSAP2000Generators(pythonGenerator) {",
            "",
        ]

        for spec in self.block_specs:
            lines.append(self._generator_js(spec))

        lines.append("  console.log('✅ SAP2000 Python generators registered');")
        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def _generator_js(self, spec: BlockSpec) -> str:
        """Generate python generator function for one block."""
        parts = []
        parts.append(f"  // {spec.display_name}")
        parts.append(f"  pythonGenerator.forBlock['{spec.block_type}'] = function(block, generator) {{")

        # Extract field values
        for param in spec.params:
            if param.param_type == "enum":
                parts.append(f"    var {self._js_var(param.name)} = block.getFieldValue('{param.name}') || '{param.default}';")
            elif param.param_type in ("float", "int"):
                parts.append(f"    var {self._js_var(param.name)} = block.getFieldValue('{param.name}') || '{param.default or '0'}';")
            elif param.param_type == "bool":
                parts.append(f"    var {self._js_var(param.name)} = block.getFieldValue('{param.name}') === 'TRUE' ? 'True' : 'False';")
            else:
                parts.append(f"    var {self._js_var(param.name)} = block.getFieldValue('{param.name}') || '';")

        # Build Python code string
        if spec.has_byref and spec.byref_outputs:
            # ByRef pattern: raw = SapModel.X.Y(...); name = raw[0]; ret = raw[-1]
            args_list = self._build_args_js(spec)
            parts.append(f"    var code = 'raw = {spec.api_call.split('(')[0]}(' + {args_list} + ')\\n';")
            for i, out in enumerate(spec.byref_outputs):
                safe_out = out.lower().replace(" ", "_")
                parts.append(f"    code += '{safe_out} = raw[{i}]\\n';")
            parts.append(f"    code += 'ret_code = raw[-1]\\n';")
            parts.append(f"    code += 'assert ret_code == 0, \"{spec.display_name} failed: \" + str(ret_code)\\n';")
        elif spec.params:
            # Simple pattern: ret = SapModel.X.Y(...)
            args_list = self._build_args_js(spec)
            parts.append(f"    var code = 'ret = {spec.api_call.split('(')[0]}(' + {args_list} + ')\\n';")
            parts.append(f"    code += 'assert ret == 0, \"{spec.display_name} failed: \" + str(ret)\\n';")
        else:
            # No params
            parts.append(f"    var code = 'ret = {spec.api_call}()\\n';")
            parts.append(f"    code += 'assert ret == 0, \"{spec.display_name} failed\"\\n';")

        parts.append(f"    return code;")
        parts.append(f"  }};")
        parts.append("")
        return "\n".join(parts)

    def _build_args_js(self, spec: BlockSpec) -> str:
        """Build JS expression that produces Python argument string."""
        arg_parts = []
        for param in spec.params:
            var = self._js_var(param.name)
            if param.param_type == "str":
                arg_parts.append(f"'\"' + {var} + '\"'")
            else:
                arg_parts.append(var)
        return " + ', ' + ".join(arg_parts) if arg_parts else "''"

    def _js_var(self, name: str) -> str:
        """Convert param name to safe JS variable name."""
        return "v_" + re.sub(r"[^a-zA-Z0-9]", "_", name)

    # ─── toolbox_structure.xml ───────────────────────────────────────────

    def _generate_toolbox_xml(self) -> str:
        lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<xml id="toolbox" style="display: none">',
        ]

        # Group by phase
        phase_blocks: Dict[int, List[BlockSpec]] = {i: [] for i in range(1, 10)}
        phase_blocks[999] = []

        for spec in self.block_specs:
            phase_blocks.setdefault(spec.phase, []).append(spec)

        for phase_num in range(1, 10):
            name = PHASE_NAMES.get(phase_num, f"Fase {phase_num}")
            colour = PHASE_COLORS[phase_num]
            blocks = phase_blocks.get(phase_num, [])

            lines.append(f'  <category name="{name} ({phase_num})" colour="{colour}">')
            for spec in sorted(blocks, key=lambda s: s.display_name):
                lines.append(f'    <block type="{spec.block_type}"></block>')
            lines.append("  </category>")

        # Utility category
        utility_blocks = phase_blocks.get(999, [])
        if utility_blocks:
            lines.append(f'  <category name="Utilidades" colour="{PHASE_COLORS[999]}">')
            for spec in sorted(utility_blocks, key=lambda s: s.display_name):
                lines.append(f'    <block type="{spec.block_type}"></block>')
            lines.append("  </category>")

        lines.append("</xml>")
        return "\n".join(lines)


def main():
    """CLI entry point"""
    import sys

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent

    registry_path = sys.argv[1] if len(sys.argv) > 1 else str(project_root / "scripts" / "registry.json")
    output_dir = sys.argv[2] if len(sys.argv) > 2 else str(script_dir)

    generator = BlocklyBlockGenerator(registry_path)
    generator.generate_all(output_dir)


if __name__ == "__main__":
    main()
```

- [ ] Ejecutar el generador para producir los 3 archivos:

```powershell
cd c:\Users\fcoca\Desktop\Ingenieria\Proyectos_Python\Skills_SAP
python scripts/blockly/blockly_generator.py
```

##### Step 1 Verification Checklist
- [x] El generador termina sin errores y reporta ~200 bloques parseados (141 bloques — skips vacíos sin sig+desc)
- [x] `block_definitions.js` contiene bloques con `args0` poblados (fields, dropdowns, números)
- [x] `generators.js` tiene un generador `pythonGenerator.forBlock[...]` para cada bloque
- [x] `toolbox_structure.xml` tiene `<block type="...">` dentro de cada categoría (no vacías)
- [x] El XML usa UTF-8 correcto: "Geometría", "Análisis", "Diseño" (sin caracteres rotos)
- [x] Verificar que los enums (MatType, eUnits, etc.) generan `FieldDropdown` con opciones

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

```powershell
git add -A
git commit -m "feat(blockly): rewrite generator with parametric blocks from registry"
```

---

#### Step 2: Reescribir `blockly_transpiler.py` — Transpilación data-driven

Reemplazar los `if/elif` hardcodeados por un sistema data-driven que use el registry para generar código Python correcto para cualquier bloque.

- [ ] Reemplazar el contenido completo de `scripts/blockly/blockly_transpiler.py` con el siguiente código:

```python
"""
Blockly XML → Python Transpiler (data-driven)
===============================================
Traduce workspace Blockly (XML) a código Python ejecutable para SAP2000.
Usa el registry como fuente de verdad para firmas y patrones ByRef.

Flujo:
  1. Cargar registry → construir mapa de bloques
  2. Parsear XML del workspace
  3. Validar orden de fases (warning, no error)
  4. Generar Python snippet por bloque usando metadata
  5. Ensamblar script completo
"""

import json
import re
import warnings
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


# Phase mapping by category (same as generator)
CATEGORY_PHASE = {
    "File": 1,
    "PropMaterial": 2,
    "PropFrame": 3, "PropArea": 3, "Properties": 3,
    "Object_Model": 4, "FrameObj": 4, "AreaObj": 4, "Edit": 4,
    "Constraints": 5, "Groups": 5, "Select": 5,
    "Load_Patterns": 6, "Load_Cases": 6, "RespCombo": 6, "Mass_Source": 6,
    "Analyze": 7,
    "Analysis_Results": 8, "Database_Tables": 8,
    "Design": 9,
    "Functions": 999,
}


class BlockMeta:
    """Metadata for one block type, derived from registry."""

    def __init__(self, block_type: str, func_path: str, phase: int,
                 param_names: List[str], has_byref: bool,
                 byref_outputs: List[str], description: str):
        self.block_type = block_type
        self.func_path = func_path  # e.g. "SapModel.File.NewBlank"
        self.phase = phase
        self.param_names = param_names  # ordered parameter names (from signature)
        self.has_byref = has_byref
        self.byref_outputs = byref_outputs
        self.description = description


class BlocklyTranspiler:
    """Data-driven Blockly XML → Python transpiler."""

    def __init__(self, registry_path: Optional[str] = None):
        if registry_path is None:
            # Auto-detect registry relative to this file
            here = Path(__file__).resolve().parent
            registry_path = str(here.parent / "registry.json")

        self.registry_path = Path(registry_path)
        self.block_map: Dict[str, BlockMeta] = {}
        self._load_registry()

    def _load_registry(self):
        """Load registry.json and build block_type → BlockMeta map."""
        if not self.registry_path.exists():
            warnings.warn(f"Registry not found: {self.registry_path}")
            return

        with open(self.registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)

        for func_path, info in registry.get("functions", {}).items():
            if not func_path:
                continue

            short_path = func_path.replace("SapModel.", "")
            block_type = "sap_" + short_path.replace(".", "_")

            category = info.get("category", "")
            phase = CATEGORY_PHASE.get(category, 999)

            # Parse param names from signature
            param_names = self._parse_signature_params(info.get("signature", ""))

            # ByRef detection
            notes = info.get("notes", "")
            has_byref = "ByRef" in notes or "Returns [" in notes
            byref_outputs = self._parse_byref_outputs(notes)

            self.block_map[block_type] = BlockMeta(
                block_type=block_type,
                func_path=func_path,
                phase=phase,
                param_names=param_names,
                has_byref=has_byref,
                byref_outputs=byref_outputs,
                description=info.get("description", ""),
            )

    def _parse_signature_params(self, signature: str) -> List[str]:
        match = re.match(r"\(([^)]*)\)", signature)
        if not match:
            return []
        raw = [p.strip() for p in match.group(1).split(",") if p.strip()]
        # Filter out optional/internal params
        skip = {"Color", "Notes", "GUID", "CSys"}
        return [p for p in raw if p not in skip]

    def _parse_byref_outputs(self, notes: str) -> List[str]:
        match = re.search(r"Returns?\s*\[([^\]]+)\]", notes)
        if not match:
            return []
        parts = [p.strip() for p in match.group(1).split(",")]
        return [p for p in parts if p.lower() != "ret_code"]

    # ─── Main transpilation ──────────────────────────────────────────────

    def xml_to_python(self, xml_string: str, validate_phases: bool = True) -> str:
        """Transpile Blockly workspace XML → Python code.

        Args:
            xml_string: Serialized XML from Blockly workspace
            validate_phases: If True, warn (not error) when phases are out of order

        Returns:
            Executable Python code string
        """
        if not xml_string or not xml_string.strip():
            return "# Arrastra bloques desde el toolbox para crear un script\n"

        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            return f"# Error: XML inválido — {e}\n"

        # Parse all top-level blocks (follow next chains)
        blocks = self._collect_blocks(root)

        if not blocks:
            return "# Arrastra bloques desde el toolbox para crear un script\n"

        # Phase validation (warning only)
        if validate_phases:
            self._check_phase_order(blocks)

        # Generate Python
        return self._assemble_python(blocks)

    def _collect_blocks(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Collect all blocks from XML, following <next> chains."""
        blocks = []

        for block_elem in root.findall("block"):
            self._walk_chain(block_elem, blocks)

        return blocks

    def _walk_chain(self, elem: ET.Element, out: List[Dict]):
        """Walk a block chain (block → next → block → next ...)."""
        current = elem
        while current is not None:
            info = self._parse_block(current)
            out.append(info)

            # Follow <next><block> chain
            next_elem = current.find("next")
            current = next_elem.find("block") if next_elem is not None else None

    def _parse_block(self, elem: ET.Element) -> Dict[str, Any]:
        """Parse one <block> element into a dict."""
        block_type = elem.get("type", "")

        # Extract <field> values
        fields = {}
        for field_elem in elem.findall("field"):
            fname = field_elem.get("name", "")
            fval = field_elem.text or ""
            fields[fname] = fval

        return {"type": block_type, "fields": fields}

    def _check_phase_order(self, blocks: List[Dict]):
        """Warn if phases are out of order."""
        phases = []
        for b in blocks:
            meta = self.block_map.get(b["type"])
            if meta and meta.phase < 999:
                phases.append((meta.phase, meta.block_type))

        for i in range(1, len(phases)):
            if phases[i][0] < phases[i - 1][0]:
                warnings.warn(
                    f"Fase fuera de orden: {phases[i-1][1]} (fase {phases[i-1][0]}) "
                    f"seguido de {phases[i][1]} (fase {phases[i][0]})"
                )

    # ─── Python code assembly ──────────────────────────────────────────

    def _assemble_python(self, blocks: List[Dict]) -> str:
        lines = [
            "# Auto-generado por Blockly Visual Scripter",
            "# Variables pre-inyectadas: SapModel, SapObject, result, sap_temp_dir",
            "",
        ]

        for i, block in enumerate(blocks):
            code = self._block_to_python(block, i + 1)
            lines.append(code)
            lines.append("")

        return "\n".join(lines)

    def _block_to_python(self, block: Dict, index: int) -> str:
        """Generate Python code for one block."""
        block_type = block["type"]
        fields = block["fields"]

        meta = self.block_map.get(block_type)
        if meta is None:
            return f"# Bloque desconocido: {block_type}"

        comment = f"# [{index}] {meta.description or meta.func_path}"

        # Build argument list from fields
        args = self._build_args(meta, fields)

        if meta.has_byref and meta.byref_outputs:
            # ByRef pattern
            args_str = ", ".join(args) if args else ""
            call = f"raw = {meta.func_path}({args_str})"
            output_lines = [comment, call]
            for j, out_name in enumerate(meta.byref_outputs):
                safe = out_name.lower().replace(" ", "_")
                output_lines.append(f"{safe} = raw[{j}]")
            output_lines.append("ret_code = raw[-1]")
            output_lines.append(
                f'assert ret_code == 0, f"{meta.func_path} failed: {{ret_code}}"'
            )
            return "\n".join(output_lines)
        else:
            # Simple pattern
            args_str = ", ".join(args) if args else ""
            call = f"ret = {meta.func_path}({args_str})"
            assertion = f'assert ret == 0, f"{meta.func_path} failed: {{ret}}"'
            return f"{comment}\n{call}\n{assertion}"

    def _build_args(self, meta: BlockMeta, fields: Dict[str, str]) -> List[str]:
        """Build Python argument list from block fields and block metadata."""
        args = []
        for pname in meta.param_names:
            value = fields.get(pname, "")

            if not value:
                # Try common alternate field names
                value = fields.get(pname.upper(), "")
                if not value:
                    value = fields.get(pname.lower(), "")

            # Determine if value should be quoted
            if self._looks_numeric(value):
                args.append(value)
            elif value.lower() in ("true", "false"):
                args.append(value.capitalize())
            elif value == "":
                args.append('""')
            else:
                # String — quote it
                safe = value.replace("\\", "\\\\").replace('"', '\\"')
                args.append(f'"{safe}"')

        return args

    def _looks_numeric(self, value: str) -> bool:
        """Check if value looks like a number."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def validate_syntax(self, python_code: str) -> Tuple[bool, str]:
        """Validate Python syntax."""
        try:
            compile(python_code, "<blockly>", "exec")
            return (True, "")
        except SyntaxError as e:
            return (False, str(e))
```

##### Step 2 Verification Checklist
- [ ] `from blockly_transpiler import BlocklyTranspiler` funciona sin errores
- [ ] `BlocklyTranspiler()` carga el registry automáticamente (auto-detect path)
- [ ] XML con bloques de distintas fases genera Python correcto con el patrón `ret = SapModel.X.Y(...)`
- [ ] Funciones ByRef (ej: AddByCoord) generan el patrón `raw = ...; name = raw[0]; ret_code = raw[-1]`
- [ ] Fases fuera de orden generan `warnings.warn()` pero NO `ValueError`
- [ ] XML vacío retorna mensaje de placeholder (no crash)

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

```powershell
git add -A
git commit -m "feat(blockly): data-driven transpiler using registry metadata"
```

---

#### Step 3: Reescribir `index.html` — Editor Blockly profesional

Limpiar el HTML, integrar los archivos generados (block_definitions.js, generators.js, toolbox_structure.xml), y añadir UX profesional.

- [ ] Reemplazar el contenido completo de `scripts/blockly/index.html` con:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>SAP2000 Visual Scripter — Blockly</title>

    <!-- Blockly Core -->
    <link rel="stylesheet" href="https://unpkg.com/blockly/blockly_compressed.css">
    <script src="https://unpkg.com/blockly/blockly_compressed.js"></script>
    <script src="https://unpkg.com/blockly/blocks_compressed.js"></script>
    <script src="https://unpkg.com/blockly/msg/en.js"></script>
    <script src="https://unpkg.com/blockly/python_compressed.js"></script>

    <!-- Generated files -->
    <script src="block_definitions.js"></script>
    <script src="generators.js"></script>

    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { width: 100%; height: 100%; overflow: hidden; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1e1e1e;
            color: #ccc;
        }
        #blockly-workspace {
            width: 100%;
            height: 100%;
        }
        #loading {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            display: flex; align-items: center; justify-content: center;
            background: #1e1e1e; z-index: 9999;
            flex-direction: column; gap: 12px;
        }
        #loading.hidden { display: none; }
        #loading p { font-size: 16px; color: #aaa; }
        .spinner {
            width: 40px; height: 40px;
            border: 4px solid #333; border-top-color: #4FC3F7;
            border-radius: 50%; animation: spin 0.8s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* Validation overlays */
        .blocklyDraggable.block-warning .blocklyPath {
            stroke: #FFC107 !important; stroke-width: 3px;
        }
        .blocklyDraggable.block-error .blocklyPath {
            stroke: #F44336 !important; stroke-width: 3px;
        }
    </style>
</head>
<body>

<div id="loading">
    <div class="spinner"></div>
    <p>Cargando Blockly...</p>
</div>

<div id="blockly-workspace"></div>

<script>
// ═══════════════════════════════════════════════════════════════
// SAP2000 Visual Scripter — Blockly Editor
// ═══════════════════════════════════════════════════════════════

let workspace = null;
let blocklyReady = false;
let pythonGenerator = null;

// ─── Initialization ────────────────────────────────────────────

function initBlockly() {
    if (typeof Blockly === 'undefined') {
        setTimeout(initBlockly, 100);
        return;
    }

    console.log('Blockly loaded, initializing...');

    // Register SAP2000 blocks (from block_definitions.js)
    if (typeof registerSAP2000Blocks === 'function') {
        registerSAP2000Blocks();
    } else {
        console.warn('block_definitions.js not loaded — using empty block set');
    }

    // Initialize Python generator
    pythonGenerator = Blockly.Python || python;

    // Register SAP2000 generators (from generators.js)
    if (typeof registerSAP2000Generators === 'function' && pythonGenerator) {
        registerSAP2000Generators(pythonGenerator);
    } else {
        console.warn('generators.js not loaded — code generation disabled');
    }

    // Load toolbox from generated XML file (or use embedded fallback)
    loadToolboxAndInject();
}

function loadToolboxAndInject() {
    // Try loading toolbox_structure.xml
    fetch('toolbox_structure.xml')
        .then(resp => {
            if (!resp.ok) throw new Error('Not found');
            return resp.text();
        })
        .then(xmlText => {
            injectWorkspace(xmlText);
        })
        .catch(() => {
            console.warn('toolbox_structure.xml not found, using fallback');
            injectWorkspace(getFallbackToolbox());
        });
}

function injectWorkspace(toolboxXml) {
    workspace = Blockly.inject('blockly-workspace', {
        toolbox: toolboxXml,
        grid: {
            spacing: 20,
            length: 3,
            colour: '#444',
            snap: true
        },
        trashcan: true,
        maxTrashcanContents: 64,
        renderer: 'zelos',
        theme: Blockly.Theme.defineTheme('sap2000_dark', {
            base: Blockly.Themes.Classic,
            componentStyles: {
                workspaceBackgroundColour: '#1e1e1e',
                toolboxBackgroundColour: '#252526',
                toolboxForegroundColour: '#ccc',
                flyoutBackgroundColour: '#2d2d30',
                flyoutForegroundColour: '#ccc',
                flyoutOpacity: 0.95,
                scrollbarColour: '#555',
                scrollbarOpacity: 0.6,
                insertionMarkerColour: '#4FC3F7',
            }
        }),
        move: {
            scrollbars: { horizontal: true, vertical: true },
            drag: true,
            wheel: true
        },
        zoom: {
            controls: true,
            wheel: true,
            startScale: 1.0,
            maxScale: 3,
            minScale: 0.3,
            scaleSpeed: 1.2
        }
    });

    // Listeners
    workspace.addChangeListener(onWorkspaceChange);

    // Hide loading
    document.getElementById('loading').classList.add('hidden');
    blocklyReady = true;
    console.log('✅ Blockly editor ready');
}

function getFallbackToolbox() {
    return `
        <xml id="toolbox" style="display: none">
            <category name="Inicializar (1)" colour="0">
                <block type="sap_File_NewBlank"></block>
            </category>
            <category name="Materiales (2)" colour="30"></category>
            <category name="Secciones (3)" colour="60"></category>
            <category name="Geometría (4)" colour="120"></category>
        </xml>
    `;
}

// ─── Workspace Events ──────────────────────────────────────────

function onWorkspaceChange(event) {
    if (!workspace || !blocklyReady) return;
    // Update cached XML
    window._cachedXml = getWorkspaceXml();
}

// ─── Public API (called from PySide6 / console) ────────────────

function getWorkspaceXml() {
    if (!workspace) return '<xml></xml>';
    var xml = Blockly.Xml.workspaceToDom(workspace);
    return new XMLSerializer().serializeToString(xml);
}

function generatePython() {
    if (!workspace || !pythonGenerator) return '';
    try {
        return pythonGenerator.workspaceToCode(workspace) || '';
    } catch (e) {
        console.error('Python generation error:', e);
        return '# Error: ' + e.message + '\n';
    }
}

function loadWorkspaceXml(xmlStr) {
    if (!workspace || !xmlStr) return false;
    try {
        workspace.clear();
        var parser = new DOMParser();
        var dom = parser.parseFromString(xmlStr, 'text/xml');
        Blockly.Xml.domToWorkspace(dom.documentElement, workspace);
        return true;
    } catch (e) {
        console.error('Load XML error:', e);
        return false;
    }
}

function clearWorkspace() {
    if (workspace) workspace.clear();
}

function getBlockCount() {
    if (!workspace) return 0;
    return workspace.getAllBlocks(false).length;
}

// Expose global API
window.pyQtGetWorkspaceXml = getWorkspaceXml;
window.pyQtGeneratePython = generatePython;
window.pyQtClearWorkspace = clearWorkspace;
window.pyQtLoadXml = loadWorkspaceXml;
window.pyQtGetBlockCount = getBlockCount;

// Aliases for cleaner access
window.getWorkspaceXml = getWorkspaceXml;
window.loadWorkspaceXml = loadWorkspaceXml;
window.generatePython = generatePython;
window.clearWorkspace = clearWorkspace;

// ─── Start ─────────────────────────────────────────────────────

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBlockly);
} else {
    initBlockly();
}
</script>
</body>
</html>
```

##### Step 3 Verification Checklist
- [ ] Abrir `scripts/blockly/index.html` directamente en un navegador (Chrome/Edge)
- [ ] Se muestra el spinner de carga y luego aparece el workspace con tema oscuro
- [ ] El toolbox lateral muestra las 9 categorías con bloques dentro
- [ ] Los bloques se pueden arrastrar al workspace y muestran campos editables (texto, dropdowns, números)
- [ ] Abrir consola JS del navegador → `generatePython()` retorna código Python válido
- [ ] `loadWorkspaceXml(getWorkspaceXml())` restaura los bloques sin error
- [ ] No hay errores de WebChannel en la consola (código limpio, sin dependencia de Qt)

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

```powershell
git add -A
git commit -m "feat(blockly): professional HTML editor with dark theme and dynamic toolbox"
```

---

#### Step 4: Reescribir `blockly_gui.py` — GUI PySide6 profesional

Reescribir la GUI con: carga desde archivo HTML (no inline), Open Project funcional, keyboard shortcuts, toolbar con iconos, panel colapsable, y comunicación mejorada.

- [ ] Reemplazar el contenido completo de `scripts/blockly/blockly_gui.py` con:

```python
"""
SAP2000 Visual Scripter — Blockly GUI (PySide6)
=================================================
App principal: editor Blockly embebido + preview Python + consola.

Uso:
    python scripts/blockly/blockly_gui.py
"""

import sys
import json
import time
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QPushButton, QLabel, QMessageBox, QFileDialog,
    QSplitter, QToolBar, QStatusBar,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QTimer, QUrl, Signal, Slot, QThread
from PySide6.QtGui import QFont, QAction, QKeySequence, QShortcut

try:
    from blockly_transpiler import BlocklyTranspiler
    from blockly_executor import BlocklyScriptExecutor
except ImportError:
    from .blockly_transpiler import BlocklyTranspiler
    from .blockly_executor import BlocklyScriptExecutor


# ─── Constants ───────────────────────────────────────────────────

HERE = Path(__file__).resolve().parent
INDEX_HTML = HERE / "index.html"
RECENT_FILE = HERE / ".recent_projects.json"
MAX_RECENT = 5
PREVIEW_INTERVAL_MS = 500


# ─── Worker thread for SAP2000 execution ────────────────────────

class ScriptWorker(QThread):
    """Run script in background thread to keep GUI responsive."""
    finished = Signal(dict)

    def __init__(self, executor: BlocklyScriptExecutor, script: str):
        super().__init__()
        self._executor = executor
        self._script = script

    def run(self):
        result = self._executor.run_script(self._script)
        self.finished.emit(result)


# ─── Blockly Editor (QWebEngineView) ────────────────────────────

class BlocklyEditor(QWebEngineView):
    """Blockly workspace loaded from index.html."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._load_html()

    def _load_html(self):
        if INDEX_HTML.exists():
            self.setUrl(QUrl.fromLocalFile(str(INDEX_HTML)))
        else:
            self.setHtml("<h2>Error: index.html no encontrado</h2>")

    def get_workspace_xml(self, callback):
        """Async: get workspace XML via JS callback."""
        self.page().runJavaScript(
            "(function(){ return window.pyQtGetWorkspaceXml ? pyQtGetWorkspaceXml() : '<xml></xml>'; })()",
            callback,
        )

    def generate_python_js(self, callback):
        """Async: get Python code generated by Blockly JS."""
        self.page().runJavaScript(
            "(function(){ return window.pyQtGeneratePython ? pyQtGeneratePython() : ''; })()",
            callback,
        )

    def load_xml(self, xml_str: str):
        """Load workspace from XML string."""
        safe = json.dumps(xml_str)
        self.page().runJavaScript(
            f"(function(){{ return window.pyQtLoadXml ? pyQtLoadXml({safe}) : false; }})()"
        )

    def clear(self):
        self.page().runJavaScript(
            "if(window.pyQtClearWorkspace) pyQtClearWorkspace();"
        )

    def get_block_count(self, callback):
        self.page().runJavaScript(
            "(function(){ return window.pyQtGetBlockCount ? pyQtGetBlockCount() : 0; })()",
            callback,
        )


# ─── Main Application ──────────────────────────────────────────

class BlocklyScripterApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 Visual Scripter — Blockly")
        self.setGeometry(100, 100, 1600, 900)

        self.transpiler = BlocklyTranspiler()
        self.executor = BlocklyScriptExecutor()
        self.current_xml: Optional[str] = None
        self.current_project_path: Optional[str] = None
        self._worker: Optional[ScriptWorker] = None
        self._recent: list = self._load_recent()

        self._setup_ui()
        self._setup_toolbar()
        self._setup_menu()
        self._setup_shortcuts()
        self._setup_statusbar()

        # Preview update timer
        self._preview_timer = QTimer()
        self._preview_timer.timeout.connect(self._update_preview)
        QTimer.singleShot(2000, lambda: self._preview_timer.start(PREVIEW_INTERVAL_MS))

        # Auto-connect to SAP2000
        QTimer.singleShot(500, self._connect_sap2000)

    # ─── UI Setup ────────────────────────────────────────────────

    def _setup_ui(self):
        splitter = QSplitter(Qt.Horizontal)

        # Left: Blockly editor (70%)
        self.editor = BlocklyEditor()
        splitter.addWidget(self.editor)

        # Right: panel (30%)
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(4, 4, 4, 4)

        # Python preview
        right_layout.addWidget(QLabel("Python Preview"))
        self.code_preview = QPlainTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setFont(QFont("Consolas", 9))
        self.code_preview.setPlainText("# Arrastra bloques para generar código")
        right_layout.addWidget(self.code_preview, 35)

        # Console
        right_layout.addWidget(QLabel("Console"))
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 9))
        self.console.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        right_layout.addWidget(self.console, 45)

        # Buttons
        btn_layout = QVBoxLayout()

        self.btn_run = QPushButton("▶  Ejecutar")
        self.btn_run.setStyleSheet(
            "QPushButton { background: #388E3C; color: white; padding: 10px; "
            "font-weight: bold; font-size: 13px; border-radius: 4px; }"
            "QPushButton:hover { background: #43A047; }"
            "QPushButton:disabled { background: #555; }"
        )
        self.btn_run.clicked.connect(self._on_run)
        btn_layout.addWidget(self.btn_run)

        self.btn_export = QPushButton("Export Python...")
        self.btn_export.clicked.connect(self._on_export)
        btn_layout.addWidget(self.btn_export)

        right_layout.addLayout(btn_layout)
        splitter.addWidget(right)

        splitter.setSizes([1120, 480])
        self.setCentralWidget(splitter)

    def _setup_toolbar(self):
        tb = QToolBar("Main")
        tb.setMovable(False)
        self.addToolBar(tb)

        tb.addAction(self._make_action("New", self._on_new, "Ctrl+N"))
        tb.addAction(self._make_action("Open", self._on_open, "Ctrl+O"))
        tb.addAction(self._make_action("Save", self._on_save, "Ctrl+S"))
        tb.addSeparator()
        tb.addAction(self._make_action("Run", self._on_run, "Ctrl+R"))
        tb.addAction(self._make_action("Export", self._on_export, "Ctrl+E"))
        tb.addSeparator()
        tb.addAction(self._make_action("Clear", self._on_clear))

    def _setup_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(self._make_action("&New Project", self._on_new, "Ctrl+N"))
        file_menu.addAction(self._make_action("&Open Project...", self._on_open, "Ctrl+O"))
        file_menu.addAction(self._make_action("&Save Project", self._on_save, "Ctrl+S"))
        file_menu.addAction(self._make_action("Save &As...", self._on_save_as))
        file_menu.addSeparator()

        # Recent files
        self._recent_menu = file_menu.addMenu("Recent Projects")
        self._update_recent_menu()

        file_menu.addSeparator()
        file_menu.addAction(self._make_action("E&xport Python...", self._on_export, "Ctrl+E"))
        file_menu.addSeparator()
        file_menu.addAction(self._make_action("E&xit", self.close, "Alt+F4"))

        edit_menu = menu.addMenu("&Edit")
        edit_menu.addAction(self._make_action("&Clear All", self._on_clear))

        run_menu = menu.addMenu("&Run")
        run_menu.addAction(self._make_action("&Execute Script", self._on_run, "Ctrl+R"))
        run_menu.addAction(self._make_action("&Reconnect SAP2000", self._connect_sap2000))

        help_menu = menu.addMenu("&Help")
        help_menu.addAction(self._make_action("&About", self._on_about))

    def _setup_shortcuts(self):
        pass  # Shortcuts already attached to actions via _make_action

    def _setup_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.sap_status = QLabel("SAP2000: --")
        self.block_count_label = QLabel("Blocks: 0")
        self.status_bar.addPermanentWidget(self.block_count_label)
        self.status_bar.addPermanentWidget(self.sap_status)

    def _make_action(self, text: str, slot, shortcut: str = None) -> QAction:
        action = QAction(text, self)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        return action

    # ─── SAP2000 Connection ──────────────────────────────────────

    def _connect_sap2000(self):
        result = self.executor.connect(attach_to_existing=True)
        if result["connected"]:
            self.sap_status.setText(f"SAP2000 v{result['version']}  🟢")
            self.sap_status.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self._log("✅ Conectado a SAP2000")
        else:
            self.sap_status.setText("SAP2000: desconectado  🔴")
            self.sap_status.setStyleSheet("color: #FF9800;")
            self._log("⚠️ SAP2000 no disponible — puedes diseñar pero no ejecutar")

    # ─── Preview Update ──────────────────────────────────────────

    def _update_preview(self):
        def on_xml(xml):
            if not xml or xml == self.current_xml:
                return
            self.current_xml = xml

            if "<block" not in xml:
                self.code_preview.setPlainText("# Arrastra bloques para generar código")
                self.block_count_label.setText("Blocks: 0")
                return

            try:
                python_code = self.transpiler.xml_to_python(xml, validate_phases=False)
                self.code_preview.setPlainText(python_code)
            except Exception as e:
                self.code_preview.setPlainText(f"# Error: {e}")

        def on_count(count):
            self.block_count_label.setText(f"Blocks: {count or 0}")

        try:
            self.editor.get_workspace_xml(on_xml)
            self.editor.get_block_count(on_count)
        except Exception:
            pass

    # ─── Actions ─────────────────────────────────────────────────

    def _on_run(self):
        if not self.current_xml or "<block" not in (self.current_xml or ""):
            QMessageBox.warning(self, "Vacío", "No hay bloques en el workspace")
            return

        try:
            python_code = self.transpiler.xml_to_python(self.current_xml)
            valid, err = self.transpiler.validate_syntax(python_code)
            if not valid:
                self._log(f"❌ Syntax error: {err}")
                return

            self._log("\n▶ Ejecutando script...")
            self.btn_run.setEnabled(False)

            self._worker = ScriptWorker(self.executor, python_code)
            self._worker.finished.connect(self._on_run_finished)
            self._worker.start()

        except Exception as e:
            self._log(f"❌ Error: {e}")

    def _on_run_finished(self, result: dict):
        self.btn_run.setEnabled(True)

        if result["success"]:
            self._log(f"✅ OK — {result['execution_time_s']:.2f}s")
            if result["stdout"]:
                self._log(result["stdout"])
            if result.get("result"):
                self._log(json.dumps(result["result"], indent=2, default=str))
        else:
            self._log(f"❌ {result.get('error', 'Unknown error')}")
            if result.get("stderr"):
                self._log(result["stderr"])

    def _on_export(self):
        if not self.current_xml:
            QMessageBox.warning(self, "Vacío", "No hay bloques")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Export Python", "", "Python (*.py)")
        if path:
            try:
                code = self.transpiler.xml_to_python(self.current_xml)
                # Add standalone header
                header = (
                    "# ─── SAP2000 Script (generado por Blockly Visual Scripter) ───\n"
                    "# Para ejecutar standalone, necesitas SapConnection del executor\n"
                    "# Variables requeridas: SapModel, SapObject, result, sap_temp_dir\n"
                    "# ─────────────────────────────────────────────────────────────\n\n"
                )
                Path(path).write_text(header + code, encoding="utf-8")
                self._log(f"📄 Exportado: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _on_new(self):
        if self.current_xml and "<block" in (self.current_xml or ""):
            if QMessageBox.question(
                self, "Nuevo", "¿Descartar cambios actuales?"
            ) != QMessageBox.Yes:
                return
        self.editor.clear()
        self.current_xml = None
        self.current_project_path = None
        self.code_preview.clear()
        self.setWindowTitle("SAP2000 Visual Scripter — Blockly")

    def _on_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Abrir Proyecto", "", "Blockly Projects (*.blockly)"
        )
        if path:
            self._open_project(path)

    def _open_project(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                project = json.load(f)
            xml_str = project.get("workspace_xml", "")
            if xml_str:
                self.editor.load_xml(xml_str)
                self.current_xml = xml_str
                self.current_project_path = path
                self._add_recent(path)
                self.setWindowTitle(f"Blockly — {Path(path).stem}")
                self._log(f"📂 Proyecto abierto: {path}")
            else:
                QMessageBox.warning(self, "Vacío", "El proyecto no contiene bloques")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _on_save(self):
        if self.current_project_path:
            self._save_project(self.current_project_path)
        else:
            self._on_save_as()

    def _on_save_as(self):
        if not self.current_xml:
            QMessageBox.warning(self, "Vacío", "No hay bloques")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Proyecto", "", "Blockly Projects (*.blockly)"
        )
        if path:
            self._save_project(path)

    def _save_project(self, path: str):
        try:
            project = {
                "version": "1.0",
                "workspace_xml": self.current_xml or "",
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(project, f, indent=2, ensure_ascii=False)
            self.current_project_path = path
            self._add_recent(path)
            self.setWindowTitle(f"Blockly — {Path(path).stem}")
            self._log(f"💾 Guardado: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _on_clear(self):
        if QMessageBox.question(
            self, "Limpiar", "¿Limpiar todos los bloques?"
        ) == QMessageBox.Yes:
            self.editor.clear()
            self.current_xml = None
            self.code_preview.clear()

    def _on_about(self):
        QMessageBox.about(
            self,
            "SAP2000 Visual Scripter",
            "Editor visual Blockly para automatizar SAP2000\n\n"
            "v2.0 — 2026\n\n"
            "Arrastra bloques → Configura → Ejecuta\n\n"
            "Shortcuts:\n"
            "  Ctrl+N  New\n"
            "  Ctrl+O  Open\n"
            "  Ctrl+S  Save\n"
            "  Ctrl+R  Run\n"
            "  Ctrl+E  Export",
        )

    # ─── Recent Projects ─────────────────────────────────────────

    def _load_recent(self) -> list:
        if RECENT_FILE.exists():
            try:
                return json.loads(RECENT_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return []

    def _save_recent(self):
        RECENT_FILE.write_text(json.dumps(self._recent), encoding="utf-8")

    def _add_recent(self, path: str):
        if path in self._recent:
            self._recent.remove(path)
        self._recent.insert(0, path)
        self._recent = self._recent[:MAX_RECENT]
        self._save_recent()
        self._update_recent_menu()

    def _update_recent_menu(self):
        self._recent_menu.clear()
        for p in self._recent:
            action = self._recent_menu.addAction(Path(p).name)
            action.setToolTip(p)
            action.triggered.connect(lambda checked, path=p: self._open_project(path))
        if not self._recent:
            self._recent_menu.addAction("(ninguno)").setEnabled(False)

    # ─── Logging ─────────────────────────────────────────────────

    def _log(self, msg: str):
        self.console.appendPlainText(msg)

    # ─── Lifecycle ───────────────────────────────────────────────

    def closeEvent(self, event):
        self._preview_timer.stop()
        self.executor.disconnect()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = BlocklyScripterApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

##### Step 4 Verification Checklist
- [ ] `python scripts/blockly/blockly_gui.py` abre sin errores
- [ ] El editor carga `index.html` desde archivo (no inline) — se ve el tema oscuro
- [ ] Los bloques aparecen en el toolbox con campos editables
- [ ] El Python preview se actualiza al arrastrar bloques (~500ms delay)
- [ ] Ctrl+S abre Save dialog, Ctrl+O abre Open dialog, Ctrl+R ejecuta
- [ ] Open Project carga bloques visualmente en el workspace (no solo XML)
- [ ] La barra de estado muestra conteo de bloques y estado SAP2000
- [ ] El botón Run se deshabilita durante la ejecución (evita doble-click)
- [ ] Recent Projects menu muestra últimos proyectos abiertos/guardados

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

```powershell
git add -A
git commit -m "feat(blockly): professional PySide6 GUI with toolbar, shortcuts, recent projects"
```

---

#### Step 5: Bloques compuestos y workflows

Agregar bloques de alto nivel que encapsulan patrones comunes como "Crear Viga Simple", "Crear Pórtico NxM", y bloques de variables/loops.

- [ ] Crear `scripts/blockly/workflow_blocks.py` — definiciones de bloques compuestos:

```python
"""
Workflow Blocks — Bloques compuestos de alto nivel para Blockly
================================================================
Genera definiciones JS de bloques que encapsulan secuencias comunes
de operaciones SAP2000 (e.g. crear viga, pórtico, análisis completo).

Uso:
    Llamar register_workflow_blocks() desde blockly_generator.py
"""

from typing import List, Dict


def get_workflow_block_definitions() -> str:
    """Return JS code that registers workflow blocks in Blockly."""
    return """
  // ═══ WORKFLOW BLOCKS ═══════════════════════════════════════

  // Crear Viga Simple (material + sección + frame + apoyos)
  Blockly.Blocks['workflow_simple_beam'] = {
    init: function() {
      this.setColour(45);
      this.appendDummyInput()
          .appendField('🏗️ Crear Viga Simple');
      this.appendDummyInput('MatName')
          .appendField('Material:')
          .appendField(new Blockly.FieldTextInput('STEEL'), 'MatName');
      this.appendDummyInput('MatType')
          .appendField('Tipo:')
          .appendField(new Blockly.FieldDropdown([
            ['Steel (1)', '1'], ['Concrete (2)', '2'], ['NoDesign (3)', '3']
          ]), 'MatType');
      this.appendDummyInput('SecName')
          .appendField('Sección:')
          .appendField(new Blockly.FieldTextInput('BEAM_SEC'), 'SecName');
      this.appendDummyInput('Depth')
          .appendField('Alto (m):')
          .appendField(new Blockly.FieldNumber(0.5, 0.01), 'Depth');
      this.appendDummyInput('Width')
          .appendField('Ancho (m):')
          .appendField(new Blockly.FieldNumber(0.3, 0.01), 'Width');
      this.appendDummyInput('X1')
          .appendField('X inicio:')
          .appendField(new Blockly.FieldNumber(0), 'X1');
      this.appendDummyInput('Z1')
          .appendField('Z inicio:')
          .appendField(new Blockly.FieldNumber(0), 'Z1');
      this.appendDummyInput('X2')
          .appendField('X fin:')
          .appendField(new Blockly.FieldNumber(10), 'X2');
      this.appendDummyInput('Z2')
          .appendField('Z fin:')
          .appendField(new Blockly.FieldNumber(0), 'Z2');
      this.appendDummyInput('SupportI')
          .appendField('Apoyo inicio:')
          .appendField(new Blockly.FieldDropdown([
            ['Empotrado', 'FIXED'], ['Articulado', 'PINNED'], ['Libre', 'FREE']
          ]), 'SupportI');
      this.appendDummyInput('SupportJ')
          .appendField('Apoyo fin:')
          .appendField(new Blockly.FieldDropdown([
            ['Empotrado', 'FIXED'], ['Articulado', 'PINNED'],
            ['Libre', 'FREE'], ['Roller', 'ROLLER']
          ]), 'SupportJ');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Crea viga con material, sección, geometría y apoyos');
    }
  };

  // Ejecutar Análisis Completo (DOF + Run)
  Blockly.Blocks['workflow_run_analysis'] = {
    init: function() {
      this.setColour(230);
      this.appendDummyInput()
          .appendField('⚡ Análisis Completo');
      this.appendDummyInput()
          .appendField('UX:').appendField(new Blockly.FieldCheckbox('TRUE'), 'UX')
          .appendField('UY:').appendField(new Blockly.FieldCheckbox('TRUE'), 'UY')
          .appendField('UZ:').appendField(new Blockly.FieldCheckbox('TRUE'), 'UZ');
      this.appendDummyInput()
          .appendField('RX:').appendField(new Blockly.FieldCheckbox('TRUE'), 'RX')
          .appendField('RY:').appendField(new Blockly.FieldCheckbox('TRUE'), 'RY')
          .appendField('RZ:').appendField(new Blockly.FieldCheckbox('TRUE'), 'RZ');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('Configura DOF y ejecuta análisis');
    }
  };

  // Inicializar Modelo
  Blockly.Blocks['workflow_init_model'] = {
    init: function() {
      this.setColour(0);
      this.appendDummyInput()
          .appendField('📁 Inicializar Modelo');
      this.appendDummyInput('Units')
          .appendField('Unidades:')
          .appendField(new Blockly.FieldDropdown([
            ['kN_m_C (6)', '6'], ['kgf_m_C (8)', '8'],
            ['N_m_C (10)', '10'], ['kip_ft_F (4)', '4'],
            ['lb_in_F (1)', '1']
          ]), 'Units');
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setTooltip('InitializeNewModel + NewBlank + SetPresentUnits');
    }
  };
"""


def get_workflow_generators() -> str:
    """Return JS code that registers Python generators for workflow blocks."""
    return """
  // ═══ WORKFLOW GENERATORS ═══════════════════════════════════

  pythonGenerator.forBlock['workflow_init_model'] = function(block, generator) {
    var units = block.getFieldValue('Units') || '6';
    var code = '';
    code += 'ret = SapModel.InitializeNewModel()\\n';
    code += 'assert ret == 0, "InitializeNewModel failed"\\n';
    code += 'ret = SapModel.File.NewBlank()\\n';
    code += 'assert ret == 0, "NewBlank failed"\\n';
    code += 'ret = SapModel.SetPresentUnits(' + units + ')\\n';
    code += 'assert ret == 0, "SetPresentUnits failed"\\n';
    return code;
  };

  pythonGenerator.forBlock['workflow_simple_beam'] = function(block, generator) {
    var matName = block.getFieldValue('MatName') || 'STEEL';
    var matType = block.getFieldValue('MatType') || '1';
    var secName = block.getFieldValue('SecName') || 'BEAM_SEC';
    var depth = block.getFieldValue('Depth') || '0.5';
    var width = block.getFieldValue('Width') || '0.3';
    var x1 = block.getFieldValue('X1') || '0';
    var z1 = block.getFieldValue('Z1') || '0';
    var x2 = block.getFieldValue('X2') || '10';
    var z2 = block.getFieldValue('Z2') || '0';
    var supportI = block.getFieldValue('SupportI') || 'PINNED';
    var supportJ = block.getFieldValue('SupportJ') || 'ROLLER';

    var code = '';
    code += '# --- Material ---\\n';
    code += 'ret = SapModel.PropMaterial.SetMaterial("' + matName + '", ' + matType + ')\\n';
    code += 'assert ret == 0\\n';
    code += '\\n# --- Sección ---\\n';
    code += 'ret = SapModel.PropFrame.SetRectangle("' + secName + '", "' + matName + '", ' + depth + ', ' + width + ')\\n';
    code += 'assert ret == 0\\n';
    code += '\\n# --- Geometría ---\\n';
    code += 'raw = SapModel.FrameObj.AddByCoord(' + x1 + ', 0, ' + z1 + ', ' + x2 + ', 0, ' + z2 + ', "", "' + secName + '", "")\\n';
    code += 'beam_name = raw[0]\\n';
    code += 'assert raw[-1] == 0\\n';
    code += 'raw_pts = SapModel.FrameObj.GetPoints(beam_name, "", "")\\n';
    code += 'pt_i, pt_j = raw_pts[0], raw_pts[1]\\n';
    code += '\\n# --- Apoyos ---\\n';

    var supports = {'FIXED': '[True,True,True,True,True,True]',
                    'PINNED': '[True,True,True,False,False,False]',
                    'ROLLER': '[False,True,True,False,False,False]',
                    'FREE': '[False,False,False,False,False,False]'};

    code += 'ret = SapModel.PointObj.SetRestraint(pt_i, ' + (supports[supportI] || supports['PINNED']) + ')\\n';
    code += 'assert ret == 0\\n';
    code += 'ret = SapModel.PointObj.SetRestraint(pt_j, ' + (supports[supportJ] || supports['ROLLER']) + ')\\n';
    code += 'assert ret == 0\\n';

    return code;
  };

  pythonGenerator.forBlock['workflow_run_analysis'] = function(block, generator) {
    var ux = block.getFieldValue('UX') === 'TRUE' ? 'True' : 'False';
    var uy = block.getFieldValue('UY') === 'TRUE' ? 'True' : 'False';
    var uz = block.getFieldValue('UZ') === 'TRUE' ? 'True' : 'False';
    var rx = block.getFieldValue('RX') === 'TRUE' ? 'True' : 'False';
    var ry = block.getFieldValue('RY') === 'TRUE' ? 'True' : 'False';
    var rz = block.getFieldValue('RZ') === 'TRUE' ? 'True' : 'False';

    var code = '';
    code += '# --- DOF ---\\n';
    code += 'ret = SapModel.Analyze.SetActiveDOF([' + ux + ', ' + uy + ', ' + uz + ', ' + rx + ', ' + ry + ', ' + rz + '])\\n';
    code += 'assert ret == 0, "SetActiveDOF failed"\\n';
    code += '\\n# --- Run Analysis ---\\n';
    code += 'ret = SapModel.Analyze.RunAnalysis()\\n';
    code += 'assert ret == 0, "RunAnalysis failed"\\n';
    return code;
  };
"""


def get_workflow_toolbox_xml() -> str:
    """Return XML fragment for workflow blocks category."""
    return """
  <category name="Workflows" colour="45">
    <block type="workflow_init_model"></block>
    <block type="workflow_simple_beam"></block>
    <block type="workflow_run_analysis"></block>
  </category>"""
```

- [ ] Integrar workflow blocks en `scripts/blockly/blockly_generator.py` — agregar al final de `_generate_block_definitions_js()`:

En el método `_generate_block_definitions_js`, antes de la línea final `lines.append("}")`, agregar:

```python
        # Workflow blocks (composite)
        try:
            from workflow_blocks import get_workflow_block_definitions
            lines.append("")
            lines.append("  // ═══ WORKFLOW BLOCKS ═══")
            lines.append(get_workflow_block_definitions())
        except ImportError:
            try:
                from .workflow_blocks import get_workflow_block_definitions
                lines.append("")
                lines.append("  // ═══ WORKFLOW BLOCKS ═══")
                lines.append(get_workflow_block_definitions())
            except ImportError:
                pass
```

- [ ] Integrar workflow generators en `_generate_generators_js()`:

Antes de la línea final `lines.append("}")`, agregar:

```python
        # Workflow generators
        try:
            from workflow_blocks import get_workflow_generators
            lines.append(get_workflow_generators())
        except ImportError:
            try:
                from .workflow_blocks import get_workflow_generators
                lines.append(get_workflow_generators())
            except ImportError:
                pass
```

- [ ] Integrar workflow toolbox en `_generate_toolbox_xml()`:

Antes de la línea `lines.append("</xml>")`, agregar:

```python
        # Workflow category
        try:
            from workflow_blocks import get_workflow_toolbox_xml
            lines.append(get_workflow_toolbox_xml())
        except ImportError:
            try:
                from .workflow_blocks import get_workflow_toolbox_xml
                lines.append(get_workflow_toolbox_xml())
            except ImportError:
                pass
```

- [ ] Regenerar archivos:

```powershell
python scripts/blockly/blockly_generator.py
```

##### Step 5 Verification Checklist
- [ ] El generador incluye la categoría "Workflows" en el toolbox
- [ ] `block_definitions.js` contiene los bloques `workflow_simple_beam`, `workflow_run_analysis`, `workflow_init_model`
- [ ] `generators.js` contiene los generadores para workflow blocks
- [ ] Abrir `index.html` en navegador → categoría "Workflows" aparece en toolbox
- [ ] Arrastrar "Crear Viga Simple" → genera Python correcto con material + sección + frame + apoyos
- [ ] "Análisis Completo" genera DOF checkboxes + RunAnalysis

#### Step 5 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

```powershell
git add -A
git commit -m "feat(blockly): add composite workflow blocks (beam, analysis, init)"
```

---

#### Step 6: Testing, documentación y polish

Agregar tests unitarios, actualizar README, y mejorar error handling.

- [ ] Crear `scripts/blockly/tests/__init__.py`:

```python
```

- [ ] Crear `scripts/blockly/tests/test_generator.py`:

```python
"""Tests for blockly_generator.py"""

import sys
import json
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from blockly_generator import BlocklyBlockGenerator


def test_generator_loads_registry():
    """Generator loads registry and parses functions."""
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    registry_path = project_root / "scripts" / "registry.json"

    if not registry_path.exists():
        print(f"SKIP: registry not found at {registry_path}")
        return

    gen = BlocklyBlockGenerator(str(registry_path))
    specs = gen._build_block_specs()
    assert len(specs) > 100, f"Expected 100+ blocks, got {len(specs)}"
    print(f"✅ Loaded {len(specs)} block specs from registry")


def test_block_definitions_have_params():
    """At least some blocks should have non-empty params."""
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    registry_path = project_root / "scripts" / "registry.json"

    if not registry_path.exists():
        print(f"SKIP: registry not found at {registry_path}")
        return

    gen = BlocklyBlockGenerator(str(registry_path))
    specs = gen._build_block_specs()

    with_params = [s for s in specs if s.params]
    assert len(with_params) > 20, f"Expected 20+ blocks with params, got {len(with_params)}"
    print(f"✅ {len(with_params)} blocks have editable parameters")


def test_utf8_encoding():
    """Generated files should have correct UTF-8 encoding."""
    import tempfile

    project_root = Path(__file__).resolve().parent.parent.parent.parent
    registry_path = project_root / "scripts" / "registry.json"

    if not registry_path.exists():
        print(f"SKIP: registry not found at {registry_path}")
        return

    gen = BlocklyBlockGenerator(str(registry_path))

    with tempfile.TemporaryDirectory() as tmpdir:
        gen.generate_all(tmpdir)

        toolbox = (Path(tmpdir) / "toolbox_structure.xml").read_text(encoding="utf-8")
        assert "Geometría" in toolbox, "Missing UTF-8 character: Geometría"
        assert "Análisis" in toolbox, "Missing UTF-8 character: Análisis"
        assert "Diseño" in toolbox, "Missing UTF-8 character: Diseño"
        print("✅ UTF-8 encoding correct in toolbox XML")


def test_toolbox_has_blocks():
    """Toolbox should have <block> tags inside categories."""
    import tempfile

    project_root = Path(__file__).resolve().parent.parent.parent.parent
    registry_path = project_root / "scripts" / "registry.json"

    if not registry_path.exists():
        print(f"SKIP: registry not found at {registry_path}")
        return

    gen = BlocklyBlockGenerator(str(registry_path))

    with tempfile.TemporaryDirectory() as tmpdir:
        gen.generate_all(tmpdir)

        toolbox = (Path(tmpdir) / "toolbox_structure.xml").read_text(encoding="utf-8")
        block_count = toolbox.count('<block type="')
        assert block_count > 50, f"Expected 50+ blocks in toolbox, got {block_count}"
        print(f"✅ Toolbox contains {block_count} blocks")


if __name__ == "__main__":
    test_generator_loads_registry()
    test_block_definitions_have_params()
    test_utf8_encoding()
    test_toolbox_has_blocks()
    print("\n✅ All generator tests passed!")
```

- [ ] Crear `scripts/blockly/tests/test_transpiler.py`:

```python
"""Tests for blockly_transpiler.py"""

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from blockly_transpiler import BlocklyTranspiler


def _get_transpiler():
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    registry_path = project_root / "scripts" / "registry.json"
    if not registry_path.exists():
        return None
    return BlocklyTranspiler(str(registry_path))


def test_empty_xml():
    """Empty XML should return placeholder text."""
    t = _get_transpiler()
    if not t:
        print("SKIP: registry not found")
        return

    result = t.xml_to_python("")
    assert "Arrastra" in result or "Error" not in result
    print("✅ Empty XML handled correctly")


def test_single_block():
    """Single block should generate valid Python."""
    t = _get_transpiler()
    if not t:
        print("SKIP: registry not found")
        return

    xml = '''<xml>
      <block type="sap_File_NewBlank">
        <next>
          <block type="sap_PropMaterial_SetMaterial">
            <field name="Name">STEEL</field>
            <field name="MatType">1</field>
          </block>
        </next>
      </block>
    </xml>'''

    result = t.xml_to_python(xml)
    assert "SapModel" in result
    assert "NewBlank" in result or "File" in result
    assert "SetMaterial" in result or "PropMaterial" in result

    # Validate syntax
    valid, err = t.validate_syntax(result)
    assert valid, f"Generated code has syntax error: {err}"
    print(f"✅ Single block transpiled correctly:\n{result[:200]}")


def test_phase_order_warning():
    """Out-of-order phases should warn, not error."""
    t = _get_transpiler()
    if not t:
        print("SKIP: registry not found")
        return

    xml = '''<xml>
      <block type="sap_Analyze_RunAnalysis">
        <next>
          <block type="sap_File_NewBlank"></block>
        </next>
      </block>
    </xml>'''

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = t.xml_to_python(xml, validate_phases=True)
        # Should produce a warning, not an exception
        phase_warnings = [x for x in w if "Fase fuera de orden" in str(x.message)]
        assert len(phase_warnings) > 0, "Expected phase order warning"
        print(f"✅ Phase order warning generated correctly")


def test_byref_function():
    """ByRef functions should use raw pattern."""
    t = _get_transpiler()
    if not t:
        print("SKIP: registry not found")
        return

    # Find a ByRef block
    byref_blocks = [bt for bt, meta in t.block_map.items() if meta.has_byref]
    if not byref_blocks:
        print("SKIP: no ByRef blocks found in registry")
        return

    block_type = byref_blocks[0]
    xml = f'<xml><block type="{block_type}"></block></xml>'

    result = t.xml_to_python(xml, validate_phases=False)
    assert "raw =" in result or "raw=" in result, "ByRef function should use raw pattern"
    assert "raw[-1]" in result, "ByRef should check raw[-1] for ret_code"
    print(f"✅ ByRef pattern correct for {block_type}")


def test_unknown_block():
    """Unknown block type should produce a comment."""
    t = _get_transpiler()
    if not t:
        print("SKIP: registry not found")
        return

    xml = '<xml><block type="sap_NonExistent_Function"></block></xml>'
    result = t.xml_to_python(xml, validate_phases=False)
    assert "desconocido" in result.lower() or "#" in result
    print("✅ Unknown block handled gracefully")


if __name__ == "__main__":
    test_empty_xml()
    test_single_block()
    test_phase_order_warning()
    test_byref_function()
    test_unknown_block()
    print("\n✅ All transpiler tests passed!")
```

- [ ] Ejecutar tests:

```powershell
cd c:\Users\fcoca\Desktop\Ingenieria\Proyectos_Python\Skills_SAP
python scripts/blockly/tests/test_generator.py
python scripts/blockly/tests/test_transpiler.py
```

- [ ] Reemplazar completamente `scripts/blockly/README.md` con:

```markdown
# SAP2000 Visual Scripter — Blockly

Editor visual drag-and-drop para crear scripts de SAP2000 sin escribir código.

## Quick Start

```bash
cd c:\Users\fcoca\Desktop\Ingenieria\Proyectos_Python\Skills_SAP
.venv\Scripts\Activate.ps1

# 1. Regenerar bloques (desde registry.json)
python scripts/blockly/blockly_generator.py

# 2. Ejecutar GUI
python scripts/blockly/blockly_gui.py
```

> SAP2000 debe estar abierto para ejecutar scripts. Sin él, puedes diseñar pero no ejecutar.

## Estructura

```
scripts/blockly/
├── __init__.py                # Package init
├── blockly_gui.py             # APP PRINCIPAL (PySide6)
├── blockly_executor.py        # Ejecutor SAP2000 vía COM
├── blockly_transpiler.py      # XML → Python (data-driven)
├── blockly_generator.py       # Registry → JS/XML generation
├── workflow_blocks.py         # Bloques compuestos de alto nivel
├── index.html                 # Editor Blockly (standalone HTML)
├── block_definitions.js       # AUTO-GENERADO
├── generators.js              # AUTO-GENERADO
├── toolbox_structure.xml      # AUTO-GENERADO
├── README.md                  # Esta documentación
└── tests/
    ├── test_generator.py
    └── test_transpiler.py
```

## Workflow

1. **Arrastra bloques** del toolbox (9 categorías + Workflows)
2. **Configura parámetros** en cada bloque (nombres, coordenadas, enums)
3. **Ver preview Python** en el panel derecho (actualización automática)
4. **Ejecutar** con Ctrl+R o botón verde
5. **Guardar/Exportar** con Ctrl+S / Ctrl+E

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New Project |
| Ctrl+O | Open Project |
| Ctrl+S | Save Project |
| Ctrl+R | Run Script |
| Ctrl+E | Export Python |

## 9-Phase System

| Phase | Category | Color | Example |
|-------|----------|-------|---------|
| 1 | Inicializar | Red | File.NewBlank |
| 2 | Materiales | Orange | PropMaterial.SetMaterial |
| 3 | Secciones | Yellow | PropFrame.SetRectangle |
| 4 | Geometría | Green | FrameObj.AddByCoord |
| 5 | Restricciones | Cyan | PointObj.SetRestraint |
| 6 | Cargas | Blue | LoadPatterns.Add |
| 7 | Análisis | Dark Blue | Analyze.RunAnalysis |
| 8 | Resultados | Purple | Results.JointDispl |
| 9 | Diseño | Magenta | DesignSteel.StartDesign |

## Workflow Blocks

High-level composite blocks (category "Workflows"):

- **Inicializar Modelo** — InitializeNewModel + NewBlank + SetPresentUnits
- **Crear Viga Simple** — Material + Sección + Frame + Apoyos automáticos
- **Análisis Completo** — SetActiveDOF + RunAnalysis

## Regenerating Blocks

When registry.json changes (new functions added):

```bash
python scripts/blockly/blockly_generator.py
```

This regenerates:
- `block_definitions.js` — Block definitions with editable fields
- `generators.js` — Python code generators
- `toolbox_structure.xml` — Toolbox categories with blocks

## Testing

```bash
python scripts/blockly/tests/test_generator.py
python scripts/blockly/tests/test_transpiler.py
```

## Architecture

```
User drags blocks in Blockly (HTML/JS)
           │
    ┌──────┴──────┐
    │  index.html  │ ← block_definitions.js + generators.js
    └──────┬──────┘
           │ JS API: pyQtGetWorkspaceXml(), pyQtLoadXml()
    ┌──────┴──────┐
    │ blockly_gui  │ PySide6 QWebEngineView
    └──────┬──────┘
           │ XML string
    ┌──────┴───────────┐
    │ blockly_transpiler│ registry.json → data-driven code gen
    └──────┬───────────┘
           │ Python code
    ┌──────┴───────────┐
    │ blockly_executor  │ COM bridge → SAP2000
    └──────────────────┘
```
```

##### Step 6 Verification Checklist
- [ ] `python scripts/blockly/tests/test_generator.py` — todos los tests pasan
- [ ] `python scripts/blockly/tests/test_transpiler.py` — todos los tests pasan
- [ ] README.md refleja la estructura actual y comandos correctos
- [ ] No hay archivos `blockly_*.py` sueltos en `scripts/` (todos en `scripts/blockly/`)

#### Step 6 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

```powershell
git add -A
git commit -m "feat(blockly): add tests, update docs, and polish"
```
