# Workflow de Dos Fases: Script Interactivo → GUI Standalone

## Goal
Implement a complete two-phase workflow system: (1) formalize the interactive script creation process with Phase 6 GUI generation, (2) create standalone backend/GUI templates using `comtypes` (no MCP), (3) migrate existing `ring_areas` and `placabase` to the new standalone pattern, and (4) update skill documentation.

## Prerequisites
Make sure that the user is currently on the `workflow-two-phase-gui` branch before beginning implementation.
If not, move them to the correct branch. If the branch does not exist, create it from main.

---

### Step-by-Step Instructions

---

#### Step 1: Create Backend Template (`scripts/templates/backend_template.py`)

- [x] Create the directory `scripts/templates/`
- [x] Create file `scripts/templates/backend_template.py` with the complete code below:

```python
"""
Backend Template — SAP2000 Standalone (COM Directo)
====================================================
Plantilla base para backends que conectan a SAP2000 vía comtypes.client
sin depender del MCP server.

Uso:
    1. Copiar este archivo como backend_{nombre}.py
    2. Renombrar la clase MyBackend → {Nombre}Backend
    3. Reemplazar el método run() con la lógica del script verificado
    4. Ajustar los parámetros de entrada en run(params)

Convenciones:
    - SapConnection maneja connect/disconnect COM directo
    - Backend.run(params) ejecuta la lógica y retorna dict de resultados
    - Sin imports de mcp_server/, sap_bridge, sap_executor
    - Estilo de script: tareas numeradas, asserts, result dict
      (referencia: example_1001_simple_beam.py)
"""

import math
import comtypes.client
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Any


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    # ── Conectar ──────────────────────────────────────────────────────────────

    def connect(self, attach_to_existing: bool = True) -> dict:
        """Conecta a una instancia de SAP2000 en ejecución.

        Args:
            attach_to_existing: Si True, se conecta a una instancia ya abierta.

        Returns:
            dict con claves: connected (bool), version (str), model_path (str),
            error (str, solo si falla).
        """
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                self.sap_object.ApplicationStart()

            self.sap_model = self.sap_object.SapModel

            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())

            return {
                "connected": True,
                "version": version,
                "model_path": model_path,
            }
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    # ── Desconectar ───────────────────────────────────────────────────────────

    def disconnect(self) -> dict:
        """Libera la referencia COM (no cierra SAP2000)."""
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Configuración (Dataclass)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class MyConfig:
    """Parámetros de entrada para el backend.

    Reemplazar con los parámetros específicos de tu script.
    Ejemplo para ring_areas: r_inner, r_outer, t1, t2, n_segs, etc.
    """

    param_1: float = 1.0
    param_2: float = 2.0
    param_3: str = "DEFAULT"


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class MyBackend:
    """Backend standalone para SAP2000.

    Renombrar a {Nombre}Backend (ej: RingAreasBackend, PlacaBaseBackend).
    """

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config: MyConfig) -> dict:
        """Ejecuta la lógica principal del script.

        Args:
            config: Parámetros de entrada.

        Returns:
            dict con resultados (éxito, métricas, errores).
        """
        SapModel = self.sap_model
        result = {}

        # ── Task 1: Inicializar ──────────────────────────────────────────
        ret = SapModel.InitializeNewModel()
        assert ret == 0, f"InitializeNewModel failed: {ret}"

        ret = SapModel.File.NewBlank()
        assert ret == 0, f"NewBlank failed: {ret}"

        ret = SapModel.SetPresentUnits(6)  # kN_m_C
        assert ret == 0, f"SetPresentUnits failed: {ret}"

        result["task_1_init"] = True

        # ── Task 2: Material ─────────────────────────────────────────────
        # TODO: Reemplazar con la lógica de tu script verificado
        ret = SapModel.PropMaterial.SetMaterial(config.param_3, 2)
        assert ret == 0, f"SetMaterial failed: {ret}"

        result["task_2_material"] = config.param_3

        # ── Task N: ... ──────────────────────────────────────────────────
        # Copiar tareas del script verificado, reemplazando:
        #   - Variables globales → config.param_X
        #   - SapModel global → self.sap_model (ya asignado arriba)
        #   - result global → result local (dict)

        result["success"] = True
        return result


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = MyBackend(conn)
        config = MyConfig(param_1=1.0, param_2=2.0, param_3="TEST_MAT")

        try:
            output = backend.run(config)
            import json
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
```

- [x] Verify syntax is valid:
```powershell
python -c "import ast, pathlib; ast.parse(pathlib.Path('scripts/templates/backend_template.py').read_text(encoding='utf-8')); print('syntax OK')"
```

- [x] Verify NO imports from `mcp_server/`:
```powershell
python -c "t=open('scripts/templates/backend_template.py',encoding='utf-8').read(); assert 'sap_bridge' not in t; assert 'sap_executor' not in t; assert 'mcp_server' not in t; print('no MCP imports ✔')"
```

##### Step 1 Verification Checklist
- [x] File `scripts/templates/backend_template.py` exists
- [x] `ast.parse` succeeds — no syntax errors
- [x] No imports from `mcp_server`, `sap_bridge`, or `sap_executor`
- [x] Contains `SapConnection` class with `connect()`, `disconnect()`, `is_connected`
- [x] Contains `MyBackend` class with `run(config) -> dict`
- [x] Contains `MyConfig` dataclass
- [x] Has `if __name__ == "__main__"` standalone test block

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 2: Create GUI Template (`scripts/templates/gui_template.py`)

- [x] Create file `scripts/templates/gui_template.py` with the complete code below:

```python
"""
GUI Template — SAP2000 Standalone PySide6
==========================================
Plantilla base para GUIs standalone que conectan a SAP2000 vía COM directo
(a través de backend_{nombre}.py), sin depender del MCP server.

Uso:
    1. Copiar este archivo como gui_{nombre}.py
    2. Importar el backend correspondiente: from backend_{nombre} import ...
    3. Reemplazar los inputs del QGroupBox con los parámetros del backend
    4. Ajustar _build_config() para leer los inputs y crear el Config
    5. Ajustar _format_result() para mostrar los resultados

Convenciones:
    - 3 botones core: Conectar, Ejecutar, Desconectar
    - Workers (QThread + Signal) para operaciones SAP2000 async
    - Output log (QTextEdit read-only, Consolas 9pt)
    - Status indicator (rojo/verde)
    - _busy(True/False) para deshabilitar botones durante ejecución
    - Sin imports de mcp_server/, sap_bridge, sap_executor
"""

import sys
import json

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

# ── Importar backend (ajustar nombre) ─────────────────────────────────────────
from backend_template import SapConnection, MyBackend, MyConfig


# ══════════════════════════════════════════════════════════════════════════════
# Workers — operaciones SAP2000 fuera del hilo GUI
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    """Conecta a SAP2000 en un hilo separado."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.connect(attach_to_existing=True)
        self.finished.emit(result)


class RunWorker(QThread):
    """Ejecuta el backend en un hilo separado."""
    finished = Signal(dict)

    def __init__(self, backend: MyBackend, config: MyConfig):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            result = self._backend.run(self._config)
            self.finished.emit(result)
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class DisconnectWorker(QThread):
    """Desconecta de SAP2000 en un hilo separado."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.disconnect()
        self.finished.emit(result)


# ══════════════════════════════════════════════════════════════════════════════
# Helper — campo de entrada con label
# ══════════════════════════════════════════════════════════════════════════════

def _field(label: str, default: str, tooltip: str = "") -> tuple:
    """Crea un par (QLabel, QLineEdit) para un campo de entrada."""
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    edit = QLineEdit(default)
    edit.setMinimumWidth(90)
    if tooltip:
        edit.setToolTip(tooltip)
        lbl.setToolTip(tooltip)
    return lbl, edit


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QWidget):
    """GUI standalone para SAP2000.

    Renombrar a {Nombre}GUI (ej: RingAreasGUI, PlacaBaseGUI).
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Template GUI")
        self.setMinimumWidth(640)

        # ── Estado interno ────────────────────────────────────────────────
        self._conn = SapConnection()
        self._backend = MyBackend(self._conn)
        self._worker = None  # referencia al QThread activo (evita GC)

        # ── Layout raíz ──────────────────────────────────────────────────
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Status ───────────────────────────────────────────────────────
        status_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        status_row.addWidget(self._status_lbl)
        status_row.addStretch()
        root.addLayout(status_row)

        # ── Botón Conectar ───────────────────────────────────────────────
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)
        root.addWidget(self._btn_connect)

        # ── Inputs ───────────────────────────────────────────────────────
        inputs_box = QGroupBox("Parámetros de entrada")
        grid = QGridLayout(inputs_box)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        r = 0

        # --- Reemplazar con los inputs de tu backend ---
        lbl, self._input_param1 = _field("Param 1", "1.0", "Primer parámetro")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._input_param1, r, 1)
        lbl, self._input_param2 = _field("Param 2", "2.0", "Segundo parámetro")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._input_param2, r, 3)
        r += 1

        lbl, self._input_param3 = _field("Nombre", "DEFAULT", "Nombre del material")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._input_param3, r, 1)
        r += 1

        root.addWidget(inputs_box)

        # ── Botón Ejecutar ───────────────────────────────────────────────
        self._btn_run = QPushButton("Ejecutar")
        self._btn_run.setFixedHeight(34)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Output log ───────────────────────────────────────────────────
        output_box = QGroupBox("Salida")
        out_layout = QVBoxLayout(output_box)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(200)
        out_layout.addWidget(self._log)
        root.addWidget(output_box)

        # ── Botón Desconectar ────────────────────────────────────────────
        self._btn_disconnect = QPushButton("Desconectar de SAP2000")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        root.addWidget(self._btn_disconnect)

    # ══════════════════════════════════════════════════════════════════════
    # Helpers internos
    # ══════════════════════════════════════════════════════════════════════

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_run.setEnabled(connected)
        self._btn_disconnect.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")

    def _log_append(self, text: str):
        self._log.append(text)

    def _busy(self, is_busy: bool):
        """Deshabilita todos los botones mientras un worker está activo."""
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_run.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)

    def _build_config(self) -> MyConfig:
        """Lee los inputs de la GUI y construye el Config.

        Ajustar para leer los campos específicos de tu backend.
        """
        return MyConfig(
            param_1=float(self._input_param1.text()),
            param_2=float(self._input_param2.text()),
            param_3=self._input_param3.text(),
        )

    def _format_result(self, data: dict) -> str:
        """Formatea el resultado para mostrar en el log.

        Ajustar para resaltar los valores importantes de tu backend.
        """
        return json.dumps(data, indent=2, ensure_ascii=False)

    # ══════════════════════════════════════════════════════════════════════
    # Conectar
    # ══════════════════════════════════════════════════════════════════════

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            self._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._set_connected(True)
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    # ══════════════════════════════════════════════════════════════════════
    # Ejecutar
    # ══════════════════════════════════════════════════════════════════════

    def _on_run(self):
        try:
            config = self._build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return

        self._log_append("\n─── Ejecutando ─────────────────────────────────────")
        self._busy(True)
        self._worker = RunWorker(self._backend, config)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Ejecución exitosa")
            self._log_append(self._format_result(result))
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ Error: {err}")

    # ══════════════════════════════════════════════════════════════════════
    # Desconectar
    # ══════════════════════════════════════════════════════════════════════

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._busy(False)
        self._log_append("✔ Desconectado de SAP2000")
        self._set_connected(False)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
```

