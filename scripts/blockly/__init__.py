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
