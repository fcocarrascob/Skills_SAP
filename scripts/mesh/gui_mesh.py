"""
GUI — SAP2000 Generador de Mallas (Standalone)
===============================================
PySide6 interface con dos pestañas:
  - Malla Rectangular: genera una grilla de áreas AddByCoord.
  - Malla con Orificio: genera una malla interpolada entre anillo
    interno y externo, con soporte de forma Círculo/Cuadrado.

Conexión directa vía comtypes (sin MCP). Un solo SapConnection
compartido por ambas pestañas.

Layout
------
  [Estado de conexión]
  [Conectar]  [Desconectar]
  ┌─────────────────────────────────────────────┐
  │  Malla Rectangular │ Malla con Orificio      │
  │  ┌──────────────────────────────────────┐   │
  │  │  Parámetros + botón Generar          │   │
  │  │  Log de salida                       │   │
  │  └──────────────────────────────────────┘   │
  └─────────────────────────────────────────────┘
"""

import sys
import json
import math

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTextEdit,
    QTabWidget,
)

from backend_mesh_rect import SapConnection, RectMeshBackend, RectMeshConfig
from backend_mesh_hole import HoleMeshBackend, HoleMeshConfig


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


class RectRunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: RectMeshBackend, config: RectMeshConfig):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            self.finished.emit(self._backend.run(self._config))
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class HoleRunWorker(QThread):
    finished = Signal(dict)

    def __init__(self, backend: HoleMeshBackend, config: HoleMeshConfig):
        super().__init__()
        self._backend = backend
        self._config = config

    def run(self):
        try:
            self.finished.emit(self._backend.run(self._config))
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})


