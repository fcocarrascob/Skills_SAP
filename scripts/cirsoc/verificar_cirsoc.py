"""
verificar_cirsoc — autochequeo contra números calculados a mano.

Corre sin SAP2000. Cada aserción lleva al lado el cálculo que la respalda,
para poder rehacerlo con lápiz si algo cambia en el Reglamento.

    python verificar_cirsoc.py
"""

from __future__ import annotations
import math
import sys

from espectro_cirsoc103 import (
    EspectroCIRSOC, cu, periodo_aproximado, periodo_de_calculo,
    coeficiente_sismico, factor_escala_espectral, verificar_85,
    peso_sismico, distorsion_ultima, sitio_por_vs30,
    TABLA_5_1_ACERO, F1, F2, DISTORSION_LIMITE, G,
)
from combos_cirsoc import generar, Parametros

FALLOS: list[str] = []


def chk(etiqueta: str, obtenido, esperado, tol: float = 1e-3):
    if isinstance(esperado, float):
        ok = abs(obtenido - esperado) <= tol * max(1.0, abs(esperado))
    else:
        ok = obtenido == esperado
    marca = "OK  " if ok else "FALLA"
    print(f"  [{marca}] {etiqueta:52s} {obtenido!r}"
          + ("" if ok else f"   esperado {esperado!r}"))
    if not ok:
        FALLOS.append(etiqueta)


# ==========================================================================
print("\n1. Clasificación del sitio — Tabla 2.2")
chk("Vs30 = 1200 m/s", sitio_por_vs30(1200), "SB")
chk("Vs30 = 450 m/s (El Pachón, INF.MINA)", sitio_por_vs30(450), "SC")
chk("Vs30 = 300 m/s", sitio_por_vs30(300), "SD")

# ==========================================================================
print("\n2. Espectro Zona 4, sitio SC — Tabla 3.1, Na=1,00 Nv=1,20")
e = EspectroCIRSOC.desde_zona(4, "SC")
chk("Ca = 0,37 · Na", e.Ca, 0.370)
chk("Cv = 0,51 · Nv = 0,51 · 1,20", e.Cv, 0.612)
chk("T2 = Cv/(2,5·Ca) = 0,612/0,925          [3.13]", e.T2, 0.612 / 0.925)
chk("T1 = 0,2·T2                             [3.14]", e.T1, 0.2 * 0.612 / 0.925)
chk("T3 (Zona 4)                             Tabla 3.2", e.T3, 13.0)
chk("Sa(0) = Ca                              [3.1]", e.Sa(0.0), 0.370)
chk("Sa(T1) = 2,5·Ca                         [3.2]", e.Sa(e.T1), 0.925)
chk("Sa(T2) = 2,5·Ca                         [3.2]", e.Sa(e.T2), 0.925)
chk("Sa(1,0) = Cv/1,0                        [3.3]", e.Sa(1.0), 0.612)
chk("Sa(2,0) = Cv/2,0                        [3.3]", e.Sa(2.0), 0.306)
chk("Sa(T3) = Cv/13                          [3.3]", e.Sa(13.0), 0.612 / 13)
chk("Sa(20) = Cv·T3/20²                      [3.4]", e.Sa(20.0), 0.612 * 13 / 400)
# continuidad en los quiebres
chk("continuidad en T1", e.Sa(e.T1 * 0.9999), e.Sa(e.T1 * 1.0001), 1e-3)
chk("continuidad en T2", e.Sa(e.T2 * 0.9999), e.Sa(e.T2 * 1.0001), 1e-3)
chk("continuidad en T3", e.Sa(e.T3 * 0.9999), e.Sa(e.T3 * 1.0001), 1e-3)
chk("Ev = (Ca/2)·γr, γr=1,3                  [3.10]", e.Ev(1.3), 0.185 * 1.3)

print("\n   Mínimos de Na y Nv — [3.11] y [3.12]")
for bad, msg in ((dict(Na=0.9), "Na < 1,00"), (dict(Nv=1.0), "Nv < 1,20")):
    try:
        EspectroCIRSOC.desde_zona(4, "SC", **bad)
        chk(f"rechaza {msg}", False, True)
    except ValueError:
        chk(f"rechaza {msg}", True, True)

# ==========================================================================
print("\n3. Amortiguamiento distinto de 5 % — [3.5]-[3.9]")
e3 = EspectroCIRSOC.desde_zona(4, "SC", xi=0.03)
chk("fa = [7/(2+3)]^0,5                      [3.9]", e3.fa, math.sqrt(7 / 5))
chk("meseta = 2,5·fa·Ca", e3.Sa_max, 2.5 * math.sqrt(7 / 5) * 0.370)
chk("fa = 1 para xi = 5 %", EspectroCIRSOC.desde_zona(4, "SC").fa, 1.0)

