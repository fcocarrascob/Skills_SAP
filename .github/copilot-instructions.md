# SAP2000 API Skill — Instrucciones de Copilot

## ¿Qué es este workspace?

Framework para automatizar SAP2000 mediante scripts Python ejecutados a través
de un MCP bridge local (COM). Permite generar modelos estructurales, asignar
cargas, ejecutar análisis y extraer resultados de forma programática.

## Mapa de Documentación

| Documento | Para qué |
|-----------|----------|
| `.github/agents/sap2000-scripter.agent.md` | Agente con workflow completo (usa `@sap2000-scripter`) |
| `.github/skills/sap2000-api/SKILL.md` | Referencia técnica API (convenciones, templates, registry) |
| `.github/skills/sap2000-api/references/api-patterns.md` | Patrones detallados de operaciones comunes |
| `.github/skills/sap2000-api/references/enum-reference.md` | Enumeraciones completas (eUnits, eMatType, etc.) |
| `.github/skills/sap2000-api/references/common-workflows.md` | Workflows paso a paso + Patrón Universal de scripts |
| `.github/skills/sap2000-api/references/script-templates.md` | Templates paramétricos (grid, circular, placa) |
| `.github/skills/sap2000-api/references/gui-generation.md` | Guía de generación de GUI standalone (PySide6) |
| `scripts/wrappers/` | Funciones verificadas (fuente de verdad para firmas) |
| `scripts/templates/` | Templates base para backend y GUI standalone |
| `scripts/registry.json` | Registry de funciones verificadas |

> ⚠️ NUNCA editar `scripts/registry.json` directamente. Usar `register_verified_function`.

## Configuración MCP

El servidor MCP se autoconfigura via `.vscode/mcp.json`:
- **Python venv:** `.venv/Scripts/python.exe`
- **Script:** `mcp_server/server.py`
- **Protocolo:** stdio (auto-start al invocar herramientas)
- **Tools expuestos:** 12 (connect, disconnect, get_model_info, execute_sap_function,
  run_sap_script, list_scripts, load_script, search_api_docs, list_api_categories,
  query_function_registry, register_verified_function, list_registry_categories)

## Cuándo usar qué

### Agente SAP2000 Scripter (`@sap2000-scripter`)

**Usar para:**
- Generar scripts de SAP2000 (marcos, áreas, análisis)
- Automatización estructural completa
- Workflow: research → **plan → aprobación** → código → ejecución → verificación → guardado

**Capacidades:**
- Research automático para scripts complejos (via subagent Explore)
- Planificación pre-generación con clasificación de complejidad
- Consulta inteligente al registry de funciones verificadas
- Generación iterativa con testing incremental
- Oferta de GUI standalone al finalizar

> Para el workflow detallado paso a paso (incluyendo planificación),
> ver el agente `@sap2000-scripter`.

### Skill sap2000-api (attachment)

**Usar para:**
- Consultas rápidas sobre convenciones API (ByRef, return codes)
- Patrones de código específicos
- Referencia de enumeraciones y jerarquía de objetos

## Requisitos del Sistema

- Windows OS (SAP2000 solo corre en Windows)
- Python 3.10+
- SAP2000 instalado localmente
- Paquetes: `comtypes`, `mcp[cli]` (ver `mcp_server/requirements.txt`)

## Quick Start

1. Activar venv: `.venv/Scripts/Activate.ps1`
2. Invocar agente: `@sap2000-scripter genera una viga simple con carga muerta`
3. El agente maneja el resto (conexión, registry, planificación, generación, ejecución)
