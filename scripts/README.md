# SAP2000 Script Library

Auto-managed collection of verified SAP2000 API scripts.

Scripts are saved here automatically when the agent runs them successfully with `save_as`.
Use `list_scripts` to browse and `load_script` to reload any script.

## Usage

Scripts are designed to be executed via the `run_sap_script` MCP tool.
They expect `SapModel`, `SapObject`, and `result` to be pre-injected.

## Wrappers

The `wrappers/` subdirectory contains minimal, self-contained scripts that
demonstrate the correct usage of individual API functions. See
[wrappers/README.md](wrappers/README.md) for details.

## Registry

The file `registry.json` tracks all verified API functions across all scripts.
Query it via the `query_function_registry` MCP tool, or inspect the JSON directly.

---

## `galpon_altiplano_*` — el galpón a dos aguas del altiplano

Modelo de la serie de posts del sitio (memoria de cálculo:
`fcocarrascob.github.io/SERIE-GALPON.md`). Galpón 24 × 24 m, dos aguas 10°, marcos de peralte
variable, Pica (Tarapacá). NCh2369:2025 + NCh3171:2017 + NCh432:2025.

### Orden obligatorio — no es sugerencia

```
galpon_altiplano_build  ->  _espectral  ->  _combos  ->  _envolvente  ->  _deriva
```

**`build` hace `InitializeNewModel` y borra todo lo que crearon los otros cuatro.** Correrlo
después de `_espectral` deja los casos RS inexistentes, y entonces `RespCombo.SetCaseList`
devuelve `1` sin explicar por qué. Si tocas `build`, se re-corren los cuatro siguientes.

Dos advertencias de operación, aprendidas a la mala:

- **No encadenes muchos ciclos de `InitializeNewModel` + `RunAnalysis` en un solo script.** Seis
  seguidos (~100 s) tumbaron el RPC de SAP2000 con `0x800706BE` y cerraron el programa. En tandas
  de tres corre en ~31 s sin problema.
- Después de esa caída el MCP conserva un handle muerto y `connect_sap2000` responde «Already
  connected». Hay que `disconnect_sap2000` primero y reconectar con `attach_to_existing=False`.

### Superados — se conservan como registro, NO se corren

Estos tres son pasos intermedios de la construcción iterativa. Su lógica quedó absorbida por
`build`, y **sus cabeceras `Result:` tienen números que ya no son los del modelo**:

| Script | Por qué quedó fuera | Trampa de su cabecera |
|---|---|---|
| `_cargas_gravedad` | aplicaba las cargas como **nodales** en las líneas de costanera; se cambió a distribuidas sobre barras porque las nodales metían masa en nodos sin atadura | sus resultantes sí son válidas (`DSD` 302,964 kN, `SBAL` 691,2 kN) |
| `_cargas_viento` | el cálculo de presiones es el bueno y se conservó, pero la **asignación** se movió a `build` | sus `resultante_analitica_kN` coinciden con las vigentes |
| `_modal` | corría **30 modos**; el modelo final necesita **60** | **peligroso**: reporta `T*_Y = 0,268 s` en el modo 8. El verdadero es **0,1610609 s en el modo 41** — los 30 modos ni siquiera alcanzaban a llegar. Su `masa_acumulada` en Y (46,7 %) no cumple el 90 % de §5.6.2 |

### Un detalle de `_espectral`

Su cabecera `Name`/`Description`/`Result` quedó estampada por una corrida de sondeo posterior
(un modelo de prueba de 3 nodos, para ver cómo reporta SAP una combinación que contiene un caso
espectral). **El código del archivo es el autoritativo**, y su bloque `T_estrella` / `R_estrella`
sí corresponde al galpón. No confíes en el resto de ese `Result:`.

### Los números que tienen que salir

Si el modelo se re-construye desde cero, estos son los valores contra los que verificar:

| | |
|---|---|
| Conteo | 105 nodos · 188 barras · 20 bases · 70 barras con `No design` |
| Acero | 23 826,406894506235 kg |
| Equilibrio | residuo **0,0** en los 11 estados |
| Masa sísmica | 674,8610909934324 kN (`D + 0,20·S`) |
| `T*` | X 0,8526565963541679 s (modo 1) · Y 0,1610608923144279 s (modo 41) |
| `R*` (R = 4) | X 4,000000 · Y 3,8301633726045696 |
| `Q₀` | X 86,960228719357 · Y 130,2571888641845 kN |
| Deriva | 0,113504 m contra el límite 0,120 m |
