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
from typing import Dict, List, Any, Optional
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
        "Steel (1)": "1", "Concrete (2)": "2", "NoDesign (3)": "3",
        "Aluminum (4)": "4", "ColdFormed (5)": "5", "Rebar (6)": "6", "Tendon (7)": "7",
    },
    "eUnits": {
        "lb_in_F (1)": "1", "lb_ft_F (2)": "2", "kip_in_F (3)": "3", "kip_ft_F (4)": "4",
        "kN_mm_C (5)": "5", "kN_m_C (6)": "6", "kgf_mm_C (7)": "7", "kgf_m_C (8)": "8",
        "N_mm_C (9)": "9", "N_m_C (10)": "10", "Ton_mm_C (11)": "11", "Ton_m_C (12)": "12",
        "kN_cm_C (13)": "13", "kgf_cm_C (14)": "14", "N_cm_C (15)": "15", "Ton_cm_C (16)": "16",
    },
    "eLoadPatternType": {
        "Dead (1)": "1", "SuperDead (2)": "2", "Live (3)": "3", "ReduceLive (4)": "4",
        "Quake (5)": "5", "Wind (6)": "6", "Snow (7)": "7", "Other (8)": "8",
        "Move (9)": "9", "Temperature (10)": "10", "RoofLive (11)": "11", "Notional (12)": "12",
    },
    "eItemType": {
        "Object (0)": "0", "Group (1)": "1", "SelectedObjects (2)": "2",
    },
    "eFrameLoadDistType": {"Force (1)": "1", "Moment (2)": "2"},
    "eFrameLoadDir": {
        "Local1 (1)": "1", "Local2 (2)": "2", "Local3 (3)": "3",
        "X (4)": "4", "Y (5)": "5", "Z (6)": "6",
        "GravityProjected (10)": "10", "GravityFull (11)": "11",
    },
    "eDOF": {"UX": "True", "UY": "True", "UZ": "True", "RX": "True", "RY": "True", "RZ": "True"},
    "eShellType": {
        "ShellThin (1)": "1", "ShellThick (2)": "2", "Membrane (3)": "3", "Plate (4)": "4",
    },
    "eCombType": {
        "LinearAdd (0)": "0", "Envelope (1)": "1", "AbsAdd (2)": "2",
        "SRSS (3)": "3", "RangeAdd (4)": "4",
    },
}