- [x] Verify syntax:
```powershell
python -c "import ast, pathlib; ast.parse(pathlib.Path('scripts/templates/gui_template.py').read_text(encoding='utf-8')); print('syntax OK')"
```

- [x] Verify no MCP imports:
```powershell
python -c "t=open('scripts/templates/gui_template.py',encoding='utf-8').read(); assert 'sap_bridge' not in t; assert 'sap_executor' not in t; assert 'mcp_server' not in t; print('no MCP imports ✔')"
```

##### Step 2 Verification Checklist
- [x] File `scripts/templates/gui_template.py` exists
- [x] `ast.parse` succeeds — no syntax errors
- [x] No imports from `mcp_server`, `sap_bridge`, or `sap_executor`
- [x] Imports from `backend_template` (relative)
- [x] Has 3 workers: `ConnectWorker`, `RunWorker`, `DisconnectWorker`
- [x] Has `MainWindow` with 3 buttons: Conectar, Ejecutar, Desconectar
- [x] Has output log (`QTextEdit`, read-only, Consolas 9pt)
- [x] Has status indicator (red/green)
- [x] Has `_busy()` method
- [x] Has `_build_config()` and `_format_result()` methods

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 3: Update `workflow-script-creation.md` — Add Phase 6

- [x] Open `plans/workflow-script-creation.md`
- [x] In the Table of Contents section, add entry 6 after the existing entry 5. Replace the ToC block with:

Find:
```markdown
1. [Fase 1: Planificación y Descomposición](#fase-1-planificación-y-descomposición)
2. [Fase 2: Investigación de API Functions](#fase-2-investigación-de-api-functions)
3. [Fase 3: Desarrollo Iterativo por Tareas](#fase-3-desarrollo-iterativo-por-tareas)
4. [Fase 4: Integración y Refinamiento](#fase-4-integración-y-refinamiento)
5. [Fase 5: Documentación y Guardado](#fase-5-documentación-y-guardado)
6. [Ejemplo Práctico: Placa Base](#ejemplo-práctico-placa-base)
```

Replace with:
```markdown
1. [Fase 1: Planificación y Descomposición](#fase-1-planificación-y-descomposición)
2. [Fase 2: Investigación de API Functions](#fase-2-investigación-de-api-functions)
3. [Fase 3: Desarrollo Iterativo por Tareas](#fase-3-desarrollo-iterativo-por-tareas)
4. [Fase 4: Integración y Refinamiento](#fase-4-integración-y-refinamiento)
5. [Fase 5: Documentación y Guardado](#fase-5-documentación-y-guardado)
6. [Fase 6: Generación de GUI Standalone (Opcional)](#fase-6-generación-de-gui-standalone-opcional)
7. [Ejemplo Práctico: Placa Base](#ejemplo-práctico-placa-base)
```

- [x] At the end of Phase 5 (after the `register_verified_function` tool block — just before the `## Ejemplo Práctico: Placa Base` heading), insert the following new section:

Find the line:
```markdown
## Ejemplo Práctico: Placa Base
```

Insert **before** it the following complete Phase 6 section:

```markdown
---

## Fase 6: Generación de GUI Standalone (Opcional)

> **Pregunta de transición (Fase 5 → Fase 6):**
> *"El script está verificado y guardado. ¿Quieres generar una GUI standalone
> para que puedas ejecutar este modelo sin necesidad del agente/MCP?"*
>
> - **Sí** → Continuar con Fase 6
> - **No** → Fin del workflow

### Objetivo

Convertir el script MCP verificado en un mini-software standalone compuesto por:
- `backend_{nombre}.py` — Lógica SAP2000 con COM directo (`comtypes.client`)
- `gui_{nombre}.py` — Interfaz PySide6 con botones Conectar/Ejecutar/Desconectar

**Resultado:** Un software que el usuario puede distribuir e integrar en sus herramientas,
**independiente del framework de IA**.

### 6.1 Identificar Inputs del Script

Revisar las variables configurables al inicio del script verificado.
Cada variable configurable se convierte en un campo de la GUI.

**Ejemplo — ring_areas:**
```python
# Estas variables del script...
r_inner = 1.0
r_mid1  = 2.0
r_mid2  = 3.5
r_outer = 5.0
t1 = 0.30
t2 = 0.20
n_segs = 36

# ...se convierten en estos inputs de GUI:
#   QLineEdit("r_inner", default="1.0")
#   QLineEdit("r_mid1",  default="2.0")
#   ...etc.
```

### 6.2 Generar Backend Standalone

Usar como base la plantilla `scripts/templates/backend_template.py`:

1. **Copiar** `backend_template.py` → `backend_{nombre}.py`
2. **Renombrar** `MyConfig` → `{Nombre}Config` con los parámetros del script
3. **Renombrar** `MyBackend` → `{Nombre}Backend`
4. **Copiar la lógica** del script verificado al método `run()`:
   - Variables globales → `config.param_x`
   - `SapModel` (pre-inyectado en sandbox) → `self.sap_model`
   - `result` global → `result` local (dict)
   - `sap_temp_dir` → Ruta configurable o `tempfile.gettempdir()`
   - Funciones auxiliares → métodos de la clase Backend
5. **Mantener asserts** y estructura de tareas numeradas

**Reglas inquebrantables:**
- ❌ NO importar `sap_bridge`, `sap_executor`, ni nada de `mcp_server/`
- ❌ NO importar `app_logger`, `sap_utils_common`, ni módulos externos
- ✅ Solo `comtypes.client`, `math`, `dataclasses`, stdlib
- ✅ `SapConnection` con `connect()`, `disconnect()`, `is_connected`

### 6.3 Generar GUI Standalone

Usar como base la plantilla `scripts/templates/gui_template.py`:

1. **Copiar** `gui_template.py` → `gui_{nombre}.py`
2. **Ajustar import:** `from backend_{nombre} import SapConnection, {Nombre}Backend, {Nombre}Config`
3. **Reemplazar inputs:** Un `QLineEdit` por cada variable configurable (de 6.1)
4. **Ajustar `_build_config()`:** Leer los inputs y crear el Config
5. **Ajustar `_format_result()`:** Mostrar métricas relevantes del resultado
6. **Renombrar** `MainWindow` → `{Nombre}GUI`
7. **Ajustar título** del `setWindowTitle()`

### 6.4 Organizar en Carpeta

```
scripts/{nombre}/
    gui_{nombre}.py         # GUI PySide6
    backend_{nombre}.py     # Lógica SAP2000 COM directo
```

**Regla:** La carpeta GUI solo contiene `gui_*.py` + `backend_*.py`.
Los scripts MCP originales van en `scripts/` root (ej: `scripts/example_*.py`).

### 6.5 Testing

1. **Sintaxis:** `python -c "import ast; ast.parse(open('backend_*.py').read())"`
2. **GUI abre:** `python gui_{nombre}.py` → debe abrir ventana (sin SAP2000)
3. **Flujo completo** (si SAP2000 disponible):
   - Conectar → status verde
   - Ingresar parámetros → Ejecutar → log muestra resultado
   - Desconectar → status rojo

### 6.6 Estilo de Referencia

Todo el código generado debe seguir el estilo de `scripts/example_1001_simple_beam.py`:
- Headers claros: `# ── Task N: Nombre ──────────────────────────────`
- Cada llamada API: `assert ret == 0, f"NombreFuncion failed: {ret}"`
- Variables configurables al inicio, separadas visualmente
- Resultado en dict (`result["key"] = value`)
- Fórmulas de referencia en comentarios (si aplica)

