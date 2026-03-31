"""
Shared — Infraestructura compartida para módulos de Steel Connections
=====================================================================
Contiene clases y funciones reutilizadas por todos los backends y GUIs
del módulo steel_connections:

  - SapConnection: conexión COM directa a SAP2000
  - _check_ret: verificación de códigos de retorno API
  - _shape_coords_2d: generación de coordenadas 2D (círculo / cuadrado)
  - _build_axes / _local_to_global_axes: transformación 3D con rotación
  - Workers GUI: ConnectWorker, DisconnectWorker, RunWorker, GetCoordsWorker
  - create_base_model: inicializa modelo base con materiales de acero
"""

import math
import comtypes.client
from typing import List, Tuple

from PySide6.QtCore import QThread, Signal


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing: bool = True) -> dict:
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                self.sap_object.ApplicationStart()

            self.sap_model = self.sap_object.SapModel
            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())
            return {"connected": True, "version": version, "model_path": model_path}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Helpers de API
# ══════════════════════════════════════════════════════════════════════════════

def _check_ret(ret) -> bool:
    """Retorna True si el código de retorno de la API es 0 (éxito)."""
    if isinstance(ret, (list, tuple)):
        return int(ret[-1]) == 0
    return int(ret) == 0


# ══════════════════════════════════════════════════════════════════════════════
# Helpers de geometría
# ══════════════════════════════════════════════════════════════════════════════

def _shape_coords_2d(
    shape_type: str,
    center_u: float,
    center_v: float,
    dim: float,
    num_points: int,
) -> List[Tuple[float, float]]:
    """Genera coordenadas 2D (u, v) distribuidas sobre la forma indicada.

    Args:
        shape_type: "circulo" o "cuadrado" (case-insensitive, acepta tildes).
        center_u, center_v: Centro en espacio local 2D.
        dim: Diámetro si es círculo, Lado si es cuadrado.
        num_points: Número de puntos a generar.
    """
    coords: List[Tuple[float, float]] = []
    radius = dim / 2.0
    shape = shape_type.lower().replace("í", "i").replace("ó", "o")

    if "circulo" in shape or "circle" in shape:
        for i in range(num_points):
            angle = -2.0 * math.pi * i / num_points
            coords.append((center_u + radius * math.cos(angle),
                           center_v + radius * math.sin(angle)))
    else:  # cuadrado
        perimeter = 4.0 * dim
        step = perimeter / float(num_points) if num_points > 0 else 0.0
        for i in range(num_points):
            dist = i * step
            if dist < radius:
                u_l, v_l = radius, -dist
            elif dist < radius + dim:
                u_l, v_l = radius - (dist - radius), -radius
            elif dist < radius + 2.0 * dim:
                u_l, v_l = -radius, -radius + (dist - radius - dim)
            elif dist < radius + 3.0 * dim:
                u_l, v_l = -radius + (dist - radius - 2.0 * dim), radius
            else:
                u_l, v_l = radius, radius - (dist - radius - 3.0 * dim)
            coords.append((center_u + u_l, center_v + v_l))

    return coords


def _build_axes(
    plane: str, angle_deg: float,
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]:
    """Construye los 3 ejes unitarios del plano con rotación arbitraria.

    Args:
        plane: "XY", "XZ" o "YZ".
        angle_deg: Ángulo de rotación dentro del plano (grados).

    Returns:
        (e_u, e_v, e_n) — vectores unitarios:
          e_u: dirección horizontal del patrón
          e_v: dirección vertical del patrón
          e_n: normal al plano
    """
    theta = math.radians(angle_deg)
    c, s = math.cos(theta), math.sin(theta)

    if plane == "XZ":
        e_u = (c, 0.0, s)
        e_v = (-s, 0.0, c)
        e_n = (0.0, 1.0, 0.0)
    elif plane == "YZ":
        e_u = (0.0, c, s)
        e_v = (0.0, -s, c)
        e_n = (1.0, 0.0, 0.0)
    else:  # XY
        e_u = (c, s, 0.0)
        e_v = (-s, c, 0.0)
        e_n = (0.0, 0.0, 1.0)

    return e_u, e_v, e_n