class GetCoordsWorker(QThread):
    """Obtiene las coordenadas del primer punto seleccionado en SAP2000."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        try:
            SapModel = self._conn.sap_model

            # SelectObj.GetSelected(NumberItems, ObjectTypes, ObjectNames)
            ret_sel = SapModel.SelectObj.GetSelected(0, [], [])
            if not (isinstance(ret_sel, (list, tuple)) and int(ret_sel[-1]) == 0):
                self.finished.emit({"success": False, "error": "GetSelected falló o no hay selección."})
                return

            num_items = int(ret_sel[0])
            if num_items == 0:
                self.finished.emit({"success": False, "error": "No hay objetos seleccionados en SAP2000."})
                return

            obj_types = ret_sel[1]
            obj_names = ret_sel[2]

            point_name = None
            for i in range(num_items):
                if int(obj_types[i]) == 1:   # 1 = PointObject
                    point_name = obj_names[i]
                    break

            if not point_name:
                self.finished.emit({"success": False, "error": "Ningún nodo (PointObject) seleccionado."})
                return

            # PointObj.GetCoordCartesian(Name, x, y, z, CSys)  →  [x, y, z, RetCode]
            ret_coord = SapModel.PointObj.GetCoordCartesian(point_name, 0.0, 0.0, 0.0, "Global")
            if not (isinstance(ret_coord, (list, tuple)) and int(ret_coord[-1]) == 0):
                self.finished.emit({"success": False, "error": "GetCoordCartesian falló."})
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
# Previsualización — widget QPainter
# ══════════════════════════════════════════════════════════════════════════════

class PreviewWidget(QWidget):
    """Previsualización en tiempo real de la malla (QPainter, sin deps externas)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self.setStyleSheet("background-color: white; border: 1px solid #aaaaaa;")
        self.mode = None
        self.data = {}

    def update_rect(self, w, l, nx, ny):
        self.mode = "rect"
        self.data = {"w": w, "l": l, "nx": nx, "ny": ny}
        self.update()

    def update_hole(self, os_, od, is_, id_, na, nr):
        self.mode = "hole"
        self.data = {"os": os_, "od": od, "is": is_, "id": id_, "na": na, "nr": nr}
        self.update()

    # ── Cotas ─────────────────────────────────────────────────────────────

    def _draw_dimension(self, painter, p1, p2, text, offset=20):
        """Dibuja una cota |---| entre p1 y p2 con texto central."""
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return

        nx_, ny_ = -dy / length, dx / length
        cx1, cy1 = x1 + nx_ * offset, y1 + ny_ * offset
        cx2, cy2 = x2 + nx_ * offset, y2 + ny_ * offset

        painter.setPen(QPen(Qt.darkGray, 1))
        painter.drawLine(x1, y1, cx1, cy1)
        painter.drawLine(x2, y2, cx2, cy2)
        painter.drawLine(cx1, cy1, cx2, cy2)

        tick = 4
        ux = dx / length * tick
        uy = dy / length * tick
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(cx1 - ux, cy1 - uy, cx1 + ux, cy1 + uy)
        painter.drawLine(cx2 - ux, cy2 - uy, cx2 + ux, cy2 + uy)

        painter.setPen(QPen(Qt.black, 1))
        mid_x, mid_y = (cx1 + cx2) / 2, (cy1 + cy2) / 2
        angle = math.degrees(math.atan2(dy, dx))
        if 90 < angle <= 270 or -270 <= angle < -90:
            angle += 180
        painter.save()
        painter.translate(mid_x, mid_y)
        painter.rotate(angle)
        painter.drawText(-150, -25, 300, 20, Qt.AlignCenter, text)
        painter.restore()

    # ── paintEvent ────────────────────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        if self.mode == "rect":
            self._draw_rect(painter, cx, cy, w, h)
        elif self.mode == "hole":
            self._draw_hole(painter, cx, cy, w, h)

    # ── Modo rectangular ──────────────────────────────────────────────────

    def _draw_rect(self, painter, cx, cy, w_px, h_px):
        d = self.data
        W = d.get("w", 100)
        L = d.get("l", 100)
        nx = d.get("nx", 1)
        ny = d.get("ny", 1)
        if W <= 0 or L <= 0:
            return

        scale = min(w_px / W, h_px / L) * 0.6
        rw, rh = W * scale, L * scale
        x0 = cx - rw / 2
        y0 = cy - rh / 2

        painter.setPen(QPen(Qt.black, 1))
        if nx > 0:
            for i in range(nx + 1):
                x = x0 + i * rw / nx
                painter.drawLine(x, y0, x, y0 + rh)
        if ny > 0:
            for j in range(ny + 1):
                y = y0 + j * rh / ny
                painter.drawLine(x0, y, x0 + rw, y)

        painter.setPen(QPen(Qt.blue, 2))
        painter.drawRect(x0, y0, rw, rh)

        dx_val = W / nx if nx > 0 else W
        self._draw_dimension(painter, (x0, y0 + rh), (x0 + rw, y0 + rh),
                             f"{nx} @ {dx_val:.2f} = {W:.2f}", offset=25)
        dy_val = L / ny if ny > 0 else L
        self._draw_dimension(painter, (x0, y0), (x0, y0 + rh),
                             f"{ny} @ {dy_val:.2f} = {L:.2f}", offset=25)

    # ── Modo con orificio ─────────────────────────────────────────────────

    def _draw_hole(self, painter, cx, cy, w_px, h_px):
        d = self.data
        outer_s = d.get("os", "Cuadrado")
        outer_d = d.get("od", 500)
        inner_s = d.get("is", "Círculo")
        inner_d = d.get("id", 200)
        na = d.get("na", 16)
        nr = d.get("nr", 2)
        if outer_d <= 0:
            return

        scale = min(w_px, h_px) / outer_d * 0.6

        def ring_coords(shape, dim, n):
            coords = []
            rad = dim / 2.0
            perimeter = 4.0 * dim
            step = perimeter / n if n > 0 else 0
            for i in range(n):
                if shape.lower() == "círculo":
                    ang = 2 * math.pi * i / n
                    coords.append((rad * math.cos(ang), rad * math.sin(ang)))
                else:
                    dist = i * step
                    if dist < rad:
                        u, v = rad, dist
                    elif dist < rad + dim:
                        u, v = rad - (dist - rad), rad
                    elif dist < rad + 2 * dim:
                        u, v = -rad, rad - (dist - (rad + dim))
                    elif dist < rad + 3 * dim:
                        u, v = -rad + (dist - (rad + 2 * dim)), -rad
                    else:
                        u, v = rad, -rad + (dist - (rad + 3 * dim))
                    coords.append((u, v))
            return coords

        inner_pts = ring_coords(inner_s, inner_d, na)
        outer_pts = ring_coords(outer_s, outer_d, na)

        pen_mesh = QPen(Qt.gray, 1)
        pen_border = QPen(Qt.blue, 2)

        for r in range(nr + 1):
            frac = r / nr if nr > 0 else 1.0
            pts = []
            for i in range(na):
                u_in, v_in = inner_pts[i]
                u_out, v_out = outer_pts[i]
                u = u_in + (u_out - u_in) * frac
                v = v_in + (v_out - v_in) * frac
                pts.append((cx + u * scale, cy - v * scale))

            painter.setPen(pen_mesh if 0 < r < nr else pen_border)
            for i in range(na):
                p1, p2 = pts[i], pts[(i + 1) % na]
                painter.drawLine(p1[0], p1[1], p2[0], p2[1])

            if r < nr:
                next_frac = (r + 1) / nr
                painter.setPen(pen_mesh)
                for i in range(na):
                    u_in, v_in = inner_pts[i]
                    u_out, v_out = outer_pts[i]
                    u1 = u_in + (u_out - u_in) * frac
                    v1 = v_in + (v_out - v_in) * frac
                    u2 = u_in + (u_out - u_in) * next_frac
                    v2 = v_in + (v_out - v_in) * next_frac
                    painter.drawLine(cx + u1 * scale, cy - v1 * scale,
                                     cx + u2 * scale, cy - v2 * scale)

        r_out = outer_d * scale / 2
        r_in = inner_d * scale / 2
        self._draw_dimension(painter,
                             (cx + r_out, cy - r_out), (cx - r_out, cy - r_out),
                             f"Ext: {outer_d:.2f} ({outer_s})", offset=30)
        self._draw_dimension(painter,
                             (cx - r_in, cy + r_in), (cx + r_in, cy + r_in),
                             f"Int: {inner_d:.2f} ({inner_s})", offset=30)