---

```

##### Step 3 Verification Checklist
- [x] ToC now has 7 entries (including new Fase 6 and renumbered Ejemplo Práctico)
- [x] Phase 6 section exists between Phase 5 and Ejemplo Práctico
- [x] Phase 6 has subsections 6.1 through 6.6
- [x] Transition question from Phase 5 → Phase 6 is clear
- [x] Template references (`backend_template.py`, `gui_template.py`) are correct
- [x] Style reference to `example_1001_simple_beam.py` is included
- [x] No MCP dependencies mentioned in Phase 6 output

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 4: Update `quick-reference-workflow.md` — Add GUI Section

- [x] Open `plans/quick-reference-workflow.md`
- [x] Append the following section at the very end of the file (after the MCP Tools Reference table):

```markdown

---

## 🖥️ GUI Standalone — Quick Reference

### Cuándo Generar GUI

Al final de la Fase 5, preguntar al usuario:
> *"¿Quieres generar una GUI standalone (PySide6) para este script?"*

### Checklist Fase 6

```
□ 6.1 Identificar inputs (variables configurables del script)
□ 6.2 Generar backend_{nombre}.py (copiar de template)
□ 6.3 Generar gui_{nombre}.py (copiar de template)
□ 6.4 Crear carpeta scripts/{nombre}/
□ 6.5 Testing: ast.parse + GUI abre + flujo completo
```

### Estructura de Carpeta

```
scripts/{nombre}/
    gui_{nombre}.py         # PySide6 GUI
    backend_{nombre}.py     # COM directo (comtypes)
```

### Template: SapConnection (COM directo)

```python
import comtypes.client

class SapConnection:
    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing=True) -> dict:
        try:
            self.sap_object = comtypes.client.GetActiveObject(
                "CSI.SAP2000.API.SapObject"
            )
            self.sap_model = self.sap_object.SapModel
            return {"connected": True,
                    "version": str(self.sap_object.GetOAPIVersionNumber()),
                    "model_path": str(self.sap_model.GetModelFilename())}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}
```

### Template: Backend.run()

```python
class MyBackend:
    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config) -> dict:
        SapModel = self.sap_model
        result = {}
        # ... lógica del script (tareas numeradas, asserts) ...
        result["success"] = True
        return result
```

### Template: QThread Worker

```python
class RunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend, config):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            result = self._backend.run(self._config)
            self.finished.emit(result)
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})
```

### Reglas

| ✅ Hacer | ❌ No Hacer |
|----------|-------------|
| `import comtypes.client` | `from sap_bridge import bridge` |
| `SapConnection.connect()` | `bridge.connect()` |
| `backend.run(config)` | `run_script(script_text)` |
| `from backend_X import ...` | `from sap_executor import ...` |
| Solo stdlib + comtypes + PySide6 | Importar `app_logger`, `sap_utils_common` |

### Naming Convention

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| Script MCP verificado | `scripts/example_*.py` | `scripts/example_ring_areas_parametric.py` |
| GUI standalone | `scripts/{nombre}/gui_{nombre}.py` | `scripts/ring_areas/gui_ring_areas.py` |
| Backend standalone | `scripts/{nombre}/backend_{nombre}.py` | `scripts/ring_areas/backend_ring_areas.py` |
| Templates | `scripts/templates/*.py` | `scripts/templates/backend_template.py` |
| Wrappers | `scripts/wrappers/func_*.py` | `scripts/wrappers/func_FrameObj_AddByCoord.py` |
```

##### Step 4 Verification Checklist
- [x] New section `## 🖥️ GUI Standalone — Quick Reference` appended
- [x] Contains checklist, folder structure, 3 code snippets (SapConnection, Backend, Worker)
- [x] Rules table clearly shows DO vs DON'T
- [x] Naming convention table is accurate
- [x] Code snippets are syntactically valid Python

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 5a: Migrate Ring Areas to Standalone Pattern

This step creates the new standalone ring_areas GUI and backend, moves the MCP script out of the old folder, and deletes the old folder.

- [x] Create directory `scripts/ring_areas/`
- [x] Create file `scripts/ring_areas/backend_ring_areas.py` with the complete code below:

```python
"""
Backend — SAP2000 Circular Ring Area Generator (Standalone)
============================================================
Genera un modelo de anillo circular (placa anular) con 3 zonas concéntricas
de área (shell), separadas por radios intermedios.

Conexión: COM directo vía comtypes.client (sin MCP).
Referencia de estilo: example_1001_simple_beam.py
"""

import math
import tempfile
import comtypes.client
from dataclasses import dataclass


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing: bool = True) -> dict:
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                self.sap_object.ApplicationStart()

            self.sap_model = self.sap_object.SapModel
            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())
            return {"connected": True, "version": version, "model_path": model_path}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class RingAreasConfig:
    """Parámetros de entrada para el generador de anillos."""

    # Radios [m]
    r_inner: float = 1.0
    r_mid1: float = 2.0
    r_mid2: float = 3.5
    r_outer: float = 5.0

    # Espesores de shell [m]
    t1: float = 0.30   # Zona 1 (interior) y Zona 3 (exterior)
    t2: float = 0.20   # Zona 2 (intermedia)

    # Material
    mat_name: str = "CONC"
    E_mat: float = 2.5e7       # [kN/m²]
    nu_mat: float = 0.2
    alpha: float = 1.0e-5      # [1/°C]

    # Discretización
    n_segs: int = 36


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class RingAreasBackend:
    """Backend standalone para generar anillos concéntricos en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Funciones auxiliares ──────────────────────────────────────────────

    @staticmethod
    def ring_pts(radius: float, n: int):
        """Devuelve lista de n puntos (x, y) sobre una circunferencia."""
        return [
            (radius * math.cos(2.0 * math.pi * i / n),
             radius * math.sin(2.0 * math.pi * i / n))
            for i in range(n)
        ]

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: RingAreasConfig) -> dict:
        """Ejecuta la generación de anillos concéntricos.

        Args:
            config: Parámetros de entrada.

        Returns:
            dict con resultados del modelo generado.
        """
        SapModel = self.sap_model
        result = {}

        # ── Task 1: Inicializar modelo ───────────────────────────────────
        ret = SapModel.InitializeNewModel()
        assert ret == 0, f"InitializeNewModel failed: {ret}"

        ret = SapModel.File.NewBlank()
        assert ret == 0, f"NewBlank failed: {ret}"

        ret = SapModel.SetPresentUnits(6)  # kN_m_C
        assert ret == 0, f"SetPresentUnits failed: {ret}"

        result["task_1_init"] = True

        # ── Task 2: Definir material ─────────────────────────────────────
        ret = SapModel.PropMaterial.SetMaterial(config.mat_name, 2)  # 2 = Concrete
        assert ret == 0, f"SetMaterial failed: {ret}"

        ret = SapModel.PropMaterial.SetMPIsotropic(
            config.mat_name, config.E_mat, config.nu_mat, config.alpha
        )
        assert ret == 0, f"SetMPIsotropic failed: {ret}"

        result["task_2_material"] = config.mat_name

        # ── Task 3: Definir propiedades de área (shell) ──────────────────
        ret = SapModel.PropArea.SetShell_1(
            "SHELL_T1", 1, True, config.mat_name, 0, config.t1, config.t1
        )
        assert ret == 0, f"SetShell_1(SHELL_T1) failed: {ret}"

        ret = SapModel.PropArea.SetShell_1(
            "SHELL_T2", 1, True, config.mat_name, 0, config.t2, config.t2
        )
        assert ret == 0, f"SetShell_1(SHELL_T2) failed: {ret}"

        result["task_3_sections"] = {"SHELL_T1": config.t1, "SHELL_T2": config.t2}

        # ── Task 4: Generar geometría de anillos concéntricos ────────────
        zones = [
            (config.r_inner, config.r_mid1,  "SHELL_T1", "ZONA1_interior"),
            (config.r_mid1,  config.r_mid2,  "SHELL_T2", "ZONA2_intermedia"),
            (config.r_mid2,  config.r_outer, "SHELL_T1", "ZONA3_exterior"),
        ]
        area_count = {
            "ZONA1_interior": 0,
            "ZONA2_intermedia": 0,
            "ZONA3_exterior": 0,
        }

        n = config.n_segs
        for (r_in, r_out, prop, label) in zones:
            pts_in = self.ring_pts(r_in, n)
            pts_out = self.ring_pts(r_out, n)

            for i in range(n):
                j = (i + 1) % n

                x = [pts_in[i][0], pts_out[i][0], pts_out[j][0], pts_in[j][0]]
                y = [pts_in[i][1], pts_out[i][1], pts_out[j][1], pts_in[j][1]]
                z = [0.0, 0.0, 0.0, 0.0]

                raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", prop, "")
                assert raw[-1] == 0, f"AddByCoord({label}[{i}]) failed: {raw[-1]}"
                area_count[label] += 1

        result["task_4_geometry"] = area_count
        result["total_areas"] = sum(area_count.values())

        # ── Task 5: Guardar modelo y refrescar vista ─────────────────────
        save_path = tempfile.gettempdir() + r"\ring_areas_model.sdb"
        ret = SapModel.File.Save(save_path)
        assert ret == 0, f"File.Save failed: {ret}"

        SapModel.View.RefreshView(0, False)
        result["task_5_saved"] = True
        result["save_path"] = save_path

        # ── Resumen final ────────────────────────────────────────────────
        result["success"] = True
        result["radii"] = {
            "r_inner": config.r_inner,
            "r_mid1": config.r_mid1,
            "r_mid2": config.r_mid2,
            "r_outer": config.r_outer,
        }
        result["thicknesses"] = {
            "t1 (Zona1+Zona3)": config.t1,
            "t2 (Zona2)": config.t2,
        }
        result["n_segments"] = config.n_segs

        return result


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = RingAreasBackend(conn)
        config = RingAreasConfig()

        try:
            output = backend.run(config)
            import json
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
```

