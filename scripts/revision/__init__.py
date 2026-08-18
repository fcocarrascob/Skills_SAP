"""
revision — infraestructura de revisión estructural **independiente de la norma**.

Lo que vive acá no sabe si el proyecto se rige por CIRSOC, NCh o E.030: lee
PDFs de reglamento, valida designaciones contra catálogos, y da formato y
persistencia a los hallazgos. La lógica normativa vive en los paquetes
hermanos (`cirsoc`, `nch`, …), que este paquete resuelve por el perfil del
proyecto.

    from revision import reporte, normas_pdf, perfil

Superficie de línea de comandos — es la única que usan los agentes:

    python -m revision.cli verificar
    python -m revision.cli auditar --json <salida.json>
    python -m revision.cli norma leer --perfil <PERFIL.json> --clave ... --pagina-impresa ...

Los módulos de `cirsoc` se importan **planos** (`import sap_utils as su`) porque
el sandbox del MCP los carga así. Para que eso siga funcionando cuando se usa
`cirsoc` como paquete, se agrega `scripts/` y `scripts/cirsoc/` a `sys.path`
aquí, que es código que nunca corre dentro del sandbox.
"""

from __future__ import annotations

import os as _os
import sys as _sys

#: Raíz de `scripts/`, que contiene este paquete y sus hermanos.
SCRIPTS = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

for _d in (SCRIPTS, _os.path.join(SCRIPTS, "cirsoc")):
    if _os.path.isdir(_d) and _d not in _sys.path:
        _sys.path.insert(0, _d)

__version__ = "0.1.0"

_SUBMODULOS = ("perfil", "normas_pdf", "catalogo", "reporte")


def __getattr__(nombre: str):
    """Importa los submódulos a demanda.

    Evita que `import revision` arrastre pymupdf cuando sólo se necesita dar
    formato a un reporte.
    """
    if nombre in _SUBMODULOS:
        import importlib
        mod = importlib.import_module(f".{nombre}", __name__)
        globals()[nombre] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {nombre!r}")


def __dir__():
    return sorted(list(globals()) + list(_SUBMODULOS))


__all__ = ["SCRIPTS", "__version__", *_SUBMODULOS]
