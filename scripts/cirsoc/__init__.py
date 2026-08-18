"""
cirsoc — reglamento argentino (CIRSOC 101/102/104, INPRES-CIRSOC 103, CIRSOC 301)
y la capa de API COM de SAP2000 sobre la que se apoya.

Es el módulo **específico de una norma**. Lo que no depende de ninguna
—leer PDFs, validar catálogos, dar formato a hallazgos— vive en el paquete
hermano `revision`. Un proyecto chileno usará `nch` con la misma forma:
lógica pura verificable sin SAP, más un puñado de funciones que reciben un
`SapModel` ya conectado.

    from cirsoc import auditoria_modelo
    auditoria_modelo.imprimir(auditoria_modelo.auditar(SapModel))

RESTRICCIÓN QUE NO SE PUEDE DESHACER
------------------------------------
Los módulos de este paquete se importan **planos** entre sí
(`import sap_utils as su`, no `from . import sap_utils`) porque el sandbox del
servidor MCP los carga de esa forma y además bloquea `os` y `sys`. Convertir
esos imports a relativos haría el paquete más ortodoxo y rompería el uso desde
el MCP, que es el camino principal.

Este `__init__.py` existe sólo para que `import cirsoc.x` funcione **fuera**
del sandbox; para lograrlo inserta su propio directorio en `sys.path` y deja
los imports internos como están. El acceso a `os`/`sys` va protegido para que,
si alguna vez alguien importa el paquete desde dentro del sandbox, degrade en
vez de fallar.

`verificar_cirsoc` no se expone acá a propósito: ejecuta su batería de
aserciones al importarse y termina con `sys.exit(1)` si algo falla. Se corre
como script, vía `python -m revision.cli verificar`.
"""

from __future__ import annotations

try:  # fuera del sandbox: habilita el import plano interno
    import os as _os
    import sys as _sys

    _DIR = _os.path.dirname(_os.path.abspath(__file__))
    if _DIR not in _sys.path:
        _sys.path.insert(0, _DIR)
except ImportError:  # dentro del sandbox del MCP, que bloquea os/sys
    _DIR = None

__version__ = "0.2.0"

_SUBMODULOS = ("sap_utils", "espectro_cirsoc103", "combos_cirsoc", "auditoria_modelo")


def __getattr__(nombre: str):
    """Importa los submódulos a demanda, para que `import cirsoc` sea barato."""
    if nombre in _SUBMODULOS:
        import importlib
        mod = importlib.import_module(f".{nombre}", __name__)
        globals()[nombre] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {nombre!r}")


def __dir__():
    return sorted(list(globals()) + list(_SUBMODULOS))


__all__ = ["__version__", *_SUBMODULOS]