# ==========================================================================
print("\n4. Calibración a un estudio de amenaza específico de sitio")
# Ausenco 2021, PACHÓN-INF.MINA, TR 2475 a, Vs30 450: S0,2 = 2,21 g · S1,0 = 1,28 g
# Diseño ASCE 7 = 2/3 del MCE:
S_DS, S_D1 = 2 / 3 * 2.21, 2 / 3 * 1.28
ec = EspectroCIRSOC.calibrado_a_sitio(S_DS, S_D1)
chk("S_DS = 2/3 · 2,21", S_DS, 1.4733)
chk("S_D1 = 2/3 · 1,28", S_D1, 0.8533)
chk("Ca = S_DS/2,5", ec.Ca, S_DS / 2.5)
chk("Cv = S_D1", ec.Cv, S_D1)
chk("meseta = S_DS", ec.Sa_max, S_DS)
chk("Sa(1,0) = S_D1", ec.Sa(1.0), S_D1)
chk("Na equivalente = Ca/0,37", ec.Na, S_DS / 2.5 / 0.37)
chk("Nv equivalente = Cv/0,51", ec.Nv, S_D1 / 0.51)
# T2 de CIRSOC == Ts de ASCE = S_D1/S_DS
chk("T2 == Ts de ASCE = S_D1/S_DS", ec.T2, S_D1 / S_DS)
chk("T1 == T0 de ASCE = 0,2·Ts", ec.T1, 0.2 * S_D1 / S_DS)
chk("relación con el espectro reglamentario", ec.Sa_max / e.Sa_max, 1.5928)

# ==========================================================================
print("\n5. Período de cálculo — Tablas 6.1 y 6.2, [6.7] y [6.8]")
chk("Cu para as = 0,35                       Tabla 6.1", cu(0.35), 1.40)
chk("Cu para as = 0,25", cu(0.25), 1.45)
chk("Cu interpolado, as = 0,30", cu(0.30), 1.425)
H = 17.2
Ta_p = periodo_aproximado(H, "PORTICO_ACERO")     # 0,0724·17,2^0,80
Ta_o = periodo_aproximado(H, "OTROS")             # 0,0488·17,2^0,75
chk("Ta pórtico de acero = 0,0724·17,2^0,80", Ta_p, 0.0724 * 17.2 ** 0.80)
chk("Ta otros = 0,0488·17,2^0,75", Ta_o, 0.0488 * 17.2 ** 0.75)
Tu, Tl, ac = periodo_de_calculo(1.127, H, 0.35, "PORTICO_ACERO")
chk("límite = 1,40·Ta", Tl, 1.40 * Ta_p)
chk("T modelo 1,127 s queda acotado", ac, True)
chk("T usado = el límite", Tu, Tl)
Tu2, Tl2, ac2 = periodo_de_calculo(0.469, H, 0.35, "OTROS")
chk("T modelo 0,469 s NO se acota", ac2, False)
chk("T usado = el del modelo", Tu2, 0.469)

# ==========================================================================
print("\n6. Coeficiente sísmico — §6.2.2, γr = 1,3 · R = 3")
gr, R = 1.3, 3.0
chk("T <= T2 → C = 2,5·Ca·γr/R              [6.3]",
    coeficiente_sismico(e, 0.469, gr, R), 0.925 * gr / R)
chk("T > T2  → C = Sa(T)·γr/R               [6.4]",
    coeficiente_sismico(e, 0.987, gr, R), (0.612 / 0.987) * gr / R)
chk("mínimo 0,8·as·Nv·γr/R                  [6.5]",
    coeficiente_sismico(e, 12.0, gr, R), 0.8 * 0.35 * 1.2 * gr / R)
chk("SF = γr/R·g                            [7.1]", factor_escala_espectral(gr, R),
    1.3 / 3.0 * G)

