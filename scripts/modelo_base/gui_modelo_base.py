"""
GUI — SAP2000 Modelo Base Generator (Standalone)
==================================================
PySide6 interface for the base model backend.
Conexión directa vía comtypes (sin MCP).

Layout
------
  [Conectar]
  ── Inputs ─────────────────────────────────
     Generales: Zona sísmica, Tipo suelo, Factor I
     Horizontal: ξx, Rx, ξy, Ry
     Vertical:   ξv, Rv
  ── ─────────────────────────────────────────
  [Vista Previa Espectro]  [Ejecutar]
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
    QComboBox,
    QPushButton,
    QTextEdit,
    QDialog,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)

try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from backend_modelo_base import (
    SapConnection, BaseModelBackend, BaseModelConfig,
    compute_nch_spectrum, compute_vertical_spectrum,
)
from config import AR_BY_ZONE, SOIL_PARAMS


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

    def __init__(self, backend: BaseModelBackend, config: BaseModelConfig):
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
# Diálogo de Vista Previa del Espectro
# ══════════════════════════════════════════════════════════════════════════════

class SpectrumPreviewDialog(QDialog):
    """Diálogo emergente con gráfico y tabla del espectro NCh2369."""

    def __init__(self, parent=None, data=None, params_text=""):
        super().__init__(parent)
        self.setWindowTitle("Vista Previa — Espectro NCh2369:2025")
        self.resize(1100, 650)
        self.setModal(True)
        self.data = data or {}
        self.params_text = params_text
        self._init_ui()
        self._plot_data()
        self._fill_table()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # ── Panel izquierdo (parámetros + tabla) ─────────────────────────
        left = QWidget()
        left_layout = QVBoxLayout(left)

        grp_params = QGroupBox("Parámetros Definidos")
        grp_lay = QVBoxLayout(grp_params)
        lbl = QLabel(self.params_text)
        lbl.setWordWrap(True)
        lbl.setStyleSheet("font-family: Consolas; font-size: 11px;")
        grp_lay.addWidget(lbl)
        left_layout.addWidget(grp_params)

        self._table = QTableWidget()
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(["T [s]", "Sa X [g]", "Sa Y [g]", "Sa V [g]"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        left_layout.addWidget(self._table)

        splitter.addWidget(left)

        # ── Panel derecho (gráfico) ──────────────────────────────────────
        right = QWidget()
        right_layout = QVBoxLayout(right)

        if MATPLOTLIB_AVAILABLE:
            self._figure = Figure(figsize=(6, 5), dpi=100)
            self._canvas = FigureCanvas(self._figure)
            self._toolbar = NavigationToolbar(self._canvas, self)
            right_layout.addWidget(self._toolbar)
            right_layout.addWidget(self._canvas)
        else:
            right_layout.addWidget(QLabel("Matplotlib no disponible."))

        splitter.addWidget(right)
        splitter.setSizes([350, 650])

        # Botón cerrar
        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(self.close)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)

    def _plot_data(self):
        if not MATPLOTLIB_AVAILABLE or not self.data:
            return

        T = self.data.get("T", [])
        Sax = self.data.get("Sax", [])
        Say = self.data.get("Say", [])
        Sav = self.data.get("Sav", [])

        ax = self._figure.add_subplot(111)
        ax.grid(True, linestyle="--", alpha=0.6)

        if Sax:
            ax.plot(T, Sax, "b-", linewidth=1.5,
                    label=f"Horizontal X (R={self.data.get('Rx', 0)})")
        if Say and self.data.get("has_y"):
            ax.plot(T, Say, "g-.", linewidth=1.5,
                    label=f"Horizontal Y (R={self.data.get('Ry', 0)})")
        if Sav:
            ax.plot(T, Sav, "r--", linewidth=1.5,
                    label=f"Vertical (R={self.data.get('Rv', 0)})")

        ax.set_xlabel("Período T [s]")
        ax.set_ylabel("Aceleración Espectral Sa [g]")
        ax.set_title("Espectro de Diseño NCh2369:2025")
        ax.legend()
        self._canvas.draw()

    def _fill_table(self):
        T = self.data.get("T", [])
        if not T:
            return

        Sax = self.data.get("Sax", [])
        Say = self.data.get("Say", [])
        Sav = self.data.get("Sav", [])

        self._table.setRowCount(len(T))
        self._table.setUpdatesEnabled(False)
        try:
            for i, t_val in enumerate(T):
                self._table.setItem(i, 0, self._centered_item(f"{t_val:.3f}"))
                self._table.setItem(i, 1, self._centered_item(
                    f"{Sax[i]:.4f}" if i < len(Sax) else ""))
                self._table.setItem(i, 2, self._centered_item(
                    f"{Say[i]:.4f}" if i < len(Say) else ""))
                self._table.setItem(i, 3, self._centered_item(
                    f"{Sav[i]:.4f}" if i < len(Sav) else ""))
        finally:
            self._table.setUpdatesEnabled(True)

    @staticmethod
    def _centered_item(text: str) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class ModeloBaseGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Modelo Base Generator")
        self.setMinimumWidth(700)

        self._conn = SapConnection()
        self._backend = BaseModelBackend(self._conn)
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
        inputs_box = QGroupBox("Parámetros del Modelo Base")
        grid = QGridLayout(inputs_box)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        def _header(text: str, row: int):
            lbl = QLabel(f"<b>{text}</b>")
            grid.addWidget(lbl, row, 0, 1, 4)

        r = 0

        # Generales
        _header("Parámetros Generales", r); r += 1

        grid.addWidget(QLabel("Zona Sísmica:"), r, 0)
        self._combo_zone = QComboBox()
        self._combo_zone.addItems(["1", "2", "3"])
        self._combo_zone.setCurrentIndex(1)  # default: zona 2
        grid.addWidget(self._combo_zone, r, 1)

        grid.addWidget(QLabel("Tipo de Suelo:"), r, 2)
        self._combo_soil = QComboBox()
        self._combo_soil.addItems(["A", "B", "C", "D", "E"])
        self._combo_soil.setCurrentIndex(2)  # default: C
        grid.addWidget(self._combo_soil, r, 3)
        r += 1

        lbl, self._importance = _field("Factor I", "1.0", "Factor de importancia")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._importance, r, 1)
        r += 1

        # Horizontal
        _header("Parámetros Horizontales", r); r += 1

        lbl, self._damp_x = _field("ξx", "0.03", "Amortiguamiento X (ej. 0.03 = 3%)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._damp_x, r, 1)
        lbl, self._R_x = _field("Rx", "3.0", "Factor de reducción R — dirección X")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._R_x, r, 3)
        r += 1

        lbl, self._damp_y = _field("ξy", "0.03", "Amortiguamiento Y (ej. 0.03 = 3%)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._damp_y, r, 1)
        lbl, self._R_y = _field("Ry", "3.0", "Factor de reducción R — dirección Y")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._R_y, r, 3)
        r += 1

        # Vertical
        _header("Parámetros Verticales", r); r += 1

        lbl, self._damp_v = _field("ξv", "0.03", "Amortiguamiento vertical")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._damp_v, r, 1)
        lbl, self._R_v = _field("Rv", "2.0", "Factor de reducción R vertical")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._R_v, r, 3)
        r += 1

        root.addWidget(inputs_box)

        # ── Botones ──────────────────────────────────────────────────────
        btn_row = QHBoxLayout()

        self._btn_preview = QPushButton("Vista Previa Espectro")
        self._btn_preview.setFixedHeight(34)
        self._btn_preview.setEnabled(MATPLOTLIB_AVAILABLE)
        if not MATPLOTLIB_AVAILABLE:
            self._btn_preview.setToolTip("pip install matplotlib para habilitar")
        else:
            self._btn_preview.clicked.connect(self._on_preview)
        btn_row.addWidget(self._btn_preview)

        self._btn_run = QPushButton("Crear Modelo Base")
        self._btn_run.setFixedHeight(34)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        btn_row.addWidget(self._btn_run)

        root.addLayout(btn_row)

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
    # Helpers
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
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_run.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)

    def _build_config(self) -> BaseModelConfig:
        return BaseModelConfig(
            zone=int(self._combo_zone.currentText()),
            soil=self._combo_soil.currentText(),
            importance=float(self._importance.text()),
            r_x=float(self._R_x.text()),
            r_y=float(self._R_y.text()),
            damping_x=float(self._damp_x.text()),
            damping_y=float(self._damp_y.text()),
            r_v=float(self._R_v.text()),
            xi_v=float(self._damp_v.text()),
        )

    def _format_result(self, data: dict) -> str:
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

        self._log_append("\n─── Creando modelo base ────────────────────────────")
        self._busy(True)
        self._worker = RunWorker(self._backend, config)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Modelo base creado exitosamente")
            self._log_append(result.get("summary", ""))
            if result.get("errors"):
                self._log_append("Advertencias:")
                for e in result["errors"]:
                    self._log_append(f"  ⚠ {e}")
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ Error: {err}")

    # ══════════════════════════════════════════════════════════════════════
    # Vista Previa Espectro
    # ══════════════════════════════════════════════════════════════════════

    def _on_preview(self):
        if not MATPLOTLIB_AVAILABLE:
            return

        try:
            config = self._build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return

        # Calcular espectros (reutiliza funciones del backend — sin SAP2000)
        T_x, Sa_x = compute_nch_spectrum(
            config.zone, config.soil, config.importance,
            config.r_x, config.damping_x
        )
        T_y, Sa_y = compute_nch_spectrum(
            config.zone, config.soil, config.importance,
            config.r_y, config.damping_y
        )
        T_v, Sa_v = compute_vertical_spectrum(
            config.zone, config.soil, config.importance,
            config.r_v, config.xi_v
        )

        has_y = (abs(config.r_x - config.r_y) > 0.01
                 or abs(config.damping_x - config.damping_y) > 0.001)

        data = {
            "T": T_x, "Sax": Sa_x, "Say": Sa_y, "Sav": Sa_v,
            "Rx": config.r_x, "Ry": config.r_y, "Rv": config.r_v,
            "has_y": has_y,
        }

        params_text = (
            f"Zona Sísmica: {config.zone}\n"
            f"Suelo: {config.soil}\n"
            f"I: {config.importance:.2f}\n\n"
            f"H-X: Rx={config.r_x}, ξ={config.damping_x}\n"
            f"H-Y: Ry={config.r_y}, ξ={config.damping_y}\n"
            f"Vert: Rv={config.r_v}, ξ={config.xi_v}"
        )

        dlg = SpectrumPreviewDialog(self, data, params_text)
        dlg.exec()

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
    win = ModeloBaseGUI()
    win.show()
    sys.exit(app.exec())
