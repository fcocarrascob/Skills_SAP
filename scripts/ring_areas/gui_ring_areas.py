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

    def _format_result(self, data: dict) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False)

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
            self._log_append(self._format_result(result))
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