- [x] Create file `scripts/ring_areas/gui_ring_areas.py` with the complete code below:

```python
"""
GUI — SAP2000 Circular Ring Area Generator (Standalone)
========================================================
PySide6 interface for the parametric ring-areas backend.
Conexión directa vía comtypes (sin MCP).

Layout
------
  [Conectar]
  ── Inputs ─────────────────────────────────
     Radios (m):   r_inner  r_mid1  r_mid2  r_outer
     Espesores (m): t1  t2
     Material:     nombre  E  nu  alpha
     Malla:        n_segs
  ── ─────────────────────────────────────────
  [Ejecutar]
  ── Output ─────────────────────────────────
     log de texto con resultado / errores
  ── ─────────────────────────────────────────
  [Desconectar]
"""

import sys
import json

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

from backend_ring_areas import SapConnection, RingAreasBackend, RingAreasConfig


# ══════════════════════════════════════════════════════════════════════════════
# Workers — operaciones SAP2000 fuera del hilo GUI
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.connect(attach_to_existing=True)
        self.finished.emit(result)


class RunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: RingAreasBackend, config: RingAreasConfig):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            result = self._backend.run(self._config)
            self.finished.emit(result)
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.disconnect()
        self.finished.emit(result)


# ══════════════════════════════════════════════════════════════════════════════
# Helper — campo de entrada con label
# ══════════════════════════════════════════════════════════════════════════════

def _field(label: str, default: str, tooltip: str = "") -> tuple:
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    edit = QLineEdit(default)
    edit.setMinimumWidth(90)
    if tooltip:
        edit.setToolTip(tooltip)
        lbl.setToolTip(tooltip)
    return lbl, edit


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class RingAreasGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Circular Ring Area Generator")
        self.setMinimumWidth(640)

        self._conn = SapConnection()
        self._backend = RingAreasBackend(self._conn)
        self._worker = None

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Status ───────────────────────────────────────────────────────
        status_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        status_row.addWidget(self._status_lbl)
        status_row.addStretch()
        root.addLayout(status_row)

        # ── Botón Conectar ───────────────────────────────────────────────
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)
        root.addWidget(self._btn_connect)

        # ── Inputs ───────────────────────────────────────────────────────
        inputs_box = QGroupBox("Parámetros de entrada")
        grid = QGridLayout(inputs_box)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        def _header(text: str, row: int):
            lbl = QLabel(f"<b>{text}</b>")
            grid.addWidget(lbl, row, 0, 1, 4)

        r = 0

        # Radios
        _header("Radios [m]", r); r += 1

        lbl, self._r_inner = _field("r_inner", "1.0", "Radio interior – borde del agujero central")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._r_inner, r, 1)
        lbl, self._r_mid1 = _field("r_mid1", "2.0", "Límite Zona 1 / Zona 2")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._r_mid1, r, 3)
        r += 1

        lbl, self._r_mid2 = _field("r_mid2", "3.5", "Límite Zona 2 / Zona 3")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._r_mid2, r, 1)
        lbl, self._r_outer = _field("r_outer", "5.0", "Radio exterior del anillo")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._r_outer, r, 3)
        r += 1

        # Espesores
        _header("Espesores de shell [m]", r); r += 1

        lbl, self._t1 = _field("t1", "0.30", "Espesor Zona 1 (interior) y Zona 3 (exterior)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._t1, r, 1)
        lbl, self._t2 = _field("t2", "0.20", "Espesor Zona 2 (intermedia)")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._t2, r, 3)
        r += 1

        # Material
        _header("Material", r); r += 1

        lbl, self._mat_name = _field("Nombre", "CONC", "Nombre del material en SAP2000")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._mat_name, r, 1)
        lbl, self._E_mat = _field("E [kN/m²]", "2.5e7", "Módulo de elasticidad")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._E_mat, r, 3)
        r += 1

        lbl, self._nu_mat = _field("nu", "0.2", "Coeficiente de Poisson")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._nu_mat, r, 1)
        lbl, self._alpha = _field("alpha [1/°C]", "1e-5", "Coeficiente de expansión térmica")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._alpha, r, 3)
        r += 1

        # Discretización
        _header("Discretización", r); r += 1

        lbl, self._n_segs = _field("n_segs", "36", "Segmentos angulares (≥ 12 recomendado)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._n_segs, r, 1)
        r += 1

        root.addWidget(inputs_box)

        # ── Botón Ejecutar ───────────────────────────────────────────────
        self._btn_run = QPushButton("Ejecutar Script")
        self._btn_run.setFixedHeight(34)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Output log ───────────────────────────────────────────────────
        output_box = QGroupBox("Salida")
        out_layout = QVBoxLayout(output_box)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(160)
        out_layout.addWidget(self._log)
        root.addWidget(output_box)

        # ── Botón Desconectar ────────────────────────────────────────────
        self._btn_disconnect = QPushButton("Desconectar de SAP2000")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        root.addWidget(self._btn_disconnect)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_run.setEnabled(connected)
        self._btn_disconnect.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")

    def _log_append(self, text: str):
        self._log.append(text)

    def _busy(self, is_busy: bool):
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_run.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)

    def _build_config(self) -> RingAreasConfig:
        return RingAreasConfig(
            r_inner=float(self._r_inner.text()),
            r_mid1=float(self._r_mid1.text()),
            r_mid2=float(self._r_mid2.text()),
            r_outer=float(self._r_outer.text()),
            t1=float(self._t1.text()),
            t2=float(self._t2.text()),
            mat_name=self._mat_name.text(),
            E_mat=float(self._E_mat.text()),
            nu_mat=float(self._nu_mat.text()),
            alpha=float(self._alpha.text()),
            n_segs=int(self._n_segs.text()),
        )

    # ── Conectar ─────────────────────────────────────────────────────────

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            self._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._set_connected(True)
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    # ── Ejecutar ─────────────────────────────────────────────────────────

    def _on_run(self):
        try:
            config = self._build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return

        self._log_append("\n─── Ejecutando script ───────────────────────────────")
        self._busy(True)
        self._worker = RunWorker(self._backend, config)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Script ejecutado exitosamente")
            self._log_append(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ Error: {err}")

    # ── Desconectar ──────────────────────────────────────────────────────

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._busy(False)
        self._log_append("✔ Desconectado de SAP2000")
        self._set_connected(False)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = RingAreasGUI()
    win.show()
    sys.exit(app.exec())
```

- [x] Move the MCP script to scripts root:
```powershell
Copy-Item "scripts/ring_areas_parametric/example_ring_areas_parametric.py" "scripts/example_ring_areas_parametric.py"
```

- [x] Delete the old folder:
```powershell
Remove-Item "scripts/ring_areas_parametric" -Recurse -Force
```

- [x] Verify syntax of both new files:
```powershell
python -c "import ast, pathlib; ast.parse(pathlib.Path('scripts/ring_areas/backend_ring_areas.py').read_text(encoding='utf-8')); print('backend OK')"
python -c "import ast, pathlib; ast.parse(pathlib.Path('scripts/ring_areas/gui_ring_areas.py').read_text(encoding='utf-8')); print('gui OK')"
```

- [x] Verify no MCP imports in new files:
```powershell
python -c "
for f in ['scripts/ring_areas/backend_ring_areas.py', 'scripts/ring_areas/gui_ring_areas.py']:
    t = open(f, encoding='utf-8').read()
    for bad in ['sap_bridge', 'sap_executor', 'mcp_server', 'run_script']:
        assert bad not in t, f'{bad} found in {f}'
print('no MCP imports ✔')
"
```

##### Step 5a Verification Checklist
- [x] `scripts/ring_areas/backend_ring_areas.py` exists with `SapConnection`, `RingAreasConfig`, `RingAreasBackend`
- [x] `scripts/ring_areas/gui_ring_areas.py` exists with `RingAreasGUI`, 3 workers
- [x] `scripts/example_ring_areas_parametric.py` exists (moved from old folder)
- [x] `scripts/ring_areas_parametric/` folder is deleted
- [x] Both files pass `ast.parse`
- [x] No MCP imports in either file
- [x] GUI imports from `backend_ring_areas` (relative)
- [x] Backend uses `comtypes.client` for connection
- [x] Backend `run()` logic matches the verified MCP script

#### Step 5a STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 5b: Migrate Placabase to Standalone Pattern

This step creates the new standalone placabase GUI and backend, then removes the old file.

- [ ] Create directory `scripts/placabase/`
- [ ] Create file `scripts/placabase/backend_placabase.py` with the complete code below:

