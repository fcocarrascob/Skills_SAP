"""
GUI — SAP2000 Perfiles de Acero como Placas Shell (Standalone)
===============================================================
Modela perfiles de acero estándar (W, HSS, L, C) como conjuntos de
elementos Area (Shell) que representan alas, almas y paredes del perfil.

Conexión directa vía comtypes (sin MCP).
Referencia de estilo: gui_bolt_plates.py

Layout
------
  [Estado de conexión]
  [Conectar]  [Desconectar]
  ┌─ Parámetros ─────────────────────┬─ Preview ─────────┐
  │  Tipo / Sección / Orientación    │  Sección transv.  │
  │  Discretización / Ubicación      │  Vista lateral    │
  └───────────────────────────────────┴───────────────────┘
  [Generar Perfil]
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
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from backend_bolt_plates import SapConnection
from backend_steel_profiles import SteelProfileBackend, SteelProfileConfig


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

    def __init__(self, backend: SteelProfileBackend, config: SteelProfileConfig):
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
                if int(obj_types[i]) == 1:
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
# Preview Widget
# ══════════════════════════════════════════════════════════════════════════════

class ProfilePreviewWidget(QWidget):
    """Previsualización: sección transversal (65%) + vista lateral (35%)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 320)
        self.setStyleSheet("background-color: white; border: 1px solid #aaaaaa;")
        self._data: dict = {}

    def update_preview(self, profile_type: str, dims: dict,
                       length: float, angle: float):
        self._data = {
            "profile_type": profile_type,
            "dims": dims,
            "length": length,
            "angle": angle,
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
        self._draw_cross_section(painter, w, top_h, d)
        self._draw_side_view(painter, 0, top_h, w, side_h, d)

    # ── Sección transversal ───────────────────────────────────────────────

    def _get_plates(self, ptype, dims):
        """Retorna lista de (nombre, cd, cw, plate_h, plate_w)."""
        if ptype == "W":
            d = dims.get("d", 0.3)
            bf = dims.get("bf", 0.15)
            tf = dims.get("tf", 0.01)
            tw = dims.get("tw", 0.007)
            hw = d - 2 * tf
            return [
                ("Ala sup.", d / 2 - tf / 2, 0.0, tf, bf),
                ("Alma", 0.0, 0.0, hw, tw),
                ("Ala inf.", -d / 2 + tf / 2, 0.0, tf, bf),
            ]
        elif ptype == "HSS":
            B = dims.get("B", 0.2)
            H = dims.get("H", 0.2)
            t = dims.get("t_hss", 0.008)
            hw = H - 2 * t
            return [
                ("Top", H / 2 - t / 2, 0.0, t, B),
                ("Bot", -H / 2 + t / 2, 0.0, t, B),
                ("Left", 0.0, -B / 2 + t / 2, hw, t),
                ("Right", 0.0, B / 2 - t / 2, hw, t),
            ]
        elif ptype == "L":
            b1 = dims.get("b1", 0.1)
            b2 = dims.get("b2", 0.1)
            t = dims.get("t_angle", 0.01)
            return [
                ("Vert.", b1 / 2, t / 2, b1, t),
                ("Horiz.", t / 2, b2 / 2, t, b2),
            ]
        else:  # C
            d = dims.get("d", 0.25)
            bf = dims.get("bf", 0.1)
            tf = dims.get("tf", 0.012)
            tw = dims.get("tw", 0.006)
            hw = d - 2 * tf
            return [
                ("Alma", 0.0, -bf / 2 + tw / 2, hw, tw),
                ("Ala sup.", d / 2 - tf / 2, 0.0, tf, bf),
                ("Ala inf.", -d / 2 + tf / 2, 0.0, tf, bf),
            ]

    def _draw_cross_section(self, painter, w_px, h_px, d):
        """Dibuja la sección transversal del perfil."""
        ptype = d.get("profile_type", "W")
        dims = d.get("dims", {})
        plates = self._get_plates(ptype, dims)
        if not plates:
            return

        # Calcular bounding box de la sección
        all_corners = []
        for _, cd, cw, ph, pw in plates:
            all_corners.append((cw - pw / 2, cd - ph / 2))
            all_corners.append((cw + pw / 2, cd + ph / 2))
        min_w = min(c[0] for c in all_corners)
        max_w = max(c[0] for c in all_corners)
        min_d = min(c[1] for c in all_corners)
        max_d = max(c[1] for c in all_corners)

        sec_w = max_w - min_w
        sec_h = max_d - min_d
        if sec_w <= 0 or sec_h <= 0:
            return

        margin = 40
        avail_w = w_px - 2 * margin
        avail_h = h_px - 2 * margin
        scale = min(avail_w / sec_w, avail_h / sec_h) * 0.85

        cx_px = w_px / 2.0
        cy_px = h_px / 2.0
        center_w = (min_w + max_w) / 2.0
        center_d = (min_d + max_d) / 2.0

        # Etiqueta
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setFont(QFont("Arial", 7))
        painter.drawText(4, 11, f"Sección transversal — Perfil {ptype}")

        # Dibujar cada placa como rectángulo
        fill_colors = [
            QColor(100, 150, 220, 180),
            QColor(80, 180, 120, 180),
            QColor(220, 140, 80, 180),
            QColor(180, 100, 180, 180),
        ]

        for idx, (name, cd, cw, ph, pw) in enumerate(plates):
            # Esquina superior izquierda en píxeles
            px = cx_px + (cw - pw / 2 - center_w) * scale
            py = cy_px - (cd + ph / 2 - center_d) * scale  # Y invertido
            pw_px = pw * scale
            ph_px = ph * scale

            color = fill_colors[idx % len(fill_colors)]
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.black, 1.5))
            painter.drawRect(int(px), int(py), max(int(pw_px), 1), max(int(ph_px), 1))

        # Cotas: peralte total y ancho total
        top_y = cy_px - (max_d - center_d) * scale
        bot_y = cy_px - (min_d - center_d) * scale
        left_x = cx_px + (min_w - center_w) * scale
        right_x = cx_px + (max_w - center_w) * scale

        self._draw_dimension(painter,
                             (right_x + 5, bot_y), (right_x + 5, top_y),
                             f"d={sec_h * 1000:.4g}mm", offset=20)
        self._draw_dimension(painter,
                             (left_x, bot_y + 5), (right_x, bot_y + 5),
                             f"bf={sec_w * 1000:.4g}mm", offset=20)

    # ── Vista lateral ─────────────────────────────────────────────────────

    def _draw_side_view(self, painter, x0, y0, w_px, h_px, d):
        """Vista lateral: perfil con la inclinación indicada."""
        length = d.get("length", 3.0)
        angle = d.get("angle", 0.0)
        ptype = d.get("profile_type", "W")
        dims = d.get("dims", {})

        if length <= 0:
            return

        # Línea separadora
        painter.setPen(QPen(Qt.lightGray, 1))
        painter.drawLine(int(x0), int(y0), int(x0 + w_px), int(y0))

        # Etiqueta
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setFont(QFont("Arial", 7))
        painter.drawText(int(x0 + 4), int(y0 + 11),
                         f"Vista lateral — θ={angle:.1f}°")

        # Calcular peralte del perfil
        if ptype == "W" or ptype == "C":
            prof_d = dims.get("d", 0.3)
        elif ptype == "HSS":
            prof_d = dims.get("H", 0.2)
        else:
            prof_d = dims.get("b1", 0.1)

        margin = 30
        avail_w = w_px - 2 * margin
        avail_h = h_px - 2 * margin - 10

        # Proyectar el perfil inclinado
        theta = math.radians(angle)
        proj_w = abs(length * math.cos(theta)) + abs(prof_d * math.sin(theta))
        proj_h = abs(length * math.sin(theta)) + abs(prof_d * math.cos(theta))

        if proj_w <= 0 or proj_h <= 0:
            return

        scale = min(avail_w / proj_w, avail_h / proj_h) * 0.85
        cx = x0 + w_px / 2.0
        cy = y0 + h_px / 2.0 + 5

        # Vectores del perfil en vista lateral
        c, s = math.cos(theta), math.sin(theta)
        # e_L proyectado: (cos θ, -sin θ) en píxeles (Y invertido)
        # e_d proyectado: (-sin θ, -cos θ)

        half_d = prof_d / 2.0

        # 4 esquinas del rectángulo del perfil
        corners = [
            (0, -half_d),
            (length, -half_d),
            (length, half_d),
            (0, half_d),
        ]

        # Transformar a píxeles
        pts = []
        for u, v in corners:
            px = cx + (u * c - v * s) * scale - (length * c * scale / 2)
            py = cy - (u * s + v * c) * scale + (length * s * scale / 2)
            pts.append((px, py))

        # Dibujar contorno del perfil
        painter.setBrush(QBrush(QColor(180, 210, 255, 120)))
        painter.setPen(QPen(QColor(60, 100, 180), 2))
        from PySide6.QtCore import QPointF
        from PySide6.QtGui import QPolygonF
        polygon = QPolygonF([QPointF(p[0], p[1]) for p in pts])
        painter.drawPolygon(polygon)

        # Centro de la sección (marcador)
        sec_cx_start = cx - (length * c * scale / 2)
        sec_cy_start = cy + (length * s * scale / 2)
        sec_cx_end = cx + (length * c * scale / 2)
        sec_cy_end = cy - (length * s * scale / 2)

        # Línea de eje longitudinal
        painter.setPen(QPen(QColor(200, 50, 50), 1, Qt.DashLine))
        painter.drawLine(int(sec_cx_start), int(sec_cy_start),
                         int(sec_cx_end), int(sec_cy_end))

        # Cota de largo
        self._draw_dimension(painter,
                             (pts[0][0], pts[0][1]),
                             (pts[1][0], pts[1][1]),
                             f"L={length:.4g}m", offset=-18)


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
# Panel principal
# ══════════════════════════════════════════════════════════════════════════════

