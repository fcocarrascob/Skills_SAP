"""
GUI — SAP2000 Placa Base Generator (Standalone)
=================================================
PySide6 interface for the parametric base plate backend.
Conexión directa vía comtypes (sin MCP).

Layout
------
  [Conectar]
  ── Inputs (scroll) ─────── | Preview |
     1. Perfil Columna:  H_col  B_col  flange_t  web_t
     2. Placa Base:       plate_thickness
     3. Pernos:           bolt_dia (combo)  A/B  centers table  preset  material
     4. Silla Anclaje:    [x] include  height  thickness
     5. Balasto:          ks
  ── ─────────────────────────────────────────
  [Ejecutar]
  ── Output ─────────────────────────────────
     log de texto con resultado / errores
  ── ─────────────────────────────────────────
  [Desconectar]
"""

import sys
import re

from PySide6.QtCore import Qt, QThread, Signal, QSize, QRectF
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush
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
    QComboBox,
    QPushButton,
    QTextEdit,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from backend_placabase import (
    SapConnection, PlacaBaseBackend, PlacaBaseConfig, DIA_TO_SPACING,
)


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
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _get_A_B_from_dia(dia: float):
    """Mapea diámetro (mm) a espaciamiento A, B."""
    d = int(round(float(dia)))
    return DIA_TO_SPACING.get(d, (100, 100))


# ══════════════════════════════════════════════════════════════════════════════
# Preview Widget
# ══════════════════════════════════════════════════════════════════════════════