def _local_to_global_axes(
    origin: Tuple[float, float, float],
    e_u: Tuple[float, float, float],
    e_v: Tuple[float, float, float],
    e_n: Tuple[float, float, float],
    u: float, v: float, n: float,
) -> Tuple[float, float, float]:
    """P_global = origin + u·ê_u + v·ê_v + n·ê_n"""
    return (
        origin[0] + u * e_u[0] + v * e_v[0] + n * e_n[0],
        origin[1] + u * e_u[1] + v * e_v[1] + n * e_n[1],
        origin[2] + u * e_u[2] + v * e_v[2] + n * e_n[2],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Workers GUI (PySide6 QThread)
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    """Conecta a SAP2000 y obtiene las propiedades Shell disponibles."""
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
    """Desconecta de SAP2000."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        self.finished.emit(self._conn.disconnect())


class RunWorker(QThread):
    """Ejecuta backend.run(config) en hilo separado."""
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
# Modelo Base — Crear modelo limpio con materiales de acero
# ══════════════════════════════════════════════════════════════════════════════

# Unidades N-mm-C (eUnits = 9)
N_MM_UNITS = 9

# Materiales estándar para conexiones de acero (unidades N-mm)
BASE_MATERIALS = [
    {
        "name": "A36",
        "E": 200000.0, "U": 0.30, "A": 1.17e-5,
        "w": 7.6973e-5,  # N/mm³
        "fy": 248.0, "fu": 400.0,
        "efy": 372.0, "efu": 440.0,
    },
    {
        "name": "A500_GrB",
        "E": 200000.0, "U": 0.30, "A": 1.17e-5,
        "w": 7.6973e-5,
        "fy": 317.0, "fu": 400.0,
        "efy": 349.0, "efu": 440.0,
    },
    {
        "name": "A325",
        "E": 200000.0, "U": 0.30, "A": 1.17e-5,
        "w": 7.6973e-5,
        "fy": 635.0, "fu": 825.0,
        "efy": 700.0, "efu": 900.0,
    },
    {
        "name": "A490",
        "E": 200000.0, "U": 0.30, "A": 1.17e-5,
        "w": 7.6973e-5,
        "fy": 895.0, "fu": 1035.0,
        "efy": 985.0, "efu": 1140.0,
    },
]


def create_base_model(sap_model) -> dict:
    """Crea un modelo nuevo en blanco con unidades N-mm-C y materiales de acero.

    Args:
        sap_model: Referencia a SapModel (COM).

    Returns:
        dict con resultados: success, materials_created, errors.
    """
    errors = []

    # ── Inicializar modelo nuevo ────────────────────────────────────────
    ret = sap_model.InitializeNewModel(N_MM_UNITS)
    if not _check_ret(ret):
        return {"success": False, "error": f"InitializeNewModel falló: {ret}"}

    ret = sap_model.File.NewBlank()
    if not _check_ret(ret):
        return {"success": False, "error": f"NewBlank falló: {ret}"}

    # ── Crear materiales ────────────────────────────────────────────────
    mat_count = 0
    for mat in BASE_MATERIALS:
        name = mat["name"]

        # 1. Definir material (tipo 1 = Steel)
        ret = sap_model.PropMaterial.SetMaterial(name, 1)
        if not _check_ret(ret):
            errors.append(f"SetMaterial '{name}' falló: {ret}")
            continue

        # 2. Propiedades isotrópicas (E, ν, α)
        ret = sap_model.PropMaterial.SetMPIsotropic(
            name, mat["E"], mat["U"], mat["A"]
        )
        if not _check_ret(ret):
            errors.append(f"SetMPIsotropic '{name}' falló")

        # 3. Peso
        ret = sap_model.PropMaterial.SetWeightAndMass(name, 1, mat["w"])
        if not _check_ret(ret):
            errors.append(f"SetWeightAndMass '{name}' falló")

        # 4. Propiedades de diseño de acero
        #    SetOSteel_1(Name, Fy, Fu, eFy, eFu,
        #                SSType, SSHysType, StrainAtHardening,
        #                StrainAtMaxStress, StrainAtRupture, FinalSlope)
        ret = sap_model.PropMaterial.SetOSteel_1(
            name, mat["fy"], mat["fu"], mat["efy"], mat["efu"],
            1,    # SSType = 1 (simple)
            0,    # SSHysType = 0 (kinematic)
            0.015,  # strain at hardening
            0.08,   # strain at max stress
            0.20,   # strain at rupture
            0.0,    # final slope
        )
        if _check_ret(ret):
            mat_count += 1
        else:
            errors.append(f"SetOSteel_1 '{name}' falló")

    return {
        "success": True,
        "materials_created": mat_count,
        "material_names": [m["name"] for m in BASE_MATERIALS],
        "units": "N-mm-C",
        "errors": errors,
    }


class BaseModelWorker(QThread):
    """Crea modelo base en hilo separado."""
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        try:
            if not self._conn.is_connected:
                self.finished.emit({"success": False, "error": "No conectado."})
                return
            result = create_base_model(self._conn.sap_model)
            # Recargar propiedades Shell después de crear modelo
            if result.get("success"):
                try:
                    ret = self._conn.sap_model.PropArea.GetNameList(0, [])
                    if isinstance(ret, (list, tuple)) and int(ret[-1]) == 0 and int(ret[0]) > 0:
                        result["shell_props"] = list(ret[1])
                    else:
                        result["shell_props"] = []
                except Exception:
                    result["shell_props"] = []
            self.finished.emit(result)
        except Exception as exc:
            self.finished.emit({"success": False, "error": str(exc)})