# ══════════════════════════════════════════════════════════════════════════════
# Helper — campo de entrada con label
# ══════════════════════════════════════════════════════════════════════════════

def _field(label: str, default: str, tooltip: str = "") -> tuple:
    """Crea un par (QLabel, QLineEdit) para un campo de entrada."""
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    edit = QLineEdit(default)
    edit.setMinimumWidth(90)
    if tooltip:
        edit.setToolTip(tooltip)
        lbl.setToolTip(tooltip)
    return lbl, edit


# ══════════════════════════════════════════════════════════════════════════════
# Tab 1 — Malla Rectangular
# ══════════════════════════════════════════════════════════════════════════════

class RectMeshTab(QWidget):
    """Pestaña de generación de malla rectangular."""

    def __init__(self, connection: SapConnection, parent=None):
        super().__init__(parent)
        self._conn = connection
        self._backend = RectMeshBackend(self._conn)
        self._worker = None
        self._coords_worker = None
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(10, 10, 10, 10)
        # ── Columna izquierda (parámetros)  │  Preview ────────────────
        _mid = QHBoxLayout()
        _mid.setSpacing(10)
        _params = QVBoxLayout()
        _params.setSpacing(10)
        # ── Parámetros de Malla ───────────────────────────────────────────
        grp_mesh = QGroupBox("Parámetros de Malla")
        grid = QGridLayout(grp_mesh)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        r = 0

        lbl, self._width = _field("Ancho (Dim 1):", "500.0", "Dimensión en dirección 1 (X en XY/XZ, Y en YZ)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._width, r, 1)
        lbl, self._length = _field("Largo (Dim 2):", "500.0", "Dimensión en dirección 2 (Y en XY, Z en XZ/YZ)")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._length, r, 3)
        r += 1

        lbl, self._nx = _field("Divisiones Nx:", "5", "Número de divisiones en Dim 1")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._nx, r, 1)
        lbl, self._ny = _field("Divisiones Ny:", "5", "Número de divisiones en Dim 2")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._ny, r, 3)
        r += 1

        _params.addWidget(grp_mesh)

        # ── Ubicación y Propiedades ───────────────────────────────────────
        grp_loc = QGroupBox("Ubicación y Propiedades")
        grid2 = QGridLayout(grp_loc)
        grid2.setHorizontalSpacing(12)
        grid2.setVerticalSpacing(8)

        r = 0

        lbl, self._sx = _field("Origen X:", "0.0")
        grid2.addWidget(lbl, r, 0); grid2.addWidget(self._sx, r, 1)
        lbl, self._sy = _field("Origen Y:", "0.0")
        grid2.addWidget(lbl, r, 2); grid2.addWidget(self._sy, r, 3)
        r += 1

        lbl, self._sz = _field("Origen Z:", "0.0")
        grid2.addWidget(lbl, r, 0); grid2.addWidget(self._sz, r, 1)

        lbl = QLabel("Plano:")
        lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._plane = QComboBox()
        self._plane.addItems(["", "XY", "XZ", "YZ"])
        self._plane.setCurrentIndex(0)
        self._plane.setToolTip("Seleccione el plano en el que se generará la malla")
        grid2.addWidget(lbl, r, 2); grid2.addWidget(self._plane, r, 3)
        r += 1

        lbl_prop = QLabel("Propiedad de Área:")
        lbl_prop.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_prop.setToolTip("Sección Shell disponible en SAP2000 (se actualiza al conectar)")
        self._prop = QComboBox()
        self._prop.setEditable(True)
        self._prop.addItem("Default")
        self._prop.setToolTip("Sección Shell disponible en SAP2000 (se actualiza al conectar)")
        grid2.addWidget(lbl_prop, r, 0); grid2.addWidget(self._prop, r, 1)

        self._btn_get_coords = QPushButton("📍 Obtener Nodo")
        self._btn_get_coords.setFixedHeight(26)
        self._btn_get_coords.setEnabled(False)
        self._btn_get_coords.setToolTip("Lee las coordenadas del nodo seleccionado en SAP2000 y las carga como Origen.")
        self._btn_get_coords.clicked.connect(self._on_get_coords)
        grid2.addWidget(self._btn_get_coords, r, 2, 1, 2)

        _params.addWidget(grp_loc)
        _params.addStretch()

        # ── Preview ───────────────────────────────────────────────────────
        self._preview = PreviewWidget()
        _mid.addLayout(_params, 1)
        _mid.addWidget(self._preview, 1)
        root.addLayout(_mid)

        # ── Señales de preview ────────────────────────────────────────────
        self._width.textChanged.connect(self._update_preview)
        self._length.textChanged.connect(self._update_preview)
        self._nx.textChanged.connect(self._update_preview)
        self._ny.textChanged.connect(self._update_preview)
        self._update_preview()

        # ── Botón Generar ─────────────────────────────────────────────────
        self._btn_run = QPushButton("Generar Malla Rectangular")
        self._btn_run.setFixedHeight(34)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Log de salida ─────────────────────────────────────────────────
        grp_log = QGroupBox("Salida")
        log_layout = QVBoxLayout(grp_log)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(160)
        log_layout.addWidget(self._log)
        root.addWidget(grp_log)

    # ── API pública ───────────────────────────────────────────────────────

    def set_connected(self, connected: bool):
        self._btn_run.setEnabled(connected)
        self._btn_get_coords.setEnabled(connected)

    def set_origin(self, x: float, y: float, z: float):
        """Rellena los campos de Origen X/Y/Z con las coordenadas dadas."""
        self._sx.setText(f"{x:.6g}")
        self._sy.setText(f"{y:.6g}")
        self._sz.setText(f"{z:.6g}")

    def populate_area_props(self, names: list):
        """Rellena el combo de Propiedad de Área con las secciones Shell de SAP2000."""
        current = self._prop.currentText()
        self._prop.clear()
        items = list(names) if names else ["Default"]
        self._prop.addItems(items)
        idx = self._prop.findText(current)
        self._prop.setCurrentIndex(idx if idx >= 0 else 0)

    def _log_append(self, text: str):
        self._log.append(text)

    def _busy(self, is_busy: bool):
        self._btn_run.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_get_coords.setEnabled(not is_busy and self._conn.is_connected)

    def _build_config(self) -> RectMeshConfig:
        plane = self._plane.currentText().strip()
        if not plane:
            raise ValueError("Debe seleccionar un Plano antes de generar la malla.")
        return RectMeshConfig(
            width=float(self._width.text()),
            length=float(self._length.text()),
            nx=int(self._nx.text()),
            ny=int(self._ny.text()),
            start_x=float(self._sx.text()),
            start_y=float(self._sy.text()),
            start_z=float(self._sz.text()),
            plane=plane,
            prop_name=self._prop.currentText().strip() or "Default",
        )

    def _format_result(self, data: dict) -> str:
        lines = [
            f"  Áreas creadas : {data.get('num_areas', '?')}",
            f"  Grilla        : {data.get('grid', '?')}",
            f"  Tamaño celda  : {data.get('cell_size', '?')}",
            f"  Plano         : {data.get('plane', '?')}",
        ]
        return "\n".join(lines)

    def _update_preview(self):
        try:
            self._preview.update_rect(
                float(self._width.text()),
                float(self._length.text()),
                int(self._nx.text()),
                int(self._ny.text()),
            )
        except ValueError:
            pass

    # ── Slots ─────────────────────────────────────────────────────────────

    def _on_run(self):
        try:
            config = self._build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return

        self._log_append("\n─── Generando malla rectangular ─────────────────")
        self._busy(True)
        self._worker = RectRunWorker(self._backend, config)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Malla generada correctamente")
            self._log_append(self._format_result(result))
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
            self.set_origin(x, y, z)
            self._log_append(f"📍 Nodo '{name}'  →  X={x:.6g}  Y={y:.6g}  Z={z:.6g}")
        else:
            self._log_append(f"✘ {result.get('error', 'Error desconocido')}")