PROFILE_TYPES = ["W", "HSS", "L", "C"]

# Definición de campos por tipo de perfil: (key, label, default, tooltip)
PROFILE_FIELDS = {
    "W": [
        ("d",  "Peralte d:",  "0.300", "Peralte total del perfil (m)"),
        ("bf", "Ancho ala bf:", "0.150", "Ancho del ala (m)"),
        ("tf", "Espesor ala tf:", "0.010", "Espesor del ala (m)"),
        ("tw", "Espesor alma tw:", "0.007", "Espesor del alma (m)"),
    ],
    "HSS": [
        ("B",     "Ancho B:",    "0.200", "Ancho del HSS (m)"),
        ("H",     "Alto H:",     "0.200", "Alto del HSS (m)"),
        ("t_hss", "Espesor t:",  "0.008", "Espesor de las paredes (m)"),
    ],
    "L": [
        ("b1",      "Ala vert. b1:", "0.100", "Largo del ala vertical (m)"),
        ("b2",      "Ala horiz. b2:", "0.100", "Largo del ala horizontal (m)"),
        ("t_angle", "Espesor t:",    "0.010", "Espesor del ángulo (m)"),
    ],
    "C": [
        ("d",  "Peralte d:",  "0.250", "Peralte total del canal (m)"),
        ("bf", "Ancho ala bf:", "0.100", "Ancho del ala (m)"),
        ("tf", "Espesor ala tf:", "0.012", "Espesor del ala (m)"),
        ("tw", "Espesor alma tw:", "0.006", "Espesor del alma (m)"),
    ],
}


