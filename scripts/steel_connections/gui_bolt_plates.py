"""
GUI — SAP2000 Conexión Pernada: Placas de Conexión + Links Gap (Standalone)
============================================================================
Genera dos placas anulares de conexión enfrentadas para cada perno,
separadas una distancia sep = (t1 + t2) / 2, conectadas nodo a nodo
mediante elementos Link con propiedad Gap (solo compresión).

Conexión directa vía comtypes (sin MCP).
Referencia de estilo: gui_mesh.py

Layout
------
  [Estado de conexión]
  [Conectar]  [Desconectar]
  ┌─ Parámetros ─────────────────────┬─ Preview ─────────┐
  │  Placas / Perno / Discretización  │  Vista superior   │
  │  Ubicación / Propiedades SAP2000  │  Vista lateral    │
  └───────────────────────────────────┴───────────────────┘
  [Generar Placas + Links Gap]
  ┌─ Salida ──────────────────────────────────────────────┐
  │  log...                                               │
  └───────────────────────────────────────────────────────┘
"""

import sys
import math

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QBrush, QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from backend_bolt_plates import BoltPlatesBackend, BoltPlatesConfig, SapConnection


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
        if result.get("connected"):
            try:
                ret = self._conn.sap_model.PropArea.GetNameList(0, [])
                if isinstance(ret, (list, tuple)) and int(ret[-1]) == 0 and int(ret[0]) > 0:
                    result["shell_props"] = list(ret[1])
                else:
                    result["shell_props"] = []
            except Exception:
                result["shell_props"] = []
        self.finished.emit(result)


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.disconnect())


class RunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: BoltPlatesBackend, config: BoltPlatesConfig):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            self.finished.emit(self._backend.run(self._config))
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class GetCoordsWorker(QThread):
    """Obtiene las coordenadas del primer nodo seleccionado en SAP2000."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        try:
            SapModel = self._conn.sap_model
            ret_sel = SapModel.SelectObj.GetSelected(0, [], [])
            if not (isinstance(ret_sel, (list, tuple)) and int(ret_sel[-1]) == 0):
                self.finished.emit({"success": False, "error": "GetSelected falló."})
                return
            num_items = int(ret_sel[0])
            if num_items == 0:
                self.finished.emit({"success": False,
                                    "error": "No hay objetos seleccionados en SAP2000."})
                return
            obj_types = ret_sel[1]
            obj_names = ret_sel[2]
            point_name = None
            for i in range(num_items):
                if int(obj_types[i]) == 1:   # 1 = PointObject
                    point_name = obj_names[i]
                    break
            if not point_name:
                self.finished.emit({"success": False,
                                    "error": "Ningún nodo (PointObject) seleccionado."})
                return
            ret_coord = SapModel.PointObj.GetCoordCartesian(
                point_name, 0.0, 0.0, 0.0, "Global"
            )
            if not (isinstance(ret_coord, (list, tuple)) and int(ret_coord[-1]) == 0):
                self.finished.emit({"success": False,
                                    "error": "GetCoordCartesian falló."})
                return
            self.finished.emit({
                "success": True,
                "name": str(point_name),
                "x": float(ret_coord[0]),
                "y": float(ret_coord[1]),
                "z": float(ret_coord[2]),
            })
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


# ══════════════════════════════════════════════════════════════════════════════
# Preview Widget (QPainter)
# ══════════════════════════════════════════════════════════════════════════════

class BoltPreviewWidget(QWidget):
    """Previsualización en tiempo real: vista superior + vista lateral.

    Vista superior (65 %): malla anular de la placa de conexión.
    Vista lateral  (35 %): esquema de las dos placas separadas por 'sep'
                            con las líneas de los links gap en rojo punteado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 320)
        self.setStyleSheet("background-color: white; border: 1px solid #aaaaaa;")
        self._data: dict = {}

    def update_preview(
        self,
        outer_shape: str,
        outer_dim: float,
        bolt_diam: float,
        na: int,
        nr: int,
        t1: float,
        t2: float,
    ):
        self._data = {
            "outer_shape": outer_shape,
            "outer_dim": outer_dim,
            "bolt_diam": bolt_diam,
            "na": na,
            "nr": nr,
            "t1": t1,
            "t2": t2,
        }
        self.update()

    # ── Dimensión ─────────────────────────────────────────────────────────

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
        painter.drawLine(x1, y1, cx1, cy1)
        painter.drawLine(x2, y2, cx2, cy2)
        painter.drawLine(cx1, cy1, cx2, cy2)
        tick = 4
        ux, uy = dx / length * tick, dy / length * tick
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(cx1 - ux, cy1 - uy, cx1 + ux, cy1 + uy)
        painter.drawLine(cx2 - ux, cy2 - uy, cx2 + ux, cy2 + uy)
        mid_x, mid_y = (cx1 + cx2) / 2, (cy1 + cy2) / 2
        angle = math.degrees(math.atan2(dy, dx))
        if 90 < angle <= 270 or -270 <= angle < -90:
            angle += 180
        painter.setPen(QPen(Qt.black, 1))
        painter.save()
        painter.translate(mid_x, mid_y)
        painter.rotate(angle)
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
        """Malla anular de la placa de conexión vista desde arriba."""
        outer_s = d.get("outer_shape", "Círculo")
        outer_d = d.get("outer_dim", 80.0)
        inner_d = d.get("bolt_diam", 22.0)
        na = max(int(d.get("na", 12)), 3)
        nr = max(int(d.get("nr", 2)), 1)

        if outer_d <= 0 or inner_d <= 0 or inner_d >= outer_d:
            return

        cx, cy = w_px / 2.0, h_px / 2.0
        scale = min(w_px, h_px) / outer_d * 0.55

        def ring_pts(shape, dim, n):
            pts = []
            rad = dim / 2.0
            sh = shape.lower().replace("í", "i").replace("ó", "o")
            for i in range(n):
                if "circulo" in sh or "circle" in sh:
                    ang = -2.0 * math.pi * i / n
                    pts.append((rad * math.cos(ang), rad * math.sin(ang)))
                else:
                    perim = 4.0 * dim
                    dist = i * perim / n
                    if dist < rad:
                        u, v = rad, -dist
                    elif dist < rad + dim:
                        u, v = rad - (dist - rad), -rad
                    elif dist < rad + 2 * dim:
                        u, v = -rad, -rad + (dist - rad - dim)
                    elif dist < rad + 3 * dim:
                        u, v = -rad + (dist - rad - 2 * dim), rad
                    else:
                        u, v = rad, rad - (dist - rad - 3 * dim)
                    pts.append((u, v))
            return pts

        inner_pts = ring_pts("Círculo", inner_d, na)
        outer_pts = ring_pts(outer_s, outer_d, na)

        for r in range(nr + 1):
            frac = r / float(nr)
            pts = []
            for i in range(na):
                u = inner_pts[i][0] + (outer_pts[i][0] - inner_pts[i][0]) * frac
                v = inner_pts[i][1] + (outer_pts[i][1] - inner_pts[i][1]) * frac
                pts.append((cx + u * scale, cy + v * scale))

            pen = QPen(Qt.blue, 2) if r == 0 or r == nr else QPen(Qt.gray, 1)
            painter.setPen(pen)
            for i in range(na):
                p1, p2 = pts[i], pts[(i + 1) % na]
                painter.drawLine(p1[0], p1[1], p2[0], p2[1])

            # Radial lines to next ring
            if r < nr:
                next_frac = (r + 1) / float(nr)
                painter.setPen(QPen(Qt.gray, 1))
                for i in range(na):
                    u1 = inner_pts[i][0] + (outer_pts[i][0] - inner_pts[i][0]) * frac
                    v1 = inner_pts[i][1] + (outer_pts[i][1] - inner_pts[i][1]) * frac
                    u2 = inner_pts[i][0] + (outer_pts[i][0] - inner_pts[i][0]) * next_frac
                    v2 = inner_pts[i][1] + (outer_pts[i][1] - inner_pts[i][1]) * next_frac
                    painter.drawLine(cx + u1 * scale, cy + v1 * scale,
                                     cx + u2 * scale, cy + v2 * scale)

        # Cotas
        r_out_px = outer_d * scale / 2.0
        r_in_px  = inner_d * scale / 2.0
        self._draw_dimension(painter,
                             (cx - r_out_px, cy), (cx + r_out_px, cy),
                             f"Ext: {outer_d:.3g} ({outer_s})", offset=-30)
        self._draw_dimension(painter,
                             (cx - r_in_px, cy + r_in_px * 0.6),
                             (cx + r_in_px, cy + r_in_px * 0.6),
                             f"∅ perno: {inner_d:.3g}", offset=22)

    # ── Vista lateral ─────────────────────────────────────────────────────

    def _draw_side_view(self, painter, x0, y0, w_px, h_px, d):
        """Esquema lateral: dos placas separadas por sep con links gap."""
        t1 = float(d.get("t1", 16.0))
        t2 = float(d.get("t2", 16.0))
        sep = (t1 + t2) / 2.0
        bolt_d = float(d.get("bolt_diam", 22.0))
        outer_d = float(d.get("outer_dim", 80.0))
        nr = max(int(d.get("nr", 2)), 1)

        if sep <= 0 or outer_d <= 0 or bolt_d <= 0 or bolt_d >= outer_d:
            return

        # Línea separadora con vista superior
        painter.setPen(QPen(Qt.lightGray, 1))
        painter.drawLine(int(x0), int(y0), int(x0 + w_px), int(y0))

        cx = x0 + w_px / 2.0
        cy = y0 + h_px / 2.0

        margin = 24
        avail_w = w_px - 2 * margin
        avail_h = h_px - 2 * margin

        # Scale: outer_dim en ancho, sep*2.5 en alto (para que haya margen)
        scale_w = avail_w / outer_d if outer_d > 0 else 1.0
        scale_h = avail_h / (sep * 2.5) if sep > 0 else 1.0
        scale = min(scale_w, scale_h)

        half_w   = outer_d / 2.0 * scale
        half_hole = bolt_d / 2.0 * scale
        half_sep_px = sep / 2.0 * scale

        # Espesor visual mínimo de cada placa
        t1_px = max(4.0, t1 * scale * 0.4)
        t2_px = max(4.0, t2 * scale * 0.4)

        # Centros verticales de cada placa
        y_p1 = cy + half_sep_px   # Placa 1 (abajo)
        y_p2 = cy - half_sep_px   # Placa 2 (arriba)

        # ── Links gap (líneas verticales punteadas rojas) ─────────────────
        # Representamos un subconjunto de los links angulares en la sección
        n_lines = min(8, d.get("na", 12))
        pen_link = QPen(QColor(200, 50, 50), 1)
        pen_link.setStyle(Qt.DashLine)
        painter.setPen(pen_link)

        for idx in range(n_lines + 1):
            frac_x = idx / float(n_lines) if n_lines > 0 else 0.5
            x_link = cx - half_w + frac_x * half_w * 2.0
            if abs(x_link - cx) <= half_hole:
                continue
            painter.drawLine(
                int(x_link), int(y_p2 + t2_px / 2.0),
                int(x_link), int(y_p1 - t1_px / 2.0),
            )

        # ── Placas (dos rectángulos por placa, con orificio central) ──────
        for y_p, t_px in ((y_p1, t1_px), (y_p2, t2_px)):
            painter.setBrush(QBrush(QColor(180, 210, 255, 200)))
            painter.setPen(QPen(Qt.blue, 1.5))
            # Mitad izquierda
            painter.drawRect(
                int(cx - half_w),
                int(y_p - t_px / 2.0),
                int(half_w - half_hole),
                int(t_px),
            )
            # Mitad derecha
            painter.drawRect(
                int(cx + half_hole),
                int(y_p - t_px / 2.0),
                int(half_w - half_hole),
                int(t_px),
            )

        # ── Cota: sep ─────────────────────────────────────────────────────
        dim_x = cx + half_w + 10
        self._draw_dimension(
            painter,
            (dim_x, y_p1), (dim_x, y_p2),
            f"sep={sep:.4g}", offset=16,
        )

        # ── Etiqueta ──────────────────────────────────────────────────────
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setFont(QFont("Arial", 7))
        painter.drawText(
            int(x0 + 4), int(y0 + 11),
            "Vista lateral  (links gap = - - -)",
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

class BoltPlatesGUI(QWidget):
    """Ventana standalone para generación de placas de conexión + links gap."""

    SHAPES = ["Círculo", "Cuadrado"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Conexión Pernada: Placas de Conexión + Gap Links")
        self.setMinimumWidth(740)

        self._conn = SapConnection()
        self._backend = BoltPlatesBackend(self._conn)
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

        # ── Grupo: Placas ─────────────────────────────────────────────────
        grp_plates = QGroupBox("Placas Conectadas")
        g = QGridLayout(grp_plates)
        g.setHorizontalSpacing(12)
        g.setVerticalSpacing(8)

        lbl, self._t1 = _field("Espesor Placa 1:", "16.0",
                                "Espesor de la placa 1 (unidades del modelo)")
        g.addWidget(lbl, 0, 0); g.addWidget(self._t1, 0, 1)

        lbl, self._t2 = _field("Espesor Placa 2:", "16.0",
                                "Espesor de la placa 2 (unidades del modelo)")
        g.addWidget(lbl, 0, 2); g.addWidget(self._t2, 0, 3)

        lbl_sep = QLabel("Separación (sep):")
        lbl_sep.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_sep.setToolTip("sep = (t1 + t2) / 2  — calculado automáticamente")
        self._sep_lbl = QLabel("16.0")
        self._sep_lbl.setStyleSheet("color: #1a6e1a; font-weight: bold;")
        self._sep_lbl.setToolTip("sep = (t1 + t2) / 2")
        g.addWidget(lbl_sep, 1, 0); g.addWidget(self._sep_lbl, 1, 1)

        params_col.addWidget(grp_plates)

        # ── Grupo: Geometría del perno ─────────────────────────────────────
        grp_bolt = QGroupBox("Geometría del Perno / Orificio")
        g2 = QGridLayout(grp_bolt)
        g2.setHorizontalSpacing(12)
        g2.setVerticalSpacing(8)

        lbl, self._bolt_diam = _field("Diám. Perno/Orificio:", "22.0",
                                      "Diámetro del perno = diámetro del orificio interno")
        g2.addWidget(lbl, 0, 0); g2.addWidget(self._bolt_diam, 0, 1)

        lbl, self._outer_dim = _field("Dim. Exterior:", "80.0",
                                      "Diámetro o lado de la placa de conexión")
        g2.addWidget(lbl, 0, 2); g2.addWidget(self._outer_dim, 0, 3)

        lbl_shape = QLabel("Forma exterior:")
        lbl_shape.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._outer_shape = QComboBox()
        self._outer_shape.addItems(self.SHAPES)
        self._outer_shape.setCurrentText("Círculo")
        self._outer_shape.setToolTip("Forma del contorno exterior de la placa de conexión")
        g2.addWidget(lbl_shape, 2, 0); g2.addWidget(self._outer_shape, 2, 1)

        lbl, self._bolt_material = _field("Material Perno:", "A36",
                                           "Material SAP2000 para la sección Frame circular del perno")
        g2.addWidget(lbl, 1, 0); g2.addWidget(self._bolt_material, 1, 1)

        params_col.addWidget(grp_bolt)

        # ── Grupo: Discretización ──────────────────────────────────────────
        grp_disc = QGroupBox("Discretización")
        g3 = QGridLayout(grp_disc)
        g3.setHorizontalSpacing(12)
        g3.setVerticalSpacing(8)

        lbl, self._n_angular = _field("Div. Angulares:", "12",
                                      "Puntos por anillo (>= 3, recomendado 12–16)")
        g3.addWidget(lbl, 0, 0); g3.addWidget(self._n_angular, 0, 1)

        lbl, self._n_radial = _field("Div. Radiales:", "2",
                                     "Anillos entre el orificio y el borde exterior (>= 1)")
        g3.addWidget(lbl, 0, 2); g3.addWidget(self._n_radial, 0, 3)

        params_col.addWidget(grp_disc)

        # ── Grupo: Ubicación ───────────────────────────────────────────────
        grp_loc = QGroupBox("Ubicación del Centro del Perno")
        g4 = QGridLayout(grp_loc)
        g4.setHorizontalSpacing(12)
        g4.setVerticalSpacing(8)

        lbl, self._cx = _field("Centro X:", "0.0")
        g4.addWidget(lbl, 0, 0); g4.addWidget(self._cx, 0, 1)
        lbl, self._cy_f = _field("Centro Y:", "0.0")
        g4.addWidget(lbl, 0, 2); g4.addWidget(self._cy_f, 0, 3)
        lbl, self._cz = _field("Centro Z:", "0.0")
        g4.addWidget(lbl, 1, 0); g4.addWidget(self._cz, 1, 1)

        lbl_plane = QLabel("Plano:")
        lbl_plane.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._plane = QComboBox()
        self._plane.addItems(["", "XY", "XZ", "YZ"])
        self._plane.setCurrentIndex(0)
        self._plane.setToolTip("Plano de las placas de conexión (la separación es perpendicular)")
        g4.addWidget(lbl_plane, 1, 2); g4.addWidget(self._plane, 1, 3)

        self._btn_get_coords = QPushButton("📍 Obtener Nodo")
        self._btn_get_coords.setFixedHeight(26)
        self._btn_get_coords.setEnabled(False)
        self._btn_get_coords.setToolTip(
            "Lee las coordenadas del nodo seleccionado en SAP2000 "
            "y las carga como centro del perno."
        )
        self._btn_get_coords.clicked.connect(self._on_get_coords)
        g4.addWidget(self._btn_get_coords, 2, 0, 1, 4)

        params_col.addWidget(grp_loc)

        # ── Grupo: Propiedades SAP2000 ─────────────────────────────────────
        grp_sap = QGroupBox("Propiedades SAP2000")
        g5 = QGridLayout(grp_sap)
        g5.setHorizontalSpacing(12)
        g5.setVerticalSpacing(8)

        lbl_prop = QLabel("Prop. Área Shell:")
        lbl_prop.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_prop.setToolTip("Sección Shell para las áreas de las placas de conexión")
        self._area_prop = QComboBox()
        self._area_prop.setEditable(True)
        self._area_prop.addItem("Default")
        self._area_prop.setToolTip("Sección Shell para las áreas de las placas de conexión")
        g5.addWidget(lbl_prop, 0, 0); g5.addWidget(self._area_prop, 0, 1)

        lbl, self._gap_name = _field("Nombre Prop. Gap:", "GAP_BOLT",
                                     "Nombre de la propiedad Link Gap a crear en SAP2000")
        g5.addWidget(lbl, 0, 2); g5.addWidget(self._gap_name, 0, 3)

        lbl, self._gap_k = _field("Rigidez Gap:", "1e6",
                                  "Rigidez axial del gap (mismas unidades que el modelo)")
        g5.addWidget(lbl, 1, 0); g5.addWidget(self._gap_k, 1, 1)

        lbl, self._gap_dis = _field("Apertura Inicial:", "0.0",
                                    "Distancia inicial de apertura del gap (normalmente 0)")
        g5.addWidget(lbl, 1, 2); g5.addWidget(self._gap_dis, 1, 3)

        params_col.addWidget(grp_sap)
        params_col.addStretch()

        # ── Preview ───────────────────────────────────────────────────────
        self._preview = BoltPreviewWidget()
        self._preview.setMinimumWidth(280)

        body.addLayout(params_col, 1)
        body.addWidget(self._preview, 1)
        root.addLayout(body)

        # ── Botón generar ─────────────────────────────────────────────────
        self._btn_run = QPushButton("Generar Placas de Conexión + Links Gap")
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
        for w in (self._t1, self._t2, self._bolt_diam, self._outer_dim,
                  self._n_angular, self._n_radial):
            w.textChanged.connect(self._update_preview)
        self._outer_shape.currentTextChanged.connect(self._update_preview)
        self._t1.textChanged.connect(self._update_sep_label)
        self._t2.textChanged.connect(self._update_sep_label)

        self._update_preview()
        self._update_sep_label()

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

    def _update_preview(self):
        try:
            self._preview.update_preview(
                outer_shape=self._outer_shape.currentText(),
                outer_dim=float(self._outer_dim.text()),
                bolt_diam=float(self._bolt_diam.text()),
                na=int(self._n_angular.text()),
                nr=int(self._n_radial.text()),
                t1=float(self._t1.text()),
                t2=float(self._t2.text()),
            )
        except ValueError:
            pass

    def _build_config(self) -> BoltPlatesConfig:
        plane = self._plane.currentText().strip()
        if not plane:
            raise ValueError("Debe seleccionar un Plano antes de generar.")
        return BoltPlatesConfig(
            plate_thickness_1=float(self._t1.text()),
            plate_thickness_2=float(self._t2.text()),
            bolt_diameter=float(self._bolt_diam.text()),
            outer_dim=float(self._outer_dim.text()),
            outer_shape=self._outer_shape.currentText(),
            num_angular=int(self._n_angular.text()),
            num_radial=int(self._n_radial.text()),
            bolt_center_x=float(self._cx.text()),
            bolt_center_y=float(self._cy_f.text()),
            bolt_center_z=float(self._cz.text()),
            plane=plane,
            area_prop=self._area_prop.currentText().strip() or "Default",
            gap_prop_name=self._gap_name.text().strip() or "GAP_BOLT",
            gap_stiffness=float(self._gap_k.text()),
            initial_gap=float(self._gap_dis.text()),
            bolt_material=self._bolt_material.text().strip() or "A36",
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
                self._log_append(
                    f"  Propiedades Shell cargadas: {len(props)}"
                )
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

        sep = (config.plate_thickness_1 + config.plate_thickness_2) / 2.0
        self._log_append(
            f"\n─── Generando placas de conexión  |  sep = {sep:.4g}  |  "
            f"links = {(config.num_radial + 1) * config.num_angular} ───"
        )
        self._busy(True)
        self._run_worker = RunWorker(self._backend, config)
        self._run_worker.finished.connect(self._on_run_done)
        self._run_worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Generado correctamente")
            bar_info = result.get('bolt_bar') or "—"
            sec_info = result.get('bolt_section') or "—"
            body_names = result.get('body_names', [])
            body_info = ", ".join(body_names) if body_names else "—"
            self._log_append(
                f"  Áreas creadas      : {result.get('num_areas', '?')}\n"
                f"  Puntos creados     : {result.get('num_points', '?')}\n"
                f"  Links gap          : {result.get('num_links', '?')}\n"
                f"  Barra perno        : {bar_info}  (secc. {sec_info})\n"
                f"  Body constraints   : {result.get('body_constraints', '?')}  [{body_info}]\n"
                f"  Separación         : {result.get('separation', '?'):.4g}\n"
                f"  Prop. gap          : {result.get('gap_prop', '?')}\n"
                f"  Plano              : {result.get('plane', '?')}"
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
            self._cx.setText(f"{x:.6g}")
            self._cy_f.setText(f"{y:.6g}")
            self._cz.setText(f"{z:.6g}")
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
    window = BoltPlatesGUI()
    window.show()
    sys.exit(app.exec())
