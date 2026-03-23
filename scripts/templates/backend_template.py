"""
Backend Template — SAP2000 Standalone (COM Directo)
====================================================
Plantilla base para backends que conectan a SAP2000 vía comtypes.client
sin depender del MCP server.

Uso:
    1. Copiar este archivo como backend_{nombre}.py
    2. Renombrar la clase MyBackend → {Nombre}Backend
    3. Reemplazar el método run() con la lógica del script verificado
    4. Ajustar los parámetros de entrada en run(params)

Convenciones:
    - SapConnection maneja connect/disconnect COM directo
    - Backend.run(params) ejecuta la lógica y retorna dict de resultados
    - Sin imports de mcp_server/, sap_bridge, sap_executor
    - Estilo de script: tareas numeradas, asserts, result dict
      (referencia: example_1001_simple_beam.py)
"""

import math
import comtypes.client
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Any


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    # ── Conectar ──────────────────────────────────────────────────────────────

    def connect(self, attach_to_existing: bool = True) -> dict:
        """Conecta a una instancia de SAP2000 en ejecución.

        Args:
            attach_to_existing: Si True, se conecta a una instancia ya abierta.

        Returns:
            dict con claves: connected (bool), version (str), model_path (str),
            error (str, solo si falla).
        """
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

            return {
                "connected": True,
                "version": version,
                "model_path": model_path,
            }
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    # ── Desconectar ───────────────────────────────────────────────────────────

    def disconnect(self) -> dict:
        """Libera la referencia COM (no cierra SAP2000)."""
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Configuración (Dataclass)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class MyConfig:
    """Parámetros de entrada para el backend.

    Reemplazar con los parámetros específicos de tu script.
    Ejemplo para ring_areas: r_inner, r_outer, t1, t2, n_segs, etc.
    """

    param_1: float = 1.0
    param_2: float = 2.0
    param_3: str = "DEFAULT"


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class MyBackend:
    """Backend standalone para SAP2000.

    Renombrar a {Nombre}Backend (ej: RingAreasBackend, PlacaBaseBackend).
    """

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config: MyConfig) -> dict:
        """Ejecuta la lógica principal del script.

        Args:
            config: Parámetros de entrada.

        Returns:
            dict con resultados (éxito, métricas, errores).
        """
        SapModel = self.sap_model
        result = {}

        # ── Task 1: Inicializar ──────────────────────────────────────────
        ret = SapModel.InitializeNewModel()
        assert ret == 0, f"InitializeNewModel failed: {ret}"

        ret = SapModel.File.NewBlank()
        assert ret == 0, f"NewBlank failed: {ret}"

        ret = SapModel.SetPresentUnits(6)  # kN_m_C
        assert ret == 0, f"SetPresentUnits failed: {ret}"

        result["task_1_init"] = True

        # ── Task 2: Material ─────────────────────────────────────────────
        # TODO: Reemplazar con la lógica de tu script verificado
        ret = SapModel.PropMaterial.SetMaterial(config.param_3, 2)
        assert ret == 0, f"SetMaterial failed: {ret}"

        result["task_2_material"] = config.param_3

        # ── Task N: ... ──────────────────────────────────────────────────
        # Copiar tareas del script verificado, reemplazando:
        #   - Variables globales → config.param_X
        #   - SapModel global → self.sap_model (ya asignado arriba)
        #   - result global → result local (dict)

        result["success"] = True
        return result


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = MyBackend(conn)
        config = MyConfig(param_1=1.0, param_2=2.0, param_3="TEST_MAT")

        try:
            output = backend.run(config)
            import json
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