@dataclass
class ParamDef:
    """Definición de un parámetro para un bloque Blockly."""
    name: str
    param_type: str  # "str", "float", "int", "bool", "enum"
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
    api_call: str = ""


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

        self.block_specs = self._build_block_specs()
        print(f"{len(self.block_specs)} bloques parseados del registry")
        skipped_count = len(self.registry.get("functions", {})) - len(self.block_specs)
        if skipped_count:
            print(f"AVISO: {skipped_count} funciones omitidas (sin signature/description/parameter_notes)")
            print("   Usa register_verified_function con el campo 'signature' para incluirlas en Blockly.")

        defs_js = self._generate_block_definitions_js()
        toolbox_xml = self._generate_toolbox_xml()
        gens_js = self._generate_generators_js()

        (self.output_dir / "block_definitions.js").write_text(defs_js, encoding="utf-8")
        (self.output_dir / "toolbox_structure.xml").write_text(toolbox_xml, encoding="utf-8")
        (self.output_dir / "generators.js").write_text(gens_js, encoding="utf-8")

        print(f"Generados en {self.output_dir}:")
        print(f"   block_definitions.js  ({len(defs_js):,} bytes)")
        print(f"   toolbox_structure.xml ({len(toolbox_xml):,} bytes)")
        print(f"   generators.js         ({len(gens_js):,} bytes)")

    # ─── Registry → BlockSpec parsing ────────────────────────────────────

    def _build_block_specs(self) -> List[BlockSpec]:
        specs = []
        skipped = []
        functions = self.registry.get("functions", {})

        for func_path, info in functions.items():
            if not func_path:
                continue

            signature = info.get("signature", "")
            description = info.get("description", "") or info.get("docstring", "")
            parameter_notes_check = info.get("parameter_notes", "") or ""
            if not signature and not description and not parameter_notes_check:
                skipped.append(func_path)
                continue

            block_type = "sap_" + func_path.replace(".", "_")

            category = info.get("category", "")
            phase = CATEGORY_PHASE.get(category, 999)
            if phase == 999:
                parts = func_path.split(".")
                for part in parts:
                    if part in CATEGORY_PHASE:
                        phase = CATEGORY_PHASE[part]
                        break

            parts = [p for p in func_path.split(".") if p != "SapModel"]
            display_name = ".".join(parts[-2:]) if len(parts) >= 2 else func_path

            params = self._parse_params(info)

            notes = info.get("notes", "") or ""
            param_notes = info.get("parameter_notes", "") or ""
            combined_notes = notes + " " + param_notes
            byref_outputs = self._parse_byref_outputs(combined_notes)
            has_byref = len(byref_outputs) > 0
            api_call = func_path + "()"

            spec = BlockSpec(
                block_type=block_type,
                func_path=func_path,
                display_name=display_name,
                phase=phase,
                params=params,
                has_byref=has_byref,
                byref_outputs=byref_outputs,
                description=description[:200],
                api_call=api_call,
            )
            specs.append(spec)

        return specs

    def _parse_params(self, info: Dict) -> List[ParamDef]:
        """Parse parameters from signature + parameter_notes."""
        params = []
        signature = info.get("signature", "")
        param_notes = info.get("parameter_notes", "") or ""

        sig_match = re.match(r"\(([^)]*)\)", signature)
        if not sig_match:
            return params

        raw_params = [p.strip() for p in sig_match.group(1).split(",") if p.strip()]
        skip = {"Color", "Notes", "GUID", "CSys", "Temp"}

        for pname in raw_params:
            if pname in skip:
                continue
            pdef = ParamDef(name=pname, param_type="str")
            pdef = self._infer_param_type(pdef, param_notes, pname)
            params.append(pdef)

        return params

    def _infer_param_type(self, pdef: ParamDef, notes: str, pname: str) -> ParamDef:
        """Infer field type from parameter notes and naming conventions."""
        name_lower = pname.lower()

        if "MatType" in pname or "eMatType" in notes:
            pdef.param_type = "enum"; pdef.enum_key = "MatType"; pdef.default = "2"
        elif "Units" in pname or "eUnits" in pname:
            pdef.param_type = "enum"; pdef.enum_key = "eUnits"; pdef.default = "6"
        elif "PatternType" in pname or "eLoadPatternType" in notes:
            pdef.param_type = "enum"; pdef.enum_key = "eLoadPatternType"; pdef.default = "1"
        elif "ItemType" in pname or "eItemType" in notes:
            pdef.param_type = "enum"; pdef.enum_key = "eItemType"; pdef.default = "0"
        elif "DistType" in pname:
            pdef.param_type = "enum"; pdef.enum_key = "eFrameLoadDistType"; pdef.default = "1"
        elif pname == "Dir" or ("Dir" in pname and "load" in notes.lower()):
            pdef.param_type = "enum"; pdef.enum_key = "eFrameLoadDir"; pdef.default = "10"
        elif "ShellType" in pname:
            pdef.param_type = "enum"; pdef.enum_key = "eShellType"; pdef.default = "1"
        elif "CombType" in pname or "ComboType" in pname:
            pdef.param_type = "enum"; pdef.enum_key = "eCombType"; pdef.default = "0"
        elif any(name_lower.startswith(prefix) for prefix in
                 ("x", "y", "z", "t2", "t3", "t", "e", "u", "r", "d", "w", "h", "l", "area", "vol")):
            pdef.param_type = "float"; pdef.default = "0"
        elif name_lower in ("tf", "tw", "bftop", "bfbot", "t2b", "tfb", "hweb"):
            pdef.param_type = "float"; pdef.default = "0"
        elif any(kw in notes.lower() for kw in ("[l]", "depth", "width", "thickness",
                                                  "height", "length", "radius")):
            pdef.param_type = "float"; pdef.default = "0"
        elif name_lower in ("replace", "relative"):
            pdef.param_type = "bool"; pdef.default = "true"
        elif name_lower in ("mytype", "type", "itype", "ntype"):
            pdef.param_type = "int"; pdef.default = "1"
        elif any(kw in name_lower for kw in ("name", "prop", "mat", "label",
                                              "pattern", "case", "combo", "group")):
            pdef.param_type = "str"; pdef.default = ""
        else:
            pdef.param_type = "str"; pdef.default = ""

        return pdef

    def _parse_byref_outputs(self, notes: str) -> List[str]:
        """Extract ByRef output names from notes like 'Returns [Name, ret_code]'."""
        match = re.search(r"Returns?\s*\[([^\]]+)\]", notes)
        if not match:
            return []
        parts = [p.strip() for p in match.group(1).split(",")]
        return [p for p in parts if p.lower() not in ("ret_code", "ret")]

    # ─── block_definitions.js ────────────────────────────────────────────

    def _generate_block_definitions_js(self) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            "// ===========================================================",
            "// SAP2000 Block Definitions - Auto-generated",
            "// Generated: " + ts,
            "// DO NOT EDIT MANUALLY - run blockly_generator.py to regenerate",
            "// ===========================================================",
            "",
            "function registerSAP2000Blocks() {",
            "",
        ]

        for spec in self.block_specs:
            lines.append(self._block_definition_js(spec))

        lines.append("  console.log('\u2705 ' + Object.keys(Blockly.Blocks)"
                     ".filter(k => k.startsWith(\"sap_\")).length + ' SAP2000 blocks registered');")
        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def _block_definition_js(self, spec: BlockSpec) -> str:
        """Generate Blockly.Blocks[type] = { init: ... } for one block."""
        colour = PHASE_COLORS.get(spec.phase, PHASE_COLORS[999])

        parts = []
        parts.append("  // " + spec.display_name)
        parts.append("  Blockly.Blocks['" + spec.block_type + "'] = {")
        parts.append("    init: function() {")
        parts.append("      this.setColour(" + str(colour) + ");")

        if spec.params:
            first = True
            for param in spec.params:
                field_js = self._field_js(param)
                if first:
                    parts.append("      this.appendDummyInput()")
                    parts.append("          .appendField('" + spec.display_name + "')")
                    parts.append("          .appendField(new Blockly.FieldLabel('" + param.name + ":'))")
                    parts.append("          " + field_js + ";")
                    first = False
                else:
                    parts.append("      this.appendDummyInput()")
                    parts.append("          .appendField(new Blockly.FieldLabel('" + param.name + ":'))")
                    parts.append("          " + field_js + ";")
        else:
            parts.append("      this.appendDummyInput()")
            parts.append("          .appendField('" + spec.display_name + "()');")

        parts.append("      this.setPreviousStatement(true);")
        parts.append("      this.setNextStatement(true);")
        tooltip = spec.description.replace("'", "\\'")[:120]
        parts.append("      this.setTooltip('" + tooltip + "');")
        parts.append("    }")
        parts.append("  };")
        parts.append("")

        return "\n".join(parts)

    def _field_js(self, param: ParamDef, label_prefix: str = "") -> str:
        """Generate a single field/input for a block parameter."""
        if param.param_type == "enum" and param.enum_key in ENUM_MAPS:
            options = ENUM_MAPS[param.enum_key]
            options_js = json.dumps([[k, v] for k, v in options.items()])
            return ".appendField(new Blockly.FieldDropdown(" + options_js + "), '" + param.name + "')"
        elif param.param_type == "float":
            default_val = param.default or "0"
            return (".appendField(new Blockly.FieldNumber("
                    + default_val + ", -Infinity, Infinity, 0.001), '" + param.name + "')")
        elif param.param_type == "int":
            default_val = param.default or "0"
            return (".appendField(new Blockly.FieldNumber("
                    + default_val + ", -Infinity, Infinity, 1), '" + param.name + "')")
        elif param.param_type == "bool":
            default_val = (param.default or "true").upper()
            return ".appendField(new Blockly.FieldCheckbox('" + default_val + "'), '" + param.name + "')"
        else:
            default_val = (param.default or "").replace("'", "\\'")
            return ".appendField(new Blockly.FieldTextInput('" + default_val + "'), '" + param.name + "')"

    # ─── generators.js ───────────────────────────────────────────────────

    def _generate_generators_js(self) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            "// ===========================================================",
            "// SAP2000 Python Generators - Auto-generated",
            "// Generated: " + ts,
            "// DO NOT EDIT MANUALLY",
            "// ===========================================================",
            "",
            "function registerSAP2000Generators(pythonGenerator) {",
            "",
        ]

        for spec in self.block_specs:
            lines.append(self._generator_js(spec))

        lines.append("  console.log('\u2705 SAP2000 Python generators registered');")
        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def _generator_js(self, spec: BlockSpec) -> str:
        """Generate python generator function for one block."""
        # NL = JS newline escape (backslash + n) for Python code strings
        NL = chr(92) + "n"
        Q = chr(34)  # double-quote character

        parts = []
        parts.append("  // " + spec.display_name)
        parts.append("  pythonGenerator.forBlock['" + spec.block_type
                     + "'] = function(block, generator) {")

        # Extract field values
        for param in spec.params:
            var = self._js_var(param.name)
            if param.param_type == "enum":
                parts.append("    var " + var + " = block.getFieldValue('"
                              + param.name + "') || '" + (param.default or "") + "';")
            elif param.param_type in ("float", "int"):
                parts.append("    var " + var + " = block.getFieldValue('"
                              + param.name + "') || '" + str(param.default or "0") + "';")
            elif param.param_type == "bool":
                parts.append("    var " + var + " = block.getFieldValue('"
                              + param.name + "') === 'TRUE' ? 'True' : 'False';")
            else:
                # String: wrap in single quotes for Python
                parts.append("    var " + var + " = \"'\" + (block.getFieldValue('"
                              + param.name + "') || '') + \"'\";")

        args_expr = self._build_args_js(spec)

        if spec.has_byref and spec.byref_outputs:
            parts.append("    var code = '';")
            parts.append("    code += 'raw = " + spec.func_path
                         + "(' + " + args_expr + " + ')" + NL + "';")
            for idx, out in enumerate(spec.byref_outputs):
                safe_out = re.sub(r"[^a-zA-Z0-9_]", "_", out.lower())
                parts.append("    code += '" + safe_out
                              + " = raw[" + str(idx) + "]" + NL + "';")
            parts.append("    code += 'ret_code = raw[-1]" + NL + "';")
            parts.append("    code += 'assert ret_code == 0, " + Q
                         + spec.display_name + " failed: " + Q
                         + " + str(ret_code)" + NL + "';")
        elif spec.params:
            parts.append("    var code = '';")
            parts.append("    code += 'ret = " + spec.func_path
                         + "(' + " + args_expr + " + ')" + NL + "';")
            parts.append("    code += 'assert ret == 0, " + Q
                         + spec.display_name + " failed: " + Q
                         + " + str(ret)" + NL + "';")
        else:
            parts.append("    var code = '';")
            parts.append("    code += 'ret = " + spec.func_path + "()" + NL + "';")
            parts.append("    code += 'assert ret == 0, " + Q
                         + spec.display_name + " failed" + Q + NL + "';")

        parts.append("    return code;")
        parts.append("  };")
        parts.append("")
        return "\n".join(parts)

    def _build_args_js(self, spec: BlockSpec) -> str:
        """Build JS expression that produces Python argument string."""
        arg_parts = [self._js_var(p.name) for p in spec.params]
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

        phase_blocks: Dict[int, List[BlockSpec]] = {i: [] for i in range(1, 10)}
        phase_blocks[999] = []

        for spec in self.block_specs:
            phase_blocks.setdefault(spec.phase, []).append(spec)

        for phase_num in range(1, 10):
            name = PHASE_NAMES.get(phase_num, "Fase " + str(phase_num))
            colour = PHASE_COLORS.get(phase_num, PHASE_COLORS[999])
            lines.append('  <category name="' + name + '" colour="' + str(colour) + '">')
            for spec in phase_blocks.get(phase_num, []):
                lines.append('    <block type="' + spec.block_type + '"></block>')
            lines.append("  </category>")

        utility_blocks = phase_blocks.get(999, [])
        if utility_blocks:
            lines.append('  <category name="Utilidades" colour="' + str(PHASE_COLORS[999]) + '">')
            for spec in utility_blocks:
                lines.append('    <block type="' + spec.block_type + '"></block>')
            lines.append("  </category>")

        lines.append("</xml>")
        return "\n".join(lines)


def main():
    """CLI entry point"""
    import sys

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent  # scripts/blockly/ -> scripts/ -> project_root/

    registry_path = sys.argv[1] if len(sys.argv) > 1 else str(project_root / "scripts" / "registry.json")
    output_dir = sys.argv[2] if len(sys.argv) > 2 else str(script_dir)

    generator = BlocklyBlockGenerator(registry_path)
    generator.generate_all(output_dir)


if __name__ == "__main__":
    main()