class SteelProfilesGUI(QWidget):
    """Panel standalone para generación de perfiles de acero como placas Shell."""

    def __init__(self, connection: SapConnection = None):
        super().__init__()
        self.setWindowTitle("SAP2000 — Perfiles de Acero como Placas Shell")
        self.setMinimumWidth(740)

        self._conn = connection or SapConnection()
        self._backend = SteelProfileBackend(self._conn)
        self._worker = None
        self._run_worker = None
        self._coords_worker = None

        # Almacena los QLineEdit de la sección dinámica
        self._section_fields: dict = {}    # key → QLineEdit
        self._section_labels: dict = {}    # key → QLabel

        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Estado y conexión ────────────────────────────────────────────
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

        # ── Cuerpo: parámetros │ preview ─────────────────────────────────
        body = QHBoxLayout()
        body.setSpacing(10)
        params_col = QVBoxLayout()
        params_col.setSpacing(8)

        # ── Grupo: Tipo de Perfil ────────────────────────────────────────
        grp_type = QGroupBox("Tipo de Perfil")
        g_type = QGridLayout(grp_type)
        g_type.setHorizontalSpacing(12)
        g_type.setVerticalSpacing(8)

        lbl_type = QLabel("Perfil:")
        lbl_type.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._profile_type = QComboBox()
        self._profile_type.addItems(PROFILE_TYPES)
        self._profile_type.setCurrentText("W")
        self._profile_type.currentTextChanged.connect(self._on_profile_type_changed)
        g_type.addWidget(lbl_type, 0, 0)
        g_type.addWidget(self._profile_type, 0, 1)

        params_col.addWidget(grp_type)

        # ── Grupo: Dimensiones de Sección (dinámico) ─────────────────────
        self._grp_section = QGroupBox("Dimensiones de Sección")
        self._section_layout = QGridLayout(self._grp_section)
        self._section_layout.setHorizontalSpacing(12)
        self._section_layout.setVerticalSpacing(8)
        params_col.addWidget(self._grp_section)

        # Crear todos los campos (se muestran/ocultan según tipo)
        all_keys = set()
        for fields in PROFILE_FIELDS.values():
            for key, label, default, tooltip in fields:
                if key not in all_keys:
                    lbl, edit = _field(label, default, tooltip)
                    self._section_labels[key] = lbl
                    self._section_fields[key] = edit
                    all_keys.add(key)

        # ── Grupo: Longitud y Orientación ────────────────────────────────
        grp_orient = QGroupBox("Longitud y Orientación")
        g_orient = QGridLayout(grp_orient)
        g_orient.setHorizontalSpacing(12)
        g_orient.setVerticalSpacing(8)

        lbl, self._length = _field("Largo:", "3.0", "Largo del perfil (m)")
        g_orient.addWidget(lbl, 0, 0); g_orient.addWidget(self._length, 0, 1)

        lbl_plane = QLabel("Plano:")
        lbl_plane.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_plane.setToolTip("Plano donde se extiende el largo del perfil")
        self._plane = QComboBox()
        self._plane.addItems(["XZ", "YZ", "XY"])
        self._plane.setCurrentText("XZ")
        g_orient.addWidget(lbl_plane, 0, 2); g_orient.addWidget(self._plane, 0, 3)

        lbl, self._angle = _field("Ángulo θ:", "0.0",
                                  "Inclinación en grados dentro del plano (0°=horizontal)")
        g_orient.addWidget(lbl, 1, 0); g_orient.addWidget(self._angle, 1, 1)

        params_col.addWidget(grp_orient)

        # ── Grupo: Discretización ────────────────────────────────────────
        grp_disc = QGroupBox("Discretización")
        g_disc = QGridLayout(grp_disc)
        g_disc.setHorizontalSpacing(12)
        g_disc.setVerticalSpacing(8)

        lbl, self._n_length = _field("Div. Largo:", "6",
                                     "Divisiones a lo largo del perfil (≥ 1)")
        g_disc.addWidget(lbl, 0, 0); g_disc.addWidget(self._n_length, 0, 1)

        lbl, self._n_width = _field("Div. Ancho:", "2",
                                    "Divisiones a lo ancho de cada placa (≥ 1)")
        g_disc.addWidget(lbl, 0, 2); g_disc.addWidget(self._n_width, 0, 3)

        params_col.addWidget(grp_disc)

        # ── Grupo: Ubicación ─────────────────────────────────────────────
        grp_loc = QGroupBox("Ubicación Punto Base (inicio del perfil)")
        g_loc = QGridLayout(grp_loc)
        g_loc.setHorizontalSpacing(12)
        g_loc.setVerticalSpacing(8)

        lbl, self._ox = _field("X:", "0.0")
        g_loc.addWidget(lbl, 0, 0); g_loc.addWidget(self._ox, 0, 1)
        lbl, self._oy = _field("Y:", "0.0")
        g_loc.addWidget(lbl, 0, 2); g_loc.addWidget(self._oy, 0, 3)
        lbl, self._oz = _field("Z:", "0.0")
        g_loc.addWidget(lbl, 1, 0); g_loc.addWidget(self._oz, 1, 1)

        self._btn_get_coords = QPushButton("📍 Obtener Nodo")
        self._btn_get_coords.setFixedHeight(26)
        self._btn_get_coords.setEnabled(False)
        self._btn_get_coords.setToolTip(
            "Lee las coordenadas del nodo seleccionado en SAP2000"
        )
        self._btn_get_coords.clicked.connect(self._on_get_coords)
        g_loc.addWidget(self._btn_get_coords, 2, 0, 1, 4)

        params_col.addWidget(grp_loc)

        # ── Grupo: Propiedad SAP2000 ─────────────────────────────────────
        grp_sap = QGroupBox("Propiedad SAP2000")
        g_sap = QGridLayout(grp_sap)
        g_sap.setHorizontalSpacing(12)
        g_sap.setVerticalSpacing(8)

        lbl_prop = QLabel("Prop. Área Shell:")
        lbl_prop.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._area_prop = QComboBox()
        self._area_prop.setEditable(True)
        self._area_prop.addItem("Default")
        g_sap.addWidget(lbl_prop, 0, 0); g_sap.addWidget(self._area_prop, 0, 1)

        lbl, self._group_name = _field("Grupo:", "STEEL_PROFILE",
                                       "Nombre del grupo SAP2000 para las áreas")
        g_sap.addWidget(lbl, 0, 2); g_sap.addWidget(self._group_name, 0, 3)

        params_col.addWidget(grp_sap)
        params_col.addStretch()

        # ── Preview ──────────────────────────────────────────────────────
        self._preview = ProfilePreviewWidget()
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

        # ── Botón generar ────────────────────────────────────────────────
        self._btn_run = QPushButton("Generar Perfil como Placas Shell")
        self._btn_run.setFixedHeight(36)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Log ──────────────────────────────────────────────────────────
        grp_log = QGroupBox("Salida")
        log_layout = QVBoxLayout(grp_log)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(140)
        log_layout.addWidget(self._log)
        root.addWidget(grp_log)

        # ── Señales preview ──────────────────────────────────────────────
        self._length.textChanged.connect(self._update_preview)
        self._angle.textChanged.connect(self._update_preview)
        self._profile_type.currentTextChanged.connect(self._update_preview)

        # Conectar señales de los campos de sección
        for key in self._section_fields:
            self._section_fields[key].textChanged.connect(self._update_preview)

        # Inicializar campos visibles según tipo por defecto
        self._on_profile_type_changed("W")

    # ── Campos dinámicos según tipo ──────────────────────────────────────

    def _on_profile_type_changed(self, ptype: str):
        """Muestra solo los campos relevantes al tipo de perfil seleccionado."""
        # Ocultar todos
        for key in self._section_fields:
            self._section_labels[key].setVisible(False)
            self._section_fields[key].setVisible(False)

        # Limpiar layout
        while self._section_layout.count():
            self._section_layout.takeAt(0)

        # Mostrar los del tipo actual
        fields = PROFILE_FIELDS.get(ptype, [])
        for row, (key, label, default, tooltip) in enumerate(fields):
            lbl = self._section_labels[key]
            edit = self._section_fields[key]
            lbl.setText(label)
            lbl.setToolTip(tooltip)
            edit.setToolTip(tooltip)
            lbl.setVisible(True)
            edit.setVisible(True)
            col = 0 if row % 2 == 0 else 2
            r = row // 2
            self._section_layout.addWidget(lbl, r, col)
            self._section_layout.addWidget(edit, r, col + 1)

        self._update_preview()

    # ── Helpers ──────────────────────────────────────────────────────────

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

    def _get_current_dims(self) -> dict:
        """Lee los valores actuales de los campos de sección visibles."""
        ptype = self._profile_type.currentText()
        dims = {}
        for key, _, default, _ in PROFILE_FIELDS.get(ptype, []):
            try:
                dims[key] = float(self._section_fields[key].text())
            except (ValueError, KeyError):
                dims[key] = float(default)
        return dims

    def _update_preview(self):
        try:
            dims = self._get_current_dims()
            self._preview.update_preview(
                profile_type=self._profile_type.currentText(),
                dims=dims,
                length=float(self._length.text()),
                angle=float(self._angle.text()),
            )
        except ValueError:
            pass

    def _build_config(self) -> SteelProfileConfig:
        ptype = self._profile_type.currentText()
        dims = self._get_current_dims()

        cfg = SteelProfileConfig(
            profile_type=ptype,
            length=float(self._length.text()),
            origin_x=float(self._ox.text()),
            origin_y=float(self._oy.text()),
            origin_z=float(self._oz.text()),
            plane=self._plane.currentText(),
            angle=float(self._angle.text()),
            n_length=int(self._n_length.text()),
            n_width=int(self._n_width.text()),
            area_prop=self._area_prop.currentText().strip() or "Default",
            group_name=self._group_name.text().strip() or "STEEL_PROFILE",
        )

        # Asignar dimensiones según tipo
        if ptype == "W" or ptype == "C":
            cfg.d = dims.get("d", cfg.d)
            cfg.bf = dims.get("bf", cfg.bf)
            cfg.tf = dims.get("tf", cfg.tf)
            cfg.tw = dims.get("tw", cfg.tw)
        elif ptype == "HSS":
            cfg.B = dims.get("B", cfg.B)
            cfg.H = dims.get("H", cfg.H)
            cfg.t_hss = dims.get("t_hss", cfg.t_hss)
        elif ptype == "L":
            cfg.b1 = dims.get("b1", cfg.b1)
            cfg.b2 = dims.get("b2", cfg.b2)
            cfg.t_angle = dims.get("t_angle", cfg.t_angle)

        return cfg

    def populate_area_props(self, names: list):
        current = self._area_prop.currentText()
        self._area_prop.clear()
        items = list(names) if names else ["Default"]
        self._area_prop.addItems(items)
        idx = self._area_prop.findText(current)
        self._area_prop.setCurrentIndex(idx if idx >= 0 else 0)

    # ── Slots ────────────────────────────────────────────────────────────

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
            f"\n─── Generando perfil {config.profile_type}  |  "
            f"L={config.length}m  |  θ={config.angle}°  |  "
            f"plano={config.plane} ───"
        )
        self._busy(True)
        self._run_worker = RunWorker(self._backend, config)
        self._run_worker.finished.connect(self._on_run_done)
        self._run_worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Perfil generado correctamente")
            self._log_append(
                f"  Tipo perfil        : {result.get('profile_type', '?')}\n"
                f"  Placas generadas   : {result.get('num_plates', '?')}  "
                f"{result.get('plate_names', [])}\n"
                f"  Áreas creadas      : {result.get('num_areas', '?')}\n"
                f"  Áreas por placa    : {result.get('areas_per_plate', '?')}\n"
                f"  Largo              : {result.get('length', '?')}m\n"
                f"  Ángulo             : {result.get('angle', '?')}°\n"
                f"  Plano              : {result.get('plane', '?')}\n"
                f"  Grupo              : {result.get('group', '?')}"
            )
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
# Entry point (standalone)
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteelProfilesGUI()
    window.show()
    sys.exit(app.exec())
