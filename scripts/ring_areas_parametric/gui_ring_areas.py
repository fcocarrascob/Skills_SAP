"""
GUI — SAP2000 Circular Ring Area Generator
==========================================
PySide6 interface for the parametric ring-areas script.

Layout
------
  [Connect]           <- conecta a SAP2000 en ejecución
  ── Inputs ─────────────────────────────────
     Radios (m):   r_inner  r_mid1  r_mid2  r_outer
     Espesores (m): t1  t2
     Material:     nombre  E  nu  alpha
     Malla:        n_segs
  ── ─────────────────────────────────────────
  [Run Script]        <- genera y ejecuta el script con los valores ingresados
  ── Output ─────────────────────────────────
     log de texto con resultado / errores
  ── ─────────────────────────────────────────
  [Disconnect]
"""

import sys
import os
import textwrap

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
    QSplitter,
    QSizePolicy,
)

# ── Resolve path to mcp_server ────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_MCP_SERVER_DIR = os.path.join(_SCRIPT_DIR, "..", "..", "mcp_server")
sys.path.insert(0, os.path.normpath(_MCP_SERVER_DIR))

from sap_bridge import bridge          # noqa: E402  (after sys.path patch)
from sap_executor import run_script    # noqa: E402


# ══════════════════════════════════════════════════════════════════════════════
# Worker threads — run blocking SAP2000 calls off the GUI thread
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)   # emits bridge.connect() result dict

    def run(self):
        result = bridge.connect(attach_to_existing=True)
        self.finished.emit(result)


class RunWorker(QThread):
    finished = Signal(dict)   # emits run_script() result dict

    def __init__(self, script: str):
        super().__init__()
        self._script = script

    def run(self):
        result = run_script(self._script)
        self.finished.emit(result)


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def run(self):
        result = bridge.disconnect(save_model=False)
        self.finished.emit(result)


# ══════════════════════════════════════════════════════════════════════════════
# Helper — labelled input row
# ══════════════════════════════════════════════════════════════════════════════

def _field(label: str, default: str, tooltip: str = "") -> tuple[QLabel, QLineEdit]:
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    edit = QLineEdit(default)
    edit.setMinimumWidth(90)
    if tooltip:
        edit.setToolTip(tooltip)
        lbl.setToolTip(tooltip)
    return lbl, edit


# ══════════════════════════════════════════════════════════════════════════════
# Main window
# ══════════════════════════════════════════════════════════════════════════════

class RingAreasGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Circular Ring Area Generator")
        self.setMinimumWidth(640)

        self._worker = None   # reference to active QThread (prevent GC)

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Status bar ────────────────────────────────────────────────────────
        status_row = QHBoxLayout()
        self._status_lbl = QLabel("Estado: desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        status_row.addWidget(self._status_lbl)
        status_row.addStretch()
        root.addLayout(status_row)

        # ── Connect button ───────────────────────────────────────────────────
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(34)
        self._btn_connect.clicked.connect(self._on_connect)
        root.addWidget(self._btn_connect)

        # ── Input groups ─────────────────────────────────────────────────────
        inputs_box = QGroupBox("Parámetros de entrada")
        grid = QGridLayout(inputs_box)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        # --- Sub-header helper ------------------------------------------------
        def _header(text: str, row: int):
            lbl = QLabel(f"<b>{text}</b>")
            grid.addWidget(lbl, row, 0, 1, 4)

        col_span = 4
        r = 0

        # Radios
        _header("Radios [m]", r); r += 1

        lbl, self._r_inner = _field("r_inner", "1.0",  "Radio interior – borde del agujero central")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._r_inner, r, 1)
        lbl, self._r_mid1  = _field("r_mid1",  "2.0",  "Límite Zona 1 / Zona 2")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._r_mid1,  r, 3)
        r += 1

        lbl, self._r_mid2  = _field("r_mid2",  "3.5",  "Límite Zona 2 / Zona 3")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._r_mid2,  r, 1)
        lbl, self._r_outer = _field("r_outer", "5.0",  "Radio exterior del anillo")
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
        lbl, self._E_mat    = _field("E [kN/m²]", "2.5e7", "Módulo de elasticidad")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._E_mat,    r, 3)
        r += 1

        lbl, self._nu_mat = _field("nu", "0.2", "Coeficiente de Poisson")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._nu_mat, r, 1)
        lbl, self._alpha  = _field("alpha [1/°C]", "1e-5", "Coeficiente de expansión térmica")
        grid.addWidget(lbl, r, 2); grid.addWidget(self._alpha,  r, 3)
        r += 1

        # Discretización
        _header("Discretización", r); r += 1

        lbl, self._n_segs = _field("n_segs", "36", "Segmentos angulares (≥ 12 recomendado)")
        grid.addWidget(lbl, r, 0); grid.addWidget(self._n_segs, r, 1)
        r += 1

        root.addWidget(inputs_box)

        # ── Run button ────────────────────────────────────────────────────────
        self._btn_run = QPushButton("Ejecutar Script")
        self._btn_run.setFixedHeight(34)
        self._btn_run.setEnabled(False)
        self._btn_run.clicked.connect(self._on_run)
        root.addWidget(self._btn_run)

        # ── Output log ────────────────────────────────────────────────────────
        output_box = QGroupBox("Salida")
        out_layout = QVBoxLayout(output_box)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 9))
        self._log.setMinimumHeight(160)
        out_layout.addWidget(self._log)
        root.addWidget(output_box)

        # ── Disconnect button ─────────────────────────────────────────────────
        self._btn_disconnect = QPushButton("Desconectar de SAP2000")
        self._btn_disconnect.setFixedHeight(34)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        root.addWidget(self._btn_disconnect)

    # ── Slot helpers ──────────────────────────────────────────────────────────

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
        """Disable all action buttons while a worker is running."""
        self._btn_connect.setEnabled(not is_busy and not bridge.is_connected)
        self._btn_run.setEnabled(not is_busy and bridge.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and bridge.is_connected)

    # ── Connect ───────────────────────────────────────────────────────────────

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy(True)
        self._worker = ConnectWorker()
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

    # ── Run ───────────────────────────────────────────────────────────────────

    def _build_script(self) -> str:
        """Read the input fields and render the parametric script."""
        return textwrap.dedent(f"""\
            # ─── Generated by gui_ring_areas.py ────────────────────────────────────────

            r_inner = {self._r_inner.text()}
            r_mid1  = {self._r_mid1.text()}
            r_mid2  = {self._r_mid2.text()}
            r_outer = {self._r_outer.text()}

            t1 = {self._t1.text()}
            t2 = {self._t2.text()}

            mat_name = "{self._mat_name.text()}"
            E_mat    = {self._E_mat.text()}
            nu_mat   = {self._nu_mat.text()}
            alpha    = {self._alpha.text()}

            n_segs = {self._n_segs.text()}

            # ── helpers ────────────────────────────────────────────────────────────────

            def ring_pts(radius, n):
                return [
                    (radius * math.cos(2.0 * math.pi * i / n),
                     radius * math.sin(2.0 * math.pi * i / n))
                    for i in range(n)
                ]

            # ── Task 1: init ────────────────────────────────────────────────────────────

            ret = SapModel.InitializeNewModel()
            assert ret == 0, f"InitializeNewModel failed: {{ret}}"
            ret = SapModel.File.NewBlank()
            assert ret == 0, f"NewBlank failed: {{ret}}"
            ret = SapModel.SetPresentUnits(6)
            assert ret == 0, f"SetPresentUnits failed: {{ret}}"
            result["task_1_init"] = True

            # ── Task 2: material ────────────────────────────────────────────────────────

            ret = SapModel.PropMaterial.SetMaterial(mat_name, 2)
            assert ret == 0, f"SetMaterial failed: {{ret}}"
            ret = SapModel.PropMaterial.SetMPIsotropic(mat_name, E_mat, nu_mat, alpha)
            assert ret == 0, f"SetMPIsotropic failed: {{ret}}"
            result["task_2_material"] = mat_name

            # ── Task 3: shell sections ──────────────────────────────────────────────────

            ret = SapModel.PropArea.SetShell_1("SHELL_T1", 1, True, mat_name, 0, t1, t1)
            assert ret == 0, f"SetShell_1(SHELL_T1) failed: {{ret}}"
            ret = SapModel.PropArea.SetShell_1("SHELL_T2", 1, True, mat_name, 0, t2, t2)
            assert ret == 0, f"SetShell_1(SHELL_T2) failed: {{ret}}"
            result["task_3_sections"] = {{"SHELL_T1": t1, "SHELL_T2": t2}}

            # ── Task 4: geometry ────────────────────────────────────────────────────────

            zones = [
                (r_inner, r_mid1,  "SHELL_T1", "ZONA1_interior"),
                (r_mid1,  r_mid2,  "SHELL_T2", "ZONA2_intermedia"),
                (r_mid2,  r_outer, "SHELL_T1", "ZONA3_exterior"),
            ]
            area_count = {{"ZONA1_interior": 0, "ZONA2_intermedia": 0, "ZONA3_exterior": 0}}

            for (r_in, r_out, prop, label) in zones:
                pts_in  = ring_pts(r_in,  n_segs)
                pts_out = ring_pts(r_out, n_segs)
                for i in range(n_segs):
                    j = (i + 1) % n_segs
                    x = [pts_in[i][0], pts_out[i][0], pts_out[j][0], pts_in[j][0]]
                    y = [pts_in[i][1], pts_out[i][1], pts_out[j][1], pts_in[j][1]]
                    z = [0.0, 0.0, 0.0, 0.0]
                    raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", prop, "")
                    assert raw[-1] == 0, f"AddByCoord({{label}}[{{i}}]) failed: {{raw[-1]}}"
                    area_count[label] += 1

            result["task_4_geometry"] = area_count
            result["total_areas"]     = sum(area_count.values())

            # ── Task 5: save & refresh ──────────────────────────────────────────────────

            ret = SapModel.File.Save(sap_temp_dir + r"\\ring_areas_model.sdb")
            assert ret == 0, f"File.Save failed: {{ret}}"
            SapModel.View.RefreshView(0, False)
            result["task_5_saved"] = True

            # ── summary ────────────────────────────────────────────────────────────────

            result["success"]     = True
            result["radii"]       = {{"r_inner": r_inner, "r_mid1": r_mid1,
                                      "r_mid2": r_mid2,  "r_outer": r_outer}}
            result["thicknesses"] = {{"t1 (Zona1+Zona3)": t1, "t2 (Zona2)": t2}}
            result["n_segments"]  = n_segs
        """)

    def _on_run(self):
        script = self._build_script()
        self._log_append("\n─── Ejecutando script ───────────────────────────────")
        self._busy(True)
        self._worker = RunWorker(script)
        self._worker.finished.connect(self._on_run_done)
        self._worker.start()

    def _on_run_done(self, res: dict):
        self._busy(False)
        if res.get("success"):
            self._log_append("✔ Script ejecutado exitosamente")
            data = res.get("result", {})
            if data:
                import json as _json
                self._log_append(_json.dumps(data, indent=2, ensure_ascii=False))
        else:
            err  = res.get("error", "")
            stdout = res.get("stdout", "")
            stderr = res.get("stderr", "")
            self._log_append(f"✘ Error: {err}")
            if stdout:
                self._log_append(f"stdout:\n{stdout}")
            if stderr:
                self._log_append(f"stderr:\n{stderr}")

    # ── Disconnect ────────────────────────────────────────────────────────────

    def _on_disconnect(self):
        self._log_append("Desconectando...")
        self._busy(True)
        self._worker = DisconnectWorker()
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