```python
"""
Backend — SAP2000 Placa Base Generator (Standalone)
=====================================================
Genera un modelo parametrizado de placa base con pernos de anclaje,
silla opcional, body constraints, TC limits, y resortes de balasto.

Conexión: COM directo vía comtypes.client (sin MCP).
Basado en: placabase_backend.py (migrado a standalone, sin app_logger/sap_utils_common)
"""

import math
import tempfile
import comtypes.client
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing: bool = True) -> dict:
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                self.sap_object.ApplicationStart()

            self.sap_model = self.sap_object.SapModel
            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())
            return {"connected": True, "version": version, "model_path": model_path}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

DIA_TO_SPACING = {
    16: (80, 80), 19: (100, 100), 22: (100, 100), 25: (100, 100),
    32: (125, 125), 38: (150, 150), 44: (175, 175), 51: (200, 200),
    57: (225, 225), 64: (250, 250),
}


@dataclass
class PlacaBaseConfig:
    """Parámetros de entrada para el generador de placa base."""

    # Pernos
    bolt_dia: float = 25.0
    bolt_material: str = "A36"
    n_pernos: int = 4
    bolt_centers: List[Tuple[float, float, float]] = field(default_factory=list)

    # Columna
    H_col: float = 300.0
    B_col: float = 250.0

    # Espesores
    plate_thickness: float = 20.0
    flange_thickness: float = 15.0
    web_thickness: float = 10.0

    # Silla de anclaje
    include_anchor_chair: bool = False
    anchor_chair_height: float = 50.0
    anchor_chair_thickness: float = 15.0

    # Balasto
    ks_balasto: float = 0.0  # kgf/cm³ — 0 para omitir

    @staticmethod
    def map_dia_to_spacing(dia: float) -> Tuple[float, float]:
        d = int(round(float(dia)))
        return DIA_TO_SPACING.get(d, (100.0, 100.0))

    def resolve_bolt_centers(self):
        """Auto-genera bolt_centers si está vacío."""
        if not self.bolt_centers:
            A, _ = self.map_dia_to_spacing(self.bolt_dia)
            H = self.H_col
            self.bolt_centers = [
                (A / 2.0, H / 2.0, 0.0), (3 * A / 2.0, H / 2.0, 0.0),
                (-A / 2.0, H / 2.0, 0.0), (-3 * A / 2.0, H / 2.0, 0.0),
                (A / 2.0, -H / 2.0, 0.0), (3 * A / 2.0, -H / 2.0, 0.0),
                (-A / 2.0, -H / 2.0, 0.0), (-3 * A / 2.0, -H / 2.0, 0.0),
            ]
            self.bolt_centers = self.bolt_centers[: self.n_pernos]


# ══════════════════════════════════════════════════════════════════════════════
# Helpers — ret code checking (inline, replaces sap_utils_common)
# ══════════════════════════════════════════════════════════════════════════════

def _check_ret(ret) -> bool:
    """Verifica si un return code/tuple indica éxito (0)."""
    if isinstance(ret, (list, tuple)):
        return len(ret) > 0 and int(ret[-1]) == 0
    return int(ret) == 0


def _get_name(ret, fallback: str) -> str:
    """Extrae el nombre creado de un retorno COM (primer elemento)."""
    if isinstance(ret, (list, tuple)) and len(ret) >= 2 and ret[-1] == 0:
        val = ret[0]
        if isinstance(val, (list, tuple)) and len(val) > 0:
            return str(val[0])
        return str(val)
    return fallback


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class PlacaBaseBackend:
    """Backend standalone para generar placa base en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Funciones de geometría ───────────────────────────────────────────

    def _create_point(self, x: float, y: float, z: float, user_name: str = "") -> Optional[str]:
        ret = self.sap_model.PointObj.AddCartesian(x, y, z, "", user_name)
        if _check_ret(ret):
            return _get_name(ret, user_name)
        return None

    def _create_area_by_points(self, points: List[str], prop: str, user_name: str = "") -> Optional[str]:
        ret = self.sap_model.AreaObj.AddByPoint(len(points), points, "", prop, user_name)
        if _check_ret(ret):
            return _get_name(ret, user_name)
        return None

    def _create_area_by_coord(self, xs, ys, zs, prop: str, user_name: str = "") -> Optional[str]:
        ret = self.sap_model.AreaObj.AddByCoord(len(xs), xs, ys, zs, "", prop, user_name, "Global")
        if _check_ret(ret):
            return _get_name(ret, user_name)
        return None

    def _get_point_coord(self, name: str) -> Optional[Tuple[float, float, float]]:
        try:
            ret = self.sap_model.PointObj.GetCoordCartesian(name, 0.0, 0.0, 0.0, "Global")
            if _check_ret(ret):
                return (ret[0], ret[1], ret[2])
        except Exception:
            pass
        return None

    def _create_shell_prop(self, name: str, thickness: float, mat: str = "A992Fy50"):
        ret = self.sap_model.PropArea.SetShell_1(name, 1, True, mat, 0.0, thickness, thickness)
        assert _check_ret(ret), f"SetShell_1({name}) failed"

    def _create_circle_points(self, cx, cy, z, radius, num_points=16, prefix="P_c"):
        names = []
        for j in range(num_points):
            angle = -math.radians(j * (360.0 / num_points))
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            nm = self._create_point(x, y, z, f"{prefix}{j + 1}")
            names.append(nm)
        return names

    def _create_square_points(self, cx, cy, z, side, num_points=16, prefix="P_s"):
        half = side / 2.0
        perimeter = 4.0 * side
        names = []
        if num_points < 4:
            num_points = 4

        for i in range(num_points):
            s = (i * perimeter) / num_points
            if s < half:
                x, y = half, -s
            elif s < half + side:
                rem = s - half
                x, y = half - rem, -half
            elif s < half + 2 * side:
                rem = s - (half + side)
                x, y = -half, -half + rem
            elif s < half + 3 * side:
                rem = s - (half + 2 * side)
                x, y = -half + rem, half
            else:
                rem = s - (half + 3 * side)
                x, y = half, half - rem

            nm = self._create_point(cx + x, cy + y, z, f"{prefix}{i + 1}")
            names.append(nm)
        return names

    def _sort_points_angularly(self, point_names, center):
        valid_pts = []
        for pn in point_names:
            if not pn:
                continue
            coord = self._get_point_coord(pn)
            if coord:
                angle = math.atan2(coord[1] - center[1], coord[0] - center[0])
                valid_pts.append((pn, angle))
        valid_pts.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in valid_pts]

    def _align_rings(self, inner_pts, outer_pts, center):
        inner_sorted = self._sort_points_angularly(inner_pts, center)
        outer_sorted = self._sort_points_angularly(outer_pts, center)
        if not inner_sorted or not outer_sorted:
            return inner_sorted, outer_sorted

        def get_angles(pts):
            angles = []
            for p in pts:
                c = self._get_point_coord(p)
                if c:
                    angles.append(math.atan2(c[1] - center[1], c[0] - center[0]))
                else:
                    angles.append(0)
            return angles

        inner_angs = get_angles(inner_sorted)
        outer_angs = get_angles(outer_sorted)
        n = len(inner_sorted)
        best_shift = 0
        min_diff = float("inf")
        for shift in range(n):
            diff = 0
            for i in range(n):
                a1 = inner_angs[i]
                a2 = outer_angs[(i + shift) % n]
                d = abs(a1 - a2) % (2 * math.pi)
                d = min(d, 2 * math.pi - d)
                diff += d
            if diff < min_diff:
                min_diff = diff
                best_shift = shift
        if best_shift != 0:
            outer_sorted = outer_sorted[best_shift:] + outer_sorted[:best_shift]
        return inner_sorted, outer_sorted

    def _create_ring_mesh(self, inner_pts, outer_pts, center, prefix, prop):
        inner, outer = self._align_rings(inner_pts, outer_pts, center)
        n = min(len(inner), len(outer))
        for i in range(n):
            p1 = inner[i]
            p2 = inner[(i + 1) % n]
            p3 = outer[(i + 1) % n]
            p4 = outer[i]
            self._create_area_by_points([p1, p2, p3, p4], prop, f"{prefix}_{i + 1}")

    def _coordinate_range(self, xmin, xmax, ymin, ymax, zmin, zmax,
                          deselect=False, csys="Global", include_intersections=False,
                          point=True, line=True, area=True, solid=True, link=True):
        try:
            ret = self.sap_model.SelectObj.CoordinateRange(
                float(xmin), float(xmax), float(ymin), float(ymax),
                float(zmin), float(zmax), bool(deselect), str(csys),
                bool(include_intersections),
                bool(point), bool(line), bool(area), bool(solid), bool(link),
            )
        except Exception:
            return False, None
        if isinstance(ret, (list, tuple)):
            return int(ret[-1]) == 0, ret
        return int(ret) == 0, ret

    def _divide_area_by_selection(self, area_name: str) -> list:
        try:
            ret = self.sap_model.EditArea.Divide(
                str(area_name), 3, 0, [], 0, 0, 0.0, 0.0, False, False, True
            )
            if _check_ret(ret) and len(ret) >= 2:
                names = ret[1]
                if isinstance(names, (list, tuple)):
                    return list(names)
        except Exception:
            pass
        return []

    def _subdivide_areas(self, area_names, n1=2, n2=2):
        for name in area_names:
            try:
                self.sap_model.EditArea.Divide(name, 1, 0, [], n1, n2)
            except Exception:
                pass

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: PlacaBaseConfig) -> dict:
        """Ejecuta la generación completa de placa base.

        Args:
            config: Parámetros de entrada (auto-resuelve bolt_centers si vacío).

        Returns:
            dict con resultados del modelo generado.
        """
        config.resolve_bolt_centers()
        SapModel = self.sap_model
        result = {}

        H = config.H_col
        B = config.B_col
        A, B_bolt = config.map_dia_to_spacing(config.bolt_dia)
        circle_radius = config.bolt_dia / 2.0
        outer_half = B_bolt / 2.0
        inner_half = (circle_radius + outer_half) / 2.0
        inner_side = inner_half * 2.0
        bolt_length = 8.0 * config.bolt_dia
        z_col = 2.0 * H

        # ── Task 1: Propiedades de material y shell ──────────────────────
        plate_prop = "PLACA_BASE"
        if config.plate_thickness:
            self._create_shell_prop(plate_prop, config.plate_thickness)
        if config.flange_thickness:
            self._create_shell_prop("ALA", config.flange_thickness)
        if config.web_thickness:
            self._create_shell_prop("ALMA", config.web_thickness)

        chair_prop = None
        if config.include_anchor_chair and config.anchor_chair_height > 0 and config.anchor_chair_thickness > 0:
            chair_prop = "ChairPlate"
            self._create_shell_prop(chair_prop, config.anchor_chair_thickness)

        result["task_1_properties"] = True

        # ── Task 1b: Sección Frame para pernos ──────────────────────────
        bolt_section = f"BOLT_{int(config.bolt_dia)}"
        ret = SapModel.PropFrame.SetCircle(bolt_section, config.bolt_material, config.bolt_dia)
        bolt_section_ok = _check_ret(ret)
        result["bolt_section"] = bolt_section if bolt_section_ok else None

        # ── Task 2: Geometría de columna ─────────────────────────────────
        self._create_area_by_coord(
            [-B / 2, B / 2, B / 2, -B / 2],
            [H / 2, H / 2, H / 2, H / 2],
            [0, 0, z_col, z_col],
            "ALA", "COL_FLANGE_TOP",
        )
        self._create_area_by_coord(
            [-B / 2, B / 2, B / 2, -B / 2],
            [-H / 2, -H / 2, -H / 2, -H / 2],
            [0, 0, z_col, z_col],
            "ALA", "COL_FLANGE_BOTTOM",
        )
        self._create_area_by_coord(
            [0, 0, 0, 0],
            [H / 2, -H / 2, -H / 2, H / 2],
            [0, 0, z_col, z_col],
            "ALMA", "COL_WEB",
        )
        result["task_2_column"] = True

        # ── Task 3: Áreas de pernos y mesh ───────────────────────────────
        outer_square_points_list = []
        chair_outer_square_points_list = []
        bolt_frame_names = []

        for idx, (cx, cy, cz) in enumerate(config.bolt_centers, 1):
            self._create_point(cx, cy, cz, f"CENTER_{idx}")

            c_pts = self._create_circle_points(cx, cy, cz, circle_radius, 16, f"P_c{idx}_")
            in_pts = self._create_square_points(cx, cy, cz, inner_side, 16, f"P_s_in{idx}_")
            out_pts = self._create_square_points(cx, cy, cz, B_bolt, 16, f"P_s_out{idx}_")
            outer_square_points_list.append(out_pts)

            if config.plate_thickness:
                self._create_ring_mesh(c_pts, in_pts, (cx, cy), f"A_ring_in{idx}", plate_prop)
                self._create_ring_mesh(in_pts, out_pts, (cx, cy), f"A_ring_out{idx}", plate_prop)

            # Bolt Frames + Body Constraints
            if bolt_section_ok:
                center_name = f"CENTER_{idx}"

                if chair_prop:
                    # CON SILLA: perno de 2 tramos
                    chair_center, chair_c_pts, chair_out_pts = self._create_single_chair(
                        idx, cx, cy, config.anchor_chair_height,
                        circle_radius, inner_side, B_bolt, chair_prop,
                    )
                    chair_outer_square_points_list.append(chair_out_pts)

                    # Tramo superior: silla → placa
                    chair_frame = self._create_chair_bolt_frame(
                        chair_center, center_name, bolt_section, idx
                    )
                    if chair_frame:
                        bolt_frame_names.append(chair_frame)

                    # Tramo inferior: placa → fundación
                    frame_name, bottom_pt = self._create_bolt_frame(
                        center_name, cx, cy, cz, bolt_section, bolt_length, idx
                    )
                    if frame_name:
                        bolt_frame_names.append(frame_name)

                    # Body Constraint en silla (todos DOF)
                    self._create_body_constraint(
                        f"BOLT_BODY_CHAIR_{idx}", chair_center, chair_c_pts,
                        [True, True, True, True, True, True],
                    )
                    # Body Constraint en placa (UZ libre)
                    self._create_body_constraint(
                        f"BOLT_BODY_{idx}", center_name, c_pts,
                        [True, True, False, True, True, True],
                    )
                    if frame_name and bottom_pt:
                        self._set_pin_restraint(bottom_pt)
                else:
                    # SIN SILLA: perno de 1 tramo
                    frame_name, bottom_pt = self._create_bolt_frame(
                        center_name, cx, cy, cz, bolt_section, bolt_length, idx
                    )
                    if frame_name:
                        bolt_frame_names.append(frame_name)
                        self._create_body_constraint(
                            f"BOLT_BODY_{idx}", center_name, c_pts,
                            [True, True, True, True, True, True],
                        )
                        self._set_pin_restraint(bottom_pt)

        result["task_3_bolts"] = len(config.bolt_centers)
        result["bolt_frames"] = len(bolt_frame_names)

        # ── Task 4: Área de enlace ───────────────────────────────────────
        if len(config.bolt_centers) >= 4 and len(outer_square_points_list) == len(config.bolt_centers):
            try:
                N = len(config.bolt_centers) // 2
                if 2 * N - 1 < len(outer_square_points_list):
                    p1 = outer_square_points_list[N][10]
                    p2 = outer_square_points_list[2 * N - 1][14]
                    p3 = outer_square_points_list[N - 1][2]
                    p4 = outer_square_points_list[0][6]
                    link_area = self._create_area_by_points(
                        [p1, p2, p3, p4], plate_prop, "A_outer_link"
                    )
                    if link_area:
                        self.sap_model.EditArea.Divide(link_area, 1, 0, [], 4 * config.n_pernos, 10)
            except Exception:
                pass

        if chair_prop and len(chair_outer_square_points_list) >= 4:
            try:
                N = len(config.bolt_centers) // 2
                if 2 * N - 1 < len(chair_outer_square_points_list):
                    p1 = chair_outer_square_points_list[N][10]
                    p2 = chair_outer_square_points_list[2 * N - 1][14]
                    p3 = chair_outer_square_points_list[N - 1][2]
                    p4 = chair_outer_square_points_list[0][6]
                    chair_link = self._create_area_by_points(
                        [p1, p2, p3, p4], chair_prop, "A_chair_link"
                    )
                    if chair_link:
                        self.sap_model.EditArea.Divide(chair_link, 1, 0, [], 4 * config.n_pernos, 10)
            except Exception:
                pass

        # Chair-level column points
        if chair_prop and config.anchor_chair_height:
            z_ch = config.anchor_chair_height
            self._create_point(-B / 2, H / 2, z_ch, "COL_FT_CHAIR_L")
            self._create_point(B / 2, H / 2, z_ch, "COL_FT_CHAIR_R")
            self._create_point(-B / 2, -H / 2, z_ch, "COL_FB_CHAIR_L")
            self._create_point(B / 2, -H / 2, z_ch, "COL_FB_CHAIR_R")
            self._create_point(0, H / 2, z_ch, "COL_WEB_CHAIR_T")
            self._create_point(0, -H / 2, z_ch, "COL_WEB_CHAIR_B")

        result["task_4_link_area"] = True

        # ── Task 5: Mesh refinement ──────────────────────────────────────
        try:
            z_target = 0.0

            # Top flange
            SapModel.SelectObj.ClearSelection()
            ok, _ = self._coordinate_range(
                -B / 2, B / 2, H / 2, H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if chair_prop and config.anchor_chair_height:
                self._coordinate_range(
                    -B / 2, B / 2, H / 2, H / 2,
                    config.anchor_chair_height, config.anchor_chair_height,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
            if ok:
                new_areas = self._divide_area_by_selection("COL_FLANGE_TOP")
                self._subdivide_areas(new_areas, 1, 2)

            # Bottom flange
            SapModel.SelectObj.ClearSelection()
            ok, _ = self._coordinate_range(
                -B / 2, B / 2, -H / 2, -H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if chair_prop and config.anchor_chair_height:
                self._coordinate_range(
                    -B / 2, B / 2, -H / 2, -H / 2,
                    config.anchor_chair_height, config.anchor_chair_height,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
            if ok:
                new_areas = self._divide_area_by_selection("COL_FLANGE_BOTTOM")
                self._subdivide_areas(new_areas, 1, 2)

            # Link area at top flange line
            SapModel.SelectObj.ClearSelection()
            x_limit = A * config.n_pernos / 2.0
            ok, _ = self._coordinate_range(
                -x_limit, x_limit, H / 2, H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if ok:
                new_areas = self._divide_area_by_selection("A_outer_link")
                self._subdivide_areas(new_areas, 1, 2)

            # Chair link
            if chair_prop and config.anchor_chair_height:
                SapModel.SelectObj.ClearSelection()
                z_ch = config.anchor_chair_height
                ok, _ = self._coordinate_range(
                    -x_limit, x_limit, H / 2, H / 2, z_ch, z_ch,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
                if ok:
                    new_areas = self._divide_area_by_selection("A_chair_link")
                    self._subdivide_areas(new_areas, 1, 2)

            # Web
            SapModel.SelectObj.ClearSelection()
            ok, _ = self._coordinate_range(
                0.0, 0.0, -H / 2, H / 2, z_target, z_target,
                deselect=False, csys="Global", include_intersections=True,
                point=True, line=False, area=False, solid=False, link=False,
            )
            if chair_prop and config.anchor_chair_height:
                self._coordinate_range(
                    0.0, 0.0, -H / 2, H / 2,
                    config.anchor_chair_height, config.anchor_chair_height,
                    deselect=False, csys="Global", include_intersections=True,
                    point=True, line=False, area=False, solid=False, link=False,
                )
            if ok:
                new_areas = self._divide_area_by_selection("COL_WEB")
                self._subdivide_areas(new_areas, 1, 2)

        except Exception:
            pass

        result["task_5_mesh"] = True

        # ── Task 6: TC Limits (compresión=0 en pernos) ──────────────────
        tc_ok = 0
        for name in bolt_frame_names:
            try:
                ret = SapModel.FrameObj.SetTCLimits(str(name), True, 0.0, False, 0.0, 0)
                if _check_ret(ret):
                    tc_ok += 1
            except Exception:
                pass
        result["task_6_tc_limits"] = tc_ok

        # ── Task 7: Módulo de balasto ────────────────────────────────────
        if config.ks_balasto and config.ks_balasto > 0:
            current_units = SapModel.GetPresentUnits()
            SapModel.SetPresentUnits(14)  # kgf_cm_C
            try:
                SapModel.SelectObj.ClearSelection()
                ok, _ = self._coordinate_range(
                    -1e10, 1e10, -1e10, 1e10, 0.0, 0.0,
                    deselect=False, csys="Global", include_intersections=True,
                    point=False, line=False, area=True, solid=False, link=False,
                )
                if ok:
                    vec = [0.0, 0.0, 0.0]
                    ret = SapModel.AreaObj.SetSpring(
                        "ALL", 1, float(config.ks_balasto), 2, "", -1, 2, 1,
                        True, vec, 0.0, True, "Local", 2,
                    )
                    result["task_7_balasto"] = _check_ret(ret)
                else:
                    result["task_7_balasto"] = False
            finally:
                SapModel.SetPresentUnits(current_units)
        else:
            result["task_7_balasto"] = "skipped"

        # ── Task 8: Refresh ──────────────────────────────────────────────
        try:
            SapModel.View.RefreshView(0, False)
            SapModel.View.RefreshWindow()
        except Exception:
            pass

        result["success"] = True
        result["n_pernos"] = len(config.bolt_centers)
        result["bolt_frames_total"] = len(bolt_frame_names)
        result["include_anchor_chair"] = config.include_anchor_chair

        return result

    # ── Helpers internos de pernos ───────────────────────────────────────

    def _create_bolt_frame(self, center_name, cx, cy, cz, section, bolt_length, idx):
        z_bottom = cz - bolt_length
        bottom_pt = self._create_point(cx, cy, z_bottom, f"BOLT_BASE_{idx}")
        if not bottom_pt:
            return None, None
        try:
            ret = self.sap_model.FrameObj.AddByPoint(
                center_name, bottom_pt, "", section, f"BOLT_FRAME_{idx}"
            )
            if _check_ret(ret):
                return _get_name(ret, f"BOLT_FRAME_{idx}"), bottom_pt
        except Exception:
            pass
        return None, None

    def _create_chair_bolt_frame(self, chair_pt, plate_pt, section, idx):
        try:
            ret = self.sap_model.FrameObj.AddByPoint(
                chair_pt, plate_pt, "", section, f"BOLT_CHAIR_FRAME_{idx}"
            )
            if _check_ret(ret):
                return _get_name(ret, f"BOLT_CHAIR_FRAME_{idx}")
        except Exception:
            pass
        return None

    def _create_body_constraint(self, name, center_pt, circle_pts, dof_values):
        try:
            ret = self.sap_model.ConstraintDef.SetBody(name, dof_values, "Global")
            if not _check_ret(ret):
                return False
        except Exception:
            return False

        try:
            self.sap_model.PointObj.SetConstraint(center_pt, name)
        except Exception:
            return False

        for pt in circle_pts:
            if pt:
                try:
                    self.sap_model.PointObj.SetConstraint(pt, name)
                except Exception:
                    pass
        return True

    def _set_pin_restraint(self, point_name):
        try:
            value = [True, True, True, False, False, False]
            ret = self.sap_model.PointObj.SetRestraint(point_name, value)
            return _check_ret(ret)
        except Exception:
            return False

    def _create_single_chair(self, idx, cx, cy, z_level, circle_radius, inner_side, B_bolt, prop):
        chair_center = self._create_point(cx, cy, z_level, f"CHAIR_CENTER_{idx}")
        c_pts = self._create_circle_points(cx, cy, z_level, circle_radius, 16, f"CHAIR_c{idx}_")
        in_pts = self._create_square_points(cx, cy, z_level, inner_side, 16, f"CHAIR_sin{idx}_")
        out_pts = self._create_square_points(cx, cy, z_level, B_bolt, 16, f"CHAIR_sout{idx}_")
        self._create_ring_mesh(c_pts, in_pts, (cx, cy), f"CHAIR_ring_in{idx}", prop)
        self._create_ring_mesh(in_pts, out_pts, (cx, cy), f"CHAIR_ring_out{idx}", prop)
        return chair_center or f"CHAIR_CENTER_{idx}", c_pts, out_pts


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = PlacaBaseBackend(conn)
        config = PlacaBaseConfig()

        try:
            output = backend.run(config)
            import json
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
```

