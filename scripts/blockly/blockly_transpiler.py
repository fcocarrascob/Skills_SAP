"""
Blockly XML → Python Transpiler
================================
Traduce workspace Blockly (XML) a código Python ejecutable para SAP2000.

Flujo:
  1. Parsear XML del workspace
  2. Validar orden de fases (1→2→3...→9)
  3. Generar Python snippet por bloque
  4. Ensamblar script completo
  5. Opcional: Inyectar setup/teardown

Ejemplo:
    transpiler = BlocklyTranspiler()
    python_code = transpiler.xml_to_python(blockly_xml_string)
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple
import re


class BlockDefinition:
    """Definición de cómo traducir un tipo de bloque a Python"""
    
    def __init__(self, block_type: str, python_template: str, phase: int = 0):
        self.block_type = block_type
        self.python_template = python_template
        self.phase = phase


class BlocklyTranspiler:
    """Transpilar Blockly XML → Python"""
    
    # Mapeo: block_type → Python generation function
    BLOCK_GENERATORS = {
        'sap_File_NewBlank': lambda block, ctx: 'ret = SapModel.File.NewBlank()\nassert ret == 0\n',
        'sap_File_Save': lambda block, ctx: 'ret = SapModel.File.Save(sap_temp_dir + r"\\model.sdb")\nassert ret == 0\n',
        'sap_Select_All': lambda block, ctx: 'ret = SapModel.Select.All()\nassert ret == 0\n',
    }
    
    # Mapeo: block_type → phase
    BLOCK_PHASES = {
        'sap_File_NewBlank': 1,
        'sap_File_Save': 1,
        'sap_PropMaterial_SetMaterial': 2,
        'sap_PropFrame_SetRectangle': 3,
        'sap_FrameObj_AddByCoord': 4,
        'sap_PointObj_SetRestraint': 5,
        'sap_LoadPatterns_Add': 6,
        'sap_Analyze_RunAnalysis': 7,
        'sap_Results_JointDispl': 8,
        'sap_DesignSteel_StartDesign': 9,
    }
    
    def __init__(self):
        self.blocks = []
        self.phase_order = []
        self.variables = {}  # track variable names (names of created objects)
    
    def xml_to_python(self, xml_string: str, validate_phases: bool = True) -> str:
        """Transpilar XML workspace → Python code
        
        Args:
            xml_string: XML serializado del workspace Blockly
            validate_phases: Si True, valida que las fases estén en orden correcto
        
        Returns:
            Código Python ejecutable
        
        Raises:
            ValueError: Si el XML es inválido o las fases están fuera de orden
        """
        
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"XML inválido: {e}")
        
        # Parsear bloques
        self.blocks = []
        self.phase_order = []
        
        for block_elem in root.findall('.//block'):
            block_info = self._parse_block(block_elem)
            self.blocks.append(block_info)
            phase = self.BLOCK_PHASES.get(block_info['type'], 0)
            if phase > 0:
                self.phase_order.append(phase)
        
        # Validar orden de fases
        if validate_phases:
            self._validate_phase_order()
        
        # Generar Python
        python_code = self._generate_python_code()
        
        return python_code
    
    def _parse_block(self, block_elem: ET.Element) -> Dict[str, Any]:
        """Parsear un elemento block XML"""
        
        block_type = block_elem.get('type')
        block_id = block_elem.get('id')
        
        # Extraer campos (field)
        fields = {}
        for field_elem in block_elem.findall('field'):
            field_name = field_elem.get('name')
            field_value = field_elem.text or ''
            fields[field_name] = field_value
        
        # Extraer valores (input_value)
        inputs = {}
        for input_elem in block_elem.findall('value'):
            input_name = input_elem.get('name')
            # Buscar bloque anidado
            inner_block = input_elem.find('block')
            if inner_block:
                inputs[input_name] = self._parse_block(inner_block)
            else:
                inputs[input_name] = None
        
        return {
            'type': block_type,
            'id': block_id,
            'fields': fields,
            'inputs': inputs,
        }
    
    def _validate_phase_order(self):
        """Validar que las fases estén en orden creciente (sin saltos)"""
        if not self.phase_order:
            return
        
        # Verificar orden: cada fase debe ser >= anterior
        for i in range(1, len(self.phase_order)):
            if self.phase_order[i] < self.phase_order[i-1]:
                raise ValueError(
                    f"Fase fuera de orden: fase {self.phase_order[i-1]} "
                    f"seguida de fase {self.phase_order[i]}. "
                    f"Las fases deben estar en orden: 1→2→3→...→9"
                )
    
    def _generate_python_code(self) -> str:
        """Generar script Python completo"""
        
        lines = [
            "# Auto-generado por Blockly Visual Scripter",
            "# NO editar manualmente — regenerado cada ejecución",
            "",
        ]
        
        # Si no hay bloques, dar instrucción
        if not self.blocks:
            lines.append("# Arrastra bloques desde el toolbox para crear un script")
            return "\n".join(lines)
        
        lines.extend([
            "# Variables pre-inyectadas:",
            "# - SapModel: modelo SAP2000 activo",
            "# - SapObject: aplicación SAP2000",
            "# - result: dict para escribir outputs",
            "# - sap_temp_dir: directorio temporal",
            "",
            "result = {}",
            "",
        ])
        
        # Generar código para cada bloque
        for i, block_info in enumerate(self.blocks):
            block_code = self._generate_block_code(block_info)
            if block_code:
                lines.append(f"# Bloque {i+1}")
                lines.append(block_code)
                lines.append("")
        
        return "\n".join(lines)
    
    def _generate_block_code(self, block_info: Dict[str, Any]) -> str:
        """Generar Python para un bloque específico"""
        
        block_type = block_info['type']
        fields = block_info['fields']
        inputs = block_info['inputs']
        
        # Log: qué bloque estamos procesando
        # print(f"DEBUG: Procesando bloque tipo={block_type}, fields={fields}")
        
        # Caso 1: File.NewBlank
        if 'NewBlank' in block_type:
            return 'ret = SapModel.File.NewBlank()\nassert ret == 0, "NewBlank failed"'
        
        # Caso 2: File.Save
        elif 'Save' in block_type:
            file_path = fields.get('FilePath', 'model.sdb')
            return f'ret = SapModel.File.Save(sap_temp_dir + r"\\{file_path}")\nassert ret == 0, "File.Save failed"'
        
        # Caso 3: PropMaterial.SetMaterial
        elif 'SetMaterial' in block_type and 'PropMaterial' in block_type:
            name = fields.get('Name', fields.get('NAME', 'MAT1'))
            mat_type = fields.get('MatType', fields.get('TYPE', '2'))
            return f'ret = SapModel.PropMaterial.SetMaterial("{name}", {mat_type})\nassert ret == 0, "SetMaterial failed"'
        
        # Caso 4: PropFrame.SetRectangle
        elif 'SetRectangle' in block_type or 'Rectang' in block_type:
            name = fields.get('Name', fields.get('NAME', 'SEC1'))
            material = fields.get('Material', 'CONC')
            t3 = fields.get('T3', '0.3')
            t2 = fields.get('T2', '0.3')
            return f'ret = SapModel.PropFrame.SetRectangle("{name}", "{material}", {t3}, {t2})\nassert ret == 0, "SetRectangle failed"'
        
        # Caso 5: FrameObj.AddByCoord
        elif 'AddByCoord' in block_type and 'Frame' in block_type:
            x1 = fields.get('X1', '0')
            y1 = fields.get('Y1', '0')
            z1 = fields.get('Z1', '0')
            x2 = fields.get('X2', '0')
            y2 = fields.get('Y2', '0')
            z2 = fields.get('Z2', '10')
            prop = fields.get('Prop', 'Default')
            group = fields.get('Group', '1')
            
            code = (
                f'raw = SapModel.FrameObj.AddByCoord({x1}, {y1}, {z1}, {x2}, {y2}, {z2}, "", "{prop}", "{group}")\n'
                f'frame_name = raw[0]\n'
                f'ret_code = raw[-1]\n'
                f'assert ret_code == 0, f"AddByCoord failed: {{ret_code}}"\n'
                f'result["frame_name"] = frame_name'
            )
            return code
        
        # Caso 6: PointObj.AddCartesian
        elif 'AddCartesian' in block_type:
            x = fields.get('X', '0')
            y = fields.get('Y', '0')
            z = fields.get('Z', '0')
            name = fields.get('PointName', '')
            
            code = (
                f'raw = SapModel.PointObj.AddCartesian({x}, {y}, {z}, "", "{name}")\n'
                f'point_name = raw[0]\n'
                f'ret_code = raw[-1]\n'
                f'assert ret_code == 0, f"AddCartesian failed: {{ret_code}}"\n'
                f'result["point_name"] = point_name'
            )
            return code
        
        # Caso 7: PointObj.SetRestraint
        elif 'SetRestraint' in block_type:
            point_name = fields.get('PointName', 'all')
            ux = '1' if fields.get('UX') == 'true' else '0'
            uy = '1' if fields.get('UY') == 'true' else '0'
            uz = '1' if fields.get('UZ') == 'true' else '0'
            rx = '1' if fields.get('RX') == 'true' else '0'
            ry = '1' if fields.get('RY') == 'true' else '0'
            rz = '1' if fields.get('RZ') == 'true' else '0'
            
            code = (
                f'ret = SapModel.PointObj.SetRestraint("{point_name}", {ux}, {uy}, {uz}, {rx}, {ry}, {rz})\n'
                f'assert ret == 0, "SetRestraint failed"'
            )
            return code
        
        # Caso 8: Analyze.RunAnalysis
        elif 'RunAnalysis' in block_type:
            return (
                'ret = SapModel.Analyze.RunAnalysis()\n'
                'assert ret == 0, "RunAnalysis failed"'
            )
        
        # Caso 9: Select.All
        elif 'Select_All' in block_type or 'SelectAll' in block_type:
            return (
                'ret = SapModel.Select.All()\n'
                'assert ret == 0, "Select.All failed"'
            )
        
        # Default: Return pass con tipo de bloque en comentario
        else:
            return f'# Bloque no implementado: {block_type}'
    
    def validate_syntax(self, python_code: str) -> Tuple[bool, str]:
        """Validar sintaxis Python generado
        
        Returns:
            (is_valid, error_message)
        """
        try:
            compile(python_code, '<blockly>', 'exec')
            return (True, "")
        except SyntaxError as e:
            return (False, str(e))


def example_usage():
    """Ejemplo de uso"""
    
    # XML de ejemplo (workspace Blockly)
    blockly_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <xml>
      <block type="sap_File_NewBlank" id="1">
        <field name="Name">NewBlank</field>
      </block>
      <block type="sap_PropMaterial_SetMaterial" id="2">
        <field name="Name">CONC</field>
        <field name="MatType">2</field>
      </block>
      <block type="sap_FrameObj_AddByCoord" id="3">
        <field name="X1">0</field>
        <field name="Y1">0</field>
        <field name="Z1">0</field>
        <field name="X2">0</field>
        <field name="Y2">0</field>
        <field name="Z2">10</field>
        <field name="Prop">SEC1</field>
        <field name="Group">1</field>
      </block>
    </xml>
    '''
    
    transpiler = BlocklyTranspiler()
    python_code = transpiler.xml_to_python(blockly_xml)
    
    print("=== Generated Python Code ===")
    print(python_code)
    print()
    
    # Validar
    is_valid, error = transpiler.validate_syntax(python_code)
    print(f"Validez sintaxis: {is_valid}")
    if error:
        print(f"Error: {error}")


if __name__ == "__main__":
    example_usage()