# ══════════════════════════════════════════════════════════════════════════════
# Tab 2 — Malla con Orificio
# ══════════════════════════════════════════════════════════════════════════════

class HoleMeshTab(QWidget):
    """Pestaña de generación de malla con orificio."""

    SHAPES = ["Círculo", "Cuadrado"]

    def __init__(self, connection: SapConnection, parent=None):
        super().__init__(parent)
        self._conn = connection
        self._backend = HoleMeshBackend(self._conn)
        self._worker = None
        self._coords_worker = None
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(10, 10, 10, 10)

        # ── Columna izquierda (parámetros)  │  Preview ────────────────
        _mid = QHBoxLayout()
        _mid.setSpacing(10)
        _params = QVBoxLayout()
        _params.setSpacing(10)

        # ── Forma externa ─────────────────────────────────────────────────
        grp_outer = QGroupBox("Geometría Externa")
        grid_o = QGridLayout(grp_outer)
        grid_o.setHorizontalSpacing(12)
        grid_o.setVerticalSpacing(8)

        r = 0

        lbl = QLabel("Forma:")
        lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._outer_shape = QComboBox()
        self._outer_shape.addItems(self.SHAPES)
        self._outer_shape.setCurrentText("Cuadrado")
        self._outer_shape.setToolTip("Forma del contorno externo")
        grid_o.addWidget(lbl, r, 0); grid_o.addWidget(self._outer_shape, r, 1)

        lbl, self._outer_dim = _field("Dimensión (Lado/Diám.):", "500.0", "Lado si Cuadrado, Diámetro si Círculo")
        grid_o.addWidget(lbl, r, 2); grid_o.addWidget(self._outer_dim, r, 3)

        _params.addWidget(grp_outer)

        # ── Forma interna (orificio) ──────────────────────────────────────
        grp_inner = QGroupBox("Geometría Interna (Orificio)")
        grid_i = QGridLayout(grp_inner)
        grid_i.setHorizontalSpacing(12)
        grid_i.setVerticalSpacing(8)

        r = 0

        lbl = QLabel("Forma:")
        lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._inner_shape = QComboBox()
        self._inner_shape.addItems(self.SHAPES)
        self._inner_shape.setCurrentText("Círculo")
        self._inner_shape.setToolTip("Forma del orificio interno")
        grid_i.addWidget(lbl, r, 0); grid_i.addWidget(self._inner_shape, r, 1)

        lbl, self._inner_dim = _field("Dimensión (Lado/Diám.):", "200.0", "Lado si Cuadrado, Diámetro si Círculo")
        grid_i.addWidget(lbl, r, 2); grid_i.addWidget(self._inner_dim, r, 3)

        _params.addWidget(grp_inner)

        # ── Discretización ────────────────────────────────────────────────
        grp_disc = QGroupBox("Discretización")
        grid_d = QGridLayout(grp_disc)
        grid_d.setHorizontalSpacing(12)
        grid_d.setVerticalSpacing(8)

        r = 0

        lbl, self._n_angular = _field("Divisiones angulares:", "16", "Número de puntos por anillo (mínimo 3)")
        grid_d.addWidget(lbl, r, 0); grid_d.addWidget(self._n_angular, r, 1)
        lbl, self._n_radial = _field("Divisiones radiales:", "3", "Número de anillos de áreas entre interno y externo")
        grid_d.addWidget(lbl, r, 2); grid_d.addWidget(self._n_radial, r, 3)

        _params.addWidget(grp_disc)

        # ── Ubicación y Propiedades ───────────────────────────────────────
        grp_loc = QGroupBox("Ubicación y Propiedades")
        grid2 = QGridLayout(grp_loc)
        grid2.setHorizontalSpacing(12)
        grid2.setVerticalSpacing(8)

        r = 0

        lbl, self._ox = _field("Origen X:", "0.0")
        grid2.addWidget(lbl, r, 0); grid2.addWidget(self._ox, r, 1)
        lbl, self._oy = _field("Origen Y:", "0.0")
        grid2.addWidget(lbl, r, 2); grid2.addWidget(self._oy, r, 3)
        r += 1

        lbl, self._oz = _field("Origen Z:", "0.0")
        grid2.addWidget(lbl, r, 0); grid2.addWidget(self._oz, r, 1)

        lbl = QLabel("Plano:")
        lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._plane = QComboBox()
        self._plane.addItems(["", "XY", "XZ", "YZ"])
        self._plane.setCurrentIndex(0)
        self._plane.setToolTip("Seleccione el plano en el que se generará la malla")
        grid2.addWidget(lbl, r, 2); grid2.addWidget(self._plane, r, 3)
        r += 1

        lbl_prop = QLabel("Propiedad de Área:")
        lbl_prop.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl_prop.setToolTip("Sección Shell disponible en SAP2000 (se actualiza al conectar)")
        self._prop = QComboBox()
        self._prop.setEditable(True)
        self._prop.addItem("Default")
        self._prop.setToolTip("Sección Shell disponible en SAP2000 (se actualiza al conectar)")
        grid2.addWidget(lbl_prop, r, 0); grid2.addWidget(self._prop, r, 1)

        self._btn_get_coords = QPushButton("📍 Obtener Nodo")
        self._btn_get_coords.setFixedHeight(26)
        self._btn_get_coords.setEnabled(False)
        self._btn_get_coords.setToolTip("Lee las coordenadas del nodo seleccionado en SAP2000 y las carga como Origen.")
        self._btn_get_coords.clicked.connect(self._on_get_coords)
        grid2.addWidget(self._btn_get_coords, r, 2, 1, 2)

        _params.addWidget(grp_loc)
        _params.addStretch()

        # ── Preview ───────────────────────────────────────────────────────
        self._preview = PreviewWidget()
        _mid.addLayout(_params, 1)
        _mid.addWidget(self._preview, 1)
        root.addLayout(_mid)

        # ── Señales de preview ────────────────────────────────────────────
        self._outer_dim.textChanged.connect(self._update_preview)
        self._inner_dim.textChanged.connect(self._update_preview)
        self._n_angular.textChanged.connect(self._update_preview)
        self._n_radial.textChanged.connect(self._update_preview)
        self._outer_shape.currentIndexChanged.connect(self._update_preview)
        self._inner_shape.currentIndexChanged.connect(self._update_preview)
        self._update_preview()

        # ── Botón Generar ─────────────────────────────────────────────────
        self._btn_run = QPushButton("Generar Malla con Orificio")
        self._btn_run.setFixedHeight(34)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Log de salida ─────────────────────────────────────────────────
        grp_log = QGroupBox("Salida")
        log_layout = QVBoxLayout(grp_log)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(160)
        log_layout.addWidget(self._log)
        root.addWidget(grp_log)

    # ── API pública ───────────────────────────────────────────────────────

    def set_connected(self, connected: bool):
        self._btn_run.setEnabled(connected)
        self._btn_get_coords.setEnabled(connected)

    def set_origin(self, x: float, y: float, z: float):
        """Rellena los campos de Origen X/Y/Z con las coordenadas dadas."""
        self._ox.setText(f"{x:.6g}")
        self._oy.setText(f"{y:.6g}")
        self._oz.setText(f"{z:.6g}")

    def populate_area_props(self, names: list):
        """Rellena el combo de Propiedad de Área con las secciones Shell de SAP2000."""
        current = self._prop.currentText()
        self._prop.clear()
        items = list(names) if names else ["Default"]
        self._prop.addItems(items)
        idx = self._prop.findText(current)
        self._prop.setCurrentIndex(idx if idx >= 0 else 0)

    def _log_append(self, text: str):
        self._log.append(text)

    def _busy(self, is_busy: bool):
        self._btn_run.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_get_coords.setEnabled(not is_busy and self._conn.is_connected)

    def _build_config(self) -> HoleMeshConfig:
        plane = self._plane.currentText().strip()
        if not plane:
            raise ValueError("Debe seleccionar un Plano antes de generar la malla.")
        return HoleMeshConfig(
            outer_shape=self._outer_shape.currentText(),
            outer_dim=float(self._outer_dim.text()),
            inner_shape=self._inner_shape.currentText(),
            inner_dim=float(self._inner_dim.text()),
            num_angular=int(self._n_angular.text()),
            num_radial=int(self._n_radial.text()),
            origin_x=float(self._ox.text()),
            origin_y=float(self._oy.text()),
            origin_z=float(self._oz.text()),
            plane=plane,
            prop_name=self._prop.currentText().strip() or "Default",
        )

    def _format_result(self, data: dict) -> str:
        lines = [
            f"  Áreas creadas       : {data.get('num_areas', '?')}",
            f"  Puntos creados      : {data.get('num_points', '?')}",
            f"  Divisiones angulares: {data.get('angular_divisions', '?')}",
            f"  Anillos radiales    : {data.get('radial_rings', '?')}",
            f"  Plano               : {data.get('plane', '?')}",
        ]
        return "\n".join(lines)

    def _update_preview(self):
        try:
            self._preview.update_hole(
                self._outer_shape.currentText(),
                float(self._outer_dim.text()),
                self._inner_shape.currentText(),
                float(self._inner_dim.text()),
                int(self._n_angular.text()),
                int(self._n_radial.text()),
            )
        except ValueError:
            pass

    # ── Slots ─────────────────────────────────────────────────────────────

    def _on_run(self):
        try:
            config = self._build_config()
        except ValueError as e:
            self._log_append(f"✘ Error en parámetros: {e}")
            return

        self._log_append("\n─── Generando malla con orificio ─────────────────")
        self._busy(True)
        self._worker = HoleRunWorker(self._backend, config)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    def _on_run_done(self, result: dict):
        self._busy(False)
        if result.get("success"):
            self._log_append("✔ Malla generada correctamente")
            self._log_append(self._format_result(result))
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
            self.set_origin(x, y, z)
            self._log_append(f"📍 Nodo '{name}'  →  X={x:.6g}  Y={y:.6g}  Z={z:.6g}")
        else:
            self._log_append(f"✘ {result.get('error', 'Error desconocido')}")


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal
# ══════════════════════════════════════════════════════════════════════════════

