"""
GUI Standalone — Fundaciones SAP2000
=====================================
Interfaz para crear secciones de pedestal/losa y modelar fundaciones
directamente contra SAP2000 vía COM.

Uso:
    python -m fundaciones.gui_fundaciones
    python scripts/fundaciones/gui_fundaciones.py
"""

import sys
import re
import json

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QTextEdit,
    QComboBox, QTabWidget, QFormLayout, QScrollArea,
)

from backend_fundaciones import (
    SapConnection, FundacionesBackend,
    PedestalSectionConfig, LosaSectionConfig, FundacionConfig,
)


# ══════════════════════════════════════════════════════════════════════════════
# Workers
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, conn: SapConnection):
        super().__init__()
        self._conn = conn

    def run(self):
        self.finished.emit(self._conn.connect(attach_to_existing=True))


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, conn: SapConnection):
        super().__init__()
        self._conn = conn

    def run(self):
        self.finished.emit(self._conn.disconnect())


class LoadDataWorker(QThread):
    """Carga materiales y secciones del modelo en background."""
    finished = Signal(dict)

    def __init__(self, backend: FundacionesBackend):
        super().__init__()
        self._b = backend

    def run(self):
        try:
            self.finished.emit({
                "concrete": self._b.get_concrete_materials(),
                "rebar_mats": self._b.get_rebar_materials(),
                "rebar_sizes": self._b.get_rebar_sizes(),
                "frames": self._b.get_frame_sections(),
                "shells": self._b.get_shell_sections(),
            })
        except Exception as exc:
            self.finished.emit({"error": str(exc)})


class CreatePedestalWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: FundacionesBackend, cfg: PedestalSectionConfig):
        super().__init__()
        self._b = backend
        self._cfg = cfg

    def run(self):
        self.finished.emit(self._b.create_pedestal_section(self._cfg))


class CreateLosaWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: FundacionesBackend, cfg: LosaSectionConfig):
        super().__init__()
        self._b = backend
        self._cfg = cfg

    def run(self):
        self.finished.emit(self._b.create_losa_sections(cfg=self._cfg))


class ModelarWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: FundacionesBackend, cfg: FundacionConfig):
        super().__init__()
        self._b = backend
        self._cfg = cfg

    def run(self):
        self.finished.emit(self._b.model_foundation(self._cfg))


class FetchCoordsWorker(QThread):
    finished = Signal(object)

    def __init__(self, backend: FundacionesBackend):
        super().__init__()
        self._b = backend

    def run(self):
        self.finished.emit(self._b.get_selected_point_coords())


# ══════════════════════════════════════════════════════════════════════════════
# Helpers UI
# ══════════════════════════════════════════════════════════════════════════════

def _field(label: str, default: str, tooltip: str = "", width: int = 80):
    """Par (QLabel, QLineEdit) para usar en layouts."""
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    edit = QLineEdit(default)
    edit.setMaximumWidth(width)
    if tooltip:
        edit.setToolTip(tooltip)
        lbl.setToolTip(tooltip)
    return lbl, edit


def _combo_row(label: str, tooltip: str = ""):
    """Par (QLabel, QComboBox) editable."""
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    cb = QComboBox()
    cb.setEditable(True)
    cb.setMinimumWidth(140)
    if tooltip:
        cb.setToolTip(tooltip)
        lbl.setToolTip(tooltip)
    return lbl, cb


def _reload_btn(tooltip: str = "Actualizar desde SAP2000") -> QPushButton:
    btn = QPushButton("↺")
    btn.setFixedSize(28, 28)
    btn.setToolTip(tooltip)
    btn.setEnabled(False)
    return btn


# ══════════════════════════════════════════════════════════════════════════════
# Ventana principal
# ══════════════════════════════════════════════════════════════════════════════

class FundacionesGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Fundaciones")
        self.setMinimumWidth(680)

        self._conn = SapConnection()
        self._backend = FundacionesBackend(self._conn)
        self._worker = None

        root = QVBoxLayout(self)
        root.setSpacing(8)
        root.setContentsMargins(10, 10, 10, 10)

        # ── Barra de estado + conexión ────────────────────────────────────
        top_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        top_row.addWidget(self._status_lbl)
        top_row.addStretch()
        self._btn_connect = QPushButton("Conectar")
        self._btn_connect.setFixedHeight(30)
        self._btn_connect.clicked.connect(self._on_connect)
        top_row.addWidget(self._btn_connect)
        self._btn_reload_all = QPushButton("↺ Cargar datos")
        self._btn_reload_all.setFixedHeight(30)
        self._btn_reload_all.setEnabled(False)
        self._btn_reload_all.setToolTip("Recargar materiales y secciones desde SAP2000")
        self._btn_reload_all.clicked.connect(self._on_load_data)
        top_row.addWidget(self._btn_reload_all)
        self._btn_disconnect = QPushButton("Desconectar")
        self._btn_disconnect.setFixedHeight(30)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        top_row.addWidget(self._btn_disconnect)
        root.addLayout(top_row)

        # ── Tabs ──────────────────────────────────────────────────────────
        self._tabs = QTabWidget()
        root.addWidget(self._tabs)

        self._tabs.addTab(self._build_tab_definiciones(), "📋 Definiciones")
        self._tabs.addTab(self._build_tab_modelar(), "🏗️ Modelar")

        # ── Log ───────────────────────────────────────────────────────────
        log_box = QGroupBox("Log")
        log_layout = QVBoxLayout(log_box)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setFixedHeight(130)
        log_layout.addWidget(self._log)
        root.addWidget(log_box)

        self._log_append("Módulo de Fundaciones listo.")

    # ══════════════════════════════════════════════════════════════════════
    # Construcción de tabs
    # ══════════════════════════════════════════════════════════════════════

    def _build_tab_definiciones(self) -> QWidget:
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(12)
        layout.setContentsMargins(6, 6, 6, 6)

        # ── Materiales compartidos ────────────────────────────────────────
        grp_mat = QGroupBox("Materiales")
        form_mat = QFormLayout(grp_mat)
        form_mat.setVerticalSpacing(6)

        row_conc = QHBoxLayout()
        _, self._cb_concrete = _combo_row("", "Material de hormigón")
        self._cb_concrete.addItem("-- Sin conexión --")
        row_conc.addWidget(self._cb_concrete)
        row_conc.addStretch()
        form_mat.addRow("Hormigón:", row_conc)

        row_rebar = QHBoxLayout()
        _, self._cb_rebar_mat = _combo_row("", "Material de acero de refuerzo")
        self._cb_rebar_mat.addItem("-- Sin conexión --")
        row_rebar.addWidget(self._cb_rebar_mat)
        row_rebar.addStretch()
        form_mat.addRow("Acero refuerzo:", row_rebar)

        layout.addWidget(grp_mat)

        # ── Sección pedestal ──────────────────────────────────────────────
        grp_ped = QGroupBox("Crear Sección Pedestal (Section Designer)")
        form_ped = QFormLayout(grp_ped)
        form_ped.setVerticalSpacing(6)

        dims_row = QHBoxLayout()
        _, self._ped_width = _field("Ancho Y (mm):", "500", "Dimensión Y global")
        _, self._ped_height = _field("Alto X (mm):", "500", "Dimensión X global")
        dims_row.addWidget(QLabel("Y:"))
        dims_row.addWidget(self._ped_width)
        dims_row.addSpacing(10)
        dims_row.addWidget(QLabel("X:"))
        dims_row.addWidget(self._ped_height)
        dims_row.addStretch()
        form_ped.addRow("Dimensiones:", dims_row)

        self._ped_name = QLineEdit("PED_500x500")
        self._ped_name.setReadOnly(True)
        self._ped_name.setMaximumWidth(150)
        self._ped_name.setToolTip("Nombre auto-generado")
        form_ped.addRow("Nombre:", self._ped_name)

        bar_row_corner = QHBoxLayout()
        _, self._cb_corner_bars = _combo_row("", "Barras en esquinas")
        self._cb_corner_bars.addItems(["12mm", "16mm", "20mm", "25mm", "#6", "#8", "#10"])
        self._cb_corner_bars.setCurrentText("16mm")
        bar_row_corner.addWidget(self._cb_corner_bars)
        bar_row_corner.addStretch()
        form_ped.addRow("Barras esquinas:", bar_row_corner)

        bar_row_edge = QHBoxLayout()
        _, self._cb_edge_bars = _combo_row("", "Barras distribuidas en bordes")
        self._cb_edge_bars.addItems(["12mm", "16mm", "20mm", "25mm", "#6", "#8", "#10"])
        self._cb_edge_bars.setCurrentText("12mm")
        bar_row_edge.addWidget(self._cb_edge_bars)
        bar_row_edge.addStretch()
        form_ped.addRow("Barras bordes:", bar_row_edge)

        reinf_row = QHBoxLayout()
        _, self._ped_spacing = _field("", "150", "Espaciamiento centro-a-centro (mm)")
        _, self._ped_cover = _field("", "50", "Recubrimiento libre (mm)")
        reinf_row.addWidget(QLabel("Esp:"))
        reinf_row.addWidget(self._ped_spacing)
        reinf_row.addWidget(QLabel("mm"))
        reinf_row.addSpacing(10)
        reinf_row.addWidget(QLabel("Recub:"))
        reinf_row.addWidget(self._ped_cover)
        reinf_row.addWidget(QLabel("mm"))
        reinf_row.addStretch()
        form_ped.addRow("Refuerzo:", reinf_row)

        self._btn_create_ped = QPushButton("✨ Crear sección pedestal")
        self._btn_create_ped.setFixedHeight(30)
        self._btn_create_ped.setEnabled(False)
        self._btn_create_ped.clicked.connect(self._on_create_pedestal)
        form_ped.addRow("", self._btn_create_ped)

        layout.addWidget(grp_ped)

        # ── Sección losa ──────────────────────────────────────────────────
        grp_losa = QGroupBox("Crear Sección Losa (Shell-Thick)")
        form_losa = QFormLayout(grp_losa)
        form_losa.setVerticalSpacing(6)

        _, self._losa_thickness = _field("", "300", "Espesor en mm")
        row_esp = QHBoxLayout()
        row_esp.addWidget(self._losa_thickness)
        row_esp.addWidget(QLabel("mm"))
        row_esp.addStretch()
        form_losa.addRow("Espesor:", row_esp)

        self._losa_name = QLineEdit("LOSA_300")
        self._losa_name.setReadOnly(True)
        self._losa_name.setMaximumWidth(150)
        self._losa_name.setToolTip("Se crearán: LOSA_300 y LOSA_300PED")
        form_losa.addRow("Nombre base:", self._losa_name)

        self._btn_create_losa = QPushButton("✨ Crear secciones losa")
        self._btn_create_losa.setFixedHeight(30)
        self._btn_create_losa.setEnabled(False)
        self._btn_create_losa.clicked.connect(self._on_create_losa)
        form_losa.addRow("", self._btn_create_losa)

        info = QLabel("💡 Se crearán 2 secciones con colores distintos (losa general + bajo pedestal)")
        info.setWordWrap(True)
        form_losa.addRow(info)

        layout.addWidget(grp_losa)
        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(tab)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        # Conectar auto-nombre
        self._ped_width.textChanged.connect(self._update_ped_name)
        self._ped_height.textChanged.connect(self._update_ped_name)
        self._losa_thickness.textChanged.connect(self._update_losa_name)

        return tab

    def _build_tab_modelar(self) -> QWidget:
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(12)
        layout.setContentsMargins(6, 6, 6, 6)

        # ── Ubicación ─────────────────────────────────────────────────────
        grp_ubic = QGroupBox("📍 Origen")
        ubic_layout = QHBoxLayout(grp_ubic)

        _, self._orig_x = _field("X:", "0.0")
        _, self._orig_y = _field("Y:", "0.0")
        _, self._orig_z = _field("Z:", "0.0")
        for lbl, edit in [(QLabel("X:"), self._orig_x),
                          (QLabel("Y:"), self._orig_y),
                          (QLabel("Z:"), self._orig_z)]:
            ubic_layout.addWidget(lbl)
            ubic_layout.addWidget(edit)
            ubic_layout.addWidget(QLabel("mm"))
            ubic_layout.addSpacing(6)

        self._btn_fetch_coords = QPushButton("📍 Desde nodo seleccionado")
        self._btn_fetch_coords.setEnabled(False)
        self._btn_fetch_coords.clicked.connect(self._on_fetch_coords)
        ubic_layout.addWidget(self._btn_fetch_coords)
        ubic_layout.addStretch()

        layout.addWidget(grp_ubic)

        # ── Componentes ───────────────────────────────────────────────────
        grp_comp = QGroupBox("🏗️ Componentes")
        form_comp = QFormLayout(grp_comp)
        form_comp.setVerticalSpacing(8)

        _, self._cb_frame_sec = _combo_row("", "Sección Frame del pedestal")
        self._cb_frame_sec.addItem("-- Sin conexión --")
        self._cb_frame_sec.currentTextChanged.connect(self._on_frame_sec_changed)
        row_fr = QHBoxLayout()
        row_fr.addWidget(self._cb_frame_sec)
        row_fr.addStretch()
        form_comp.addRow("Sección Frame:", row_fr)

        ped_dims = QHBoxLayout()
        _, self._mod_h_ped = _field("", "1000", "Altura pedestal (mm)")
        _, self._mod_wx_ped = _field("", "500", "Ancho X pedestal (mm)")
        _, self._mod_wy_ped = _field("", "500", "Alto Y pedestal (mm)")
        for lbl_txt, edit in [("H:", self._mod_h_ped),
                               ("Ancho X:", self._mod_wx_ped),
                               ("Alto Y:", self._mod_wy_ped)]:
            ped_dims.addWidget(QLabel(lbl_txt))
            ped_dims.addWidget(edit)
            ped_dims.addWidget(QLabel("mm"))
            ped_dims.addSpacing(6)
        ped_dims.addStretch()
        form_comp.addRow("Pedestal:", ped_dims)

        _, self._cb_shell_zapata = _combo_row("", "Sección losa zapata")
        self._cb_shell_zapata.addItem("-- Sin conexión --")
        self._cb_shell_zapata.currentTextChanged.connect(self._on_shell_zapata_changed)
        row_sz = QHBoxLayout()
        row_sz.addWidget(self._cb_shell_zapata)
        row_sz.addStretch()
        form_comp.addRow("Losa zapata:", row_sz)

        _, self._cb_shell_ped = _combo_row("", "Sección losa bajo pedestal")
        self._cb_shell_ped.addItem("-- Sin conexión --")
        row_sp = QHBoxLayout()
        row_sp.addWidget(self._cb_shell_ped)
        row_sp.addStretch()
        form_comp.addRow("Losa pedestal:", row_sp)

        esp_bal_row = QHBoxLayout()
        _, self._mod_esp = _field("", "300", "Espesor zapata para geometría (mm)")
        _, self._mod_balasto = _field("", "5", "Módulo balasto ks (kgf/cm³)")
        esp_bal_row.addWidget(QLabel("Esp. zapata:"))
        esp_bal_row.addWidget(self._mod_esp)
        esp_bal_row.addWidget(QLabel("mm"))
        esp_bal_row.addSpacing(10)
        esp_bal_row.addWidget(QLabel("Balasto ks:"))
        esp_bal_row.addWidget(self._mod_balasto)
        esp_bal_row.addWidget(QLabel("kgf/cm³"))
        esp_bal_row.addStretch()
        form_comp.addRow("", esp_bal_row)

        layout.addWidget(grp_comp)

        # ── Malla ─────────────────────────────────────────────────────────
        grp_mesh = QGroupBox("⚙️ Malla y geometría")
        form_mesh = QFormLayout(grp_mesh)

        mesh_row = QHBoxLayout()
        _, self._mod_nx = _field("", "4", "Divisiones X", width=50)
        _, self._mod_ny = _field("", "4", "Divisiones Y", width=50)
        mesh_row.addWidget(QLabel("Divisiones X:"))
        mesh_row.addWidget(self._mod_nx)
        mesh_row.addSpacing(10)
        mesh_row.addWidget(QLabel("Y:"))
        mesh_row.addWidget(self._mod_ny)
        mesh_row.addStretch()
        form_mesh.addRow("Malla:", mesh_row)

        vuelo_row = QHBoxLayout()
        _, self._mod_vuelo = _field("", "500", "Sobresal de zapata más allá del pedestal (mm)")
        vuelo_row.addWidget(self._mod_vuelo)
        vuelo_row.addWidget(QLabel("mm"))
        vuelo_row.addStretch()
        form_mesh.addRow("Vuelo:", vuelo_row)

        layout.addWidget(grp_mesh)

        # ── Botón modelar ─────────────────────────────────────────────────
        self._btn_modelar = QPushButton("🏗️ Modelar fundación")
        self._btn_modelar.setFixedHeight(36)
        self._btn_modelar.setEnabled(False)
        self._btn_modelar.clicked.connect(self._on_modelar)
        layout.addWidget(self._btn_modelar)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(tab)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return tab

    # ══════════════════════════════════════════════════════════════════════
    # Helpers internos
    # ══════════════════════════════════════════════════════════════════════

    def _log_append(self, text: str):
        self._log.append(text)

    def _busy(self, on: bool):
        connected = self._conn.is_connected
        self._btn_connect.setEnabled(not on and not connected)
        self._btn_reload_all.setEnabled(not on and connected)
        self._btn_disconnect.setEnabled(not on and connected)
        self._btn_create_ped.setEnabled(not on and connected)
        self._btn_create_losa.setEnabled(not on and connected)
        self._btn_fetch_coords.setEnabled(not on and connected)
        self._btn_modelar.setEnabled(not on and connected)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_reload_all.setEnabled(connected)
        self._btn_disconnect.setEnabled(connected)
        self._btn_create_ped.setEnabled(connected)
        self._btn_create_losa.setEnabled(connected)
        self._btn_fetch_coords.setEnabled(connected)
        self._btn_modelar.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
            self._clear_combos()

    def _clear_combos(self):
        placeholder = "-- Sin conexión --"
        for cb in (self._cb_concrete, self._cb_rebar_mat,
                   self._cb_corner_bars, self._cb_edge_bars,
                   self._cb_frame_sec, self._cb_shell_zapata, self._cb_shell_ped):
            cb.clear()
            cb.addItem(placeholder)

    def _restore_combo(self, cb: QComboBox, items: list, previous: str):
        cb.clear()
        if items:
            cb.addItems(items)
            idx = cb.findText(previous)
            cb.setCurrentIndex(idx if idx >= 0 else 0)
        else:
            cb.addItem("-- No encontrado --")

    # ── Auto-nombre ────────────────────────────────────────────────────────

    def _update_ped_name(self):
        w = self._ped_width.text().strip()
        h = self._ped_height.text().strip()
        def fmt(s):
            try:
                v = float(s)
                return str(int(v)) if v == int(v) else s
            except ValueError:
                return s or "?"
        self._ped_name.setText(f"PED_{fmt(w)}x{fmt(h)}")

    def _update_losa_name(self):
        t = self._losa_thickness.text().strip()
        try:
            v = float(t)
            t_str = str(int(v)) if v == int(v) else t
        except ValueError:
            t_str = t or "?"
        self._losa_name.setText(f"LOSA_{t_str}")

    # ── Callbacks de combos ────────────────────────────────────────────────

    def _on_frame_sec_changed(self, name: str):
        """Rellena dims del pedestal si el nombre es PED_ANCHOxALTO."""
        m = re.match(r'^PED_(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)$', name.strip(), re.I)
        if m:
            self._mod_wx_ped.setText(m.group(2))
            self._mod_wy_ped.setText(m.group(1))

    def _on_shell_zapata_changed(self, name: str):
        """Rellena espesor zapata si el nombre es LOSA_ESPESOR."""
        m = re.match(r'^LOSA_(\d+(?:\.\d+)?)$', name.strip(), re.I)
        if m:
            self._mod_esp.setText(m.group(1))

    # ══════════════════════════════════════════════════════════════════════
    # Slots — Conectar / Desconectar
    # ══════════════════════════════════════════════════════════════════════

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, res: dict):
        self._busy(False)
        if res.get("connected"):
            self._log_append(f"✔ Conectado — v{res.get('version','?')} | {res.get('model_path','(sin modelo)')}")
            self._set_connected(True)
            self._on_load_data()
        else:
            self._log_append(f"✘ Error: {res.get('error','desconocido')}")
            self._set_connected(False)

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, _):
        self._busy(False)
        self._log_append("✔ Desconectado.")
        self._set_connected(False)

    # ══════════════════════════════════════════════════════════════════════
    # Slots — Cargar datos
    # ══════════════════════════════════════════════════════════════════════

    def _on_load_data(self):
        self._log_append("Cargando datos del modelo...")
        self._busy(True)
        self._worker = LoadDataWorker(self._backend)
        self._worker.finished.connect(self._on_load_done)
        self._worker.start()

    def _on_load_done(self, data: dict):
        self._busy(False)
        if "error" in data:
            self._log_append(f"✘ Error cargando datos: {data['error']}")
            return

        self._restore_combo(self._cb_concrete, data["concrete"], self._cb_concrete.currentText())
        self._restore_combo(self._cb_rebar_mat, data["rebar_mats"], self._cb_rebar_mat.currentText())

        sizes = data["rebar_sizes"] or ["12mm", "16mm", "20mm", "25mm", "#6", "#8", "#10"]
        self._restore_combo(self._cb_corner_bars, sizes, self._cb_corner_bars.currentText() or "16mm")
        self._restore_combo(self._cb_edge_bars, sizes, self._cb_edge_bars.currentText() or "12mm")

        self._restore_combo(self._cb_frame_sec, data["frames"], self._cb_frame_sec.currentText())
        self._restore_combo(self._cb_shell_zapata, data["shells"], self._cb_shell_zapata.currentText())
        self._restore_combo(self._cb_shell_ped, data["shells"], self._cb_shell_ped.currentText())

        self._log_append(
            f"✔ {len(data['concrete'])} hormigones | "
            f"{len(data['rebar_mats'])} aceros | "
            f"{len(data['frames'])} frames | "
            f"{len(data['shells'])} shells"
        )

    # ══════════════════════════════════════════════════════════════════════
    # Slots — Crear sección pedestal
    # ══════════════════════════════════════════════════════════════════════

    def _on_create_pedestal(self):
        try:
            cfg = PedestalSectionConfig(
                section_name=self._ped_name.text().strip(),
                concrete_mat=self._cb_concrete.currentText().strip(),
                rebar_mat=self._cb_rebar_mat.currentText().strip(),
                width=float(self._ped_width.text()),
                height=float(self._ped_height.text()),
                corner_bar_size=self._cb_corner_bars.currentText().strip(),
                edge_bar_size=self._cb_edge_bars.currentText().strip(),
                edge_spacing=float(self._ped_spacing.text()),
                cover=float(self._ped_cover.text()),
            )
        except ValueError as e:
            self._log_append(f"✘ Parámetros inválidos: {e}")
            return

        self._log_append(f"Creando sección pedestal: {cfg.section_name} ({cfg.width}×{cfg.height} mm)...")
        self._busy(True)
        self._worker = CreatePedestalWorker(self._backend, cfg)
        self._worker.finished.connect(self._on_create_ped_done)
        self._worker.start()

    def _on_create_ped_done(self, res: dict):
        self._busy(False)
        if res.get("success"):
            self._log_append(f"✔ Sección '{res['section_name']}' creada correctamente.")
            self._on_load_data()
        else:
            self._log_append(f"✘ Error: {res.get('error','desconocido')}")

    # ══════════════════════════════════════════════════════════════════════
    # Slots — Crear sección losa
    # ══════════════════════════════════════════════════════════════════════

    def _on_create_losa(self):
        try:
            cfg = LosaSectionConfig(
                base_name=self._losa_name.text().strip(),
                concrete_mat=self._cb_concrete.currentText().strip(),
                thickness=float(self._losa_thickness.text()),
            )
        except ValueError as e:
            self._log_append(f"✘ Parámetros inválidos: {e}")
            return

        self._log_append(f"Creando secciones losa: {cfg.base_name} / {cfg.base_name}PED ...")
        self._busy(True)
        self._worker = CreateLosaWorker(self._backend, cfg)
        self._worker.finished.connect(self._on_create_losa_done)
        self._worker.start()

    def _on_create_losa_done(self, res: dict):
        self._busy(False)
        if res.get("success"):
            self._log_append(f"✔ Secciones creadas: {', '.join(res['sections'])}")
            self._on_load_data()
        else:
            self._log_append(f"✘ Error: {res.get('error','desconocido')}")

    # ══════════════════════════════════════════════════════════════════════
    # Slots — Obtener coords
    # ══════════════════════════════════════════════════════════════════════

    def _on_fetch_coords(self):
        self._busy(True)
        self._worker = FetchCoordsWorker(self._backend)
        self._worker.finished.connect(self._on_fetch_done)
        self._worker.start()

    def _on_fetch_done(self, coords):
        self._busy(False)
        if coords:
            self._orig_x.setText(f"{coords['x']:.4f}")
            self._orig_y.setText(f"{coords['y']:.4f}")
            self._orig_z.setText(f"{coords['z']:.4f}")
            self._log_append(f"✔ Coords desde nodo '{coords['name']}': ({coords['x']:.1f}, {coords['y']:.1f}, {coords['z']:.1f})")
        else:
            self._log_append("⚠️ No hay nodo seleccionado en SAP2000.")

    # ══════════════════════════════════════════════════════════════════════
    # Slots — Modelar
    # ══════════════════════════════════════════════════════════════════════

    def _on_modelar(self):
        try:
            cfg = FundacionConfig(
                frame_section=self._cb_frame_sec.currentText().strip(),
                shell_zapata=self._cb_shell_zapata.currentText().strip(),
                shell_pedestal=self._cb_shell_ped.currentText().strip(),
                origen_x=float(self._orig_x.text()),
                origen_y=float(self._orig_y.text()),
                origen_z=float(self._orig_z.text()),
                altura_pedestal=float(self._mod_h_ped.text()),
                ancho_pedestal=float(self._mod_wx_ped.text()),
                alto_pedestal=float(self._mod_wy_ped.text()),
                espesor_zapata=float(self._mod_esp.text()),
                vuelo=float(self._mod_vuelo.text()),
                mesh_nx=int(self._mod_nx.text()),
                mesh_ny=int(self._mod_ny.text()),
                balasto=float(self._mod_balasto.text()),
            )
        except ValueError as e:
            self._log_append(f"✘ Parámetros inválidos: {e}")
            return

        self._log_append("─" * 50)
        self._log_append(f"Modelando fundación en ({cfg.origen_x}, {cfg.origen_y}, {cfg.origen_z}) mm...")
        self._busy(True)
        self._worker = ModelarWorker(self._backend, cfg)
        self._worker.finished.connect(self._on_modelar_done)
        self._worker.start()

    def _on_modelar_done(self, res: dict):
        self._busy(False)
        if res.get("success"):
            self._log_append(f"✔ Fundación modelada — Frame: {res['frame']} | Áreas: {res['num_areas']}")
        else:
            self._log_append(f"✘ Error: {res.get('error','desconocido')}")


# ══════════════════════════════════════════════════════════════════════════════
# Punto de entrada
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FundacionesGUI()
    win.show()
    sys.exit(app.exec())
