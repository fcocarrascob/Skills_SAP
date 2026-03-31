"""
GUI — SAP2000 Placa Simple con Orientación Arbitraria (Standalone)
===================================================================
Genera una placa rectangular mallada con soporte de orientación
arbitraria (plano + ángulo) para hacer match con conexiones inclinadas.

Conexión directa vía comtypes (sin MCP).
Referencia de estilo: gui_multi_bolt.py

Layout
------
  [Estado de conexión]
  [Conectar]  [Desconectar]
  ┌─ Parámetros ─────────────────────┬─ Preview ─────────┐
  │  Dimensiones / Discretización    │  Vista superior   │
  │  Orientación / Ubicación         │  (malla de placa) │
  │  Propiedades SAP2000             │                   │
  └───────────────────────────────────┴───────────────────┘
  [Generar Placa Simple]
  ┌─ Salida ──────────────────────────────────────────────┐
  │  log...                                               │
  └───────────────────────────────────────────────────────┘
"""

import sys
import math

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from shared import (
    SapConnection,
    ConnectWorker,
    DisconnectWorker,
    RunWorker,
    GetCoordsWorker,
)
from backend_simple_plate import SimplePlateBackend, SimplePlateConfig


# ══════════════════════════════════════════════════════════════════════════════
# Preview Widget (QPainter)
# ══════════════════════════════════════════════════════════════════════════════