# ==========================================================================
print("\n7. Escalado del dinámico al 85 % — §7.2.5")
W = 16780.9
v = verificar_85(e, 0.469, 4861.4, W, H, gr, R, "OTROS")
chk("C en X", v["C"], 0.4008, 1e-3)
chk("V estático en X = C·W", v["V_estatico"], 0.4008 * W, 1e-3)
chk("factor en X = 0,85·Voe/Vod", v["factor"], 0.85 * 0.4008 * W / 4861.4, 2e-3)
vy = verificar_85(e, 1.127, 3713.6, W, H, gr, R, "PORTICO_ACERO")
chk("T en Y queda acotado", vy["acotado"], True)
chk("C en Y con T acotado", vy["C"], (0.612 / vy["T_usado"]) * gr / R, 1e-3)
chk("factor en Y", vy["factor"], 0.85 * vy["C"] * W / 3713.6, 2e-3)
sin_escalar = verificar_85(e, 0.469, 9999.0, W, H, gr, R, "OTROS")
chk("no escala si el dinámico ya supera el 85 %", sin_escalar["factor"], 1.0)

# ==========================================================================
print("\n8. Peso sísmico y deformaciones — [3.15], Tabla 3.3, [7.3]")
chk("f2 no evacúa nieve                      Tabla 3.3", F2["no_evacua"], 0.70)
chk("f2 otros casos", F2["otros"], 0.20)
chk("f1 otros casos", F1["otros"], 0.20)
chk("W = D + 0,20·L + 0,70·S", peso_sismico(1000, 200, 500, 0.20, 0.70),
    1000 + 40 + 350)
chk("du = Cd·de/γr, Cd=3 γr=1,3              [7.3]",
    distorsion_ultima(0.030, 3.0, 1.3), 3.0 * 0.030 / 1.3)
chk("límite Grupo B, condición D             Tabla 6.4",
    DISTORSION_LIMITE[("B", "D")], 0.015)

# ==========================================================================
print("\n9. Factores de comportamiento — Tabla 5.1")
for sis, esp in (("OMF", (3.0, 3.0, 3.0)), ("OCBF", (3.0, 3.0, 2.0)),
                 ("SCBF", (5.0, 5.5, 2.0)), ("TRUSS_MF", (6.0, 5.5, 3.0)),
                 ("EBF", (7.0, 4.0, 2.0))):
    chk(f"{sis} (R, Cd, Ω0)", TABLA_5_1_ACERO[sis], esp)

# ==========================================================================
print("\n10. Combinaciones — CIRSOC 301-2018 §B.2.2 + CIRSOC 103 §3.7.1")
cs = generar()
from collections import Counter
fam = Counter(c.familia for c in cs)
chk("gravitatorias: B.2.1 + 2 B.2.2 + 2 B.2.3", fam["gravitatoria"], 5)
chk("viento: (B.2.3b + B.2.4)·2·4·2 + B.2.6·4·2", fam["viento"], 40)
chk("puente grúa: B.2.7 · 2 techos · 4 vientos · 2 signos", fam["grua"], 16)
chk("sísmicas: 2 dir · 2 signos de Ev · 2 exprs", fam["sismica"], 8)
chk("sobrerresistencia: 2 dir · 2 exprs", fam["sobrerresistencia"], 4)
chk("total", len(cs), 73)
chk("sin B.2.7 (sin puente grúa)",
    len(generar(par=Parametros(puente_grua=False))), 57)
chk("sin Ω₀", len(generar(par=Parametros(incluir_omega=False))), 69)

b1 = next(c for c in cs if c.referencia == "B.2.1")
chk("(B.2.1) 1,4·D", dict(b1.terminos)["D"], 1.4)
b4 = next(c for c in cs if c.referencia == "B.2.4")
chk("(B.2.4) viento con factor **1,5**, no 1,6", abs(dict(b4.terminos)["WX_i1"]), 1.5)
chk("(B.2.4) f1 sobre L", dict(b4.terminos)["LIVE"], 1.0)
b7 = next(c for c in cs if c.referencia == "B.2.7")
chk("(B.2.7) existe — obligatoria con puente grúa", b7.nombre.startswith("B7"), True)
chk("(B.2.7) 1,6·L + 0,8·W", dict(b7.terminos)["LIVE"], 1.6)
chk("(B.2.7) viento a 0,8", abs(dict(b7.terminos)["WX_i1"]), 0.8)

b5 = next(c for c in cs if c.referencia.startswith("B.2.5"))
chk("(B.2.5) 1,20·D", dict(b5.terminos)["D"], 1.20)
chk("(B.2.5) f2 = 0,70 sobre nieve", dict(b5.terminos)["SNOW"], 0.70)
chk("(B.2.5) f1 = 1,00 sobre L (carga de puente grúa)", dict(b5.terminos)["LIVE"], 1.0)
chk("(B.2.5) **Lr entra con f1** — se olvida seguido", dict(b5.terminos)["ROOF"], 1.0)
chk("(B.2.5) E_V con su signo                [3.18]", dict(b5.terminos)["EQZ"], 1.0)
s3 = next(c for c in cs if c.referencia == "IC103 [3.19]")
chk("[3.19] Ω₀ = 2 sobre E_H", dict(s3.terminos)["EQX"], 2.0)
chk("[3.19] marcada como sobrerresistencia", s3.sobrerresistencia, True)
chk("ninguna combinación mezcla EQX con EQY   §3.2",
    all(not ({"EQX", "EQY"} <= {t[0] for t in c.terminos}) for c in cs), True)
