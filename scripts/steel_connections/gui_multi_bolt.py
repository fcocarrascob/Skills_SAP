"""
GUI — SAP2000 Patrón Multi-Perno (Standalone)
===============================================
Genera un patrón de múltiples pernos (filas × columnas) con soporte
para orientación arbitraria, preview en tiempo real y ejecución en SAP2000.

Conexión directa vía comtypes (sin MCP).
Referencia de estilo: gui_bolt_plates.py

Layout
------
  [Estado de conexión]
  [Conectar]  [Desconectar]
  ┌─ Parámetros ─────────────────────┬─ Preview ─────────┐
  │  Patrón / Perno / Placas         │  Vista superior   │
  │  Discretización / Orientación    │  (grilla pernos)  │
  │  Ubicación / Propiedades SAP2000 │  Vista lateral    │
  └───────────────────────────────────┴───────────────────┘
  [Generar Patrón Multi-Perno]
  ┌─ Salida ──────────────────────────────────────────────┐
  │  log...                                               │
  └───────────────────────────────────────────────────────┘
"""

import sys
import math

from PySide6.QtCore import Qt, QPointF, QThread, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
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
from backend_multi_bolt import MultiBoltBackend, MultiBoltConfig, _generate_grid_centers


# ══════════════════════════════════════════════════════════════════════════════
# Preview Widget (QPainter)
# ══════════════════════════════════════════════════════════════════════════════

