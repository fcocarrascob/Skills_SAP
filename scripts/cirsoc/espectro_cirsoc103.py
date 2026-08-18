"""
espectro_cirsoc103 — espectro de diseño de INPRES-CIRSOC 103 Parte I (2018).

Todo lo que no toca SAP2000 son funciones puras y se puede verificar a mano.
Las que sí lo tocan están al final y reciben un `SapModel` ya conectado.

Referencias (leídas del PDF del Reglamento, ed. 2018):
  [3.1]-[3.4]   espectro elástico, §3.5.1
  [3.5]-[3.9]   corrección por amortiguamiento distinto de 5 %
  [3.10]        componente vertical, §3.5.2
  [3.11][3.12]  Na >= 1,00   Nv >= 1,20
  [3.13][3.14]  T2 = Cv/(2,5·Ca)      T1 = 0,2·T2
  [3.15]        W = D + f1·L + f2·S,  Tabla 3.3
  [6.3]-[6.6]   coeficiente sísmico del método estático, §6.2.2
  [6.7][6.8]    T <= Cu·Ta,  Ta = Cr·H^x   (Tablas 6.1 y 6.2)
  [7.1]         Cm = Sam·γr/R
  [7.2]         escalado del dinámico al 85 % del estático, §7.2.5
  [7.3]         du = Cd·de/γr
  Tabla 5.1     factores de comportamiento R, Cd, Ω0

OJO — el espectro de la edición 2018 tiene la forma Ca/Cv (meseta 2,5·Ca y
rama Cv/T), **no** la trilineal `as, b, T1, T2` con rama (T2/T)^(2/3) de las
ediciones anteriores. Es exactamente la misma familia de expresiones que
ASCE 7 (S_DS = 2,5·Ca y S_D1 = Cv), lo que permite calibrar Na y Nv contra un
estudio de amenaza específico de sitio sin cambiar de norma.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import math

G = 9.81  # m/s²

# --------------------------------------------------------------------------
# Tablas del Reglamento
# --------------------------------------------------------------------------

#: Tabla 3.1 — {zona: {tipo_espectral: (coef_Ca, coef_Cv)}} y aceleración as.
#: Ca = coef_Ca·Na  y  Cv = coef_Cv·Nv  en zonas 3 y 4; en 1 y 2 son valores fijos.
TABLA_3_1 = {
    4: {"as": 0.35, 1: (0.37, 0.51), 2: (0.40, 0.59), 3: (0.36, 0.90)},
    3: {"as": 0.25, 1: (0.29, 0.39), 2: (0.32, 0.47), 3: (0.35, 0.74)},
    2: {"as": 0.15, 1: (0.18, 0.25), 2: (0.22, 0.32), 3: (0.30, 0.50)},
    1: {"as": 0.08, 1: (0.09, 0.13), 2: (0.12, 0.18), 3: (0.19, 0.26)},
}

#: Tabla 3.2 — período T3 [s] por zona sísmica.
TABLA_3_2 = {4: 13.0, 3: 8.0, 2: 5.0, 1: 3.0}

#: Tabla 2.2 — tipo espectral según el sitio.
TIPO_ESPECTRAL = {"SA": 1, "SB": 1, "SC": 1, "SD": 2, "SE": 3}

#: Tabla 2.2 — clasificación por Vs30 [m/s].
def sitio_por_vs30(vs30: float) -> str:
    if vs30 > 1500: return "SA"
    if vs30 >= 760: return "SB"
    if vs30 >= 360: return "SC"
    if vs30 >= 180: return "SD"
    return "SE"

#: Cap. 2.4 — factor de riesgo por grupo de la construcción.
GAMMA_R = {"Ao": 1.5, "A": 1.3, "B": 1.0, "C": 0.8}

#: Tabla 5.1 — factores de comportamiento (R, Cd, Ω0) para estructuras de acero.
TABLA_5_1_ACERO = {
    "SMF":        (7.0, 5.5, 3.0),   # 18 pórticos no arriostrados especiales
    "IMF":        (4.5, 4.0, 3.0),   # 19 intermedios
    "OMF":        (3.0, 3.0, 3.0),   # 20 convencionales
    "TRUSS_MF":   (6.0, 5.5, 3.0),   # 21 pórticos con vigas reticuladas
    "SCBF":       (5.0, 5.5, 2.0),   # 22 arriostrados concéntricos especiales
    "OCBF":       (3.0, 3.0, 2.0),   # 23 arriostrados concéntricos convencionales
    "EBF":        (7.0, 4.0, 2.0),   # 24 arriostrados excéntricos
    "SIN_MOMENTO_CONC": (4.0, 5.0, 2.5),  # 36 uniones viga-columna no rígidas
    "ELASTICO":   (1.5, None, None), # [5.1]
}

#: Tabla 6.1 — Cu, límite superior del período de cálculo, en función de as.
TABLA_6_1 = [(0.35, 1.40), (0.25, 1.45), (0.15, 1.60), (0.08, 1.70)]

#: Tabla 6.2 — (Cr, x) para Ta = Cr·H^x.
TABLA_6_2 = {
    "PORTICO_ACERO":     (0.0724, 0.80),  # 100 % del corte, sin diagonales ni relleno
    "PORTICO_HORMIGON":  (0.0466, 0.90),
    "ACERO_EBF_BRB":     (0.0731, 0.75),
    "OTROS":             (0.0488, 0.75),  # incluye arriostrados concéntricos
}

#: Tabla 3.3 — factor de simultaneidad de la sobrecarga de uso.
F1 = {
    "excepcional": 0.00,   # techos accesibles sólo para mantenimiento
    "reducida":    0.25,   # vivienda, oficinas
    "intermedia":  0.50,   # públicos, escuelas, cines
    "elevada":     0.75,   # depósitos, archivos
    "permanente":  1.00,   # tanques, silos llenos
    "otros":       0.20,
}

#: Tabla 3.3 — factor de simultaneidad de la nieve. **No existe 0,50.**
F2 = {
    "no_evacua": 0.70,     # cubiertas horizontales o que no permiten evacuación
    "otros":     0.20,
}

#: Tabla 6.4 — distorsión de piso máxima.
DISTORSION_LIMITE = {
    ("Ao", "D"): 0.010, ("A", "D"): 0.010, ("B", "D"): 0.015,
    ("Ao", "ND"): 0.015, ("A", "ND"): 0.015, ("B", "ND"): 0.025,
}


def cu(a_s: float) -> float:
    """Tabla 6.1 con interpolación lineal entre valores tabulados."""
    tab = sorted(TABLA_6_1, key=lambda t: t[0])
    if a_s <= tab[0][0]:
        return tab[0][1]
    if a_s >= tab[-1][0]:
        return tab[-1][1]
    for (a1, c1), (a2, c2) in zip(tab, tab[1:]):
        if a1 <= a_s <= a2:
            return c1 + (c2 - c1) * (a_s - a1) / (a2 - a1)
    return tab[-1][1]


# --------------------------------------------------------------------------
# El espectro
# --------------------------------------------------------------------------

@dataclass
class EspectroCIRSOC:
    """Espectro elástico de pseudo-aceleraciones, §3.5.1.

    Se construye desde la zona y el sitio (`desde_zona`) o directamente desde
    Ca y Cv (`__init__`) — esto último permite calibrar contra un estudio de
    amenaza específico de sitio.
    """
    Ca: float
    Cv: float
    T3: float = 13.0
    a_s: float = 0.35
    xi: float = 0.05          # razón de amortiguamiento
    zona: int | None = None
    sitio: str | None = None
    Na: float = 1.0
    Nv: float = 1.2

    T1: float = field(init=False)
    T2: float = field(init=False)

    def __post_init__(self):
        self.T2 = self.Cv / (2.5 * self.Ca)          # [3.13]
        self.T1 = 0.2 * self.T2                      # [3.14]

    # -- constructores -----------------------------------------------------
    @classmethod
    def desde_zona(cls, zona: int, sitio: str, Na: float = 1.0, Nv: float = 1.2,
                   xi: float = 0.05) -> "EspectroCIRSOC":
        if Na < 1.0:
            raise ValueError("Na >= 1,00 [3.11]")
        if Nv < 1.2:
            raise ValueError("Nv >= 1,20 [3.12]")
        tipo = TIPO_ESPECTRAL[sitio.upper()]
        cCa, cCv = TABLA_3_1[zona][tipo]
        if zona in (3, 4):
            Ca, Cv = cCa * Na, cCv * Nv
        else:                                   # zonas 1 y 2: valores fijos
            Ca, Cv = cCa, cCv
        return cls(Ca=Ca, Cv=Cv, T3=TABLA_3_2[zona], a_s=TABLA_3_1[zona]["as"],
                   xi=xi, zona=zona, sitio=sitio.upper(), Na=Na, Nv=Nv)

    @classmethod
    def calibrado_a_sitio(cls, S_DS: float, S_D1: float, zona: int = 4,
                          sitio: str = "SC", T3: float = 13.0,
                          xi: float = 0.05) -> "EspectroCIRSOC":
        """Reproduce un espectro de diseño de un estudio específico de sitio
        manteniendo la forma y el marco de reducción de CIRSOC.

        Como la meseta es 2,5·Ca y la rama de velocidad Cv/T, basta con
        Ca = S_DS/2,5 y Cv = S_D1. Los Na y Nv equivalentes salen de dividir
        por los coeficientes de la Tabla 3.1 — sirven para documentar cuánto
        se apartó del mapa reglamentario.
        """
        tipo = TIPO_ESPECTRAL[sitio.upper()]
        cCa, cCv = TABLA_3_1[zona][tipo]
        Ca, Cv = S_DS / 2.5, S_D1
        e = cls(Ca=Ca, Cv=Cv, T3=T3, a_s=TABLA_3_1[zona]["as"], xi=xi,
                zona=zona, sitio=sitio.upper(),
                Na=Ca / cCa, Nv=Cv / cCv)
        return e

    # -- ordenadas ---------------------------------------------------------
    @property
    def fa(self) -> float:
        """[3.9] amplificación por amortiguamiento < 5 %. Vale 1 si xi = 5 %."""
        if abs(self.xi - 0.05) < 1e-9:
            return 1.0
        return (7.0 / (2.0 + 100.0 * self.xi)) ** 0.5

    @property
    def Sa_max(self) -> float:
        """Meseta del espectro elástico [g]."""
        return 2.5 * self.fa * self.Ca

    def Sa(self, T: float) -> float:
        """Pseudo-aceleración elástica en g. [3.1]-[3.4] / [3.5]-[3.8]."""
        fa = self.fa
        if T <= self.T1:
            return self.Ca * (1.0 + (2.5 * fa - 1.0) * T / self.T1)
        if T <= self.T2:
            return 2.5 * fa * self.Ca
        if T <= self.T3:
            return fa * self.Cv / T
        return fa * self.Cv * self.T3 / (T * T)

    def Ev(self, gamma_r: float) -> float:
        """[3.10] coeficiente sísmico vertical, en g. Sin reducción por R."""
        return self.Ca / 2.0 * gamma_r

    def puntos(self, T_max: float = 20.0) -> tuple[list[float], list[float]]:
        """Pares (T, Sa) listos para cargar como función en SAP2000.

        Discretización fina en la rama ascendente y quiebres exactos en
        T1, T2 y T3 para que la interpolación lineal de SAP no recorte la
        meseta ni redondee los vértices.
        """
        Ts: list[float] = []
        t = 0.0
        while t < self.T1 - 1e-9:
            Ts.append(round(t, 5)); t += self.T1 / 13.0
        Ts.append(self.T1)
        t = self.T1 + (self.T2 - self.T1) / 25.0
        while t < self.T2 - 1e-9:
            Ts.append(round(t, 5)); t += (self.T2 - self.T1) / 25.0
        Ts.append(self.T2)
        for f in (1.03, 1.06, 1.12, 1.2, 1.3, 1.45, 1.6, 1.8, 2.0, 2.3,
                  2.7, 3.2, 3.8, 4.5, 5.5, 7.0, 9.0, 12.0, 15.0, 19.0):
            v = round(self.T2 * f, 4)
            if v < self.T3:
                Ts.append(v)
        Ts.append(self.T3)
        for v in (self.T3 * 1.1, self.T3 * 1.3, T_max):
            if v > self.T3:
                Ts.append(round(v, 4))
        Ts = sorted(set(t for t in Ts if t <= T_max))
        return Ts, [round(self.Sa(t), 6) for t in Ts]

    def resumen(self) -> dict:
        return {
            "zona": self.zona, "sitio": self.sitio, "as": self.a_s,
            "Na": round(self.Na, 4), "Nv": round(self.Nv, 4),
            "Ca": round(self.Ca, 4), "Cv": round(self.Cv, 4),
            "T1": round(self.T1, 4), "T2": round(self.T2, 4), "T3": self.T3,
            "Sa_max_g": round(self.Sa_max, 4),
            "S_DS_equiv": round(2.5 * self.Ca, 4),
            "S_D1_equiv": round(self.Cv, 4),
        }


# --------------------------------------------------------------------------
# Método estático y escalado del dinámico
# --------------------------------------------------------------------------

def periodo_aproximado(H: float, tipo: str = "OTROS") -> float:
    """[6.8] Ta = Cr·H^x, con H la altura de la construcción [m]."""
    Cr, x = TABLA_6_2[tipo]
    return Cr * H ** x


def periodo_de_calculo(T_modelo: float, H: float, a_s: float,
                       tipo: str = "OTROS") -> tuple[float, float, bool]:
    """[6.7] acota el período del modelo. Devuelve (T_usado, T_limite, acotado).

    Saltarse este límite subestima el corte basal estático y hace parecer que
    el escalado del §7.2.5 no hace falta.
    """
    Tlim = cu(a_s) * periodo_aproximado(H, tipo)
    return (min(T_modelo, Tlim), Tlim, T_modelo > Tlim)


def coeficiente_sismico(esp: EspectroCIRSOC, T: float, gamma_r: float,
                        R: float) -> float:
    """§6.2.2 — C del método estático, con el mínimo de zonas 3 y 4."""
    C = (2.5 * esp.Ca if T <= esp.T2 else esp.Sa(T)) * gamma_r / R   # [6.3]/[6.4]
    if esp.zona in (3, 4):
        C = max(C, 0.8 * esp.a_s * esp.Nv * gamma_r / R)             # [6.5]
    else:
        C = max(C, 0.11 * esp.Ca * gamma_r)                          # [6.6]
    return C


def factor_escala_espectral(gamma_r: float, R: float, g: float = G) -> float:
    """[7.1] Cm = Sam·γr/R → el factor de escala del caso Response Spectrum
    cuando la función se carga **elástica y en g**."""
    return gamma_r / R * g


def verificar_85(esp: EspectroCIRSOC, T_modelo: float, V_dinamico: float,
                 W: float, H: float, gamma_r: float, R: float,
                 tipo_estructura: str = "OTROS") -> dict:
    """§7.2.5 — escalado del corte dinámico al 85 % del estático.

    `V_dinamico` debe ser el corte **sin** escalar, es decir el que sale con
    el factor de escala base γr/R·g.
    """
    T_us, T_lim, acotado = periodo_de_calculo(T_modelo, H, esp.a_s, tipo_estructura)
    C = coeficiente_sismico(esp, T_us, gamma_r, R)
    Voe = C * W
    limite = 0.85 * Voe
    factor = max(1.0, limite / V_dinamico) if V_dinamico > 0 else 1.0
    return {
        "T_modelo": round(T_modelo, 4), "T_limite": round(T_lim, 4),
        "T_usado": round(T_us, 4), "acotado": acotado,
        "C": round(C, 5), "W": round(W, 1),
        "V_estatico": round(Voe, 1), "0.85_V_estatico": round(limite, 1),
        "V_dinamico": round(V_dinamico, 1),
        "factor": round(factor, 4),
        "SF_final": round(factor_escala_espectral(gamma_r, R) * factor, 4),
    }


def peso_sismico(D: float, L: float = 0.0, S: float = 0.0,
                 f1: float = 0.20, f2: float = 0.70) -> float:
    """[3.15] W = D + f1·L + f2·S."""
    return D + f1 * L + f2 * S


def distorsion_ultima(delta_elastico: float, Cd: float, gamma_r: float) -> float:
    """[6.17]/[7.3] du = Cd·de/γr.

    Contraintuitivo: γr amplifica la acción pero **divide** el desplazamiento
    de control, porque ya entró en de.
    """
    return Cd * delta_elastico / gamma_r


# --------------------------------------------------------------------------
# Puente hacia SAP2000
# --------------------------------------------------------------------------

def cargar_funcion(SapModel, esp: EspectroCIRSOC, nombre: str = "Sa_CIRSOC103",
                   T_max: float = 20.0) -> int:
    """Define/actualiza la función de espectro de respuesta, elástica y en g."""
    T, Sa = esp.puntos(T_max)
    res = SapModel.Func.FuncRS.SetUser(nombre, len(T), T, Sa, esp.xi)
    return res[-1] if not isinstance(res, int) else res


def configurar_casos(SapModel, gamma_r: float, R: float,
                     nombre_funcion: str = "Sa_CIRSOC103",
                     caso_x: str = "EQX", caso_y: str = "EQY",
                     factores: dict | None = None) -> dict:
    """Apunta los casos Response Spectrum a la función y fija el factor de escala.

    `factores` permite pasar el escalado del §7.2.5 por dirección,
    p. ej. {'X': 1.176, 'Y': 1.032}.
    """
    factores = factores or {}
    SF = factor_escala_espectral(gamma_r, R)
    out = {}
    for d, caso, dirn in (("X", caso_x, "U1"), ("Y", caso_y, "U2")):
        sf = SF * factores.get(d, 1.0)
        SapModel.LoadCases.ResponseSpectrum.SetLoads(
            caso, 1, [dirn], [nombre_funcion], [sf], ["GLOBAL"], [0.0])
        out[d] = round(sf, 4)
    return out


def configurar_vertical(SapModel, esp: EspectroCIRSOC, gamma_r: float,
                        caso: str = "EQZ", g: float = G) -> float:
    """[3.10] EQZ como aceleración estática vertical (Ca/2)·γr·g. Sin R."""
    sf = esp.Ev(gamma_r) * g
    SapModel.LoadCases.StaticLinear.SetLoads(caso, 1, ["Accel"], ["UZ"], [sf])
    return round(sf, 5)


# --------------------------------------------------------------------------
if __name__ == "__main__":
    print("El Pachón — Zona 4, sitio SC (Vs30 = 450 m/s), Grupo A\n")
    e = EspectroCIRSOC.desde_zona(4, "SC")
    for k, v in e.resumen().items():
        print(f"  {k:12s} {v}")
    print(f"\n  Sa(0)    = {e.Sa(0.0):.4f} g   (= Ca)")
    print(f"  Sa(T1)   = {e.Sa(e.T1):.4f} g   (= 2,5·Ca)")
    print(f"  Sa(1,0)  = {e.Sa(1.0):.4f} g   (= Cv/T)")
    print(f"  Ev(1,3)  = {e.Ev(1.3):.4f} g")
    print(f"  SF       = {factor_escala_espectral(1.3, 3.0):.4f} m/s²")

    print("\n  Calibrado al estudio de amenaza (S_DS = 1,473 · S_D1 = 0,853):")
    ec = EspectroCIRSOC.calibrado_a_sitio(1.473, 0.853)
    for k, v in ec.resumen().items():
        print(f"    {k:12s} {v}")
