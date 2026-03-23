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
