"""
Backend — SAP2000 Modelo Base Generator (Standalone)
=====================================================
Crea un modelo base estandarizado con materiales, patrones de carga,
secciones, espectros NCh2369 y combinaciones (LRFD/ASD/NCh).

Conexión: COM directo vía comtypes.client (sin MCP).
"""

import math
import comtypes.client
from dataclasses import dataclass
from typing import List, Tuple, Optional

from config import (
    TON_M_UNITS, GRAVITY, AR_BY_ZONE, SOIL_PARAMS,
    LOAD_PATTERNS, DEFAULT_MATERIALS,
    DEFAULT_REBARS, DEFAULT_I_SECTIONS, DEFAULT_TUBE_SECTIONS,
    DEFAULT_ANGLE_SECTIONS, DEFAULT_CHANNEL_SECTIONS,
    NCH_COMBOS, LRFD_COMBOS, ASD_COMBOS,
)


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
# Configuración de Entrada
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BaseModelConfig:
    """Parámetros sísmicos para el modelo base."""

    zone: int = 2            # Zona sísmica (1, 2, 3)
    soil: str = "C"          # Tipo de suelo (A-E)
    importance: float = 1.0  # Factor de importancia I

    # Horizontal
    r_x: float = 3.0        # Factor de reducción R dirección X
    r_y: float = 3.0        # Factor de reducción R dirección Y
    damping_x: float = 0.03 # Amortiguamiento X (ej. 0.03 = 3%)
    damping_y: float = 0.03 # Amortiguamiento Y

    # Vertical
    r_v: float = 2.0        # Factor de reducción R vertical
    xi_v: float = 0.03      # Amortiguamiento vertical


# ══════════════════════════════════════════════════════════════════════════════
# Helpers — ret code checking (reemplaza sap_utils_common)
# ══════════════════════════════════════════════════════════════════════════════

def _check_ret(ret) -> bool:
    """Verifica si un return code/tuple indica éxito (0)."""
    if isinstance(ret, (list, tuple)):
        return len(ret) > 0 and int(ret[-1]) == 0
    return int(ret) == 0


# ══════════════════════════════════════════════════════════════════════════════
# Funciones de Espectro NCh2369 — módulo-level (sin dependencia SAP2000)
# ══════════════════════════════════════════════════════════════════════════════

def _spectrum_shape(ar: float, sp, T: float,
                    scale_factor: float = 1.0, period_shift: float = 1.0) -> float:
    """Calcula la forma espectral Sa para un período dado.

    Args:
        ar: Aceleración efectiva de la zona.
        sp: SoilParameters.
        T: Período estructural (s).
        scale_factor: 1.0 horizontal, 0.7 vertical.
        period_shift: 1.0 horizontal, 1.7 vertical.

    Returns:
        Aceleración espectral (g) sin reducción R ni corrección damping.
    """
    if T == 0:
        return scale_factor * ar * sp.S

    T_shifted = period_shift * T
    ratio = (T_shifted / sp.T0) if sp.T0 > 0 else 0.0
    num = 1.0 + sp.r * (ratio ** sp.p)
    den = 1.0 + (ratio ** sp.q)
    return scale_factor * ar * sp.S * num / den


def _r_star(T: float, R: float, t1: float) -> float:
    """Calcula R* (factor de reducción corregido por período corto).

    NCh2369: Para períodos cortos, R se interpola linealmente
    desde 1.5 hasta R en el rango [0, 0.16·R·T1].
    """
    limit = 0.16 * R * t1
    if limit <= 0 or T >= limit:
        return R
    return 1.5 + (R - 1.5) * (T / limit)