- [ ] Create file `scripts/placabase/gui_placabase.py` with the complete code below:

```python
"""
GUI — SAP2000 Placa Base Generator (Standalone)
=================================================
PySide6 interface for the parametric base plate backend.
Conexión directa vía comtypes (sin MCP).

Layout
------
  [Conectar]
  ── Inputs ─────────────────────────────────
     Pernos:    bolt_dia  n_pernos  bolt_material
     Columna:   H_col  B_col
     Espesores: plate  flange  web
     Silla:     [x] include  height  thickness
     Balasto:   ks_balasto
  ── ─────────────────────────────────────────
  [Ejecutar]
  ── Output ─────────────────────────────────
     log de texto con resultado / errores
  ── ─────────────────────────────────────────
  [Desconectar]
"""

import sys
import json

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QTextEdit,
)

from backend_placabase import SapConnection, PlacaBaseBackend, PlacaBaseConfig


# ══════════════════════════════════════════════════════════════════════════════
# Workers
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.connect(attach_to_existing=True)
        self.finished.emit(result)


class RunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: PlacaBaseBackend, config: PlacaBaseConfig):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            result = self._backend.run(self._config)
            self.finished.emit(result)
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.disconnect()
        self.finished.emit(result)


# ══════════════════════════════════════════════════════════════════════════════
# Helper
# ══════════════════════════════════════════════════════════════════════════════

def _field(label: str, default: str, tooltip: str = "") -> tuple:
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    edit = QLineEdit(default)
    edit.setMinimumWidth(90)
    if tooltip:
        edit.setToolTip(tooltip)
        lbl.setToolTip(tooltip)
    return lbl, edit


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class PlacaBaseGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Placa Base Generator")
        self.setMinimumWidth(660)

        self._conn = SapConnection()
        self._backend = PlacaBaseBackend(self._conn)
        self._worker = None

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Status ───────────────────────────────────────────────────────
        status_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        status_row.addWidget(self._status_lbl)
        status_row.addStretch()
        root.addLayout(status_row)

        # ── Botón Conectar ───────────────────────────────────────────────
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)
        root.addWidget(self._btn_connect)

        # ── Inputs ───────────────────────────────────────────────────────
        inputs_box = QGroupBox("Parámetros de entrada")
        grid = QGridLayout(inputs_box)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        def _header(text: str, row: int):
            lbl = QLabel(f"<b>{text}</b>")
            grid.addWidget(lbl, row, 0, 1, 4)

        r = 0

        # Pernos
        _header("Pernos de Anclaje", r); r += 1

        lbl, self._bolt_dia = _field("Diámetro [mm]", "25.0", "Diámetro del perno")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._bolt_dia, r, 1)
        lbl, self._n_pernos = _field("n_pernos", "4", "Número de pernos (par)")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._n_pernos, r, 3)
        r += 1

        lbl, self._bolt_material = _field("Material", "A36", "Material de los pernos")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._bolt_material, r, 1)
        r += 1

        # Columna
        _header("Dimensiones de Columna [mm]", r); r += 1

        lbl, self._H_col = _field("H_col", "300.0", "Altura de la sección")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._H_col, r, 1)
        lbl, self._B_col = _field("B_col", "250.0", "Ancho de la sección")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._B_col, r, 3)
        r += 1

        # Espesores
        _header("Espesores [mm]", r); r += 1

        lbl, self._plate_t = _field("Placa base", "20.0", "Espesor de placa base")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._plate_t, r, 1)
        lbl, self._flange_t = _field("Ala", "15.0", "Espesor de alas")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._flange_t, r, 3)
        r += 1

        lbl, self._web_t = _field("Alma", "10.0", "Espesor de alma")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._web_t, r, 1)
        r += 1

        # Silla de anclaje
        _header("Silla de Anclaje", r); r += 1

        self._chk_chair = QCheckBox("Incluir silla de anclaje")
        grid.addWidget(self._chk_chair, r, 0, 1, 2)
        r += 1

        lbl, self._chair_height = _field("Altura [mm]", "50.0", "Altura de la silla")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._chair_height, r, 1)
        lbl, self._chair_thick = _field("Espesor [mm]", "15.0", "Espesor de la silla")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._chair_thick, r, 3)
        r += 1

        # Balasto
        _header("Módulo de Balasto", r); r += 1

        lbl, self._ks = _field("ks [kgf/cm³]", "5.0", "Módulo de balasto (0 = omitir)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._ks, r, 1)
        r += 1

        root.addWidget(inputs_box)

        # ── Botón Ejecutar ───────────────────────────────────────────────
        self._btn_run = QPushButton("Ejecutar")
        self._btn_run.setFixedHeight(34)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Output log ───────────────────────────────────────────────────
        output_box = QGroupBox("Salida")
        out_layout = QVBoxLayout(output_box)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(200)
        out_layout.addWidget(self._log)
        root.addWidget(output_box)

        # ── Botón Desconectar ────────────────────────────────────────────
        self._btn_disconnect = QPushButton("Desconectar de SAP2000")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        root.addWidget(self._btn_disconnect)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_run.setEnabled(connected)
        self._btn_disconnect.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")

    def _log_append(self, text: str):
        self._log.append(text)

    def _busy(self, is_busy: bool):
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_run.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)

    def _build_config(self) -> PlacaBaseConfig:
        return PlacaBaseConfig(
            bolt_dia=float(self._bolt_dia.text()),
            bolt_material=self._bolt_material.text(),
            n_pernos=int(self._n_pernos.text()),
            H_col=float(self._H_col.text()),
            B_col=float(self._B_col.text()),
            plate_thickness=float(self._plate_t.text()),
            flange_thickness=float(self._flange_t.text()),
            web_thickness=float(self._web_t.text()),
            include_anchor_chair=self._chk_chair.isChecked(),
            anchor_chair_height=float(self._chair_height.text()),
            anchor_chair_thickness=float(self._chair_thick.text()),
            ks_balasto=float(self._ks.text()),
        )

    # ── Conectar ─────────────────────────────────────────────────────────

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            self._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._set_connected(True)
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    # ── Ejecutar ─────────────────────────────────────────────────────────

    def _on_run(self):
        try:
            config = self._build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return

        self._log_append("\n─── Ejecutando ─────────────────────────────────────")
        self._busy(True)
        self._worker = RunWorker(self._backend, config)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Placa base generada exitosamente")
            self._log_append(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ Error: {err}")

    # ── Desconectar ──────────────────────────────────────────────────────

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._busy(False)
        self._log_append("✔ Desconectado de SAP2000")
        self._set_connected(False)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = PlacaBaseGUI()
    win.show()
    sys.exit(app.exec())
```

