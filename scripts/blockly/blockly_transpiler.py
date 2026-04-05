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

            # Must match blockly_generator.py: "sap_" + full path with dots→underscores
            block_type = "sap_" + func_path.replace(".", "_")

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

        # Strip Blockly XML namespaces (Blockly v10 serializes with xmlns=...)
        # so ElementTree can find tags without namespace prefix
        xml_clean = re.sub(r'\s+xmlns(?::\w+)?="[^"]*"', "", xml_string)

        try:
            root = ET.fromstring(xml_clean)
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