class SimplePlatePreviewWidget(QWidget):
    """Previsualización en tiempo real: vista superior con malla rotada."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 320)
        self.setStyleSheet("background-color: white; border: 1px solid #aaaaaa;")
        self._data: dict = {}

    def update_preview(
        self,
        width: float,
        height: float,
        nx: int,
        ny: int,
        angle: float,
    ):
        self._data = {
            "width": width, "height": height,
            "nx": nx, "ny": ny, "angle": angle,
        }
        self.update()

    # ── Dimensión con flechas ─────────────────────────────────────────────

    def _draw_dimension(self, painter, p1, p2, text, offset=20):
        x1, y1 = float(p1[0]), float(p1[1])
        x2, y2 = float(p2[0]), float(p2[1])
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1e-9:
            return
        nx_, ny_ = -dy / length, dx / length
        cx1, cy1 = x1 + nx_ * offset, y1 + ny_ * offset
        cx2, cy2 = x2 + nx_ * offset, y2 + ny_ * offset
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.drawLine(int(x1), int(y1), int(cx1), int(cy1))
        painter.drawLine(int(x2), int(y2), int(cx2), int(cy2))
        painter.drawLine(int(cx1), int(cy1), int(cx2), int(cy2))
        tick = 4
        ux, uy = dx / length * tick, dy / length * tick
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(int(cx1 - ux), int(cy1 - uy), int(cx1 + ux), int(cy1 + uy))
        painter.drawLine(int(cx2 - ux), int(cy2 - uy), int(cx2 + ux), int(cy2 + uy))
        mid_x, mid_y = (cx1 + cx2) / 2, (cy1 + cy2) / 2
        angle_r = math.degrees(math.atan2(dy, dx))
        if 90 < angle_r <= 270 or -270 <= angle_r < -90:
            angle_r += 180
        painter.setPen(QPen(Qt.black, 1))
        painter.save()
        painter.translate(mid_x, mid_y)
        painter.rotate(angle_r)
        painter.drawText(-150, -25, 300, 20, Qt.AlignCenter, text)
        painter.restore()

    # ── paintEvent ───────────────────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)
        d = self._data
        if not d:
            return
        w_px, h_px = self.width(), self.height()
        self._draw_plate_view(painter, w_px, h_px, d)

    # ── Vista de placa (malla rotada) ─────────────────────────────────────

    def _draw_plate_view(self, painter, w_px, h_px, d):
        plate_w = float(d.get("width", 500.0))
        plate_h = float(d.get("height", 500.0))
        nx = max(int(d.get("nx", 5)), 1)
        ny = max(int(d.get("ny", 5)), 1)
        angle = float(d.get("angle", 0.0))

        # Margen y área útil
        margin = 50
        draw_w = w_px - 2 * margin
        draw_h = h_px - 2 * margin
        if draw_w < 40 or draw_h < 40:
            return

        # Diagonal máxima (para escalar considerando rotación)
        diag = math.sqrt(plate_w ** 2 + plate_h ** 2)
        scale = min(draw_w, draw_h) / max(diag, 1e-9)

        # Centro geométrico de la placa en coordenadas locales
        cu, cv = plate_w / 2.0, plate_h / 2.0

        theta = math.radians(angle)
        cos_a, sin_a = math.cos(theta), math.sin(theta)

        # Offset para que el centro geométrico de la placa quede en pantalla
        screen_cx = w_px / 2.0
        screen_cy = h_px / 2.0
        off_x = (cu * cos_a - cv * sin_a) * scale
        off_y = (cu * sin_a + cv * cos_a) * scale

        def to_screen(u, v):
            """Convierte coordenadas locales (origen = inf-izq) a pantalla."""
            rx = u * cos_a - v * sin_a
            ry = u * sin_a + v * cos_a
            return (screen_cx - off_x + rx * scale,
                    screen_cy + off_y - ry * scale)

        # ── Dibujar celdas de la malla ──────────────────────────────────
        d_u = plate_w / nx
        d_v = plate_h / ny

        fill_brush = QBrush(QColor(200, 220, 255, 100))
        painter.setBrush(fill_brush)
        painter.setPen(QPen(QColor(70, 130, 180), 1.5))

        for i in range(nx):
            for j in range(ny):
                u0 = i * d_u
                v0 = j * d_v

                corners = [
                    to_screen(u0,       v0),
                    to_screen(u0 + d_u, v0),
                    to_screen(u0 + d_u, v0 + d_v),
                    to_screen(u0,       v0 + d_v),
                ]

                from PySide6.QtCore import QPointF
                from PySide6.QtGui import QPolygonF
                poly = QPolygonF([QPointF(x, y) for x, y in corners])
                painter.drawPolygon(poly)

        # ── Contorno exterior (más grueso) ──────────────────────────────
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 70, 130), 2.5))
        outline = [
            to_screen(0,       0),
            to_screen(plate_w, 0),
            to_screen(plate_w, plate_h),
            to_screen(0,       plate_h),
        ]
        from PySide6.QtCore import QPointF
        from PySide6.QtGui import QPolygonF
        poly_out = QPolygonF([QPointF(x, y) for x, y in outline])
        painter.drawPolygon(poly_out)

        # ── Punto de inserción (esquina inf-izq) ────────────────────────
        ox, oy = to_screen(0, 0)
        painter.setPen(QPen(Qt.red, 1))
        painter.setBrush(QBrush(Qt.red))
        painter.drawEllipse(int(ox) - 4, int(oy) - 4, 8, 8)

        # ── Acotaciones ─────────────────────────────────────────────────
        p_bl = to_screen(0, 0)
        p_br = to_screen(plate_w, 0)
        p_tl = to_screen(0, plate_h)

        self._draw_dimension(painter, p_bl, p_br,
                             f"W = {plate_w:.4g}", offset=28)
        self._draw_dimension(painter, p_bl, p_tl,
                             f"H = {plate_h:.4g}", offset=-28)

        # ── Ángulo ──────────────────────────────────────────────────────
        if abs(angle) > 0.01:
            ref_len = min(plate_w, plate_h) * 0.4 * scale
            painter.setPen(QPen(QColor(180, 0, 0), 1, Qt.DashLine))
            # Línea horizontal de referencia desde punto de inserción
            painter.drawLine(int(ox), int(oy),
                             int(ox + ref_len), int(oy))
            # Línea rotada
            painter.setPen(QPen(QColor(180, 0, 0), 1.5))
            painter.drawLine(int(ox), int(oy),
                             int(ox + ref_len * cos_a),
                             int(oy - ref_len * sin_a))
            # Etiqueta ángulo
            painter.setPen(QPen(Qt.darkRed, 1))
            painter.drawText(
                int(ox + ref_len * 0.5 + 5),
                int(oy - 15),
                f"θ = {angle:.1f}°"
            )

        # ── Título ──────────────────────────────────────────────────────
        painter.setPen(QPen(Qt.black, 1))
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        painter.drawText(8, 16, f"Malla {nx}×{ny}  |  ángulo {angle:.1f}°")


# ══════════════════════════════════════════════════════════════════════════════
# Helper: campo (label + QLineEdit)
# ══════════════════════════════════════════════════════════════════════════════

def _field(label: str, default: str, tooltip: str = "") -> tuple:
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    le = QLineEdit(default)
    le.setFixedWidth(90)
    if tooltip:
        le.setToolTip(tooltip)
    return lbl, le


# ══════════════════════════════════════════════════════════════════════════════
# GUI Principal
# ══════════════════════════════════════════════════════════════════════════════

class SimplePlateGUI(QWidget):
    """GUI standalone para generar placas simples con orientación arbitraria."""

    def __init__(self, connection: SapConnection | None = None):
        super().__init__()
        self.setWindowTitle("SAP2000 — Placa Simple")
        self.setMinimumSize(720, 620)

        self._conn = connection or SapConnection()
        self._backend = SimplePlateBackend(self._conn)
        self._worker = None
        self._run_worker = None
        self._coords_worker = None

        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Estado de conexión ────────────────────────────────────────────
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        root.addWidget(self._status_lbl)

        conn_row = QHBoxLayout()
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(30)
        self._btn_connect.clicked.connect(self._on_connect)
        self._btn_disconnect = QPushButton("Desconectar")
        self._btn_disconnect.setFixedHeight(30)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        conn_row.addWidget(self._btn_connect)
        conn_row.addWidget(self._btn_disconnect)
        root.addLayout(conn_row)

        # ── Body: params + preview ────────────────────────────────────────
        body = QHBoxLayout()
        params_col = QVBoxLayout()
        params_col.setSpacing(8)

        # ── Grupo: Dimensiones ────────────────────────────────────────────
        grp_dim = QGroupBox("Dimensiones (mm)")
        g1 = QGridLayout(grp_dim)
        g1.setHorizontalSpacing(12)
        g1.setVerticalSpacing(8)

        lbl, self._width = _field("Ancho (W):", "500.0",
                                  "Ancho de la placa en dirección u")
        g1.addWidget(lbl, 0, 0); g1.addWidget(self._width, 0, 1)
        lbl, self._height = _field("Alto (H):", "500.0",
                                   "Alto de la placa en dirección v")
        g1.addWidget(lbl, 0, 2); g1.addWidget(self._height, 0, 3)

        params_col.addWidget(grp_dim)

        # ── Grupo: Discretización ─────────────────────────────────────────
        grp_mesh = QGroupBox("Discretización")
        g2 = QGridLayout(grp_mesh)
        g2.setHorizontalSpacing(12)
        g2.setVerticalSpacing(8)

        lbl, self._nx = _field("Div. u (nx):", "5",
                               "Divisiones en dirección u (ancho)")
        g2.addWidget(lbl, 0, 0); g2.addWidget(self._nx, 0, 1)
        lbl, self._ny = _field("Div. v (ny):", "5",
                               "Divisiones en dirección v (alto)")
        g2.addWidget(lbl, 0, 2); g2.addWidget(self._ny, 0, 3)

        # Etiqueta info de tamaño de celda
        lbl_cell = QLabel("Celda:")
        lbl_cell.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._cell_lbl = QLabel("—")
        g2.addWidget(lbl_cell, 1, 0); g2.addWidget(self._cell_lbl, 1, 1, 1, 3)

        params_col.addWidget(grp_mesh)

        # ── Grupo: Orientación ────────────────────────────────────────────
        grp_orient = QGroupBox("Orientación")
        g3 = QGridLayout(grp_orient)
        g3.setHorizontalSpacing(12)
        g3.setVerticalSpacing(8)

        lbl_plane = QLabel("Plano:")
        lbl_plane.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._plane = QComboBox()
        self._plane.addItems(["", "XY", "XZ", "YZ"])
        g3.addWidget(lbl_plane, 0, 0); g3.addWidget(self._plane, 0, 1)

        lbl, self._angle = _field("Ángulo (°):", "0.0",
                                  "Rotación dentro del plano seleccionado")
        g3.addWidget(lbl, 0, 2); g3.addWidget(self._angle, 0, 3)

        params_col.addWidget(grp_orient)

        # ── Grupo: Ubicación ──────────────────────────────────────────────
        grp_loc = QGroupBox("Ubicación (esquina inferior izquierda)")
        g4 = QGridLayout(grp_loc)
        g4.setHorizontalSpacing(12)
        g4.setVerticalSpacing(8)

        lbl, self._ox = _field("X:", "0.0")
        g4.addWidget(lbl, 0, 0); g4.addWidget(self._ox, 0, 1)
        lbl, self._oy = _field("Y:", "0.0")
        g4.addWidget(lbl, 0, 2); g4.addWidget(self._oy, 0, 3)
        lbl, self._oz = _field("Z:", "0.0")
        g4.addWidget(lbl, 1, 0); g4.addWidget(self._oz, 1, 1)

        self._btn_get_coords = QPushButton("📍 Obtener Nodo")
        self._btn_get_coords.setFixedHeight(26)
        self._btn_get_coords.setEnabled(False)
        self._btn_get_coords.setToolTip(
            "Lee las coordenadas del nodo seleccionado en SAP2000 "
            "y las carga como esquina inferior izquierda de la placa."
        )
        self._btn_get_coords.clicked.connect(self._on_get_coords)
        g4.addWidget(self._btn_get_coords, 2, 0, 1, 4)

        params_col.addWidget(grp_loc)

        # ── Grupo: Propiedades SAP2000 ────────────────────────────────────
        grp_sap = QGroupBox("Propiedades SAP2000")
        g5 = QGridLayout(grp_sap)
        g5.setHorizontalSpacing(12)
        g5.setVerticalSpacing(8)

        lbl_prop = QLabel("Prop. Área Shell:")
        lbl_prop.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._area_prop = QComboBox()
        self._area_prop.setEditable(True)
        self._area_prop.addItem("Default")
        g5.addWidget(lbl_prop, 0, 0); g5.addWidget(self._area_prop, 0, 1)

        lbl, self._material = _field("Material:", "A36",
                                     "Material para auto-crear propiedad Shell")
        g5.addWidget(lbl, 0, 2); g5.addWidget(self._material, 0, 3)

        lbl, self._thickness = _field("Espesor (mm):", "16.0",
                                      "Espesor de la placa")
        g5.addWidget(lbl, 1, 0); g5.addWidget(self._thickness, 1, 1)

        self._auto_prop = QCheckBox("Auto-crear propiedad Shell")
        self._auto_prop.setToolTip(
            "Si marcado, crea una propiedad ShellThin con el material y "
            "espesor indicados. Si no, usa la propiedad seleccionada arriba."
        )
        g5.addWidget(self._auto_prop, 1, 2, 1, 2)

        lbl, self._group_name = _field("Grupo:", "SIMPLE_PLATE",
                                       "Nombre del grupo SAP2000")
        g5.addWidget(lbl, 2, 0); g5.addWidget(self._group_name, 2, 1)

        params_col.addWidget(grp_sap)
        params_col.addStretch()

        # ── Preview ───────────────────────────────────────────────────────
        self._preview = SimplePlatePreviewWidget()
        self._preview.setMinimumWidth(280)

        params_widget = QWidget()
        params_widget.setLayout(params_col)
        params_scroll = QScrollArea()
        params_scroll.setWidgetResizable(True)
        params_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        params_scroll.setStyleSheet("QScrollArea { border: none; }")
        params_scroll.setWidget(params_widget)

        body.addWidget(params_scroll, 1)
        body.addWidget(self._preview, 1)
        root.addLayout(body)

        # ── Botón generar ─────────────────────────────────────────────────
        self._btn_run = QPushButton("Generar Placa Simple")
        self._btn_run.setFixedHeight(36)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Log ───────────────────────────────────────────────────────────
        grp_log = QGroupBox("Salida")
        log_layout = QVBoxLayout(grp_log)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(120)
        log_layout.addWidget(self._log)
        root.addWidget(grp_log)

        # ── Señales preview ───────────────────────────────────────────────
        for w in (self._width, self._height, self._nx, self._ny, self._angle):
            w.textChanged.connect(self._update_preview)

        self._width.textChanged.connect(self._update_cell_label)
        self._height.textChanged.connect(self._update_cell_label)
        self._nx.textChanged.connect(self._update_cell_label)
        self._ny.textChanged.connect(self._update_cell_label)

        self._update_preview()
        self._update_cell_label()

    # ── Helpers internos ──────────────────────────────────────────────────

    def _log_append(self, text: str):
        self._log.append(text)

    def _busy(self, is_busy: bool):
        connected = self._conn.is_connected
        self._btn_run.setEnabled(not is_busy and connected)
        self._btn_get_coords.setEnabled(not is_busy and connected)
        self._btn_connect.setEnabled(not is_busy and not connected)
        self._btn_disconnect.setEnabled(not is_busy and connected)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        self._btn_run.setEnabled(connected)
        self._btn_get_coords.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")

    def _update_cell_label(self):
        try:
            w = float(self._width.text())
            h = float(self._height.text())
            nx = int(self._nx.text())
            ny = int(self._ny.text())
            if nx > 0 and ny > 0:
                self._cell_lbl.setText(f"{w / nx:.4g} × {h / ny:.4g} mm")
            else:
                self._cell_lbl.setText("—")
        except ValueError:
            self._cell_lbl.setText("—")

    def _update_preview(self):
        try:
            self._preview.update_preview(
                width=float(self._width.text()),
                height=float(self._height.text()),
                nx=int(self._nx.text()),
                ny=int(self._ny.text()),
                angle=float(self._angle.text()),
            )
        except ValueError:
            pass

    def _build_config(self) -> SimplePlateConfig:
        plane = self._plane.currentText().strip()
        if not plane:
            raise ValueError("Debe seleccionar un Plano antes de generar.")
        return SimplePlateConfig(
            width=float(self._width.text()),
            height=float(self._height.text()),
            nx=int(self._nx.text()),
            ny=int(self._ny.text()),
            origin_x=float(self._ox.text()),
            origin_y=float(self._oy.text()),
            origin_z=float(self._oz.text()),
            plane=plane,
            angle=float(self._angle.text()),
            prop_name=self._area_prop.currentText().strip() or "Default",
            material=self._material.text().strip() or "A36",
            thickness=float(self._thickness.text()),
            auto_prop=self._auto_prop.isChecked(),
            group_name=self._group_name.text().strip() or "SIMPLE_PLATE",
        )

    def populate_area_props(self, names: list):
        current = self._area_prop.currentText()
        self._area_prop.clear()
        items = list(names) if names else ["Default"]
        self._area_prop.addItems(items)
        idx = self._area_prop.findText(current)
        self._area_prop.setCurrentIndex(idx if idx >= 0 else 0)

    # ── Slots ─────────────────────────────────────────────────────────────

    def _on_connect(self):
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            props = result.get("shell_props", [])
            self._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self.populate_area_props(props)
            if props:
                self._log_append(f"  Propiedades Shell cargadas: {len(props)}")
            else:
                self._log_append("  Sin propiedades Shell en el modelo (usando 'Default')")
            self._set_connected(True)
        else:
            err = result.get("error", "Error desconocido")
            self._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    def _on_disconnect(self):
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._busy(False)
        self._log_append("✔ Desconectado de SAP2000")
        self.populate_area_props([])
        self._set_connected(False)

    def _on_run(self):
        try:
            config = self._build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return

        self._log_append(
            f"\n─── Generando placa {config.width:.4g}×{config.height:.4g} mm  "
            f"|  malla {config.nx}×{config.ny}  |  θ = {config.angle}° ───"
        )
        self._busy(True)
        self._run_worker = RunWorker(self._backend, config)
        self._run_worker.finished.connect(self._on_run_done)
        self._run_worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Placa generada correctamente")
            self._log_append(
                f"  Áreas creadas       : {result.get('num_areas', '?')}\n"
                f"  Malla               : {result.get('grid', '?')}\n"
                f"  Tamaño celda        : {result.get('cell_size', '?')}\n"
                f"  Ángulo              : {result.get('angle', '?')}°\n"
                f"  Plano               : {result.get('plane', '?')}\n"
                f"  Prop. Shell         : {result.get('shell_prop', '?')}\n"
                f"  Grupo               : {result.get('group', '?')}"
            )
            self._plane.setCurrentIndex(0)
        else:
            self._log_append(f"✘ Error: {result.get('error', 'Error desconocido')}")

    def _on_get_coords(self):
        self._busy(True)
        self._coords_worker = GetCoordsWorker(self._conn)
        self._coords_worker.finished.connect(self._on_get_coords_done)
        self._coords_worker.start()

    def _on_get_coords_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            x, y, z = result["x"], result["y"], result["z"]
            name = result.get("name", "?")
            self._ox.setText(f"{x:.6g}")
            self._oy.setText(f"{y:.6g}")
            self._oz.setText(f"{z:.6g}")
            self._log_append(
                f"📍 Nodo '{name}'  →  X={x:.6g}  Y={y:.6g}  Z={z:.6g}"
            )
        else:
            self._log_append(f"✘ {result.get('error', 'Error desconocido')}")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimplePlateGUI()
    window.show()
    sys.exit(app.exec())