- [ ] Delete the old `scripts/placabase_backend.py`:
```powershell
Remove-Item "scripts/placabase_backend.py"
```

- [ ] Verify syntax of both new files:
```powershell
python -c "import ast, pathlib; ast.parse(pathlib.Path('scripts/placabase/backend_placabase.py').read_text(encoding='utf-8')); print('backend OK')"
python -c "import ast, pathlib; ast.parse(pathlib.Path('scripts/placabase/gui_placabase.py').read_text(encoding='utf-8')); print('gui OK')"
```

- [ ] Verify no MCP/external imports:
```powershell
python -c "
for f in ['scripts/placabase/backend_placabase.py', 'scripts/placabase/gui_placabase.py']:
    t = open(f, encoding='utf-8').read()
    for bad in ['sap_bridge', 'sap_executor', 'mcp_server', 'app_logger', 'sap_utils_common']:
        assert bad not in t, f'{bad} found in {f}'
print('no forbidden imports ✔')
"
```

##### Step 5b Verification Checklist
- [ ] `scripts/placabase/backend_placabase.py` exists with `SapConnection`, `PlacaBaseConfig`, `PlacaBaseBackend`
- [ ] `scripts/placabase/gui_placabase.py` exists with `PlacaBaseGUI`, 3 workers, QCheckBox for anchor chair
- [ ] `scripts/placabase_backend.py` is deleted
- [ ] Both files pass `ast.parse`
- [ ] No imports from `mcp_server`, `sap_bridge`, `sap_executor`, `app_logger`, `sap_utils_common`
- [ ] Backend uses `comtypes.client` for connection
- [ ] Backend `run()` logic replicates the full placabase process (8 tasks)
- [ ] inline `_check_ret` and `_get_name` replace `check_ret_code` from `sap_utils_common`