class MultiBoltPreviewWidget(QWidget):
    """Previsualización en tiempo real: vista superior + vista lateral.

    Vista superior (65 %): patrón de pernos en grilla con rotación.
    Vista lateral  (35 %): esquema de las dos placas separadas por 'sep'.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 320)
        self.setStyleSheet("background-color: white; border: 1px solid #aaaaaa;")
        self._data: dict = {}

    def update_preview(
        self,
        n_rows: int,
        n_cols: int,
        spacing_h: float,
        spacing_v: float,
        bolt_diam: float,
        outer_dim: float,
        outer_shape: str,
        t1: float,
        t2: float,
        angle: float,
    ):
        self._data = {
            "n_rows": n_rows, "n_cols": n_cols,
            "spacing_h": spacing_h, "spacing_v": spacing_v,
            "bolt_diam": bolt_diam, "outer_dim": outer_dim,
            "outer_shape": outer_shape,
            "t1": t1, "t2": t2, "angle": angle,
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
        w, h = self.width(), self.height()
        top_h = int(h * 0.65)
        side_h = h - top_h
        self._draw_top_view(painter, w, top_h, d)
        self._draw_side_view(painter, 0, top_h, w, side_h, d)

    # ── Vista superior ────────────────────────────────────────────────────

    def _draw_top_view(self, painter, w_px, h_px, d):
        """Patrón de pernos en grilla con rotación por ángulo."""
        n_rows = max(int(d.get("n_rows", 2)), 1)
        n_cols = max(int(d.get("n_cols", 3)), 1)
        spacing_h = float(d.get("spacing_h", 75.0))
        spacing_v = float(d.get("spacing_v", 75.0))
        bolt_diam = float(d.get("bolt_diam", 22.0))
        outer_dim = float(d.get("outer_dim", 50.0))
        outer_shape = d.get("outer_shape", "Círculo")
        angle = float(d.get("angle", 0.0))

        if bolt_diam <= 0 or outer_dim <= 0 or outer_dim <= bolt_diam:
            return
        if spacing_h <= 0 or spacing_v <= 0:
            return

        # Etiqueta
        n_total = n_rows * n_cols
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setFont(QFont("Arial", 7))
        angle_txt = f"  θ={angle:.1f}°" if abs(angle) > 0.01 else ""
        painter.drawText(
            4, 11,
            f"Vista superior — {n_total} pernos ({n_rows}×{n_cols}){angle_txt}",
        )

        # Dimensiones del patrón
        total_w = (n_cols - 1) * spacing_h + outer_dim
        total_h = (n_rows - 1) * spacing_v + outer_dim

        # Escala
        margin = 50
        avail_w = w_px - 2 * margin
        avail_h = h_px - 2 * margin - 14  # espacio para etiqueta

        # Si hay ángulo, el bounding box rotado es mayor
        theta = math.radians(angle)
        cos_a, sin_a = math.cos(theta), math.sin(theta)
        # Bounding box rotado: considerar las 4 esquinas del patrón
        hw, hh = total_w / 2.0, total_h / 2.0
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        rot_corners = [(c[0] * cos_a - c[1] * sin_a,
                        c[0] * sin_a + c[1] * cos_a) for c in corners]
        min_ru = min(c[0] for c in rot_corners)
        max_ru = max(c[0] for c in rot_corners)
        min_rv = min(c[1] for c in rot_corners)
        max_rv = max(c[1] for c in rot_corners)
        rot_w = max_ru - min_ru
        rot_h = max_rv - min_rv

        if rot_w <= 0 or rot_h <= 0:
            return

        scale = min(avail_w / rot_w, avail_h / rot_h) * 0.85
        cx = w_px / 2.0
        cy = h_px / 2.0 + 7  # compensar etiqueta

        # Generar centros
        centers = _generate_grid_centers(n_rows, n_cols, spacing_h, spacing_v)

        # Transformar a píxeles (con rotación)
        def to_px(u, v):
            ru = u * cos_a - v * sin_a
            rv = u * sin_a + v * cos_a
            return cx + ru * scale, cy - rv * scale

        # Dibujar líneas de grilla (conectar filas y columnas)
        pen_grid = QPen(QColor(200, 200, 200), 1, Qt.DashLine)
        painter.setPen(pen_grid)
        painter.setBrush(Qt.NoBrush)

        for row in range(n_rows):
            for col in range(n_cols - 1):
                idx1 = row * n_cols + col
                idx2 = idx1 + 1
                px1, py1 = to_px(*centers[idx1])
                px2, py2 = to_px(*centers[idx2])
                painter.drawLine(int(px1), int(py1), int(px2), int(py2))

        for col in range(n_cols):
            for row in range(n_rows - 1):
                idx1 = row * n_cols + col
                idx2 = (row + 1) * n_cols + col
                px1, py1 = to_px(*centers[idx1])
                px2, py2 = to_px(*centers[idx2])
                painter.drawLine(int(px1), int(py1), int(px2), int(py2))

        # Dibujar cada perno
        r_inner = bolt_diam / 2.0 * scale
        r_outer = outer_dim / 2.0 * scale
        is_circle = "circulo" in outer_shape.lower().replace("í", "i")

        for u, v in centers:
            bx, by = to_px(u, v)

            # Forma exterior (arandela)
            painter.setPen(QPen(QColor(150, 150, 150), 1))
            painter.setBrush(QBrush(QColor(210, 225, 245, 100)))
            if is_circle:
                painter.drawEllipse(QPointF(bx, by), r_outer, r_outer)
            else:
                painter.save()
                painter.translate(bx, by)
                painter.rotate(-angle)  # rotar el cuadrado con el patrón
                painter.drawRect(
                    int(-r_outer), int(-r_outer),
                    int(2 * r_outer), int(2 * r_outer),
                )
                painter.restore()

            # Orificio del perno (circle siempre)
            painter.setPen(QPen(QColor(50, 100, 200), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(bx, by), r_inner, r_inner)

            # Centro
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(30, 60, 150)))
            painter.drawEllipse(QPointF(bx, by), 2, 2)

        # ── Cotas ────────────────────────────────────────────────────────
        if n_cols >= 2:
            px1, py1 = to_px(*centers[0])
            px2, py2 = to_px(*centers[1])
            self._draw_dimension(
                painter, (px1, py1), (px2, py2),
                f"sh={spacing_h:.4g}", offset=-22,
            )

        if n_rows >= 2:
            px1, py1 = to_px(*centers[0])
            px2, py2 = to_px(*centers[n_cols])
            self._draw_dimension(
                painter, (px1, py1), (px2, py2),
                f"sv={spacing_v:.4g}", offset=22,
            )

    # ── Vista lateral ─────────────────────────────────────────────────────

    def _draw_side_view(self, painter, x0, y0, w_px, h_px, d):
        """Esquema lateral: corte por una fila mostrando las dos placas."""
        t1 = float(d.get("t1", 16.0))
        t2 = float(d.get("t2", 16.0))
        sep = (t1 + t2) / 2.0
        n_cols = max(int(d.get("n_cols", 3)), 1)
        spacing_h = float(d.get("spacing_h", 75.0))
        bolt_diam = float(d.get("bolt_diam", 22.0))
        outer_dim = float(d.get("outer_dim", 50.0))

        if sep <= 0 or outer_dim <= 0 or bolt_diam <= 0:
            return

        # Línea separadora
        painter.setPen(QPen(Qt.lightGray, 1))
        painter.drawLine(int(x0), int(y0), int(x0 + w_px), int(y0))

        # Etiqueta
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setFont(QFont("Arial", 7))
        painter.drawText(
            int(x0 + 4), int(y0 + 11),
            f"Vista lateral — sep={sep:.4g}  (links gap = - - -)",
        )

        cx = x0 + w_px / 2.0
        cy = y0 + h_px / 2.0 + 5

        # Ancho total del corte (una fila)
        total_w = (n_cols - 1) * spacing_h + outer_dim
        margin = 30
        avail_w = w_px - 2 * margin
        avail_h = h_px - 2 * margin - 10

        scale_w = avail_w / total_w if total_w > 0 else 1.0
        scale_h = avail_h / (sep * 2.5) if sep > 0 else 1.0
        scale = min(scale_w, scale_h)

        half_sep_px = sep / 2.0 * scale
        t1_px = max(4.0, t1 * scale * 0.4)
        t2_px = max(4.0, t2 * scale * 0.4)

        y_p1 = cy + half_sep_px   # Placa 1 (abajo)
        y_p2 = cy - half_sep_px   # Placa 2 (arriba)

        # Centros de pernos en la fila (centrados en 0)
        bolt_xs = []
        total_row_w = (n_cols - 1) * spacing_h
        for col in range(n_cols):
            u = col * spacing_h - total_row_w / 2.0
            bolt_xs.append(cx + u * scale)

        half_hole = bolt_diam / 2.0 * scale
        half_outer = outer_dim / 2.0 * scale

        # ── Links gap (líneas rojas punteadas) ───────────────────────────
        pen_link = QPen(QColor(200, 50, 50), 1)
        pen_link.setStyle(Qt.DashLine)
        painter.setPen(pen_link)

        for bx in bolt_xs:
            # Dos líneas de link a cada lado del orificio
            for dx in (-half_outer * 0.7, -half_outer * 0.35,
                       half_outer * 0.35, half_outer * 0.7):
                painter.drawLine(
                    int(bx + dx), int(y_p2 + t2_px / 2.0),
                    int(bx + dx), int(y_p1 - t1_px / 2.0),
                )

        # ── Placas (rectángulos con orificios) ───────────────────────────
        for y_p, t_px in ((y_p1, t1_px), (y_p2, t2_px)):
            painter.setBrush(QBrush(QColor(180, 210, 255, 200)))
            painter.setPen(QPen(Qt.blue, 1.5))

            # Dibujar segmentos de placa entre pernos
            total_half = total_w / 2.0 * scale
            left_edge = cx - total_half

            # Borde izquierdo hasta primer orificio
            if bolt_xs:
                seg_left = bolt_xs[0] - half_hole
                if seg_left > left_edge:
                    painter.drawRect(
                        int(left_edge), int(y_p - t_px / 2.0),
                        int(seg_left - left_edge), int(t_px),
                    )

                # Segmentos entre orificios
                for k in range(len(bolt_xs) - 1):
                    seg_l = bolt_xs[k] + half_hole
                    seg_r = bolt_xs[k + 1] - half_hole
                    if seg_r > seg_l:
                        painter.drawRect(
                            int(seg_l), int(y_p - t_px / 2.0),
                            int(seg_r - seg_l), int(t_px),
                        )

                # Último orificio hasta borde derecho
                right_edge = cx + total_half
                seg_right = bolt_xs[-1] + half_hole
                if right_edge > seg_right:
                    painter.drawRect(
                        int(seg_right), int(y_p - t_px / 2.0),
                        int(right_edge - seg_right), int(t_px),
                    )

        # ── Cota: sep ─────────────────────────────────────────────────────
        dim_x = cx + total_w / 2.0 * scale + 12
        self._draw_dimension(
            painter,
            (dim_x, y_p1), (dim_x, y_p2),
            f"sep={sep:.4g}", offset=16,
        )


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
# Ventana principal
# ══════════════════════════════════════════════════════════════════════════════

class MultiBoltGUI(QWidget):
    """Ventana standalone para generación de patrón multi-perno."""

    SHAPES = ["Círculo", "Cuadrado"]

    def __init__(self, connection: SapConnection = None):
        super().__init__()
        self.setWindowTitle("SAP2000 — Patrón Multi-Perno")
        self.setMinimumWidth(740)

        self._conn = connection or SapConnection()
        self._backend = MultiBoltBackend(self._conn)
        self._worker = None
        self._run_worker = None
        self._coords_worker = None

        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Estado y conexión ─────────────────────────────────────────────
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        root.addWidget(self._status_lbl)

        conn_row = QHBoxLayout()
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)

        self._btn_disconnect = QPushButton("Desconectar")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)

        conn_row.addWidget(self._btn_connect)
        conn_row.addWidget(self._btn_disconnect)
        root.addLayout(conn_row)

        # ── Cuerpo: parámetros │ preview ──────────────────────────────────
        body = QHBoxLayout()
        body.setSpacing(10)
        params_col = QVBoxLayout()
        params_col.setSpacing(8)

        # ── Grupo: Patrón de Pernos ───────────────────────────────────────
        grp_pattern = QGroupBox("Patrón de Pernos")
        g1 = QGridLayout(grp_pattern)
        g1.setHorizontalSpacing(12)
        g1.setVerticalSpacing(8)

        lbl, self._n_rows = _field("Filas:", "2", "Número de filas de pernos (≥ 1)")
        g1.addWidget(lbl, 0, 0); g1.addWidget(self._n_rows, 0, 1)

        lbl, self._n_cols = _field("Columnas:", "3", "Número de columnas de pernos (≥ 1)")
        g1.addWidget(lbl, 0, 2); g1.addWidget(self._n_cols, 0, 3)

        lbl, self._spacing_h = _field(
            "Espac. Horizontal:", "75.0",
            "Separación horizontal entre pernos (unidades del modelo)",
        )
        g1.addWidget(lbl, 1, 0); g1.addWidget(self._spacing_h, 1, 1)

        lbl, self._spacing_v = _field(
            "Espac. Vertical:", "75.0",
            "Separación vertical entre pernos (unidades del modelo)",
        )
        g1.addWidget(lbl, 1, 2); g1.addWidget(self._spacing_v, 1, 3)

        lbl_total = QLabel("Total pernos:")
        lbl_total.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._total_lbl = QLabel("6")
        self._total_lbl.setStyleSheet("color: #1a6e1a; font-weight: bold;")
        g1.addWidget(lbl_total, 2, 0); g1.addWidget(self._total_lbl, 2, 1)

        params_col.addWidget(grp_pattern)

        # ── Grupo: Perno / Orificio ───────────────────────────────────────
        grp_bolt = QGroupBox("Perno / Orificio")
        g2 = QGridLayout(grp_bolt)
        g2.setHorizontalSpacing(12)
        g2.setVerticalSpacing(8)

        lbl, self._bolt_diam = _field(
            "Diám. Perno:", "22.0",
            "Diámetro del perno = diámetro del orificio interno",
        )
        g2.addWidget(lbl, 0, 0); g2.addWidget(self._bolt_diam, 0, 1)

        lbl, self._outer_dim = _field(
            "Dim. Exterior:", "50.0",
            "Diámetro o lado de la arandela de conexión",
        )
        g2.addWidget(lbl, 0, 2); g2.addWidget(self._outer_dim, 0, 3)

        lbl_shape = QLabel("Forma exterior:")
        lbl_shape.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._outer_shape = QComboBox()
        self._outer_shape.addItems(self.SHAPES)
        self._outer_shape.setCurrentText("Círculo")
        g2.addWidget(lbl_shape, 1, 0); g2.addWidget(self._outer_shape, 1, 1)

        lbl, self._bolt_material = _field(
            "Material Perno:", "A36",
            "Material SAP2000 para la sección Frame circular del perno",
        )
        g2.addWidget(lbl, 1, 2); g2.addWidget(self._bolt_material, 1, 3)

        params_col.addWidget(grp_bolt)

        # ── Grupo: Placas ─────────────────────────────────────────────────
        grp_plates = QGroupBox("Placas Conectadas")
        g3 = QGridLayout(grp_plates)
        g3.setHorizontalSpacing(12)
        g3.setVerticalSpacing(8)

        lbl, self._t1 = _field("Espesor Placa 1:", "16.0",
                                "Espesor de la placa 1 (unidades del modelo)")
        g3.addWidget(lbl, 0, 0); g3.addWidget(self._t1, 0, 1)

        lbl, self._t2 = _field("Espesor Placa 2:", "16.0",
                                "Espesor de la placa 2 (unidades del modelo)")
        g3.addWidget(lbl, 0, 2); g3.addWidget(self._t2, 0, 3)

        lbl_sep = QLabel("Separación (sep):")
        lbl_sep.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_sep.setToolTip("sep = (t1 + t2) / 2  — calculado automáticamente")
        self._sep_lbl = QLabel("16.0")
        self._sep_lbl.setStyleSheet("color: #1a6e1a; font-weight: bold;")
        g3.addWidget(lbl_sep, 1, 0); g3.addWidget(self._sep_lbl, 1, 1)

        params_col.addWidget(grp_plates)

        # ── Grupo: Discretización ──────────────────────────────────────────
        grp_disc = QGroupBox("Discretización")
        g4 = QGridLayout(grp_disc)
        g4.setHorizontalSpacing(12)
        g4.setVerticalSpacing(8)

        lbl, self._n_angular = _field("Div. Angulares:", "12",
                                      "Puntos por anillo (≥ 3, recomendado 12–16)")
        g4.addWidget(lbl, 0, 0); g4.addWidget(self._n_angular, 0, 1)

        lbl, self._n_radial = _field("Div. Radiales:", "2",
                                     "Anillos entre el orificio y el borde exterior (≥ 1)")
        g4.addWidget(lbl, 0, 2); g4.addWidget(self._n_radial, 0, 3)

        params_col.addWidget(grp_disc)

        # ── Grupo: Orientación ────────────────────────────────────────────
        grp_orient = QGroupBox("Orientación")
        g5 = QGridLayout(grp_orient)
        g5.setHorizontalSpacing(12)
        g5.setVerticalSpacing(8)

        lbl_plane = QLabel("Plano:")
        lbl_plane.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_plane.setToolTip("Plano de las placas (la separación es perpendicular)")
        self._plane = QComboBox()
        self._plane.addItems(["", "XY", "XZ", "YZ"])
        self._plane.setCurrentIndex(0)
        g5.addWidget(lbl_plane, 0, 0); g5.addWidget(self._plane, 0, 1)

        lbl, self._angle = _field(
            "Ángulo θ:", "0.0",
            "Inclinación del patrón en grados dentro del plano (0°=horizontal)",
        )
        g5.addWidget(lbl, 0, 2); g5.addWidget(self._angle, 0, 3)

        params_col.addWidget(grp_orient)

        # ── Grupo: Ubicación ──────────────────────────────────────────────
        grp_loc = QGroupBox("Ubicación (centro del patrón)")
        g6 = QGridLayout(grp_loc)
        g6.setHorizontalSpacing(12)
        g6.setVerticalSpacing(8)

        lbl, self._ox = _field("X:", "0.0")
        g6.addWidget(lbl, 0, 0); g6.addWidget(self._ox, 0, 1)
        lbl, self._oy = _field("Y:", "0.0")
        g6.addWidget(lbl, 0, 2); g6.addWidget(self._oy, 0, 3)
        lbl, self._oz = _field("Z:", "0.0")
        g6.addWidget(lbl, 1, 0); g6.addWidget(self._oz, 1, 1)

        self._btn_get_coords = QPushButton("📍 Obtener Nodo")
        self._btn_get_coords.setFixedHeight(26)
        self._btn_get_coords.setEnabled(False)
        self._btn_get_coords.setToolTip(
            "Lee las coordenadas del nodo seleccionado en SAP2000 "
            "y las carga como centro del patrón."
        )
        self._btn_get_coords.clicked.connect(self._on_get_coords)
        g6.addWidget(self._btn_get_coords, 2, 0, 1, 4)

        params_col.addWidget(grp_loc)

        # ── Grupo: Propiedades SAP2000 ─────────────────────────────────────
        grp_sap = QGroupBox("Propiedades SAP2000")
        g7 = QGridLayout(grp_sap)
        g7.setHorizontalSpacing(12)
        g7.setVerticalSpacing(8)

        lbl_prop = QLabel("Prop. Área Shell:")
        lbl_prop.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._area_prop = QComboBox()
        self._area_prop.setEditable(True)
        self._area_prop.addItem("Default")
        g7.addWidget(lbl_prop, 0, 0); g7.addWidget(self._area_prop, 0, 1)

        lbl, self._gap_name = _field("Nombre Prop. Gap:", "GAP_BOLT",
                                     "Nombre de la propiedad Link Gap")
        g7.addWidget(lbl, 0, 2); g7.addWidget(self._gap_name, 0, 3)

        lbl, self._gap_k = _field("Rigidez Gap:", "1e6",
                                  "Rigidez axial del gap")
        g7.addWidget(lbl, 1, 0); g7.addWidget(self._gap_k, 1, 1)

        lbl, self._gap_dis = _field("Apertura Inicial:", "0.0",
                                    "Distancia inicial del gap")
        g7.addWidget(lbl, 1, 2); g7.addWidget(self._gap_dis, 1, 3)

        lbl, self._group_name = _field("Grupo:", "MULTI_BOLT",
                                       "Nombre del grupo SAP2000")
        g7.addWidget(lbl, 2, 0); g7.addWidget(self._group_name, 2, 1)

        params_col.addWidget(grp_sap)
        params_col.addStretch()

        # ── Preview ───────────────────────────────────────────────────────
        self._preview = MultiBoltPreviewWidget()
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
        self._btn_run = QPushButton("Generar Patrón Multi-Perno")
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
        self._log.setMinimumHeight(140)
        log_layout.addWidget(self._log)
        root.addWidget(grp_log)

        # ── Señales preview ───────────────────────────────────────────────
        for w in (self._n_rows, self._n_cols, self._spacing_h, self._spacing_v,
                  self._bolt_diam, self._outer_dim, self._t1, self._t2,
                  self._n_angular, self._n_radial, self._angle):
            w.textChanged.connect(self._update_preview)

        self._outer_shape.currentTextChanged.connect(self._update_preview)

        self._t1.textChanged.connect(self._update_sep_label)
        self._t2.textChanged.connect(self._update_sep_label)

        self._n_rows.textChanged.connect(self._update_total_label)
        self._n_cols.textChanged.connect(self._update_total_label)

        self._update_preview()
        self._update_sep_label()
        self._update_total_label()

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

    def _update_sep_label(self):
        try:
            t1 = float(self._t1.text())
            t2 = float(self._t2.text())
            sep = (t1 + t2) / 2.0
            self._sep_lbl.setText(f"{sep:.4g}")
        except ValueError:
            self._sep_lbl.setText("—")

    def _update_total_label(self):
        try:
            n = int(self._n_rows.text()) * int(self._n_cols.text())
            self._total_lbl.setText(str(n))
        except ValueError:
            self._total_lbl.setText("—")

    def _update_preview(self):
        try:
            self._preview.update_preview(
                n_rows=int(self._n_rows.text()),
                n_cols=int(self._n_cols.text()),
                spacing_h=float(self._spacing_h.text()),
                spacing_v=float(self._spacing_v.text()),
                bolt_diam=float(self._bolt_diam.text()),
                outer_dim=float(self._outer_dim.text()),
                outer_shape=self._outer_shape.currentText(),
                t1=float(self._t1.text()),
                t2=float(self._t2.text()),
                angle=float(self._angle.text()),
            )
        except ValueError:
            pass

    def _build_config(self) -> MultiBoltConfig:
        plane = self._plane.currentText().strip()
        if not plane:
            raise ValueError("Debe seleccionar un Plano antes de generar.")
        return MultiBoltConfig(
            n_rows=int(self._n_rows.text()),
            n_cols=int(self._n_cols.text()),
            spacing_h=float(self._spacing_h.text()),
            spacing_v=float(self._spacing_v.text()),
            plate_thickness_1=float(self._t1.text()),
            plate_thickness_2=float(self._t2.text()),
            bolt_diameter=float(self._bolt_diam.text()),
            outer_dim=float(self._outer_dim.text()),
            outer_shape=self._outer_shape.currentText(),
            num_angular=int(self._n_angular.text()),
            num_radial=int(self._n_radial.text()),
            origin_x=float(self._ox.text()),
            origin_y=float(self._oy.text()),
            origin_z=float(self._oz.text()),
            plane=plane,
            angle=float(self._angle.text()),
            area_prop=self._area_prop.currentText().strip() or "Default",
            gap_prop_name=self._gap_name.text().strip() or "GAP_BOLT",
            gap_stiffness=float(self._gap_k.text()),
            initial_gap=float(self._gap_dis.text()),
            bolt_material=self._bolt_material.text().strip() or "A36",
            group_name=self._group_name.text().strip() or "MULTI_BOLT",
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

        n_total = config.n_rows * config.n_cols
        sep = (config.plate_thickness_1 + config.plate_thickness_2) / 2.0
        links_per_bolt = (config.num_radial + 1) * config.num_angular
        self._log_append(
            f"\n─── Generando {n_total} pernos ({config.n_rows}×{config.n_cols})  "
            f"|  sep = {sep:.4g}  |  links/perno = {links_per_bolt}  "
            f"|  θ = {config.angle}° ───"
        )
        self._busy(True)
        self._run_worker = RunWorker(self._backend, config)
        self._run_worker.finished.connect(self._on_run_done)
        self._run_worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Patrón generado correctamente")
            self._log_append(
                f"  Patrón              : {result.get('pattern', '?')}\n"
                f"  Pernos creados      : {result.get('num_bolts', '?')}\n"
                f"  Áreas creadas       : {result.get('num_areas', '?')}\n"
                f"  Puntos creados      : {result.get('num_points', '?')}\n"
                f"  Links gap           : {result.get('num_links', '?')}\n"
                f"  Body constraints    : {result.get('body_constraints', '?')}\n"
                f"  Separación          : {result.get('separation', '?'):.4g}\n"
                f"  Ángulo              : {result.get('angle', '?')}°\n"
                f"  Plano               : {result.get('plane', '?')}\n"
                f"  Prop. gap           : {result.get('gap_prop', '?')}\n"
                f"  Sección perno       : {result.get('bolt_section', '?')}\n"
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
    window = MultiBoltGUI()
    window.show()
    sys.exit(app.exec())