def compute_spectrum(zone: int, soil: str, I: float, R: float, damp: float,
                     scale_factor: float = 1.0, period_shift: float = 1.0,
                     apply_r_star: bool = True) -> Tuple[List[float], List[float]]:
    """Genera un espectro de diseño NCh2369 (horizontal o vertical).

    Args:
        zone: Zona sísmica (1, 2, 3).
        soil: Tipo de suelo (A-E).
        I: Factor de importancia.
        R: Factor de reducción.
        damp: Amortiguamiento (ej. 0.05).
        scale_factor: 1.0 para horizontal, 0.7 para vertical.
        period_shift: 1.0 para horizontal, 1.7 para vertical.
        apply_r_star: True para horizontal (aplica R*), False para vertical.

    Returns:
        Tuple de (períodos, aceleraciones) en unidades g.
    """
    if zone not in AR_BY_ZONE or soil not in SOIL_PARAMS:
        return [], []

    ar = AR_BY_ZONE[zone]
    sp = SOIL_PARAMS[soil]

    period_limit = 5.0
    period_step = 0.01
    n_points = int(period_limit / period_step)

    periods = []
    accels = []

    damping_scale = (0.05 / damp) ** 0.4

    for i in range(n_points + 1):
        T = round(i * period_step, 4)
        periods.append(T)

        sa = _spectrum_shape(ar, sp, T, scale_factor, period_shift)
        r_eff = _r_star(T, R, sp.T1) if apply_r_star else R
        accel = I * sa * damping_scale / r_eff
        accels.append(accel)

    return periods, accels


def compute_nch_spectrum(zone: int, soil: str, I: float,
                         R: float, damp: float) -> Tuple[List[float], List[float]]:
    """Calcula espectro horizontal NCh2369."""
    return compute_spectrum(zone, soil, I, R, damp,
                            scale_factor=1.0, period_shift=1.0, apply_r_star=True)


