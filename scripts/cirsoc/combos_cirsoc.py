"""
combos_cirsoc — combinaciones de CIRSOC 301-2018 §B.2.2 y CIRSOC 103 §3.7.1.

Las combinaciones últimas de un proyecto argentino de acero salen del
**Reglamento CIRSOC 301-2018, Sección B.2.2** — no de ASCE 7 ni de NCh. Se
parecen, pero los factores no son los mismos:

    1,4 (D + F)                                                        (B.2.1)
    1,2 (D + F + T) + 1,6 (L + H) + (f1·Lr  ó  0,5 S  ó  0,5 R)        (B.2.2)
    1,2 D + 1,6 (Lr ó S ó R) + (f1·L  ó  0,8 W)                        (B.2.3)
    1,2 D + 1,5 W + f1·L + (f1·Lr  ó  0,5 S  ó  0,5 R)                 (B.2.4)
    1,2 D + 1,0 E + f1 (L + Lr) + f2·S                                 (B.2.5)
    0,9 D + (1,5 W  ó  1,0 E) + 1,6 H                                  (B.2.6)
    1,2 D + 1,6 L + (f1·Lr ó 0,5 S ó 0,5 R) + 0,8 W                    (B.2.7)

**(B.2.7) es obligatoria** *"para edificios industriales con puentes grúas o
monorrieles y edificios aporticados de hasta cuatro plantas"*.

Diferencias que más se pasan por alto viniendo de ASCE 7:

- El factor de viento es **1,5**, no 1,6.
- En (B.2.5) la sobrecarga de techo `Lr` entra con `f1`, no queda afuera.
- **f1 = 1,0 para cargas de puentes grúas y monorrieles**, áreas con
  concentración de público, sobrecargas > 5,0 kN/m², garajes y otras cargas
  concentradas > 50 kN. **f1 = 0,5 para el resto.**
- `f2 = 0,7` sólo *"para configuraciones particulares de techos (tales como las
  de diente de sierra) que no permiten evacuar la nieve acumulada"*; `0,2` para
  el resto. Es un criterio **más estrecho** que el de CIRSOC 103 Tabla 3.3
  ("cubiertas horizontales o que no permitan la evacuación").

Las combinaciones **sísmicas de sobrerresistencia** [3.19] y [3.20] sólo existen
en CIRSOC 103 §3.7.1, y sólo aplican *"en componentes sensibles a los efectos de
la sobrerresistencia estructural"* — no a toda la estructura.

Regla direccional: CIRSOC 103 §3.2 permite **direcciones independientes** cuando
el sistema sismorresistente está en dos direcciones perpendiculares. No va
100 % + 30 % + 30 %. La componente vertical se superpone siempre: E = E_H + E_V
[3.18].

Y del lado de SAP: un caso **Response Spectrum** dentro de una combinación lineal
ya trae el ±. No hay que duplicar la combinación con el signo cambiado; sí hay
que escribir los signos de los casos estáticos (viento, sismo vertical).
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Nomenclatura:
    """Nombres reales de los casos de carga en el modelo."""
    D: str = "D"                       # permanente total (incluye peso propio)
    L: str = "LIVE"                    # sobrecarga de uso (y de puente grúa)
    Lr: str = "ROOF"                   # sobrecarga de techo
    S: str = "SNOW"                    # nieve
    Ex: str = "EQX"                    # espectral X
    Ey: str = "EQY"                    # espectral Y
    Ev: str = "EQZ"                    # sismo vertical (estático)
    T: str | None = None               # térmica; None la deja fuera de (B.2.2)
    #: casos de viento; si ya incluyen la presión interna, van los cuatro
    W: tuple[str, ...] = ("WX_i1", "WX_i2", "WY_i1", "WY_i2")


@dataclass
class Parametros:
    #: B.2.2 — 1,0 para puentes grúa, público, >5 kN/m², garajes, >50 kN.
    f1: float = 1.0
    #: B.2.2 — 0,7 sólo para techos que no evacúan nieve; 0,2 el resto.
    f2: float = 0.7
    #: Tabla 5.1 de CIRSOC 103 — sobrerresistencia del sistema.
    omega0: float = 2.0
    incluir_omega: bool = True
    #: (B.2.7) obligatoria con puente grúa o monorriel.
    puente_grua: bool = True


@dataclass
class Combo:
    nombre: str
    terminos: list[tuple[str, float]]
    familia: str
    referencia: str = ""
    #: True para [3.19]/[3.20]: sólo aplican a componentes sensibles
    sobrerresistencia: bool = False


def generar(nom: Nomenclatura | None = None,
            par: Parametros | None = None) -> list[Combo]:
    """Juego completo de combinaciones últimas."""
    nom = nom or Nomenclatura()
    par = par or Parametros()
    out: list[Combo] = []
    f1, f2 = par.f1, par.f2

    def add(nombre, terminos, familia, ref, om=False):
        out.append(Combo(nombre, [(c, s) for c, s in terminos if c],
                         familia, ref, om))

    # ---------------- CIRSOC 301-2018 §B.2.2 ----------------
    add("B1_1.4D", [(nom.D, 1.4)], "gravitatoria", "B.2.1")

    # (B.2.2)  1,2(D+T) + 1,6 L + (f1·Lr ó 0,5 S ó 0,5 R)
    for etq, techo, fac in (("Lr", nom.Lr, f1), ("S", nom.S, 0.5)):
        add(f"B2.{etq}_1.2D+1.6L+{fac:g}{etq}",
            [(nom.D, 1.2), (nom.T, 1.2), (nom.L, 1.6), (techo, fac)],
            "gravitatoria", "B.2.2")

    # (B.2.3)  1,2 D + 1,6 (Lr ó S) + (f1·L ó 0,8 W)
    for etq, techo in (("Lr", nom.Lr), ("S", nom.S)):
        add(f"B3a.{etq}_1.2D+1.6{etq}+{f1:g}L",
            [(nom.D, 1.2), (techo, 1.6), (nom.L, f1)], "gravitatoria", "B.2.3")
        for w in nom.W:
            for sg, sl in ((1, "p"), (-1, "n")):
                add(f"B3b.{etq}_{w}{sl}",
                    [(nom.D, 1.2), (techo, 1.6), (w, sg * 0.8)], "viento", "B.2.3")

    # (B.2.4)  1,2 D + 1,5 W + f1·L + (f1·Lr ó 0,5 S)
    for etq, techo, fac in (("Lr", nom.Lr, f1), ("S", nom.S, 0.5)):
        for w in nom.W:
            for sg, sl in ((1, "p"), (-1, "n")):
                add(f"B4.{etq}_{w}{sl}",
                    [(nom.D, 1.2), (w, sg * 1.5), (nom.L, f1), (techo, fac)],
                    "viento", "B.2.4")

    # (B.2.6) viento  0,9 D + 1,5 W
    for w in nom.W:
        for sg, sl in ((1, "p"), (-1, "n")):
            add(f"B6w_{w}{sl}", [(nom.D, 0.9), (w, sg * 1.5)], "viento", "B.2.6")

    # (B.2.7)  obligatoria con puente grúa
    if par.puente_grua:
        for etq, techo, fac in (("Lr", nom.Lr, f1), ("S", nom.S, 0.5)):
            for w in nom.W:
                for sg, sl in ((1, "p"), (-1, "n")):
                    add(f"B7.{etq}_{w}{sl}",
                        [(nom.D, 1.2), (nom.L, 1.6), (techo, fac), (w, sg * 0.8)],
                        "grua", "B.2.7")

    # ---------------- Sísmicas: B.2.5 / B.2.6 ≡ CIRSOC 103 [3.16]/[3.17] ------
    for d, caso in (("X", nom.Ex), ("Y", nom.Ey)):
        for sv, sl in ((1, "Vp"), (-1, "Vn")):
            add(f"B5.{d}_{sl}_1.2D+E+f1(L+Lr)+f2S",
                [(nom.D, 1.2), (caso, 1.0), (nom.Ev, sv * 1.0),
                 (nom.L, f1), (nom.Lr, f1), (nom.S, f2)],
                "sismica", "B.2.5 / IC103 [3.16]")
            add(f"B6e.{d}_{sl}_0.9D+E",
                [(nom.D, 0.9), (caso, 1.0), (nom.Ev, sv * 1.0)],
                "sismica", "B.2.6 / IC103 [3.17]")
        if par.incluir_omega:
            add(f"S3.{d}_1.2D+W0EH+0.5L+0.2S",
                [(nom.D, 1.2), (caso, par.omega0), (nom.L, 0.5), (nom.S, 0.2)],
                "sobrerresistencia", "IC103 [3.19]", True)
            add(f"S4.{d}_0.9D+W0EH",
                [(nom.D, 0.9), (caso, par.omega0)],
                "sobrerresistencia", "IC103 [3.20]", True)
    return out


def generar_servicio(nom: Nomenclatura | None = None) -> list[Combo]:
    """Combinaciones de servicio — CIRSOC 301-2018 §B.2.3.

        (D + F) + (Li ó W ó T)                                    (B.2.8)
        (D + F) + 0,7 [(Li + W) ó (W + T) ó (Li + T)]             (B.2.9)
        (D + F) + 0,6 Li + 0,6 W + 0,6 T                          (B.2.10)
        Li = [L + H + (Lr ó S ó R)]                               (B.2.11)

    Acciones con sus **intensidades nominales**, sin mayorar.
    """
    nom = nom or Nomenclatura()
    out: list[Combo] = []

    def add(nombre, terminos, ref):
        out.append(Combo(nombre, [(c, s) for c, s in terminos if c],
                         "servicio", ref))

    for etq, techo in (("Lr", nom.Lr), ("S", nom.S)):
        add(f"SV1.{etq}_D+Li", [(nom.D, 1.0), (nom.L, 1.0), (techo, 1.0)], "B.2.8")
        add(f"SV2.{etq}_D+0.7(Li+W)",
            [(nom.D, 1.0), (nom.L, 0.7), (techo, 0.7), (nom.W[0], 0.7)], "B.2.9")
    for w in nom.W:
        for sg, sl in ((1, "p"), (-1, "n")):
            add(f"SV1w_{w}{sl}", [(nom.D, 1.0), (w, sg * 1.0)], "B.2.8")
    return out


# --------------------------------------------------------------------------

def escribir_en_sap(SapModel, combos: list[Combo], borrar_existentes: bool = True,
                    envolvente: str | None = "ENV_CIRSOC") -> dict:
    """Crea las combinaciones en el modelo. Devuelve un resumen.

    `RespCombo.Delete` falla si otra combinación referencia a la que se quiere
    borrar (típicamente una envolvente): por eso van dos pasadas.
    """
    RC = SapModel.RespCombo
    res: dict = {}

    if borrar_existentes:
        n0 = int(RC.GetNameList(0, [])[0])
        for _ in range(2):
            for c in list(RC.GetNameList(0, [])[1]):
                RC.Delete(c)
        res["borradas"] = n0 - int(RC.GetNameList(0, [])[0])
        res["sin_borrar"] = list(RC.GetNameList(0, [])[1])

    for c in combos:
        RC.Add(c.nombre, 0)                     # 0 = Linear Add
        for caso, sf in c.terminos:
            RC.SetCaseList(c.nombre, 0, caso, sf)   # 0 = es un caso, no un combo

    if envolvente:
        RC.Add(envolvente, 1)                   # 1 = Envelope
        for c in combos:
            RC.SetCaseList(envolvente, 1, c.nombre, 1.0)

    from collections import Counter
    res["creadas"] = len(combos)
    res["total"] = int(RC.GetNameList(0, [])[0])
    res["por_familia"] = dict(Counter(c.familia for c in combos))
    return res


def seleccionar_para_diseno(SapModel, combos: list[Combo],
                            incluir_sobrerresistencia: bool = False) -> dict:
    """Marca qué combinaciones entran en el diseño automático de acero.

    Por defecto deja fuera [3.19]/[3.20]: aplicarlas a todas las barras infla
    los ratios sin significado. Los componentes sensibles se verifican aparte.
    """
    DS = SapModel.DesignSteel
    validas = {c.nombre for c in combos
               if c.familia != "servicio"
               and (incluir_sobrerresistencia or not c.sobrerresistencia)}
    n = 0
    for c in list(SapModel.RespCombo.GetNameList(0, [])[1]):
        sel = c in validas
        DS.SetComboStrength(c, sel)
        n += int(sel)
    return {"seleccionadas": n, "excluidas_omega": not incluir_sobrerresistencia}


# --------------------------------------------------------------------------
if __name__ == "__main__":
    from collections import Counter
    cs = generar()
    print(f"{len(cs)} combinaciones últimas — CIRSOC 301-2018 §B.2.2\n")
    for fam, n in Counter(c.familia for c in cs).items():
        print(f"  {fam:20s} {n}")
    print("\nUna de cada familia:")
    vistos = set()
    for c in cs:
        if c.referencia in vistos:
            continue
        vistos.add(c.referencia)
        expr = "  ".join(f"{sf:+.2f}·{caso}" for caso, sf in c.terminos)
        marca = "   [sólo componentes sensibles]" if c.sobrerresistencia else ""
        print(f"  ({c.referencia:20s}) {expr}{marca}")
