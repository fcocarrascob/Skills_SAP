# NOTA: Este template es para GUI standalone con COM directo,
# NO para scripts ejecutados vía MCP sandbox (run_sap_script).
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
