"""
Launcher: Pórtico 2D en Blockly Visual Scripter
================================================
Pasos automáticos:
  1. Regenera block_definitions.js, generators.js y toolbox_structure.xml
     (aplica correcciones de tipo de campo Name/MatProp/LoadPat)
  2. Abre la GUI de Blockly con el proyecto portico_2d.blockly pre-cargado

Uso:
    cd c:\\Users\\fcoca\\Desktop\\Ingenieria\\Proyectos_Python\\Skills_SAP
    .venv\\Scripts\\Activate.ps1
    python scripts/blockly/launch_portico_blockly.py
"""

import sys
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
WORKSPACE  = Path(__file__).resolve().parents[2]
BLOCKLY_DIR = Path(__file__).resolve().parent
PROJECT_FILE = BLOCKLY_DIR / "projects" / "portico_2d.blockly"
REGISTRY_PATH = WORKSPACE / "scripts" / "registry.json"

sys.path.insert(0, str(WORKSPACE))

# ─── Paso 1: Regenerar ficheros Blockly ──────────────────────────────────────
print("=" * 60)
print(" SAP2000 Blockly Visual Scripter — Launcher Pórtico 2D")
print("=" * 60)
print()
print("▶ Paso 1: Regenerando block_definitions.js, generators.js,")
print("          toolbox_structure.xml desde registry...")

try:
    from scripts.blockly.blockly_generator import BlocklyBlockGenerator

    gen = BlocklyBlockGenerator(registry_path=str(REGISTRY_PATH))
    gen.generate_all(output_dir=str(BLOCKLY_DIR))
    print(f"  ✓ Generados {len(gen.block_specs)} bloques en {BLOCKLY_DIR}")
    print()
except Exception as e:
    print(f"  ⚠ No se pudo regenerar bloques: {e}")
    print("  → Continuando con los archivos existentes...")
    print()

# ─── Paso 2: Verificar proyecto ──────────────────────────────────────────────
print("▶ Paso 2: Verificando proyecto...")
if not PROJECT_FILE.exists():
    print(f"  ✗ Proyecto no encontrado: {PROJECT_FILE}")
    sys.exit(1)
print(f"  ✓ Proyecto: {PROJECT_FILE.name}")
print()

# ─── Paso 3: Abrir GUI ───────────────────────────────────────────────────────
print("▶ Paso 3: Abriendo SAP2000 Visual Scripter...")
print()
print("  El proyecto se cargará automáticamente (~2s después de que")
print("  Blockly.js termine de inicializarse).")
print()
print("  Flujo del pórtico 2D (17 bloques):")
print("  ┌─ Fase 1: Init ────── File.NewBlank()")
print("  ├─ Fase 2: Material ── SetMaterial + SetMPIsotropic (ACERO_A36)")
print("  ├─ Fase 3: Sección ─── SetRectangle ×2 (30×30 + 30×50 cm)")
print("  ├─ Fase 4: Geometría ─ AddByCoord ×3 (2 cols 4m + viga 6m)")
print("  ├─ Fase 5: Apoyos ──── SetRestraint ×2 (empotrado bases)")
print("  ├─ Fase 6: Cargas ──── LoadPatterns.Add + SetLoadDistributed ×2")
print("  ├─ Fase 7: Análisis ── File.Save + RunAnalysis()")
print("  └─ Fase 8: Resultados ─ DeselectAll + SetCaseSelectedForOutput")
print()

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer

    try:
        from scripts.blockly.blockly_gui import BlocklyScripterApp
    except ImportError:
        from blockly_gui import BlocklyScripterApp  # fallback si se corre desde blockly/

    app = QApplication(sys.argv)
    window = BlocklyScripterApp()
    window.show()

    # Cargar proyecto después de que Blockly.js se inicialice
    QTimer.singleShot(2000, lambda: window._open_project(str(PROJECT_FILE)))

    sys.exit(app.exec())

except ImportError as e:
    print(f"✗ Error al importar PySide6 o GUI: {e}")
    print()
    print("  Instala PySide6 con:")
    print("  .venv\\Scripts\\pip install PySide6")
    sys.exit(1)