def compute_vertical_spectrum(zone: int, soil: str, I: float,
                              R_v: float, xi_v: float) -> Tuple[List[float], List[float]]:
    """Calcula espectro vertical NCh2369 (factor 0.7, período 1.7×T, sin R*)."""
    return compute_spectrum(zone, soil, I, R_v, xi_v,
                            scale_factor=0.7, period_shift=1.7, apply_r_star=False)


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class BaseModelBackend:
    """Backend standalone para crear modelo base en SAP2000."""

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def _log(self, message: str):
        print(message)

    # ── Ejecución principal ──────────────────────────────────────────────

    def run(self, config: BaseModelConfig) -> dict:
        """Ejecuta la creación completa del modelo base.

        Args:
            config: Parámetros sísmicos de entrada.

        Returns:
            dict con resultados (materiales, patrones, secciones, combos creados).
        """
        SapModel = self.sap_model
        result = {}
        errors = []

        # ── Task 1: Inicializar ──────────────────────────────────────────
        self._log("Task 1: Inicializando modelo nuevo...")
        ret = SapModel.InitializeNewModel(TON_M_UNITS)
        assert _check_ret(ret), f"InitializeNewModel failed: {ret}"

        ret = SapModel.File.NewBlank()
        assert _check_ret(ret), f"NewBlank failed: {ret}"

        result["task_1_init"] = True

        # ── Task 2: Materiales ───────────────────────────────────────────
        self._log("Task 2: Configurando materiales...")
        mat_errors, mat_count = self._setup_materials()
        result["materials_created"] = mat_count
        errors.extend(mat_errors)

        # ── Task 3: Patrones de carga ────────────────────────────────────
        self._log("Task 3: Creando patrones de carga...")
        pat_count = self._setup_load_patterns()
        result["patterns_created"] = pat_count

        # ── Task 4: Secciones de frame ───────────────────────────────────
        self._log("Task 4: Definiendo secciones de frame...")
        sec_count = self._setup_frame_sections()
        result["sections_created"] = sec_count

        # ── Task 5: Armaduras (rebar) ────────────────────────────────────
        self._log("Task 5: Creando propiedades de armadura...")
        rebar_count = self._setup_rebars()
        result["rebars_created"] = rebar_count

        # ── Task 6: Espectros sísmicos + Load Cases ──────────────────────
        self._log("Task 6: Configurando espectros sísmicos...")
        func_count, case_count = self._setup_seismic_definitions(config)
        result["functions_created"] = func_count
        result["cases_created"] = case_count

        # ── Task 7: Combinaciones (NCh, LRFD, ASD) ──────────────────────
        self._log("Task 7: Creando combinaciones de carga...")
        combo_count = self._setup_combinations()
        result["combos_created"] = combo_count

        # ── Task 8: Envolventes ──────────────────────────────────────────
        self._log("Task 8: Creando envolventes...")
        self._create_envelopes()

        # ── Resumen ──────────────────────────────────────────────────────
        result["success"] = True
        result["errors"] = errors
        summary = (
            f"Modelo base creado: {mat_count} materiales, {pat_count} patrones, "
            f"{sec_count} secciones, {rebar_count} rebars, "
            f"{func_count} funciones, {case_count} casos RS, {combo_count} combinaciones."
        )
        result["summary"] = summary
        self._log(summary)

        return result

    # ── Task 2: Materiales ───────────────────────────────────────────────

    def _setup_materials(self) -> Tuple[List[str], int]:
        """Configura materiales acero y hormigón."""
        SapModel = self.sap_model
        errors = []
        count = 0

        for mat in DEFAULT_MATERIALS:
            name = mat["name"]
            m_type = mat.get("mat_type_enum", 1)

            # 1. Definir Material
            ret = SapModel.PropMaterial.SetMaterial(name, m_type)
            if not _check_ret(ret):
                errors.append(f"SetMaterial '{name}' failed (Code {ret})")
                continue

            # 2. Propiedades Isotrópicas (E, U, A)
            iso = mat["isotropic"]
            ret = SapModel.PropMaterial.SetMPIsotropic(name, iso["E"], iso["U"], iso["A"])
            if not _check_ret(ret):
                errors.append(f"SetMPIsotropic '{name}' failed")

            # 3. Peso y Masa
            ret = SapModel.PropMaterial.SetWeightAndMass(name, 1, mat["w"])
            if not _check_ret(ret):
                errors.append(f"SetWeightAndMass '{name}' failed")

            # 4. Propiedades de Diseño
            if m_type == 1:  # Steel
                s = mat["steel"]
                ret = SapModel.PropMaterial.SetOSteel_1(
                    name, s["fy"], s["fu"], s["efy"], s["efu"],
                    s["sstype"], s["shys"], s["sh"], s["smax"], s["srup"], 0.0
                )
            elif m_type == 2:  # Concrete
                c = mat["concrete"]
                ret = SapModel.PropMaterial.SetOConcrete_1(
                    name, c["fc"], c["is_light"], c["fcs"],
                    c["sstype"], c["shys"], c["sfc"], c["sult"], 0.0
                )

            if _check_ret(ret):
                count += 1
                self._log(f"  Material '{name}' creado.")
            else:
                errors.append(f"SetDesignProps '{name}' failed")

        return errors, count

    # ── Task 3: Patrones de carga ────────────────────────────────────────

    def _setup_load_patterns(self) -> int:
        """Crea patrones de carga estándar."""
        SapModel = self.sap_model
        count = 0
        for lp in LOAD_PATTERNS:
            ret = SapModel.LoadPatterns.Add(lp["name"], lp["type"], lp["self_wt"], True)
            if _check_ret(ret):
                count += 1
        self._log(f"  {count} patrones creados.")
        return count

    # ── Task 4: Secciones de frame ───────────────────────────────────────

    def _setup_frame_sections(self) -> int:
        """Crea secciones de frame predeterminadas (I, Tube, Angle, Channel)."""
        SapModel = self.sap_model
        count = 0

        # I-Sections (W shapes)
        for sec in DEFAULT_I_SECTIONS:
            ret = SapModel.PropFrame.SetISection(
                sec["name"], sec["material"],
                sec["t3"], sec["t2"], sec["tf"], sec["tw"],
                sec["t2"], sec["tf"],  # t2b, tfb (simétrico)
                -1, "", ""
            )
            if _check_ret(ret):
                count += 1

        # Tubos rectangulares (HSS)
        for sec in DEFAULT_TUBE_SECTIONS:
            ret = SapModel.PropFrame.SetTube(
                sec["name"], sec["material"],
                sec["t3"], sec["t2"], sec["t"], sec["t"],
                -1, "", ""
            )
            if _check_ret(ret):
                count += 1

        # Ángulos
        for sec in DEFAULT_ANGLE_SECTIONS:
            ret = SapModel.PropFrame.SetAngle(
                sec["name"], sec["material"],
                sec["t3"], sec["t2"], sec["t"], sec["t"],
                -1, "", ""
            )
            if _check_ret(ret):
                count += 1

        # Canales
        for sec in DEFAULT_CHANNEL_SECTIONS:
            ret = SapModel.PropFrame.SetChannel(
                sec["name"], sec["material"],
                sec["t3"], sec["t2"], sec["tf"], sec["tw"],
                -1, "", ""
            )
            if _check_ret(ret):
                count += 1

        self._log(f"  {count} secciones creadas.")
        return count

    # ── Task 5: Armaduras ────────────────────────────────────────────────

    def _setup_rebars(self) -> int:
        """Crea propiedades de armadura (rebar)."""
        SapModel = self.sap_model
        count = 0
        for rebar in DEFAULT_REBARS:
            ret = SapModel.PropRebar.SetProp(
                rebar["name"], rebar["area"], rebar["diameter"]
            )
            if _check_ret(ret):
                count += 1
        self._log(f"  {count} rebars creados.")
        return count

    # ── Task 6: Espectros sísmicos ───────────────────────────────────────

    def _setup_seismic_definitions(self, config: BaseModelConfig) -> Tuple[int, int]:
        """Calcula espectros NCh y define Functions + Load Cases."""
        SapModel = self.sap_model
        func_count = 0
        case_count = 0

        # Determinar si X e Y usan el mismo espectro
        same_r = abs(config.r_x - config.r_y) < 1e-6
        same_damp = abs(config.damping_x - config.damping_y) < 1e-6
        use_single_spectrum = same_r and same_damp

        # Espectro Horizontal X
        func_name_x = f"SaH_{config.zone}{config.soil}_R{config.r_x}"
        periods_x, accels_x = compute_nch_spectrum(
            config.zone, config.soil, config.importance, config.r_x, config.damping_x
        )
        if periods_x:
            ret = SapModel.Func.FuncRS.SetUser(
                func_name_x, len(periods_x), periods_x, accels_x, config.damping_x
            )
            if _check_ret(ret):
                func_count += 1

        # Espectro Horizontal Y (reutiliza X si son idénticos)
        if use_single_spectrum:
            func_name_y = func_name_x
        else:
            func_name_y = f"SaH_{config.zone}{config.soil}_R{config.r_y}"
            periods_y, accels_y = compute_nch_spectrum(
                config.zone, config.soil, config.importance, config.r_y, config.damping_y
            )
            if periods_y:
                ret = SapModel.Func.FuncRS.SetUser(
                    func_name_y, len(periods_y), periods_y, accels_y, config.damping_y
                )
                if _check_ret(ret):
                    func_count += 1

        # Espectro Vertical
        func_name_v = f"SaV_{config.zone}{config.soil}_R{config.r_v}"
        periods_v, accels_v = compute_vertical_spectrum(
            config.zone, config.soil, config.importance, config.r_v, config.xi_v
        )
        if periods_v:
            ret = SapModel.Func.FuncRS.SetUser(
                func_name_v, len(periods_v), periods_v, accels_v, config.xi_v
            )
            if _check_ret(ret):
                func_count += 1

        # Load Cases — Response Spectrum (scale = GRAVITY)
        scale = GRAVITY
        if self._set_rs_case("EQX", func_name_x, "U1", scale, config.damping_x):
            case_count += 1
        if self._set_rs_case("EQY", func_name_y, "U2", scale, config.damping_y):
            case_count += 1
        if self._set_rs_case("EQZ", func_name_v, "U3", scale, config.xi_v):
            case_count += 1

        self._log(f"  {func_count} funciones, {case_count} casos RS creados.")
        return func_count, case_count

    def _set_rs_case(self, case_name: str, func_name: str,
                     dir_flag: str, scale: float, damp: float) -> bool:
        """Configura un caso de espectro de respuesta."""
        SapModel = self.sap_model
        try:
            ret = SapModel.LoadCases.ResponseSpectrum.SetCase(case_name)
            if not _check_ret(ret):
                return False

            ret = SapModel.LoadCases.ResponseSpectrum.SetLoads(
                case_name, 1, [dir_flag], [func_name], [scale], ["Global"], [0.0]
            )
            if not _check_ret(ret):
                return False

            ret = SapModel.LoadCases.ResponseSpectrum.SetDampConstant(case_name, damp)
            if not _check_ret(ret):
                return False

            return True
        except Exception as e:
            self._log(f"  Error configurando caso RS '{case_name}': {e}")
            return False

    # ── Task 7: Combinaciones ────────────────────────────────────────────

    def _setup_combinations(self) -> int:
        """Crea Load Combinations (NCh, LRFD, ASD)."""
        SapModel = self.sap_model
        count = 0
        known_combos = set()

        # 1. NCh (E1, E2, E3) — se crean primero para ser referenciados
        for combo_name, items in NCH_COMBOS:
            ret = SapModel.RespCombo.Add(combo_name, 0)  # 0=Linear Add
            if _check_ret(ret):
                count += 1
                known_combos.add(combo_name)
                for case_name, sf in items:
                    SapModel.RespCombo.SetCaseList(combo_name, 0, case_name, sf)

        # 2. LRFD
        for combo_name, items in LRFD_COMBOS:
            ret = SapModel.RespCombo.Add(combo_name, 0)
            if not _check_ret(ret):
                continue
            count += 1
            known_combos.add(combo_name)
            for cname, sf in items:
                c_type = 1 if cname in known_combos else 0
                SapModel.RespCombo.SetCaseList(combo_name, c_type, cname, sf)
            SapModel.DesignSteel.SetComboStrength(combo_name, True)
            SapModel.DesignConcrete.SetComboStrength(combo_name, True)

        # 3. ASD
        for combo_name, items in ASD_COMBOS:
            ret = SapModel.RespCombo.Add(combo_name, 0)
            if not _check_ret(ret):
                continue
            count += 1
            known_combos.add(combo_name)
            for cname, sf in items:
                c_type = 1 if cname in known_combos else 0
                SapModel.RespCombo.SetCaseList(combo_name, c_type, cname, sf)
            SapModel.DesignSteel.SetComboStrength(combo_name, True)
            SapModel.DesignConcrete.SetComboStrength(combo_name, True)

        self._log(f"  {count} combinaciones creadas.")
        return count

    # ── Task 8: Envolventes ──────────────────────────────────────────────

    def _create_envelopes(self):
        """Crea envolventes de diseño (ENV_LRFD, ENV_ASD)."""
        SapModel = self.sap_model

        # ENV_LRFD
        lrfd_names = [name for name, _ in LRFD_COMBOS]
        if lrfd_names:
            SapModel.RespCombo.Add("ENV_LRFD", 1)  # 1=Envelope
            for name in lrfd_names:
                SapModel.RespCombo.SetCaseList("ENV_LRFD", 1, name, 1.0)

        # ENV_ASD
        asd_names = [name for name, _ in ASD_COMBOS]
        if asd_names:
            SapModel.RespCombo.Add("ENV_ASD", 1)
            for name in asd_names:
                SapModel.RespCombo.SetCaseList("ENV_ASD", 1, name, 1.0)

        self._log("  Envolventes ENV_LRFD y ENV_ASD creadas.")


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = BaseModelBackend(conn)
        config = BaseModelConfig(
            zone=2, soil="C",
            importance=1.0,
            r_x=3.0, r_y=3.0,
            damping_x=0.03, damping_y=0.03,
            r_v=2.0, xi_v=0.03,
        )

        try:
            import json
            output = backend.run(config)
            print(json.dumps(output, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
