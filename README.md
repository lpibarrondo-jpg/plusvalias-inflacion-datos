# Plusvalías nominales e inflación: datos y cálculos

Datos, scripts y metodología del artículo sobre cómo el IRPF grava como ganancia la parte del valor de un bien que solo es inflación.

El objetivo es que cualquier persona pueda comprobar cada cifra del artículo partiendo de fuentes oficiales.

## Fuentes

| Dato | Fuente | Serie / referencia | Estado |
| --- | --- | --- | --- |
| Índice de Precios de Consumo (IPC) | [INE](https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736176802&idp=1254735976607) | IPC290751, «Nacional. Índice general. Índice», base 2025 | Descargado |
| Variación anual del IPC (verificación) | INE | IPC290750 | Descargado |
| Variación mensual del IPC desde 1961 (contexto y encadenado anterior a 2002) | INE | IPC290752 (`ine_ipc_variacion_mensual.csv`) | Descargado |
| Tipos de interés de depósitos de hogares | [Banco de España](https://www.bde.es/webbe/es/estadisticas/temas/tipos-interes.html), Boletín Estadístico | Cuadro 19.7 (nuevas operaciones, TEDR: DN_1TI1T0010, DN_1TI2T0024 a DN_1TI2T0027) y cuadro 19.10 (saldos vivos, DN_1TI1T0060) | Descargado |
| Ganancias patrimoniales declaradas en el IRPF | AEAT, Estadística de los declarantes del IRPF 2024, bloque V: [tabla nacional](https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpf/2024/jrubikf530a7632efff77b3f64b82f5ebaacf18d5b28fc9.html) e [inmuebles](https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpf/2024/jrubikf68b5114b8e5bc6fad9e56a670a6783c3409020da.html) | «Detalle de las operaciones de transmisión de activos por tipo de activo subyacente» (total, inmuebles, valores, resto) | Descargado |
| Periodo medio de posesión de viviendas transmitidas | [Colegio de Registradores, Anuario ERI 2024](https://www.registradores.org/documents/33383/148210/ERI%2BAnuario%2B2024.pdf), resumen ejecutivo, p. 7 | 17,7 años (2024) | Citado |
| Índice de Precios de Vivienda (IPV), por CCAA | [INE](https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736152838&menu=resultados&idp=1254735976607) | Tabla 80271 (medias anuales, 2007-2025) y tabla 80270 (trimestral, hasta 2026 T2), base 2015, `data/raw/ine_ipv/` | Descargado |
| Compraventas de viviendas | INE, Estadística de Transmisiones de Derechos de la Propiedad (ETDP) | ETDP1826, «Total Nacional. General. Compraventa. Número», mensual, `data/raw/ine_etdp/` | Descargado |
| Coeficientes de actualización del IRPF de Álava (2026) | [Decreto Foral 41/2025](https://www.araba.eus/botha/Boletines/2025/146/2025_146_03735_C.pdf), BOTHA n.º 146, 26-12-2025, art. 1 (art. 45.2 de la Norma Foral 33/2013) | 2007: 1,489; 2008: 1,430 | Citado |
| Escala del ahorro del IRPF | [BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764), Ley 35/2006, arts. 66 y 76, todas sus versiones (API de legislación consolidada) | `data/raw/boe/lirpf_a66.xml`, `lirpf_a76.xml` | Descargado |

## Calculadora

`calculadora/index.html` es una página autónoma: cada persona introduce la fecha y el precio de compra y de venta de su vivienda (y, si quiere, los gastos) y ve qué parte de la ganancia es inflación, la ganancia real y el IRPF con la ley actual frente al que pagaría si se descontara la inflación. Aplica la escala del ahorro de 2026, como si esa ganancia fuera la única renta del ahorro del año, sin exenciones ni coeficientes de abatimiento.

- Se genera con `python scripts/construir_calculadora.py`, que incrusta el IPC mensual del INE en la página a partir de `calculadora/plantilla.html`.
- Desde enero de 2002 usa el índice oficial; antes lo reconstruye hacia atrás con la variación mensual oficial redondeada a un decimal, y la página avisa de que el resultado es aproximado.
- Su lógica se comprobó contra un cálculo independiente en Python en cinco casos, incluido el del gráfico 4 (32.448 € de IRPF).

## Jurisprudencia

La STC 67/2023 es la única sobre el IRPF y **desestimó** la cuestión: avaló que el impuesto no actualice con la inflación el valor de compra de los inmuebles. Las de la plusvalía municipal fueron favorables al contribuyente y se citan por contraste.

| Sentencia | Sentido del fallo | Enlace | Copia local |
| --- | --- | --- | --- |
| STC 67/2023, de 6 de junio (IRPF, coeficientes de actualización de inmuebles) | Desestima: es constitucional no corregir la inflación. Voto particular de dos magistrados | [TC](https://hj.tribunalconstitucional.es/es/Resolucion/Show/29515) · [BOE](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-16398) | `data/raw/sentencias/BOE-A-2023-16398.xml` |
| STC 221/1992, de 11 de diciembre (plusvalía municipal) | Desestima: avala el principio nominalista salvo inflación «extrema» | [TC](https://hj.tribunalconstitucional.es/es/Resolucion/Show/2108) · [BOE](https://www.boe.es/diario_boe/txt.php?id=BOE-T-1993-1242) | `data/raw/sentencias/BOE-T-1993-1242.xml` |
| STC 26/2017, de 16 de febrero (plusvalía municipal, Gipuzkoa) | Estima en parte: nula si grava incrementos inexistentes | [TC](https://hj.tribunalconstitucional.es/es/Resolucion/Show/25265) · [BOE](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2017-3255) | `data/raw/sentencias/BOE-A-2017-3255.xml` |
| STC 59/2017, de 11 de mayo (plusvalía municipal) | Estima en parte: nula si grava incrementos inexistentes | [TC](https://hj.tribunalconstitucional.es/es/Resolucion/Show/25349) · [BOE](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2017-6855) | `data/raw/sentencias/BOE-A-2017-6855.xml` |
| STC 126/2019, de 31 de octubre (plusvalía municipal) | Estima: inconstitucional cuando la cuota supera la ganancia | [TC](https://hj.tribunalconstitucional.es/es/Resolucion/Show/26072) · [BOE](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-17639) | `data/raw/sentencias/BOE-A-2019-17639.xml` |
| STC 182/2021, de 26 de octubre (plusvalía municipal) | Estima: anula el método de cálculo de la base | [TC](https://hj.tribunalconstitucional.es/es/Resolucion/Show/26840) · [BOE](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2021-19511) | `data/raw/sentencias/BOE-A-2021-19511.xml` |

## Estructura

```
data/raw/         Datos tal como los publica la fuente, sin modificar
data/processed/   Tablas derivadas (Excel con fórmulas y tablas de cada gráfico)
graficos/         Gráficos del artículo (PNG)
calculadora/      Calculadora interactiva (index.html generado y su plantilla)
scripts/          Scripts de descarga, cálculo y gráficos
```

## Cómo reproducirlo

Requisitos: Python 3.10 o superior y `openpyxl`.

```bash
python scripts/descargar_ipc.py        # descarga el IPC y su variación mensual desde la API del INE
python scripts/construir_hoja_ipc.py   # genera data/processed/IPC_Espana_base_INE.xlsx
python scripts/graficos.py             # genera graficos/ y sus tablas en data/processed/
python scripts/vender_con_perdidas.py  # gráfico 6: comprar en 2007-2008 y vender hoy, por CCAA
```

Requiere además `matplotlib` y `numpy` para los gráficos, y la fuente Inter para que los textos queden como en los PNG publicados. Con el Python de python.org en macOS, instala `certifi` (`pip install certifi`) para que la descarga del INE no falle por certificados.

Abre el Excel en Excel o LibreOffice para que se calculen las fórmulas. En la hoja, el texto azul es dato de la fuente y el negro es fórmula.

## Verificación

- La suma de los 297 índices mensuales (enero 2002 – septiembre 2026) es 23.424,447, idéntica a la que devuelve la API del INE.
- Las 285 tasas interanuales recalculadas a partir del índice coinciden con las publicadas por el INE (serie IPC290750), con una tolerancia de 0,1 puntos por el redondeo de la publicación.

## Gráficos

| Gráfico | Qué muestra | Tabla de datos |
| --- | --- | --- |
| `01_poder_adquisitivo_1000eur.png` | Valor real hoy de 1.000 € guardados sin invertir desde enero de 2002 | `grafico1_poder_adquisitivo_1000eur.csv` |
| `02_tipo_efectivo_ganancia_real.png` | Cuota del IRPF dividida entre la ganancia real, por año de compra y rentabilidad real anual | `grafico2_tipo_efectivo_real.csv` |
| `03_depositos_rentabilidad_real.png` | Rentabilidad real anual de un depósito a plazo de hasta 1 año, antes y después del IRPF | `grafico3_depositos_real.csv` |
| `04_que_arregla_cada_medida.png` | IRPF del caso de 2002 con la ley vigente, con la escala actualizada y descontando la inflación de la ganancia | `tabla_escala_ahorro_actualizada.csv` |
| `05_inflacion_en_plusvalias_inmuebles_2024.png` | Parte de las plusvalías inmobiliarias declaradas en 2024 que solo compensa la inflación, según años de tenencia | `grafico5_inflacion_plusvalias_inmuebles_2024.csv` |
| `06_compra_2007_vende_hoy.png` (y `06_compra_2008_vende_hoy.png`) | Variación del precio de la vivienda en euros y descontada la inflación desde la media de 2007 (o 2008) hasta el último trimestre, por CCAA, y ejemplo de IRPF frente a Álava | `grafico6_compra_2007_venta_hoy.csv`, `grafico6_ejemplo_compra_2007.csv` (y los de 2008) |

### Supuestos del gráfico 2

- Bien comprado por 150.000 € a mitad del año indicado y vendido en el último mes con IPC definitivo.
- Precio de venta = precio de compra × coeficiente IPC × (1 + rentabilidad real anual) ^ años de tenencia.
- Coeficiente IPC = índice del último mes / índice medio del año de compra.
- Cuota = escala del ahorro del IRPF 2026 (19 %, 21 %, 23 %, 27 % y 30 %; tramos de 6.000, 50.000, 200.000 y 300.000 €) aplicada a la ganancia nominal.
- Tipo efectivo real = cuota / (precio de venta − precio de compra × coeficiente IPC).
- Sin gastos de compraventa, exenciones (vivienda habitual de mayores de 65, reinversión), reducciones ni compensación con pérdidas.

### Supuestos del gráfico 3

- Tipo del depósito: media anual del TEDR de nuevas operaciones de depósitos a plazo de hogares hasta 1 año (Banco de España, cuadro 19.7, columna 3).
- Inflación: variación de la media anual del IPC respecto a la del año anterior.
- Rentabilidad real antes del IRPF = (1 + tipo) / (1 + inflación) − 1.
- Rentabilidad real después del IRPF = (1 + tipo × (1 − 0,19)) / (1 + inflación) − 1, con el 19 % del primer tramo de la base del ahorro.
- Lectura correcta del recuento: en 13 de los 23 años el depósito ya perdía poder adquisitivo antes de impuestos; el IRPF añadió 3 (2008, 2012 y 2013) y agravó la pérdida en el resto.
- **Convención temporal.** Se compara el tipo de cada año con la inflación de ese mismo año. Como un depósito a un año vence al siguiente, el CSV incluye también la comparación con la inflación del año siguiente (columnas `_desfasado`): salen 14 años negativos antes del IRPF y 15 después, de 22 con datos. El mensaje no cambia, pero sí años concretos: 2022 pasa de −7,6 % a −3,3 % y el peor año pasa a ser 2021 (−7,7 %).
- **Tipo del IRPF.** Se usa el 19 % en todos los años por sencillez. Los tipos reales fueron otros: escala general hasta 2006, 18 % en 2007-2009, 21 % o más en 2012-2014 y 19,5 % en 2015. Con el tipo mínimo de cada año siguen saliendo 16 años negativos.

### Escala del ahorro y gráfico 4

Umbrales de la escala del ahorro según las versiones de los arts. 66 y 76 LIRPF publicadas por el BOE, actualizados con el IPC desde la media del año en que entraron en vigor:

| Umbral legal | Vigente desde | Norma | Umbral actualizado |
| --- | --- | --- | --- |
| 6.000 € | 2010 | Ley 26/2009 | 8.505 € |
| 50.000 € | 2015 | Ley 26/2014 | 66.539 € |
| 200.000 € | 2021 | Ley 11/2020 | 248.620 € |
| 300.000 € | 2023 | Ley 31/2022 | 332.323 € |

Los importes actualizados se recalculan con cada nueva descarga del IPC.

El gráfico 4 usa el caso de 2002 con un 0,5 % de rentabilidad real anual, un escenario de rentabilidad baja. Con un 2 % (venta por 423.615 €), el IRPF sería de 64.756 € con la ley vigente, 62.430 € actualizando la escala y 35.986 € descontando la inflación de la ganancia: la conclusión se mantiene.

### Supuestos del gráfico 5

- Base: operaciones con inmuebles con ganancia y sin beneficio fiscal (sin exenciones ni reducciones) del IRPF 2024: valor de adquisición 27.400 M€ y ganancia 13.178 M€ (AEAT). Es el resultado positivo declarado; la parte imputable a 2024 es 12.936 M€ (un 1,8 % menos), porque algunas ganancias se imputan a otros ejercicios.
- Componente de inflación = valor de adquisición × (IPC medio de 2024 / IPC del mes medio de compra − 1). El mes medio de compra es mediados de 2024 menos los años de tenencia.
- Tenencia central: 17,7 años, periodo medio de posesión de las viviendas transmitidas en 2024 según el Colegio de Registradores. Como la estadística de la AEAT incluye inmuebles que no son vivienda, se muestran también 10 y 15 años.
- **Sensibilidad a la tenencia** (`grafico5_sensibilidad_tenencia.csv`). Con la distribución de los Registradores (9,64 % de 0 a 2 años, 10,43 % de 2 a 5, 12,76 % de 5 a 10 y 67,17 % de más de 10, con la cola uniforme hasta 38,5 años para que la media sea 17,7), el factor de inflación sobre el valor de compra es 0,42 con la media, 0,63 ponderando por número de ventas y 0,48 ponderando por un valor de compra proporcional al IPC. La media, por tanto, probablemente infravalora el componente de inflación. Podría ocurrir lo contrario si se pondera por precios de vivienda, que subieron más que el IPC entre 1997 y 2007. El IPC anterior a 2002 se encadena con la variación mensual oficial, redondeada a un decimal.
- El titular da un rango (del 48 % con 10 años al 87 % con 17,7) porque el resultado depende de la tenencia, que la AEAT no publica.
- IRPF atribuible: componente de inflación × 21 % (rango 19-23 %, los tramos en que se integra la mayoría de estas ganancias). Es una estimación de lo que se habría gravado sobre esa parte, no una recaudación medida: no descuenta las pérdidas de inmuebles que se compensan en la base del ahorro (5.110 M€ imputables a 2024).
- No se estiman valores (acciones y fondos) por falta de datos públicos sobre su periodo de tenencia. Tampoco se ajustan las operaciones con pérdidas, cuyas pérdidas reales también serían mayores.
- Solo aparecen las ventas realizadas: quien acumula grandes plusvalías tiende a no vender para no tributar (efecto bloqueo), así que estas cifras no recogen las ganancias latentes.

### Supuestos del gráfico 6

- Precio: IPV del INE, índice general (vivienda nueva y de segunda mano). Compra = media anual de 2007 (o 2008); venta = último trimestre publicado (2026 T2). Inflación = IPC medio del trimestre de venta / IPC medio del año de compra (+47,1 % desde 2007; +41,4 % desde 2008).
- El IPV mide precios medios a calidad constante. No dice qué le pasó a cada vivienda concreta: el gráfico describe la vivienda media de cada territorio, no a cada vendedor.
- Categorías: «Paga IRPF y pierde» = la variación nominal es positiva (hay ganancia sujeta en el IRPF de territorio común) y la real es negativa. País Vasco y Navarra tienen IRPF foral y se muestran aparte: los territorios vascos actualizan el valor de adquisición con coeficientes (Álava: 1,489 para compras de 2007 vendidas en 2026). En Navarra el precio medio ni siquiera sube en euros.
- Ejemplo: vivienda de 200.000 € comprada en 2007 que evoluciona como el IPV nacional (+33,6 %): venta por 267.200 €, ganancia nominal de 67.200 €, IRPF de 14.336 € con la escala del ahorro de 2026 y pérdida real de 27.055 €. Con gastos (10 % al comprar, 3 % al vender): ganancia de 39.184 €, IRPF de 8.109 € y pérdida real de 64.497 €. En Álava el valor de adquisición actualizado (297.800 € sin gastos) supera al de venta: hay pérdida y no hay cuota.
- No se aplican las exenciones por reinversión en vivienda habitual (art. 38 LIRPF) ni por transmisión de la vivienda habitual por mayores de 65 años (art. 33.4.b LIRPF): quien se acoge a ellas no tributa. El caso afecta sobre todo a segundas viviendas, inmuebles de inversión y viviendas habituales vendidas sin reinvertir (por ejemplo, para pasar a vivir de alquiler) por menores de 65 años.
- Compraventas: el INE registró 775.300 compraventas de vivienda en 2007 y 552.080 en 2008 (ETDP, fecha de inscripción registral). No todas siguen en manos del mismo propietario ni todas se venderán con ganancia nominal: es la dimensión de la cohorte, no el número de afectados.

### Verificación de la AEAT

La suma de las 99 cifras de importe (el fichero tiene 115 filas; 16 son recuentos de operaciones) del fichero `aeat_irpf2024_transmisiones_por_activo.csv` (1.322.549.047.380 €) coincide con la de las tablas publicadas, y la suma de los resultados por tipo de activo coincide con el total publicado.

## Verificación del Banco de España

Los 285 meses (enero 2003 – septiembre 2026) de las seis series del fichero `bde_tipos_depositos_hogares_mensual.csv` se comprobaron frente al CSV oficial del Banco de España (`be1907.csv` y `be1910.csv`), primero por sumas de columna y después mes a mes: coinciden.

## Auditoría

Antes de publicar, el repositorio pasó una auditoría independiente en solo lectura (Gemini y otra sesión de Claude), con el encargo de `AUDITORIA_GEMINI.md`. No encontró errores críticos. Sus correcciones (titular del gráfico 5 en rango, recuento del gráfico 3, sentido del fallo de la STC 67/2023, «habría gravado» en lugar de «cobró», enlaces de la AEAT y los hallazgos menores) están incorporadas.

## Notas de metodología

- **Cambio de base.** Desde enero de 2026 el INE publica el IPC en base 2025. Es un cambio de escala: las tasas de variación no cambian respecto a bases anteriores.
- **Periodo.** El índice exacto empieza en enero de 2002. Para 1961–2001 el INE solo ofrece variaciones redondeadas a un decimal, que se incluyen como contexto y no se usan en los cálculos.
- **Comparaciones.** Para un año completo se usa el índice medio anual; para una fecha concreta, el índice del mes.
- **Último dato.** Septiembre de 2026 (definitivo). Octubre de 2026 solo tiene dato adelantado y no se usa en ningún cálculo, aunque aparece en los ficheros de variación descargados para verificación (`ine_IPC290750_variacion_anual_2003plus.txt` e `ine_ipc_variacion_mensual.csv`).

Última actualización de datos: 9 de noviembre de 2026.
