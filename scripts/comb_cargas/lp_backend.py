"""Backend de Load Patterns — SAP2000 (COM directo)."""

from sap_connection import SapConnection


class LoadPatternsBackend:
    """CRUD de Load Patterns en SAP2000."""

    LOAD_TYPES = {
        1:  "Dead",
        2:  "SuperDead",
        3:  "Live",
        4:  "ReduceLive",
        5:  "Quake",
        6:  "Wind",
        7:  "Snow",
        8:  "Other",
        9:  "Move",
        10: "Temperature",
        11: "RoofLive",
        12: "Notional",
        13: "PatternLive",
        14: "Wave",
        15: "Braking",
        16: "Centrifugal",
        17: "Friction",
        18: "Ice",
        19: "WindOnLiveLoad",
        20: "HorizEarthPressure",
        21: "VertEarthPressure",
        22: "EarthSurcharge",
        23: "Downdrag",
        24: "VehicleCollision",
        25: "VesselCollision",
        26: "TempGradient",
        27: "Settlement",
        28: "Shrinkage",
        29: "Creep",
        30: "WaterLoadPressure",
        31: "LiveLoadSurcharge",
        32: "LockedInForces",
        33: "PedestrianLL",
        34: "Prestress",
        35: "Hyperstatic",
        36: "Buoyancy",
        37: "StreamFlow",
        38: "Impact",
        39: "Construction",
    }

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def get_patterns(self) -> list:
        """Retorna lista de dicts: [{'name': str, 'type': int, 'sw_mult': float}, ...]"""
        SapModel = self.sap_model
        patterns = []
        try:
            raw = SapModel.LoadPatterns.GetNameList(0, [])
            if raw[-1] != 0 or raw[0] == 0:
                return []

            names = raw[1]
            if not isinstance(names, (list, tuple)):
                names = [names]

            for name in names:
                name = str(name).strip()
                ret_type = SapModel.LoadPatterns.GetLoadType(name)
                ltype = int(ret_type[0]) if ret_type[-1] == 0 else 1
                ret_mult = SapModel.LoadPatterns.GetSelfWtMultiplier(name)
                sw_mult = float(ret_mult[0]) if ret_mult[-1] == 0 else 0.0
                patterns.append({"name": name, "type": ltype, "sw_mult": sw_mult})

        except Exception as e:
            print(f"Error obteniendo Load Patterns: {e}")
        return patterns

    def push_patterns(self, patterns_data: list, names_to_delete: list, add_load_case: bool) -> dict:
        """
        Envía Load Patterns a SAP2000: elimina primero, luego add/update.
        Para eliminar un patrón con Load Case asociado, intenta borrar el LC antes.
        Retorna: {'sent': int, 'deleted': int, 'failed_deletions': list, 'failed_adds': list}
        """
        SapModel = self.sap_model

        try:
            SapModel.SetModelIsLocked(False)
        except Exception:
            pass

        deleted = 0
        failed_deletions = []
        for name in names_to_delete:
            ret = SapModel.LoadPatterns.Delete(name)
            ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
            if ret_code != 0:
                try:
                    SapModel.LoadCases.Delete(name)
                except Exception:
                    pass
                ret2 = SapModel.LoadPatterns.Delete(name)
                ret_code2 = ret2[-1] if isinstance(ret2, (list, tuple)) else ret2
                if ret_code2 == 0:
                    deleted += 1
                else:
                    failed_deletions.append(name)
            else:
                deleted += 1

        sent = 0
        failed_adds = []

        try:
            raw = SapModel.LoadPatterns.GetNameList(0, [])
            existing = set()
            if raw[-1] == 0 and raw[0] > 0:
                ns = raw[1]
                if not isinstance(ns, (list, tuple)):
                    ns = [ns]
                existing = {str(n).strip() for n in ns}
        except Exception:
            existing = set()

        for p in patterns_data:
            name = str(p["name"]).strip()
            ltype = int(p["type"])
            sw_mult = float(p["sw_mult"])

            if not name:
                continue

            if name not in existing:
                ret = SapModel.LoadPatterns.Add(name, ltype, sw_mult, add_load_case)
                ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
                if ret_code != 0:
                    failed_adds.append(name)
                    continue
            else:
                SapModel.LoadPatterns.SetLoadType(name, ltype)
                SapModel.LoadPatterns.SetSelfWtMultiplier(name, sw_mult)

            sent += 1

        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        return {
            "sent": sent,
            "deleted": deleted,
            "failed_deletions": failed_deletions,
            "failed_adds": failed_adds,
        }
