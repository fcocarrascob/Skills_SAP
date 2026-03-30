"""
Backend de Combinaciones de Carga — SAP2000 Standalone (COM Directo)
=====================================================================
Lógica pura para gestionar combinaciones de carga en SAP2000.
Sin dependencias de MCP server, app_logger, ni sap_utils_common.

Uso:
    conn = SapConnection()
    conn.connect()
    backend = CombosBackend(conn)
    cases = backend.get_load_cases()
    combos = backend.get_combinations()
    backend.push_combinations([...])
    conn.disconnect()
"""

import comtypes.client


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
        """Conecta a una instancia de SAP2000 en ejecución.

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

            return {"connected": True, "version": version, "model_path": model_path}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        """Libera la referencia COM (no cierra SAP2000)."""
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}



# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class CombosBackend:
    """Backend standalone para gestión de combinaciones de carga en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def get_load_cases(self) -> list:
        """Retorna una lista con los nombres de todos los Load Cases."""
        SapModel = self.sap_model
        try:
            ret = SapModel.LoadCases.GetNameList()
            if ret[-1] == 0 and ret[0] > 0:
                names = ret[1]
                if not isinstance(names, (list, tuple)):
                    names = [names]
                return [str(n).strip() for n in names]
        except Exception as e:
            print(f"Error obteniendo Load Cases: {e}")
        return []

    def get_combinations(self) -> list:
        """
        Retorna lista de dicts con la definición de cada combinación.
        Estructura: [{'name': 'COMB1', 'type': 0, 'items': {'DEAD': 1.2, 'LIVE': 1.6}}, ...]
        """
        SapModel = self.sap_model
        combos = []
        try:
            ret_names = SapModel.RespCombo.GetNameList()
            if ret_names[-1] != 0 or ret_names[0] == 0:
                return []

            names = ret_names[1]
            if not isinstance(names, (list, tuple)):
                names = [names]

            for name in names:
                name = str(name).strip()

                ret_type = SapModel.RespCombo.GetTypeOAPI(name)
                c_type = ret_type[0] if ret_type[-1] == 0 else 0

                items = {}
                ret_list = SapModel.RespCombo.GetCaseList(name)

                if ret_list[-1] == 0 and ret_list[0] > 0:
                    c_types = ret_list[1]
                    c_names = ret_list[2]
                    sfs = ret_list[3]

                    if not isinstance(c_names, (list, tuple)):
                        c_names = [c_names]
                    if not isinstance(c_types, (list, tuple)):
                        c_types = [c_types]
                    if not isinstance(sfs, (list, tuple)):
                        sfs = [sfs]

                    count = min(len(c_names), len(c_types), len(sfs), ret_list[0])
                    for i in range(count):
                        try:
                            if int(c_types[i]) == 0:
                                items[str(c_names[i]).strip()] = sfs[i]
                        except Exception:
                            pass

                combos.append({"name": name, "type": c_type, "items": items})

        except Exception as e:
            print(f"Error obteniendo combinaciones: {e}")
        return combos

    def _clear_combo_items(self, name: str):
        """Elimina todos los casos de carga de una combinación existente."""
        SapModel = self.sap_model
        try:
            ret_list = SapModel.RespCombo.GetCaseList(name)
            if ret_list[-1] == 0 and ret_list[0] > 0:
                c_types = ret_list[1]
                c_names = ret_list[2]

                if not isinstance(c_names, (list, tuple)):
                    c_names = [c_names]
                if not isinstance(c_types, (list, tuple)):
                    c_types = [c_types]

                count = min(len(c_names), len(c_types), ret_list[0])
                for i in range(count):
                    try:
                        SapModel.RespCombo.DeleteCase(
                            name, int(c_types[i]), str(c_names[i]).strip()
                        )
                    except Exception:
                        pass
        except Exception as e:
            print(f"Aviso limpiando combinación {name}: {e}")

    def delete_combination(self, name: str) -> bool:
        """Elimina una combinación de SAP2000 por nombre. Retorna True si tuvo éxito."""
        SapModel = self.sap_model
        try:
            ret = SapModel.RespCombo.Delete(name)
            ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
            if ret_code != 0:
                print(f"No se pudo eliminar '{name}' (código {ret_code})")
            return ret_code == 0
        except Exception as e:
            print(f"Error eliminando combinación '{name}': {e}")
            return False

    def push_combinations(self, combos_data: list) -> int:
        """
        Envía las combinaciones a SAP2000.
        combos_data: lista de dicts {'name': str, 'type': int, 'items': {'CASE': factor}}
        Retorna el número de combinaciones procesadas con éxito.
        """
        SapModel = self.sap_model
        success_count = 0

        try:
            SapModel.SetModelIsLocked(False)
        except Exception:
            pass

        for combo in combos_data:
            name = str(combo["name"]).strip()
            ctype = int(combo["type"])
            items = combo["items"]

            if not name:
                continue

            ret_add = SapModel.RespCombo.Add(name, ctype)
            if isinstance(ret_add, (list, tuple)):
                ret_add = ret_add[-1]

            if ret_add != 0:
                SapModel.RespCombo.SetTypeOAPI(name, ctype)
                self._clear_combo_items(name)

            for case_name, factor in items.items():
                try:
                    val = float(factor)
                    if val != 0:
                        ret_case = SapModel.RespCombo.SetCaseList(
                            name, 0, str(case_name).strip(), val
                        )
                        ret_code = ret_case[-1] if isinstance(ret_case, (list, tuple)) else ret_case
                        if ret_code != 0:
                            print(f"No se pudo asignar '{case_name}' a '{name}' (código {ret_code})")
                except Exception as e:
                    print(f"Error procesando factor para {case_name}: {e}")

            success_count += 1

        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        print(f"Se procesaron {success_count} combinaciones")
        return success_count


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = CombosBackend(conn)
        try:
            cases = backend.get_load_cases()
            print(f"Load Cases ({len(cases)}): {cases}")

            combos = backend.get_combinations()
            import json
            print(json.dumps(combos, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()