#### Step 5b STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 6: Update SKILL.md and copilot-instructions.md

- [ ] Open `.github/skills/sap2000-api/SKILL.md`
- [ ] Find the existing step 9 in the "Mandatory Workflow" section:

```markdown
9. **Register new functions** — For any new API functions not yet in the
```

- [ ] After step 9, add step 10. Insert the following **after** the paragraph ending with "...adds richer documentation.":

```markdown
10. **Offer GUI generation** — After delivering a verified script, ask:
   *"¿Quieres generar una GUI standalone (PySide6) para este script?"*
   If yes, follow Phase 6 of the workflow in `plans/workflow-script-creation.md`.
   The GUI uses `comtypes.client` for direct COM connection (no MCP dependency)
   and follows the templates in `scripts/templates/`.
```

- [ ] At the end of the `SKILL.md` file (before the `## Reference Files` section), add the following new section:

```markdown

## GUI Standalone Pattern

Verified scripts can optionally be converted to standalone GUIs (PySide6 + COM direct).
These GUIs do NOT depend on the MCP server — they connect directly to SAP2000 via `comtypes`.

### Structure

```
scripts/{nombre}/
    gui_{nombre}.py         # PySide6 GUI (imports backend)
    backend_{nombre}.py     # SAP2000 logic via comtypes.client
```

### Backend Pattern

```python
import comtypes.client

class SapConnection:
    def connect(self, attach_to_existing=True) -> dict: ...
    def disconnect(self) -> dict: ...
    @property
    def is_connected(self) -> bool: ...

class MyBackend:
    def __init__(self, connection: SapConnection): ...
    def run(self, config) -> dict: ...  # Returns result dict
```

### Templates

- `scripts/templates/backend_template.py` — Backend base
- `scripts/templates/gui_template.py` — GUI base

### Workflow

See **Phase 6** in `plans/workflow-script-creation.md` for the complete
step-by-step process to generate a GUI from a verified script.

```

- [ ] Open `.github/copilot-instructions.md`
- [ ] At the end of the file (after the `### Requirements` section), add:

```markdown

### GUI Standalone Generation

The agent can also generate **standalone GUIs** (PySide6 + direct COM) from
verified scripts. These GUIs do NOT depend on the MCP server.

**When to offer:**
- After a script has been successfully verified and saved
- When the user asks for a "GUI", "standalone app", or "desktop tool"

**Structure:** `scripts/{nombre}/gui_{nombre}.py` + `backend_{nombre}.py`

**Templates:** See `scripts/templates/` for base templates.

**Workflow:** See Phase 6 in `plans/workflow-script-creation.md`.
```

##### Step 6 Verification Checklist
- [ ] `SKILL.md` has step 10 in Mandatory Workflow (Offer GUI generation)
- [ ] `SKILL.md` has new `## GUI Standalone Pattern` section before Reference Files
- [ ] `copilot-instructions.md` has new `### GUI Standalone Generation` section
- [ ] All file references (templates, workflow) are correct
- [ ] No contradictions with existing content

#### Step 6 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

## Final Structure

After all steps are complete, the workspace should look like:

```
scripts/
  templates/                          # NEW (Step 1-2)
    backend_template.py
    gui_template.py

  ring_areas/                         # NEW (Step 5a)
    gui_ring_areas.py                 # Standalone — no MCP
    backend_ring_areas.py             # COM directo

  placabase/                          # NEW (Step 5b)
    gui_placabase.py                  # Standalone — no MCP
    backend_placabase.py              # COM directo — no app_logger

  example_ring_areas_parametric.py    # MOVED (Step 5a, from ring_areas_parametric/)
  example_1001_simple_beam.py         # Unchanged
  example_placabase_parametric.py     # Unchanged

  # DELETED:
  # ring_areas_parametric/            # Old folder (Step 5a)
  # placabase_backend.py              # Old file (Step 5b)

plans/
  workflow-script-creation.md         # MODIFIED (Step 3 — Phase 6 added)
  quick-reference-workflow.md         # MODIFIED (Step 4 — GUI section added)
  workflow-two-phase/
    plan.md                           # Unchanged (source plan)
    implementation.md                 # This file

.github/
  skills/sap2000-api/SKILL.md        # MODIFIED (Step 6 — step 10 + GUI section)
  copilot-instructions.md             # MODIFIED (Step 6 — GUI section)
```
