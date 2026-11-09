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
| Ganancias patrimoniales declaradas en el IRPF | Agencia Tributaria, Estadística de declarantes del IRPF | Pendiente | Pendiente |
| Escala del ahorro del IRPF | BOE, Ley 35/2006, art. 66 y 76 | Pendiente | Pendiente |

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

## Verificación del Banco de España

Los 285 meses (enero 2003 – septiembre 2026) de las seis series del fichero `bde_tipos_depositos_hogares_mensual.csv` se comprobaron sumando cada columna frente al CSV oficial del Banco de España (`be1907.csv` y `be1910.csv`): coinciden las seis sumas.

## Notas de metodología

- **Cambio de base.** Desde enero de 2026 el INE publica el IPC en base 2025. Es un cambio de escala: las tasas de variación no cambian respecto a bases anteriores.
- **Periodo.** El índice exacto empieza en enero de 2002. Para 1961–2001 el INE solo ofrece variaciones redondeadas a un decimal, que se incluyen como contexto y no se usan en los cálculos.
- **Comparaciones.** Para un año completo se usa el índice medio anual; para una fecha concreta, el índice del mes.
- **Último dato.** Septiembre de 2026 (definitivo). Octubre de 2026 solo tiene dato adelantado y no se incluye.

Última actualización de datos: 9 de noviembre de 2026.
