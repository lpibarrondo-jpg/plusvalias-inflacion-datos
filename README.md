# Plusvalías nominales e inflación: datos y cálculos

Datos, scripts y metodología del artículo sobre cómo el IRPF grava como ganancia la parte del valor de un bien que solo es inflación.

El objetivo es que cualquier persona pueda comprobar cada cifra del artículo partiendo de fuentes oficiales.

## Fuentes

| Dato | Fuente | Serie / referencia | Estado |
| --- | --- | --- | --- |
| Índice de Precios de Consumo (IPC) | [INE](https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736176802&idp=1254735976607) | IPC290751, «Nacional. Índice general. Índice», base 2025 | Descargado |
| Variación anual del IPC (verificación) | INE | IPC290750 | Descargado |
| Variación mensual del IPC 1961–2001 (contexto) | INE | IPC290752 | Descargado |
| Tipos de interés de depósitos de hogares | Banco de España | Pendiente | Pendiente |
| Ganancias patrimoniales declaradas en el IRPF | Agencia Tributaria, Estadística de declarantes del IRPF | Pendiente | Pendiente |
| Escala del ahorro del IRPF | BOE, Ley 35/2006, art. 66 y 76 | Pendiente | Pendiente |

## Estructura

```
data/raw/         Datos tal como los publica la fuente, sin modificar
data/processed/   Tablas derivadas (Excel con fórmulas visibles)
scripts/          Scripts de descarga y cálculo
```

## Cómo reproducirlo

Requisitos: Python 3.10 o superior y `openpyxl`.

```bash
python scripts/descargar_ipc.py        # descarga el IPC desde la API del INE
python scripts/construir_hoja_ipc.py   # genera data/processed/IPC_Espana_base_INE.xlsx
```

Abre el Excel en Excel o LibreOffice para que se calculen las fórmulas. En la hoja, el texto azul es dato de la fuente y el negro es fórmula.

## Verificación

- La suma de los 297 índices mensuales (enero 2002 – septiembre 2026) es 23.424,447, idéntica a la que devuelve la API del INE.
- Las 285 tasas interanuales recalculadas a partir del índice coinciden con las publicadas por el INE (serie IPC290750), con una tolerancia de 0,1 puntos por el redondeo de la publicación.

## Notas de metodología

- **Cambio de base.** Desde enero de 2026 el INE publica el IPC en base 2025. Es un cambio de escala: las tasas de variación no cambian respecto a bases anteriores.
- **Periodo.** El índice exacto empieza en enero de 2002. Para 1961–2001 el INE solo ofrece variaciones redondeadas a un decimal, que se incluyen como contexto y no se usan en los cálculos.
- **Comparaciones.** Para un año completo se usa el índice medio anual; para una fecha concreta, el índice del mes.
- **Último dato.** Septiembre de 2026 (definitivo). Octubre de 2026 solo tiene dato adelantado y no se incluye.

Última actualización de datos: 9 de noviembre de 2026.
