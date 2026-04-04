"""
Blockly Block Generator — Auto-genera definiciones de bloques desde registry.json
===============================================================================
Genera:
  1. block_definitions.js — Blockly block JSON para cada función SAP2000
  2. toolbox_structure.xml — Toolbox organizado por 9 fases
  3. generators.js — Generador Python para cada bloque

Uso:
    generator = BlocklyBlockGenerator(registry_path="scripts/registry.json")
    generator.generate_all(output_dir="scripts/blockly")
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


# Mapeo de fases a colores Blockly
PHASE_COLORS = {
    1: 0,          # Rojo: Init (File)
    2: 45,         # Naranja: Materials
    3: 90,         # Verde claro: Sections  
    4: 120,        # Verde: Geometry
    5: 150,        # Cian: Constraints
    6: 180,        # Azul claro: Loads
    7: 210,        # Azul: Analysis
    8: 240,        # Púrpura: Results
    9: 270,        # Púrpura oscuro: Design
    999: 300,      # Gris: Utility
}

# Mapeo: función SAP2000 → Fase
FUNCTION_PHASES = {
    "File.NewBlank": 1, "File.OpenFile": 1, "File.Save": 1, "File.New2DFrame": 1,
    
    "PropMaterial.SetMaterial": 2, "PropMaterial.SetMPIsotropic": 2, "PropMaterial.SetMPOrthotropic": 2,
    
    "PropFrame.SetRectangle": 3, "PropFrame.SetISection": 3, "PropFrame.SetCircle": 3,
    "PropArea.SetShell_1": 3,
    
    "FrameObj.AddByCoord": 4, "AreaObj.AddByCoord": 4, "PointObj.AddCartesian": 4,
    "EditArea.Divide": 4,
    
    "PointObj.SetRestraint": 5, "ConstraintDef.SetDiaphragm": 5, "ConstraintDef.SetBody": 5,
    "Groups.Create": 5, "Select.All": 5, "Select.ClearSelection": 5,
    
    "LoadPatterns.Add": 6, "LoadCases.StaticLinear": 6, "RespCombo.Add": 6,
    "FrameObj.SetLoadDistributed": 6, "AreaObj.SetLoadUniform": 6, "PointObj.SetLoadForce": 6,
    
    "Analyze.RunAnalysis": 7, "Analyze.SetActiveDOF": 7, "Analyze.GetCaseStatus": 7,
    
    "Results.JointDispl": 8, "Results.FrameForce": 8, "DatabaseTables.GetTableForDisplayArray": 8,
    
    "DesignSteel.StartDesign": 9, "DesignConcrete.StartDesign": 9,
}


@dataclass
class BlockParam:
    """Descripción de un parámetro de bloque"""
    name: str
    python_type: str
    blockly_check: str
    default_value: Any = None
    enum_values: Dict[str, int] = None
    description: str = ""


class BlocklyBlockGenerator:
    """Generador de bloques Blockly desde registry SAP2000"""
    
    def __init__(self, registry_path: str = "scripts/registry.json"):
        self.registry_path = Path(registry_path)
        self.registry = self._load_registry()
        self.output_dir = None
    
    def _load_registry(self) -> Dict[str, Any]:
        """Cargar registry.json"""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry no encontrado: {self.registry_path}")
        
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def generate_all(self, output_dir: str = "scripts/blockly"):
        """Generar todos los archivos
        
        Outputs:
            - block_definitions.js
            - toolbox_structure.xml
            - generators.js
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📦 Generando {len(self.registry.get('functions', []))} bloques...")
        
        # Generar JavaScript + XML
        blocks_js = self._generate_block_definitions_js()
        toolbox_xml = self._generate_toolbox_xml()
        generators_js = self._generate_generators_js()
        
        # Escribir archivos
        (self.output_dir / "block_definitions.js").write_text(blocks_js)
        (self.output_dir / "toolbox_structure.xml").write_text(toolbox_xml)
        (self.output_dir / "generators.js").write_text(generators_js)
        
        print(f"✅ Generados:")
        print(f"   - block_definitions.js ({len(blocks_js)} bytes)")
        print(f"   - toolbox_structure.xml ({len(toolbox_xml)} bytes)")
        print(f"   - generators.js ({len(generators_js)} bytes)")
    
    def _generate_block_definitions_js(self) -> str:
        """Generar bloque JSON para cada función"""
        
        js_output = "// Auto-generado — NO editar manualmente\n"
        js_output += "// Fecha: 2026-04-04\n\n"
        js_output += "var BLOCKLY_BLOCKS = {\n"
        
        functions_dict = self.registry.get('functions', {})
        for func_path, func_info in functions_dict.items():
            # Skip si no tenemos info
            if not func_path:
                continue
            
            block_type = f"sap_{func_path.replace('.', '_')}"
            phase = self._get_phase(func_path)
            color = PHASE_COLORS.get(phase, PHASE_COLORS[999])
            
            # Extraer docstring y parámetros
            params = self._extract_parameters(func_info)
            
            # Generar JSON del bloque
            block_def = {
                "type": block_type,
                "message0": self._generate_message0(func_path, params),
                "args0": self._generate_args0(params),
                "output": self._get_output_type(func_path),
                "colour": color,
                "tooltip": func_info.get('docstring', '')[:100],
                "helpUrl": ""
            }
            
            js_output += f"  '{block_type}': {json.dumps(block_def, indent=4)},\n"
        
        js_output += "};\n"
        return js_output
    
    def _get_phase(self, func_path: str) -> int:
        """Retorna la fase (1-9) de una función"""
        return FUNCTION_PHASES.get(func_path, 999)
    
    def _extract_parameters(self, func_info: Dict) -> List[BlockParam]:
        """Extraer parámetros desde docstring"""
        # Dummy: parsear docstring o usar metadata
        # Para MVP: usar parámetros hardcodeados por función conocida
        params = []
        
        func_path = func_info.get('function_path', '')
        
        # Ejemplos hardcodeados (MVP)
        if func_path == "PropMaterial.SetMaterial":
            params = [
                BlockParam("Name", "str", "String", "", description="Nombre del material"),
                BlockParam("MatType", "int", "Number", description="Tipo: 1=Steel, 2=Concrete, etc")
            ]
        elif func_path == "FrameObj.AddByCoord":
            params = [
                BlockParam("X1", "float", "Number", 0),
                BlockParam("Y1", "float", "Number", 0),
                BlockParam("Z1", "float", "Number", 0),
                BlockParam("X2", "float", "Number", 0),
                BlockParam("Y2", "float", "Number", 0),
                BlockParam("Z2", "float", "Number", 0),
                BlockParam("Prop", "str", "String", "Default", description="Sección"),
                BlockParam("Group", "str", "String", "1"),
            ]
        
        return params
    
    def _generate_message0(self, func_path: str, params: List[BlockParam]) -> str:
        """Generar message0 amigable"""
        parts = func_path.split('.')
        msg = f"{parts[-1]}"
        
        for i, param in enumerate(params):
            msg += f" {param.name}:%{i+1}"
        
        return msg
    
    def _generate_args0(self, params: List[BlockParam]) -> List[Dict]:
        """Generar args0 para Blockly"""
        args = []
        for param in params:
            arg = {
                "type": "input_value",
                "name": param.name,
                "check": param.blockly_check
            }
            args.append(arg)
        return args
    
    def _get_output_type(self, func_path: str) -> str:
        """Retorna tipo output del bloque"""
        # Create functions retornan String (nombre del objeto)
        if any(x in func_path for x in ["AddByCoord", "AddCartesian", "Create"]):
            return "String"
        return None
    
    def _generate_toolbox_xml(self) -> str:
        """Generar toolbox.xml con 9 categorías de fases"""
        
        xml = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml += '<xml id="toolbox" style="display: none">\n'
        
        # Agrupar bloques por fase (incluyendo 999 para "sin fase asignada")
        phase_blocks = {i: [] for i in range(1, 10)}
        phase_blocks[999] = []  # Para funciones sin fase asignada
        
        functions_dict = self.registry.get('functions', {})
        for func_path, func_info in functions_dict.items():
            if not func_path:
                continue
            
            phase = self._get_phase(func_path)
            block_type = f"sap_{func_path.replace('.', '_')}"
            phase_blocks[phase].append((func_path, block_type))
        
        # Generar categorías XML
        phase_names = {
            1: "Inicializar",
            2: "Materiales",
            3: "Secciones",
            4: "Geometría",
            5: "Restricciones",
            6: "Cargas",
            7: "Análisis",
            8: "Resultados",
            9: "Diseño"
        }
        
        for phase in range(1, 10):
            phase_name = phase_names.get(phase, f"Fase {phase}")
            colour = PHASE_COLORS[phase]
            
            xml += f'  <category name="{phase_name} ({phase})" colour="{colour}">\n'
            
            for func_path, block_type in phase_blocks[phase]:
                xml += f'    <block type="{block_type}"></block>\n'
            
            xml += "  </category>\n"
        
        # Categoría Utilities
        xml += f'  <category name="Utilidades" colour="{PHASE_COLORS[999]}">\n'
        xml += '    <block type="sap_Select_All"></block>\n'
        xml += '    <block type="sap_Select_ClearSelection"></block>\n'
        xml += '  </category>\n'
        
        xml += '</xml>\n'
        return xml
    
    def _generate_generators_js(self) -> str:
        """Generar generators.js — código gen Python de bloques"""
        
        js = "// Auto-generado — Generadores Python para cada bloque\n\n"
        js += "python['sap_File_NewBlank'] = function(block) {\n"
        js += "  return 'SapModel.File.NewBlank()\\n';\n"
        js += "};\n\n"
        
        js += "python['sap_PropMaterial_SetMaterial'] = function(block) {\n"
        js += "  var name = Blockly.Python.valueToCode(block, 'Name', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var mat_type = Blockly.Python.valueToCode(block, 'MatType', Blockly.Python.ORDER_MEMBER);\n"
        js += "  return `SapModel.PropMaterial.SetMaterial(${name}, ${mat_type})\\n`;\n"
        js += "};\n\n"
        
        js += "python['sap_FrameObj_AddByCoord'] = function(block) {\n"
        js += "  var x1 = Blockly.Python.valueToCode(block, 'X1', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var y1 = Blockly.Python.valueToCode(block, 'Y1', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var z1 = Blockly.Python.valueToCode(block, 'Z1', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var x2 = Blockly.Python.valueToCode(block, 'X2', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var y2 = Blockly.Python.valueToCode(block, 'Y2', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var z2 = Blockly.Python.valueToCode(block, 'Z2', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var prop = Blockly.Python.valueToCode(block, 'Prop', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var group = Blockly.Python.valueToCode(block, 'Group', Blockly.Python.ORDER_MEMBER);\n"
        js += "  var code = `raw = SapModel.FrameObj.AddByCoord(${x1}, ${y1}, ${z1}, ${x2}, ${y2}, ${z2}, '', ${prop}, ${group})\\n`;\n"
        js += "  code += `frame_name = raw[0]\\n`;\n"
        js += "  code += `assert raw[-1] == 0, f'AddByCoord failed: {raw[-1]}'\\n`;\n"
        js += "  return code;\n"
        js += "};\n\n"
        
        return js


def main():
    """CLI entry point"""
    import sys
    
    # Detectar ubicación relativa al proyecto
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent  # scripts/blockly/ → scripts/ → project_root/
    
    registry_path = sys.argv[1] if len(sys.argv) > 1 else str(project_root / "scripts" / "registry.json")
    output_dir = sys.argv[2] if len(sys.argv) > 2 else str(script_dir)
    
    generator = BlocklyBlockGenerator(registry_path)
    generator.generate_all(output_dir)


if __name__ == "__main__":
    main()