chk("el espectral aparece una sola vez por combinación (SAP aplica el ±)",
    all(sum(1 for t in c.terminos if t[0] in ("EQX", "EQY")) <= 1 for c in cs), True)
chk("f1 por defecto = 1,0 (puente grúa)", Parametros().f1, 1.0)

print("\n11. Combinaciones de servicio — §B.2.3")
from combos_cirsoc import generar_servicio
sv = generar_servicio()
chk("todas con acciones nominales (D a 1,0)",
    all(dict(c.terminos).get("D") == 1.0 for c in sv), True)
chk("existe la de 0,7 (B.2.9)", any(c.referencia == "B.2.9" for c in sv), True)

# ==========================================================================
print("\n12. Lectura del PMM y priorización de holgura — sin SAP")
from sap_utils import gobernante, holgura_por_seccion

chk("gobierna la flexión mayor", gobernante(0.20, 0.70, 0.05)[0], "flexion_33")
chk("gobierna la axial", gobernante(0.80, 0.10, 0.05)[0], "axial")
chk("fracción del término que manda", gobernante(0.20, 0.70, 0.10)[1], 0.70)
# Un término no leído NO es un cero: una columna con PRatio ausente y
# MMajRatio 0,9 diría "gobierna la flexión" con la misma cara que una real.
chk("término ausente → no dictamina", gobernante(None, 0.90, 0.05), (None, None))
chk("todo en cero → sin fracción", gobernante(0.0, 0.0, 0.0)[1], None)

_res = {
    "GRANDE": {"n": 100, "max": 0.50, "peor": "b1", "combo": "B5.Y_Vp", "sin_disenar": []},
    "AJUSTADA": {"n": 20, "max": 0.98, "peor": "b2", "combo": "B5.Y_Vp", "sin_disenar": []},
    "CHICA": {"n": 4, "max": 0.30, "peor": "b3", "combo": "B2.Lr", "sin_disenar": []},
}
# `peso_total` sale de la tabla en la unidad de FUERZA activa (kN), no en
# toneladas: 1.326,7 son kN y equivalen a 135,2 t de W14x145. Leerlo como masa
# multiplica el acero por 9,8 y el número sigue pareciendo razonable.
_secs = {"GRANDE": {"peso_total": 981.0}, "AJUSTADA": {"peso_total": 90.0},
         "CHICA": {"peso_total": 0.4}}
h = holgura_por_seccion(_res, _secs)
chk("prioriza masa × margen, no el margen solo", h[0]["seccion"], "GRANDE")
chk("una familia ajustada no encabeza aunque pese", h[1]["seccion"], "AJUSTADA")
chk("margen = 1 - D/C máx (el máximo, no el promedio)", h[0]["margen"], 0.50)
chk("peso en kN se conserva sin convertir", h[0]["peso_kN"], 981.0)
chk("masa = peso/g, en toneladas", h[0]["masa_t"], 100.03)
chk("cota de ahorro = masa · margen [t]", h[0]["oportunidad_t_cota"], 50.02)
chk("una sección sin peso asignado no entra", len(h), 3)
chk("sección con peso 0 se descarta",
    len(holgura_por_seccion(_res, {"GRANDE": {"peso_total": 0.0}})), 0)

# El techo del diseño es SRatioLimit, no 1,0. En este modelo vale 0,95: medir
# contra 1,0 le inventa a la familia AJUSTADA un 5 % de margen que no existe.
h95 = holgura_por_seccion(_res, _secs, limite=0.95)
_aj = next(x for x in h95 if x["seccion"] == "AJUSTADA")
chk("margen contra el límite real 0,95, no contra 1,0", _aj["margen"], 0.0)
chk("con límite 1,0 el mismo caso simula 3 % de margen",
    next(x for x in h if x["seccion"] == "AJUSTADA")["margen"], 0.02)

# ==========================================================================
print()
if FALLOS:
    print(f"{len(FALLOS)} FALLOS: " + ", ".join(FALLOS))
    sys.exit(1)
print("Todo verificado.")
