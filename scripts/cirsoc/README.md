# cirsoc — diseño sismorresistente argentino sobre SAP2000

Cuatro módulos que empaquetan lo aprendido trabajando con la API COM de
SAP2000 y con **INPRES-CIRSOC 103 Parte I (2018)**. Nacieron auditando y
corrigiendo el modelo de la nave de El Pachón, pero no dependen de ese
proyecto.

| Módulo | Qué hace | Necesita SAP |
|---|---|:--:|
| `sap_utils.py` | Enums, tablas, conectividad, trampas de la API | recibe `SapModel` |
| `espectro_cirsoc103.py` | Espectro, coeficiente sísmico, escalado del 85 % | sólo al final |
| `combos_cirsoc.py` | Juego de combinaciones CIRSOC 101 + 103 | sólo al escribir |
| `auditoria_modelo.py` | Radiografía del modelo + hallazgos accionables | sí |

La lógica normativa es **pura y verificable a mano**; el contacto con SAP está
aislado en unas pocas funciones que reciben un `SapModel` ya conectado. Eso
permite usarlas igual desde el MCP (que lo inyecta) o desde un script propio
con `comtypes.client.GetActiveObject`.

```bash
python espectro_cirsoc103.py     # imprime el espectro de un sitio
python combos_cirsoc.py          # imprime el juego de combinaciones
python verificar_cirsoc.py       # autochequeo contra números calculados a mano
python auditoria_modelo.py       # audita el modelo abierto en SAP2000
```

---

## Flujo completo

```python
import sap_utils as su
from espectro_cirsoc103 import (EspectroCIRSOC, cargar_funcion, configurar_casos,
                                configurar_vertical, verificar_85,
                                factor_escala_espectral)
from combos_cirsoc import generar, escribir_en_sap, seleccionar_para_diseno
from auditoria_modelo import auditar, imprimir

GAMMA_R, R, H = 1.3, 3.0, 17.2          # Grupo A · OCBF/OMF · altura

# 0) copia de trabajo — File.Save(ruta) es un Save As
su.copia_de_trabajo(SapModel, r"...\MOD\modelo_CIRSOC.sdb")
su.desbloquear(SapModel)

# 1) espectro
esp = EspectroCIRSOC.desde_zona(zona=4, sitio="SC")
cargar_funcion(SapModel, esp)
configurar_casos(SapModel, GAMMA_R, R)
configurar_vertical(SapModel, esp, GAMMA_R)

# 2) combinaciones
combos = generar()
escribir_en_sap(SapModel, combos)

# 3) analizar y escalar al 85 % del estático (§7.2.5)
su.analizar(SapModel)
W  = su.masa_total(SapModel) * 9.81
Tx = su.periodo_traslacional(SapModel, "UX")
V0 = su.reacciones_base(SapModel, casos=["EQX"])["EQX::Max"]["FX"]
chk = verificar_85(esp, Tx, V0, W, H, GAMMA_R, R, "OTROS")
configurar_casos(SapModel, GAMMA_R, R, factores={"X": chk["factor"]})
su.analizar(SapModel)

# 4) diseñar y auditar
seleccionar_para_diseno(SapModel, combos)          # deja fuera [3.19]/[3.20]
filas = su.diseno_acero(SapModel, "Steel Design 1 - Summary Data - AISC 360-16")
print(su.resumen_diseno(SapModel, filas))
imprimir(auditar(SapModel))
```

---

## Trampas de la API que estos módulos ya resuelven

Están todas encapsuladas; se listan para saber qué hay debajo.

**`ItemType`.** El último argumento de casi todos los Get/Set de asignaciones.
Usar `SELECTED` (2) desde un script devuelve **0 resultados sin error** si no
hay nada seleccionado en la GUI. Para barrer el modelo: `GROUP` (1) con el
nombre `'All'`.

**Código de retorno.** Una función con parámetros ByRef devuelve
`(*salidas, ret)`, no el entero pelado. `SetReleases(...) == 0` es *siempre*
False aunque la llamada haya funcionado. Usar `su.ret_code()`.

**Dirección de las cargas.** Con `Dir.GRAVITY` (10) el valor **positivo es
hacia abajo**; con `Dir.GLOBAL_Z` (6) es hacia arriba. Mezclarlas hace que las
cargas se cancelen en silencio.

**Tablas.** `GetTableForDisplayArray(key, [''], '', 0, [''], 0, [''])` — pasar
`[]` en vez de `['']` da `'int' object is not iterable`. Los campos están en
el índice **2**, los datos en el **4**. Y devuelven strings con el separador
decimal del sistema: usar `su.num()`.

