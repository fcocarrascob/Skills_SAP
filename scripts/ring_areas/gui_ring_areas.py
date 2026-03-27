"""
GUI — SAP2000 Ring Areas & Cylinder Generator (Standalone)
==========================================================
PySide6 interface with two tabs:
  • Anillo   — placa anular con 3 zonas concéntricas (backend_ring_areas)
  • Cilindro — cilindro vertical discretizado       (backend_cylinder)

Conexión directa vía comtypes (sin MCP).
Barra de conexión, log y botón de desconexión compartidos entre pestañas.
"""

import sys
import json

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from backend_ring_areas import SapConnection, RingAreasBackend, RingAreasConfig
from backend_cylinder import CylinderBackend, CylinderConfig


# ══════════════════════════════════════════════════════════════════════════════
# Workers — operaciones SAP2000 fuera del hilo GUI
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.connect(attach_to_existing=True))


class GetMaterialsWorker(QThread):
    finished = Signal(list)

    def __init__(self, backend):
        super().__init__()
        self._backend = backend

    def run(self):
        try:
            self.finished.emit(self._backend.get_materials())
        except Exception:
            self.finished.emit([])


class RunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend, config):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            self.finished.emit(self._backend.run(self._config))
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.disconnect())


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
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


def _mat_label_combo(grid, row: int) -> QComboBox:
    lbl = QLabel("Material")
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    grid.addWidget(lbl, row, 0)
    cb = QComboBox()
    cb.setEnabled(False)
    cb.setToolTip("Materiales disponibles en el modelo — se cargan al conectar")
    grid.addWidget(cb, row, 1, 1, 3)
    return cb


# ══════════════════════════════════════════════════════════════════════════════
# Tab: Anillo
# ══════════════════════════════════════════════════════════════════════════════

class RingAreasTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

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
        self.mat_combo = _mat_label_combo(grid, r)
        r += 1

        # Discretización
        _header("Discretización", r); r += 1
        lbl, self._n_segs = _field("n_segs", "36", "Segmentos angulares (≥ 12 recomendado)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._n_segs, r, 1)

        layout.addWidget(inputs_box)

        self.btn_run = QPushButton("Ejecutar — Anillo")
        self.btn_run.setFixedHeight(34)
        self.btn_run.setEnabled(False)
        layout.addWidget(self.btn_run)
        layout.addStretch()

    def build_config(self) -> RingAreasConfig:
        return RingAreasConfig(
            r_inner=float(self._r_inner.text()),
            r_mid1=float(self._r_mid1.text()),
            r_mid2=float(self._r_mid2.text()),
            r_outer=float(self._r_outer.text()),
            t1=float(self._t1.text()),
            t2=float(self._t2.text()),
            mat_name=self.mat_combo.currentText(),
            n_segs=int(self._n_segs.text()),
        )

    def populate_materials(self, materials: list):
        self.mat_combo.clear()
        self.mat_combo.addItems(materials)
        self.mat_combo.setEnabled(bool(materials))

    def clear_materials(self):
        self.mat_combo.clear()
        self.mat_combo.setEnabled(False)


# ══════════════════════════════════════════════════════════════════════════════
# Tab: Cilindro
# ══════════════════════════════════════════════════════════════════════════════

class CylinderTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        inputs_box = QGroupBox("Parámetros de entrada")
        grid = QGridLayout(inputs_box)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        def _header(text: str, row: int):
            lbl = QLabel(f"<b>{text}</b>")
            grid.addWidget(lbl, row, 0, 1, 4)

        r = 0

        # Geometría
        _header("Geometría [m]", r); r += 1
        lbl, self._radius = _field("Radio", "5.0", "Radio del cilindro")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._radius, r, 1)
        lbl, self._height = _field("Altura", "10.0", "Altura total del cilindro")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._height, r, 3)
        r += 1

        # Espesor
        _header("Espesor de shell [m]", r); r += 1
        lbl, self._thickness = _field("t", "0.25", "Espesor de la pared del cilindro")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._thickness, r, 1)
        r += 1

        # Material
        _header("Material", r); r += 1
        self.mat_combo = _mat_label_combo(grid, r)
        r += 1

        # Discretización
        _header("Discretización", r); r += 1
        lbl, self._n_radial = _field("n_radial", "36", "Segmentos angulares – circunferencia (≥ 12)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._n_radial, r, 1)
        lbl, self._n_vert = _field("n_vert", "10", "Divisiones verticales")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._n_vert, r, 3)

        layout.addWidget(inputs_box)

        self.btn_run = QPushButton("Ejecutar — Cilindro")
        self.btn_run.setFixedHeight(34)
        self.btn_run.setEnabled(False)
        layout.addWidget(self.btn_run)
        layout.addStretch()

    def build_config(self) -> CylinderConfig:
        return CylinderConfig(
            radius=float(self._radius.text()),
            height=float(self._height.text()),
            thickness=float(self._thickness.text()),
            mat_name=self.mat_combo.currentText(),
            n_radial=int(self._n_radial.text()),
            n_vert=int(self._n_vert.text()),
        )

    def populate_materials(self, materials: list):
        self.mat_combo.clear()
        self.mat_combo.addItems(materials)
        self.mat_combo.setEnabled(bool(materials))

    def clear_materials(self):
        self.mat_combo.clear()
        self.mat_combo.setEnabled(False)


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class SAP2000GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Ring Areas & Cylinder Generator")
        self.setMinimumWidth(640)

        self._conn    = SapConnection()
        self._ring_be = RingAreasBackend(self._conn)
        self._cyl_be  = CylinderBackend(self._conn)
        self._worker  = None

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Status ───────────────────────────────────────────────────────
        top_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        top_row.addWidget(self._status_lbl)
        top_row.addStretch()
        root.addLayout(top_row)

        # ── Botón Conectar ───────────────────────────────────────────────
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)
        root.addWidget(self._btn_connect)

        # ── Pestañas ─────────────────────────────────────────────────────
        self._tabs     = QTabWidget()
        self._ring_tab = RingAreasTab()
        self._cyl_tab  = CylinderTab()
        self._tabs.addTab(self._ring_tab, "Anillo")
        self._tabs.addTab(self._cyl_tab,  "Cilindro")
        self._ring_tab.btn_run.clicked.connect(self._on_ring_run)
        self._cyl_tab.btn_run.clicked.connect(self._on_cyl_run)
        root.addWidget(self._tabs)

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
        self._btn_disconnect.setEnabled(connected)
        self._ring_tab.btn_run.setEnabled(connected)
        self._cyl_tab.btn_run.setEnabled(connected)
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
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)
        self._ring_tab.btn_run.setEnabled(not is_busy and self._conn.is_connected)
        self._cyl_tab.btn_run.setEnabled(not is_busy and self._conn.is_connected)

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
            ver  = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            self._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._set_connected(True)
            self._busy(True)
            self._log_append("Obteniendo materiales del modelo...")
            self._worker = GetMaterialsWorker(self._ring_be)
            self._worker.finished.connect(self._on_materials_done)
            self._worker.start()
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    def _on_materials_done(self, materials: list):
        self._busy(False)
        self._ring_tab.populate_materials(materials)
        self._cyl_tab.populate_materials(materials)
        if materials:
            self._log_append(f"  Materiales disponibles: {', '.join(materials)}")
        else:
            self._log_append("  ⚠ No se encontraron materiales en el modelo.")

    # ── Ejecutar — Anillo ─────────────────────────────────────────────────

    def _on_ring_run(self):
        try:
            config = self._ring_tab.build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return
        self._log_append("\n─── Ejecutando script — Anillo ──────────────────────")
        self._busy(True)
        self._worker = RunWorker(self._ring_be, config)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    # ── Ejecutar — Cilindro ───────────────────────────────────────────────

    def _on_cyl_run(self):
        try:
            config = self._cyl_tab.build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return
        self._log_append("\n─── Ejecutando script — Cilindro ────────────────────")
        self._busy(True)
        self._worker = RunWorker(self._cyl_be, config)
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
        self._ring_tab.clear_materials()
        self._cyl_tab.clear_materials()
        self._log_append("✔ Desconectado de SAP2000")
        self._set_connected(False)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = SAP2000GUI()
    win.show()
    sys.exit(app.exec())