class MeshGUI(QWidget):
    """GUI standalone para generación de mallas en SAP2000."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Generador de Mallas")
        self.setMinimumWidth(680)

        # ── Conexión compartida ───────────────────────────────────────────
        self._conn = SapConnection()
        self._worker = None

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Estado y botones de conexión ──────────────────────────────────
        status_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        status_row.addWidget(self._status_lbl)
        status_row.addStretch()
        root.addLayout(status_row)

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

        # ── Pestañas ──────────────────────────────────────────────────────
        self._tabs = QTabWidget()

        self._tab_rect = RectMeshTab(self._conn)
        self._tab_hole = HoleMeshTab(self._conn)

        self._tabs.addTab(self._tab_rect, "Malla Rectangular")
        self._tabs.addTab(self._tab_hole, "Malla con Orificio")

        root.addWidget(self._tabs)

    # ══════════════════════════════════════════════════════════════════════
    # Helpers internos
    # ══════════════════════════════════════════════════════════════════════

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        self._tab_rect.set_connected(connected)
        self._tab_hole.set_connected(connected)
        if connected:
            self._status_lbl.setText("Estado: conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self._status_lbl.setText("Estado: desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")

    def _busy_conn(self, is_busy: bool):
        """Deshabilita botones de conexión durante un worker activo."""
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)

    # ══════════════════════════════════════════════════════════════════════
    # Conectar
    # ══════════════════════════════════════════════════════════════════════

    def _on_connect(self):
        self._busy_conn(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy_conn(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            shell_props = result.get("shell_props", [])
            self._tab_rect._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._tab_hole._log_append(f"✔ Conectado — versión {ver}  |  modelo: {path}")
            self._tab_rect.populate_area_props(shell_props)
            self._tab_hole.populate_area_props(shell_props)
            if shell_props:
                n = len(shell_props)
                self._tab_rect._log_append(f"  Propiedades de área Shell cargadas: {n}")
                self._tab_hole._log_append(f"  Propiedades de área Shell cargadas: {n}")
            else:
                self._tab_rect._log_append("  Sin propiedades de área en el modelo (usando 'Default')")
                self._tab_hole._log_append("  Sin propiedades de área en el modelo (usando 'Default')")
            self._set_connected(True)
        else:
            err = result.get("error", "Error desconocido")
            self._tab_rect._log_append(f"✘ No se pudo conectar: {err}")
            self._set_connected(False)

    # ══════════════════════════════════════════════════════════════════════
    # Desconectar
    # ══════════════════════════════════════════════════════════════════════

    def _on_disconnect(self):
        self._busy_conn(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, result: dict):
        self._busy_conn(False)
        self._tab_rect._log_append("✔ Desconectado de SAP2000")
        self._tab_hole._log_append("✔ Desconectado de SAP2000")
        self._tab_rect.populate_area_props([])
        self._tab_hole.populate_area_props([])
        self._set_connected(False)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeshGUI()
    window.show()
    sys.exit(app.exec())