class PreviewWidget(QWidget):
    """Vista previa del perfil I y posición de pernos."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QSize(300, 300))

    def sizeHint(self):
        return QSize(400, 400)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor(255, 255, 255))

        # Find parent GUI widget
        parent = self.parent()
        while parent is not None and not hasattr(parent, '_H_col'):
            parent = parent.parent()
        if parent is None:
            return

        try:
            H = float(parent._H_col.text())
        except Exception:
            H = 300.0
        try:
            B = float(parent._B_col.text())
        except Exception:
            B = 250.0

        # Read bolt centers from table
        centers = []
        try:
            for r in range(parent._centers_table.rowCount()):
                itx = parent._centers_table.item(r, 0)
                ity = parent._centers_table.item(r, 1)
                if itx and ity:
                    centers.append((float(itx.text()), float(ity.text())))
        except Exception:
            pass

        # Compute scale
        w = rect.width()
        h = rect.height()
        margin = 20
        avail_w = max(10, w - 2 * margin)
        avail_h = max(10, h - 2 * margin)

        max_abs_bx = max((abs(c[0]) for c in centers), default=0)
        max_abs_by = max((abs(c[1]) for c in centers), default=0)

        try:
            dia_val = float(parent._bolt_combo.currentData() or 25)
        except Exception:
            dia_val = 25.0
        A_val, _ = _get_A_B_from_dia(dia_val)
        half_A_mm = A_val / 2.0
        buffer_mm = 10.0

        req_half_w = max(B / 2.0, max_abs_bx + half_A_mm + buffer_mm)
        req_half_h = max(H / 2.0, max_abs_by + half_A_mm + buffer_mm)

        scale = min(
            avail_w / (2.0 * req_half_w) if req_half_w > 0 else 1.0,
            avail_h / (2.0 * req_half_h) if req_half_h > 0 else 1.0,
        )

        cx0 = rect.left() + w / 2
        cy0 = rect.top() + h / 2

        # Thicknesses
        try:
            flange_t = max(1.0, float(parent._flange_t.text()))
        except Exception:
            flange_t = max(1.0, 0.12 * H)
        try:
            web_t = max(1.0, float(parent._web_t.text()))
        except Exception:
            web_t = max(1.0, 0.08 * B)

        half_w_px = (B / 2.0) * scale
        half_h_px = (H / 2.0) * scale
        flange_h_px = flange_t * scale
        web_w_px = max(2.0, web_t * scale)

        # I-section
        top_rect = QRectF(cx0 - half_w_px, cy0 - half_h_px, 2 * half_w_px, flange_h_px)
        bot_rect = QRectF(cx0 - half_w_px, cy0 + half_h_px - flange_h_px,
                          2 * half_w_px, flange_h_px)
        web_rect = QRectF(cx0 - web_w_px / 2, cy0 - half_h_px + flange_h_px,
                          web_w_px, 2 * half_h_px - 2 * flange_h_px)

        pen = QPen(QColor(200, 30, 30), max(1.0, scale * 0.5))
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(255, 255, 255, 0)))
        painter.drawRect(top_rect)
        painter.drawRect(bot_rect)
        painter.drawRect(web_rect)

        # Center cross
        painter.setPen(QPen(QColor(0, 150, 200), 1))
        painter.drawLine(int(cx0 - 10), int(cy0), int(cx0 + 10), int(cy0))
        painter.drawLine(int(cx0), int(cy0 - 10), int(cx0), int(cy0 + 10))

        # Bolts
        bolt_r_px = max(3, int(4 * scale))
        painter.setBrush(QBrush(QColor(200, 30, 30)))
        painter.setPen(QPen(QColor(120, 20, 20), 1))
        for bx, by in centers:
            px = cx0 + bx * scale
            py = cy0 - by * scale
            painter.drawEllipse(int(px - bolt_r_px), int(py - bolt_r_px),
                                bolt_r_px * 2, bolt_r_px * 2)

        # A×A areas around bolts
        half_A_px = half_A_mm * scale
        painter.setPen(QPen(QColor(0, 120, 180), max(1.0, scale * 0.5)))
        painter.setBrush(QBrush(QColor(0, 120, 180, 40)))
        for bx, by in centers:
            px = cx0 + bx * scale
            py = cy0 - by * scale
            painter.drawRect(QRectF(px - half_A_px, py - half_A_px,
                                    2 * half_A_px, 2 * half_A_px))


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class PlacaBaseGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Placa Base Generator")
        self.setMinimumWidth(900)

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

        # ── Inputs (scroll area + preview) ───────────────────────────────
        self._scroll_area = QScrollArea()
        self._scroll_widget = QWidget()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self._scroll_widget)
        form = QVBoxLayout(self._scroll_widget)

        # --- 1. Perfil Columna ---
        grp_col = QGroupBox("1. Perfil Columna")
        col_grid = QGridLayout()
        col_grid.addWidget(QLabel("Alto H_col (mm):"), 0, 0)
        self._H_col = QLineEdit("300.0")
        col_grid.addWidget(self._H_col, 0, 1)
        col_grid.addWidget(QLabel("Ancho B_col (mm):"), 0, 2)
        self._B_col = QLineEdit("250.0")
        col_grid.addWidget(self._B_col, 0, 3)
        col_grid.addWidget(QLabel("Espesor Ala (mm):"), 1, 0)
        self._flange_t = QLineEdit("")
        col_grid.addWidget(self._flange_t, 1, 1)
        col_grid.addWidget(QLabel("Espesor Alma (mm):"), 1, 2)
        self._web_t = QLineEdit("")
        col_grid.addWidget(self._web_t, 1, 3)
        grp_col.setLayout(col_grid)
        form.addWidget(grp_col)

        # --- 2. Placa Base ---
        grp_plate = QGroupBox("2. Placa Base")
        plate_lay = QHBoxLayout()
        plate_lay.addWidget(QLabel("Espesor Placa (mm):"))
        self._plate_t = QLineEdit("20.0")
        plate_lay.addWidget(self._plate_t)
        plate_lay.addStretch()
        grp_plate.setLayout(plate_lay)
        form.addWidget(grp_plate)

        # --- 3. Pernos ---
        grp_bolts = QGroupBox("3. Configuración de Pernos")
        bolts_lay = QVBoxLayout()

        # 3.1 Diámetro ComboBox + A/B display
        row_dia = QHBoxLayout()
        row_dia.addWidget(QLabel("Diámetro:"))
        self._bolt_combo = QComboBox()
        dia_items = [
            ('16 mm (5/8")', 16), ('19 mm (3/4")', 19), ('22 mm (7/8")', 22),
            ('25 mm (1")', 25), ('32 mm (1 1/4")', 32), ('38 mm (1 1/2")', 38),
            ('44 mm (1 3/4")', 44), ('51 mm (2")', 51), ('57 mm (2 1/4")', 57),
            ('64 mm (2 1/2")', 64),
        ]
        for label, mm in dia_items:
            self._bolt_combo.addItem(label, mm)
        row_dia.addWidget(self._bolt_combo)
        row_dia.addWidget(QLabel("A:"))
        self._A_display = QLineEdit("100")
        self._A_display.setReadOnly(True)
        self._A_display.setMaximumWidth(60)
        row_dia.addWidget(self._A_display)
        row_dia.addWidget(QLabel("B:"))
        self._B_display = QLineEdit("100")
        self._B_display.setReadOnly(True)
        self._B_display.setMaximumWidth(60)
        row_dia.addWidget(self._B_display)
        bolts_lay.addLayout(row_dia)

        # 3.2 Tabla centros
        bolts_lay.addWidget(QLabel("Centros de pernos (X, Y, Z):"))
        self._centers_table = QTableWidget(0, 3)
        self._centers_table.setHorizontalHeaderLabels(["X", "Y", "Z"])
        self._centers_table.horizontalHeader().setStretchLastSection(True)
        self._centers_table.setMaximumHeight(180)
        bolts_lay.addWidget(self._centers_table)

        row_tbl_btns = QHBoxLayout()
        self._btn_add_row = QPushButton("+ Agregar fila")
        self._btn_add_row.clicked.connect(self._add_row)
        self._btn_del_row = QPushButton("- Eliminar fila")
        self._btn_del_row.clicked.connect(self._remove_row)
        row_tbl_btns.addWidget(self._btn_add_row)
        row_tbl_btns.addWidget(self._btn_del_row)
        bolts_lay.addLayout(row_tbl_btns)

        # 3.3 Preset
        row_preset = QHBoxLayout()
        row_preset.addWidget(QLabel("Pernos por fila:"))
        self._per_row_combo = QComboBox()
        for n in (2, 3, 4, 5):
            self._per_row_combo.addItem(str(n), n)
        row_preset.addWidget(self._per_row_combo)
        self._btn_preset = QPushButton("Generar posiciones (preset)")
        self._btn_preset.clicked.connect(self._generate_preset)
        row_preset.addWidget(self._btn_preset)
        bolts_lay.addLayout(row_preset)

        # 3.4 Material
        row_mat = QHBoxLayout()
        row_mat.addWidget(QLabel("Material Perno:"))
        self._bolt_material = QComboBox()
        self._bolt_material.setEditable(True)
        self._bolt_material.addItem("A36")
        self._bolt_material.setToolTip("Material para la sección Frame del perno")
        row_mat.addWidget(self._bolt_material)
        bolts_lay.addLayout(row_mat)

        grp_bolts.setLayout(bolts_lay)
        form.addWidget(grp_bolts)

        # --- 4. Silla de Anclaje ---
        grp_chair = QGroupBox("4. Silla de Anclaje")
        chair_grid = QGridLayout()
        self._chk_chair = QCheckBox("Incluir silla de anclaje")
        self._chk_chair.toggled.connect(self._toggle_chair)
        chair_grid.addWidget(self._chk_chair, 0, 0, 1, 4)
        chair_grid.addWidget(QLabel("Altura (mm):"), 1, 0)
        self._chair_height = QLineEdit("")
        chair_grid.addWidget(self._chair_height, 1, 1)
        chair_grid.addWidget(QLabel("Espesor (mm):"), 1, 2)
        self._chair_thick = QLineEdit("")
        chair_grid.addWidget(self._chair_thick, 1, 3)
        grp_chair.setLayout(chair_grid)
        form.addWidget(grp_chair)

        # --- 5. Balasto ---
        grp_bal = QGroupBox("5. Módulo de Balasto")
        bal_lay = QHBoxLayout()
        bal_lay.addWidget(QLabel("ks [kgf/cm³]:"))
        self._ks = QLineEdit("5.0")
        self._ks.setToolTip("Módulo de balasto (0 = omitir)")
        bal_lay.addWidget(self._ks)
        bal_lay.addStretch()
        grp_bal.setLayout(bal_lay)
        form.addWidget(grp_bal)

        # Preview widget
        self._preview = PreviewWidget(self)

        content_row = QHBoxLayout()
        content_row.addWidget(self._scroll_area, 1)
        content_row.addWidget(self._preview, 1)
        root.addLayout(content_row, 1)

        # ── Botón Ejecutar ─────────────────────────────────────────────────
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
        self._log.setMinimumHeight(150)
        out_layout.addWidget(self._log)
        root.addWidget(output_box)

        # ── Botón Desconectar ────────────────────────────────────────────
        self._btn_disconnect = QPushButton("Desconectar de SAP2000")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        root.addWidget(self._btn_disconnect)

        # ── Inicialización ───────────────────────────────────────────────
        # Agregar una fila por defecto en la tabla de centros
        self._add_row()
        self._update_A_B()
        self._update_thickness_defaults()
        self._toggle_chair(self._chk_chair.isChecked())

        # Signals para refrescar preview
        self._bolt_combo.currentIndexChanged.connect(self._update_A_B)
        self._bolt_combo.currentIndexChanged.connect(lambda *_: self._preview.update())
        self._H_col.textChanged.connect(lambda *_: self._preview.update())
        self._B_col.textChanged.connect(lambda *_: self._preview.update())
        self._H_col.editingFinished.connect(self._preview.update)
        self._B_col.editingFinished.connect(self._preview.update)
        self._H_col.textChanged.connect(lambda *_: self._update_thickness_defaults())
        self._B_col.textChanged.connect(lambda *_: self._update_thickness_defaults())
        self._flange_t.textChanged.connect(lambda *_: self._preview.update())
        self._web_t.textChanged.connect(lambda *_: self._preview.update())
        self._plate_t.textChanged.connect(lambda *_: self._preview.update())
        self._centers_table.itemChanged.connect(lambda *_: self._preview.update())
        self._centers_table.cellChanged.connect(lambda *_: self._preview.update())

        self._preview.update()

    # ── Helpers de estado ─────────────────────────────────────────────────

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

    # ── Helpers de UI ─────────────────────────────────────────────────────

    def _update_A_B(self, *args):
        """Actualiza campos A/B según diámetro seleccionado."""
        try:
            data = self._bolt_combo.currentData()
            if data is None:
                m = re.search(r"(\d+(?:\.\d+)?)", self._bolt_combo.currentText())
                dia_val = float(m.group(1)) if m else 100.0
            else:
                dia_val = float(data)
        except Exception:
            dia_val = 100.0
        A, B = _get_A_B_from_dia(dia_val)
        self._A_display.setText(str(A))
        self._B_display.setText(str(B))

    def _update_thickness_defaults(self):
        """Asigna espesores estimados si los campos están vacíos."""
        try:
            H = float(self._H_col.text())
        except Exception:
            H = 300.0
        try:
            B = float(self._B_col.text())
        except Exception:
            B = 250.0
        if not self._flange_t.text().strip():
            self._flange_t.setText(str(max(1.0, round(0.12 * H, 3))))
        if not self._web_t.text().strip():
            self._web_t.setText(str(max(1.0, round(0.08 * B, 3))))
        if not self._plate_t.text().strip():
            self._plate_t.setText(str(max(1.0, round(0.06 * B, 3))))

    def _toggle_chair(self, checked: bool):
        self._chair_height.setEnabled(checked)
        self._chair_thick.setEnabled(checked)

    # ── Tabla de centros ──────────────────────────────────────────────────

    def _add_row(self):
        r = self._centers_table.rowCount()
        self._centers_table.insertRow(r)
        self._centers_table.setItem(r, 0, QTableWidgetItem("0.0"))
        self._centers_table.setItem(r, 1, QTableWidgetItem("0.0"))
        self._centers_table.setItem(r, 2, QTableWidgetItem("0.0"))
        self._preview.update()

    def _remove_row(self):
        sel = self._centers_table.selectionModel().selectedRows()
        if not sel:
            QMessageBox.information(self, "Info", "Seleccione una fila para eliminar")
            return
        rows = sorted([s.row() for s in sel], reverse=True)
        for r in rows:
            self._centers_table.removeRow(r)
        self._preview.update()

    def _generate_preset(self):
        """Genera posiciones de pernos con el preset seleccionado (n por fila)."""
        try:
            n = int(self._per_row_combo.currentData())
        except Exception:
            QMessageBox.warning(self, "Error", "Seleccione número válido de pernos por fila")
            return

        try:
            dia = float(self._bolt_combo.currentData())
        except Exception:
            m = re.search(r"(\d+(?:\.\d+)?)", self._bolt_combo.currentText())
            dia = float(m.group(1)) if m else 25.0

        A, B = _get_A_B_from_dia(dia)

        try:
            H = float(self._H_col.text())
        except Exception:
            H = 300.0

        start = -((n - 1) / 2.0) * A
        x_positions = [start + i * A for i in range(n)]
        ys = [H / 2.0 + B / 2.0, -H / 2.0 - B / 2.0]

        self._centers_table.setRowCount(0)
        for y in ys:
            for x in x_positions:
                r = self._centers_table.rowCount()
                self._centers_table.insertRow(r)
                self._centers_table.setItem(r, 0, QTableWidgetItem(str(round(x, 6))))
                self._centers_table.setItem(r, 1, QTableWidgetItem(str(round(y, 6))))
                self._centers_table.setItem(r, 2, QTableWidgetItem("0.0"))
        self._preview.update()

    # ── Build config ──────────────────────────────────────────────────────

    def _build_config(self) -> PlacaBaseConfig:
        """Construye PlacaBaseConfig desde los widgets de la GUI."""
        centers = []
        for r in range(self._centers_table.rowCount()):
            itx = self._centers_table.item(r, 0)
            ity = self._centers_table.item(r, 1)
            itz = self._centers_table.item(r, 2)
            if itx and ity:
                x = float(itx.text())
                y = float(ity.text())
                z = float(itz.text()) if itz and itz.text().strip() else 0.0
                centers.append((x, y, z))

        def _safe_float(edit, default):
            val = edit.text().strip()
            if val == '' or val.lower() == 'none':
                return default
            return float(val)

        return PlacaBaseConfig(
            bolt_dia=float(self._bolt_combo.currentData()),
            bolt_material=self._bolt_material.currentText().strip() or "A36",
            n_pernos=int(self._per_row_combo.currentData()),
            bolt_centers=centers,
            H_col=float(self._H_col.text()),
            B_col=float(self._B_col.text()),
            plate_thickness=_safe_float(self._plate_t, 20.0),
            flange_thickness=_safe_float(self._flange_t, 15.0),
            web_thickness=_safe_float(self._web_t, 10.0),
            include_anchor_chair=self._chk_chair.isChecked(),
            anchor_chair_height=_safe_float(self._chair_height, 50.0),
            anchor_chair_thickness=_safe_float(self._chair_thick, 15.0),
            ks_balasto=_safe_float(self._ks, 0.0),
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
            self._load_materials_from_model()
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    def _load_materials_from_model(self):
        """Lee materiales del modelo SAP2000 activo y los carga en el ComboBox."""
        if not self._conn.is_connected:
            return
        try:
            ret = self._conn.sap_model.PropMaterial.GetNameList()
            if ret[-1] == 0 and ret[0] > 0:
                current_text = self._bolt_material.currentText()
                self._bolt_material.clear()
                names = ret[1]
                if isinstance(names, (list, tuple)):
                    for name in names:
                        self._bolt_material.addItem(str(name))
                idx = self._bolt_material.findText(current_text)
                if idx >= 0:
                    self._bolt_material.setCurrentIndex(idx)
                elif self._bolt_material.count() > 0:
                    self._bolt_material.setCurrentIndex(0)
                self._log_append(
                    f"Materiales cargados: {self._bolt_material.count()} disponibles.")
        except Exception as e:
            self._log_append(f"No se pudieron cargar materiales: {e}")

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
            if "message" in result:
                self._log_append(str(result["message"]))
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
    win.resize(950, 700)
    win.show()
    sys.exit(app.exec())
