# Plusvalías nominales e inflación: datos y cálculos

Datos, scripts y metodología del artículo sobre cómo el IRPF grava como ganancia la parte del valor de un bien que solo es inflación.

El objetivo es que cualquier persona pueda comprobar cada cifra del artículo partiendo de fuentes oficiales.

## Fuentes

| Dato | Fuente | Serie / referencia | Estado |
| --- | --- | --- | --- |
| Índice de Precios de Consumo (IPC) | [INE](https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736176802&idp=1254735976607) | IPC290751, «Nacional. Índice general. Índice», base 2025 | Descargado |
| Variación anual del IPC (verificación) | INE | IPC290750 | Descargado |
| Variación mensual del IPC 1961–2001 (contexto) | INE | IPC290752 | Descargado |
| Tipos de interés de depósitos de hogares | [Banco de España](https://www.bde.es/webbe/es/estadisticas/temas/tipos-interes.html), Boletín Estadístico | Cuadro 19.7 (nuevas operaciones, TEDR: DN_1TI1T0010, DN_1TI2T0024 a DN_1TI2T0027) y cuadro 19.10 (saldos vivos, DN_1TI1T0060) | Descargado |
| Ganancias patrimoniales declaradas en el IRPF | [AEAT](https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpf/2024/home_parcial2e4edb04eb678058733ec5d815c2a9544ce2dea8.html), Estadística de los declarantes del IRPF 2024, bloque V | «Detalle de las operaciones de transmisión de activos por tipo de activo subyacente» (total, inmuebles, valores, resto) | Descargado |
| Periodo medio de posesión de viviendas transmitidas | [Colegio de Registradores, Anuario ERI 2024](https://www.registradores.org/documents/33383/148210/ERI%2BAnuario%2B2024.pdf), resumen ejecutivo, p. 7 | 17,7 años (2024) | Citado |
| Escala del ahorro del IRPF | [BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764), Ley 35/2006, arts. 66 y 76, todas sus versiones (API de legislación consolidada) | `data/raw/boe/lirpf_a66.xml`, `lirpf_a76.xml` | Descargado |

## Estructura

```
data/raw/         Datos tal como los publica la fuente, sin modificar
data/processed/   Tablas derivadas (Excel con fórmulas y tablas de cada gráfico)
graficos/         Gráficos del artículo (PNG)
scripts/          Scripts de descarga, cálculo y gráficos
```

## Cómo reproducirlo

Requisitos: Python 3.10 o superior y `openpyxl`.

```bash
python scripts/descargar_ipc.py        # descarga el IPC desde la API del INE
python scripts/construir_hoja_ipc.py   # genera data/processed/IPC_Espana_base_INE.xlsx
python scripts/graficos.py             # genera graficos/ y sus tablas en data/processed/
```

Requiere además `matplotlib` y `numpy` para los gráficos.

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
| `05_inflacion_en_plusvalias_inmuebles_2024.png` | Parte de las plusvalías inmobiliarias gravadas en 2024 que solo compensa la inflación, según años de tenencia | `grafico5_inflacion_plusvalias_inmuebles_2024.csv` |

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

### Escala del ahorro y gráfico 4

Umbrales de la escala del ahorro según las versiones de los arts. 66 y 76 LIRPF publicadas por el BOE, actualizados con el IPC desde la media del año en que entraron en vigor:

| Umbral legal | Vigente desde | Norma | Umbral actualizado |
| --- | --- | --- | --- |
| 6.000 € | 2010 | Ley 26/2009 | 8.505 € |
| 50.000 € | 2015 | Ley 26/2014 | 66.539 € |
| 200.000 € | 2021 | Ley 11/2020 | 248.620 € |
| 300.000 € | 2023 | Ley 31/2022 | 332.323 € |

Los importes actualizados se recalculan con cada nueva descarga del IPC.

### Supuestos del gráfico 5

- Base: operaciones con inmuebles con ganancia y sin beneficio fiscal (sin exenciones ni reducciones) del IRPF 2024: valor de adquisición 27.400 M€ y ganancia 13.178 M€ (AEAT).
- Componente de inflación = valor de adquisición × (IPC medio de 2024 / IPC del mes medio de compra − 1). El mes medio de compra es mediados de 2024 menos los años de tenencia.
- Tenencia central: 17,7 años, periodo medio de posesión de las viviendas transmitidas en 2024 según el Colegio de Registradores. Como la estadística de la AEAT incluye inmuebles que no son vivienda, se muestran también 10 y 15 años.
- El 67 % de las ventas de 2024 tenían más de 10 años de tenencia (Registradores). Usar la media en vez de la distribución completa da, si acaso, una estimación conservadora.
- IRPF atribuible: componente de inflación × 21 % (rango 19-23 %, los tramos en que se integra la mayoría de estas ganancias).
- No se estiman valores (acciones y fondos) por falta de datos públicos sobre su periodo de tenencia. Tampoco se ajustan las operaciones con pérdidas, cuyas pérdidas reales también serían mayores.

### Verificación de la AEAT

La suma de los 115 importes del fichero `aeat_irpf2024_transmisiones_por_activo.csv` (1.322.549.047.380 €) coincide con la de las tablas publicadas, y la suma de los resultados por tipo de activo coincide con el total publicado.

## Verificación del Banco de España

Los 285 meses (enero 2003 – septiembre 2026) de las seis series del fichero `bde_tipos_depositos_hogares_mensual.csv` se comprobaron sumando cada columna frente al CSV oficial del Banco de España (`be1907.csv` y `be1910.csv`): coinciden las seis sumas.

## Notas de metodología

- **Cambio de base.** Desde enero de 2026 el INE publica el IPC en base 2025. Es un cambio de escala: las tasas de variación no cambian respecto a bases anteriores.
- **Periodo.** El índice exacto empieza en enero de 2002. Para 1961–2001 el INE solo ofrece variaciones redondeadas a un decimal, que se incluyen como contexto y no se usan en los cálculos.
- **Comparaciones.** Para un año completo se usa el índice medio anual; para una fecha concreta, el índice del mes.
- **Último dato.** Septiembre de 2026 (definitivo). Octubre de 2026 solo tiene dato adelantado y no se incluye.

Última actualización de datos: 9 de noviembre de 2026.