**`Assembled Joint Masses`.** Trae una fila `SumAccelUZ` con la suma de todas
las demás. Sumar la columna a ciegas da el doble.

**Cargas invisibles.** `Frame Loads - Distributed` y `Area Loads - Uniform`
aparecen vacías cuando las cargas se aplicaron como **Uniform to Frame** sobre
las áreas. La forma robusta de saber qué está cargado es la reacción basal del
caso.

**Links.** `FrameObj.GetNameList` no los ve. El inventario completo es
frames + points + areas + **links**, contrastado contra el grupo `All`.

**Modelo bloqueado.** Después de analizar, los `Set` de definición fallan hasta
`SetModelIsLocked(False)` — que **borra los resultados**. Conviene agrupar
todas las modificaciones antes de re-analizar.

**Espectral dentro de una combinación.** SAP ya aplica el ± al término
espectral y reporta Max/Min. No hay que duplicar la combinación.

**Presión normal a superficies con orientaciones distintas.** No sirven las
direcciones globales: va `Dir.LOCAL_3`, pero el sentido del eje local depende
del orden de los nodos. `su.normal_area()` devuelve el signo correcto contra
un punto interior. Verificar siempre contra la resultante calculada a mano.

---

## Lo que trae del Reglamento

`espectro_cirsoc103.py` tiene transcritas las Tablas **2.2, 3.1, 3.2, 3.3,
5.1, 6.1, 6.2 y 6.4** y las expresiones [3.1]–[3.20], [6.3]–[6.8] y
[7.1]–[7.3].

Tres puntos que no son intuitivos y el módulo aplica solo:

1. **La edición 2018 usa la forma Ca/Cv**, no la trilineal `as, b, T1, T2` de
   las ediciones anteriores. Es la misma familia de expresiones que ASCE 7:
   `S_DS = 2,5·Ca` y `S_D1 = Cv`. Por eso
   `EspectroCIRSOC.calibrado_a_sitio(S_DS, S_D1)` reproduce exactamente un
   espectro de un estudio de amenaza sin salirse del marco de CIRSOC — y
   devuelve los `Na`/`Nv` equivalentes para documentar el apartamiento.

2. **El período de cálculo está acotado** por [6.7]: `T <= Cu·Cr·H^x`.
   Saltarse el límite subestima el corte basal estático y hace parecer que el
   escalado del §7.2.5 no hace falta.

3. **`f2` sólo vale 0,70 o 0,20** (Tabla 3.3). No existe el 0,50 que traen
   varios criterios de diseño internacionales.

Y una del lado del diseño: `[3.19]` y `[3.20]` (las de Ω₀) se aplican *"en
componentes sensibles a los efectos de la sobrerresistencia estructural"*, no
a toda la estructura. `seleccionar_para_diseno()` las deja fuera del diseño
automático por defecto.

---

## Lo que la auditoría busca

Ordenado por lo que cuesta encontrarlo a ojo:

| Chequeo | Por qué importa |
|---|---|
| Diagonales sin rótula en **ambos** extremos | El PMM se dispara por momento, no por axial. Un extremo rígido convierte el arriostramiento en voladizo |
| `Ry` contra AISC 341 Tabla A3.1 | El 1,40 del HSS A500 es el que más se olvida; deja corto todo diseño por capacidad |
| Secciones con `TotalWt = 0` | Definidas y sin asignar — placeholders olvidados |
| Casos con reacción nula | Patrones vacíos que sin embargo participan en las combinaciones |
| Multiplicadores del mass source | Un peso propio con factor 0,5 no se ve en ningún lado |
| `Provision = ASD` con combinaciones LRFD | SAP compara solicitaciones mayoradas contra resistencias admisibles y no avisa |
| Masa participante < 90 % | §7.2.3 |
| `Second Order = General 2nd Order` sin caso P-Δ | Silenciosamente inconsistente |
| Nodos sin ninguna barra | Puntas de ménsula sin nada montado encima |

---

## Verificación

`verificar_cirsoc.py` comprueba contra números calculados a mano: ordenadas
del espectro en los quiebres, `T1`/`T2`, `Cu`, `Ta`, el coeficiente sísmico en
las dos ramas, el escalado del §7.2.5 y el conteo de combinaciones por
familia. Corre sin SAP2000.

## Pendiente

- Tabla 2.3 (regularidad en planta) para decidir la excentricidad accidental
  automáticamente en vez de sólo advertir.
- Partes II a V del Reglamento (hormigón, mampostería, acero, puentes).
- Lectura de la Tabla 5.1 para proponer `R`/`Cd`/`Ω₀` a partir del sistema
  detectado en el modelo.
