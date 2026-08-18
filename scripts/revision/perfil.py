"""
perfil — el perfil normativo de un proyecto.

Es lo que hace que el panel de revisión no esté casado con ninguna norma. Cada
proyecto declara en su `PERFIL.json` bajo qué reglamento se rige, dónde están
los PDF, qué sistema estructural se adoptó y cuál es el modelo vigente; los
agentes revisan contra eso y no contra un reglamento cableado en el prompt.

    from revision import perfil
    p = perfil.cargar(r"...\\Pachon\\PERFIL.json")
    p.norma("C103-P1").ruta          # PDF del Reglamento, ruta absoluta
    p.pagina_pdf("C103-P1", 87)      # página impresa 87 -> página del visor

Un perfil puede heredar de otro archivo (`hereda`), que es donde viven las
normas compartidas entre proyectos —las chilenas y americanas de
`Documentos\\Normas\\`— para no repetirlas en cada uno. Las claves del proyecto
pisan a las heredadas.

Todas las rutas se resuelven **relativas al archivo JSON que las declara**, no
al directorio de trabajo. Así el perfil sigue siendo válido si el árbol
completo se mueve de disco o de usuario, que con OneDrive pasa.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field


@dataclass
class Norma:
    """Un documento normativo consultable.

    `offset_pagina` es la diferencia entre la página que el visor de PDF
    muestra y la que está impresa en el pie: `pagina_pdf = impresa + offset`.
    Existe porque los reglamentos traen portada, prólogo y índice sin numerar,
    y leer la página equivocada es la forma más silenciosa de validar una cita
    falsa.
    """

    clave: str
    titulo: str = ""
    edicion: str = ""
    ruta: str = ""
    offset_pagina: int = 0
    rol: str = ""
    notas: str = ""

    @property
    def existe(self) -> bool:
        return bool(self.ruta) and os.path.isfile(self.ruta)

    def cita(self, articulo: str = "", pagina_pdf: int | None = None,
             rasterizada: bool = False) -> str:
        """La cita corta que los revisores deben poner entre paréntesis."""
        partes = [f"{self.titulo or self.clave}"]
        if self.edicion:
            partes[0] += f"-{self.edicion}"
        if articulo:
            partes.append(articulo)
        if pagina_pdf is not None:
            partes.append(f"pág. {pagina_pdf}" + (" rast." if rasterizada else ""))
        return "(" + ", ".join(partes) + ")"


@dataclass
class Perfil:
    ruta_json: str
    datos: dict
    normas: dict[str, Norma] = field(default_factory=dict)

    # -- identidad -----------------------------------------------------
    @property
    def proyecto(self) -> str:
        return self.datos.get("proyecto", "")

    @property
    def raiz(self) -> str:
        """Carpeta del proyecto: la que contiene el `PERFIL.json`."""
        return os.path.dirname(os.path.abspath(self.ruta_json))

    @property
    def pais(self) -> str:
        return self.datos.get("pais", "")

    @property
    def base(self) -> str:
        """`LRFD` o `ASD`. Mezclar familias es un hallazgo, no un detalle."""
        return self.datos.get("base", "")

    # -- normas --------------------------------------------------------
    def claves(self, rol: str = "") -> list[str]:
        if not rol:
            return sorted(self.normas)
        return sorted(k for k, n in self.normas.items() if n.rol == rol)

    def norma(self, clave: str) -> Norma:
        if clave not in self.normas:
            disponibles = ", ".join(self.claves()) or "ninguna"
            raise KeyError(
                f"'{clave}' no está en el perfil de {self.proyecto or self.ruta_json}. "
                f"Claves disponibles: {disponibles}")
        return self.normas[clave]

    def faltantes(self) -> list[Norma]:
        """Normas declaradas cuyo PDF no está en disco.

        Se declaran igual, en vez de omitirlas: una norma que hace falta y no
        está es un dato que el revisor tiene que poder reportar, no un silencio.
        """
        return [n for n in self.normas.values() if not n.existe]

    def pagina_pdf(self, clave: str, pagina_impresa: int) -> int:
        return int(pagina_impresa) + self.norma(clave).offset_pagina

    def pagina_impresa(self, clave: str, pagina_pdf: int) -> int:
        return int(pagina_pdf) - self.norma(clave).offset_pagina

    # -- proyecto ------------------------------------------------------
    def ruta_proyecto(self, relativa: str) -> str:
        return os.path.normpath(os.path.join(self.raiz, relativa))

    @property
    def modelo_vigente(self) -> str:
        r = self.datos.get("modelo_vigente")
        return self.ruta_proyecto(r) if r else ""

    @property
    def dir_revision(self) -> str:
        return self.ruta_proyecto(self.datos.get("dir_revision", ".revision"))

    @property
    def dir_png(self) -> str:
        d = os.path.join(self.dir_revision, "png")
        os.makedirs(d, exist_ok=True)
        return d

    @property
    def modulo_sismico(self) -> str:
        """Nombre del paquete de norma (`cirsoc`, `nch`, …), o "" si no hay.

        Cuando está vacío, el revisor sísmico **lo declara y degrada a 🔵** en
        vez de fingir cobertura con la norma de otro país.
        """
        return self.datos.get("modulo_sismico", "")

    @property
    def sistema(self) -> dict:
        """Sistema estructural y factores adoptados, por dirección."""
        return self.datos.get("sistema", {})

    def resumen(self) -> dict:
        return {
            "proyecto": self.proyecto,
            "pais": self.pais,
            "base": self.base,
            "modulo_sismico": self.modulo_sismico or None,
            "modelo_vigente": self.modelo_vigente or None,
            "normas": len(self.normas),
            "normas_faltantes": [n.clave for n in self.faltantes()],
        }


def _fusionar(destino: dict, origen: dict) -> dict:
    for k, v in origen.items():
        if isinstance(v, dict) and isinstance(destino.get(k), dict):
            _fusionar(destino[k], v)
        else:
            destino[k] = v
    return destino


def _normas_de(datos: dict, base_dir: str) -> dict[str, Norma]:
    raiz = os.path.normpath(os.path.join(base_dir, datos.get("raiz", ".")))
    out = {}
    for clave, d in (datos.get("normas") or {}).items():
        ruta = d.get("ruta", "")
        if ruta and not os.path.isabs(ruta):
            ruta = os.path.normpath(os.path.join(raiz, ruta))
        out[clave] = Norma(
            clave=clave, titulo=d.get("titulo", ""), edicion=str(d.get("edicion", "")),
            ruta=ruta, offset_pagina=int(d.get("offset_pagina", 0)),
            rol=d.get("rol", ""), notas=d.get("notas", ""))
    return out


def cargar(ruta: str) -> Perfil:
    """Lee un `PERFIL.json`, resolviendo la herencia y las rutas relativas."""
    ruta = os.path.abspath(ruta)
    if not os.path.isfile(ruta):
        raise FileNotFoundError(
            f"No hay perfil normativo en {ruta}. Cada proyecto necesita el suyo: "
            "copiar _Plantillas/PERFIL_PLANTILLA.json y completarlo.")
    with open(ruta, encoding="utf-8") as fh:
        datos = json.load(fh)

    base_dir = os.path.dirname(ruta)
    normas: dict[str, Norma] = {}
    heredado: dict = {}

    padre = datos.get("hereda")
    if padre:
        ruta_padre = padre if os.path.isabs(padre) else os.path.normpath(
            os.path.join(base_dir, padre))
        with open(ruta_padre, encoding="utf-8") as fh:
            heredado = json.load(fh)
        normas.update(_normas_de(heredado, os.path.dirname(ruta_padre)))

    normas.update(_normas_de(datos, base_dir))

    fusion = _fusionar(dict(heredado), datos)
    fusion.pop("normas", None)
    return Perfil(ruta_json=ruta, datos=fusion, normas=normas)


def buscar_perfil(desde: str) -> str:
    """Sube por el árbol hasta encontrar un `PERFIL.json`.

    Permite invocar la CLI desde cualquier subcarpeta del proyecto sin pasar
    la ruta a mano.
    """
    d = os.path.abspath(desde if os.path.isdir(desde) else os.path.dirname(desde))
    while True:
        cand = os.path.join(d, "PERFIL.json")
        if os.path.isfile(cand):
            return cand
        padre = os.path.dirname(d)
        if padre == d:
            raise FileNotFoundError(
                f"No se encontró PERFIL.json subiendo desde {desde}")
        d = padre


__all__ = ["Norma", "Perfil", "cargar", "buscar_perfil"]
