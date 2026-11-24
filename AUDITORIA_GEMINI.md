# Encargo de auditoría independiente (solo lectura) — segunda ronda

Auditoría del repositorio de un artículo divulgativo sobre cómo el IRPF grava como ganancia la parte de las plusvalías y los intereses que solo es inflación. Se publicará en plena semana electoral (elecciones generales del 29 de noviembre de 2026): cualquier error se usará para desacreditarlo entero. El objetivo es que cada cifra sea correcta, reproducible e imparcial.

**No modifiques ningún archivo del repositorio. Entrega solo un informe.** Si necesitas ejecutar algo, hazlo en una copia temporal fuera del repositorio.

La primera ronda (gráficos 1 a 5) ya se auditó. Céntrate en lo nuevo (gráficos 6 a 12 y la calculadora) y repasa solo por encima lo anterior.

## 1. Reproducibilidad

En una copia temporal, ejecuta en este orden y compara las salidas con `data/processed/` y `graficos/`:

```
python scripts/graficos.py
python scripts/vender_con_perdidas.py   # gráfico 6
python scripts/reinversion.py           # gráfico 7
python scripts/ciudades.py              # gráfico 8 (requiere xlrd)
python scripts/acciones.py              # gráfico 9
python scripts/letras.py                # gráfico 10
python scripts/intereses_agregado.py    # gráfico 11
python scripts/quien_paga.py            # gráfico 12
```

## 2. Datos frente a la fuente oficial

Para cada archivo de `data/raw/`, vuelve a descargar la fuente (o una muestra) y compara:

- **INE, Índice de Precios de Vivienda:** `data/raw/ine_ipv/` frente a las tablas 80270 y 80271 (base y último trimestre).
- **INE, compraventas de viviendas:** `data/raw/ine_etdp/` frente a la serie ETDP1826 (totales anuales de 2007 y 2008).
- **Ministerio de Vivienda, valor tasado por municipio:** `data/raw/mivau/valor_tasado_municipios_35103500.xls`. Comprueba que se usa la columna «Total» (no «hasta 5 años») en todos los trimestres, para Madrid, Barcelona, Sevilla y Valencia en 2007, 2019 y 2026 T2.
- **Álava:** coeficientes 1,489 (2007) y 1,430 (2008) del Decreto Foral 41/2025 (BOTHA n.º 146, 26-12-2025).
- **Banco de España:** `be2225` (IBEX 35 a fin de mes), `ti_1_4` (tipo marginal de las subastas de Letras a 12 meses), `be2203` (Letras de hogares e ISFLSH) y `be1910` (tipo de los depósitos a plazo de hogares, saldos).
- **AEAT:** `data/raw/aeat_irpf_2019_2024_intereses_y_cuota_ahorro.csv` y `data/raw/aeat_irpf2024_intereses_por_tramos_renta.csv` frente a las tablas de la Estadística de los declarantes del IRPF (cada fila lleva su URL). Comprueba que son totales nacionales y no de una comunidad.
- **BOE:** arts. 33.4.b, 35, 38.1 y DT 18ª de la Ley 35/2006 y art. 41 del RD 439/2007 en `data/raw/boe/`.

## 3. Cálculos

- **Gráfico 6:** recalcula a mano España y dos comunidades para compras de 2007 (variación nominal, inflación, variación real) y el ejemplo de 200.000 € (IRPF de 14.336 € y pérdida real de 27.055 €).
- **Gráfico 7:** recalcula la exención proporcional (art. 41.1 RIRPF) en los casos de 150.000 €, 200.000 € y 150.000 € con 60.000 € de préstamo pendiente.
- **Gráfico 8:** recalcula Madrid 2007 (307.594 €, 433.472 €, 27.832 €) y Madrid 2019 (260.458 €, 38.673 €, 36 %), y otras dos casillas.
- **Gráfico 9:** recalcula 2007 (+31 % nominal, −13 % real, 3.091 € de IRPF) y 1999. Revisa el encadenamiento del IPC anterior a 2002.
- **Gráfico 10:** recalcula tres subastas y el recuento (23 con pérdida real antes de impuestos, 8 convertidas en pérdida por el IRPF, 41 en total).
- **Gráfico 11:** comprueba 11.591 millones de intereses (2021-2024) y 2.202 millones al 19 %.
- **Gráfico 12:** comprueba 6.794.229 declaraciones, 3.719.116 (55 %) de rentas de 30.000 € o menos y 184 millones de IRPF en el tramo de 12.000 a 30.000 €.
- **Calculadora** (`calculadora/index.html`): prueba tres casos y compáralos con un cálculo propio.

## 4. Metodología y sesgo

Valora si los supuestos del README son razonables y están bien explicados, y señala cualquiera que exagere o infravalore el resultado. En especial:

- usar valor de tasación medio por ciudad (gráfico 8) y precios medios a calidad constante (gráfico 6) para hablar de «un piso»;
- aportaciones mensuales a lo largo del año en el IBEX y uso del índice sin dividendos;
- tipo marginal en lugar de tipo medio en las Letras;
- IRPF al 19 % como cota inferior y comparación con el tipo medio de los depósitos a plazo para afirmar que «de media» los intereses no ganaron a la inflación;
- declaraciones frente a personas y efecto del mínimo personal en los tramos bajos (gráfico 12);
- exclusión de exenciones, gastos y compensación de pérdidas.

Comprueba también la imparcialidad política: que ningún texto atribuya el problema a un partido concreto ni pida el voto, y que se diga que los coeficientes se suprimieron con la Ley 26/2014 y que las reformas de 2020, 2022 y 2024 subieron tipos sin corregir la base.

## 5. Afirmaciones

Comprueba que cada título, subtítulo y pie de los gráficos y cada cifra del README se sostienen exactamente con los datos. En particular, estas, que irán en el artículo:

- «En 13 de los 17 territorios de régimen común, la vivienda media comprada en 2007 pierde en términos reales.»
- «Madrid: comprado en 2007 por 307.594 € y vendido por 433.472 €, paga 27.832 € de IRPF perdiendo poder adquisitivo.»
- «En 5 de 30 años de compra del IBEX el IRPF supera toda la ganancia real; en 8, más de la mitad; nunca baja del 23 %.»
- «En 31 de 41 subastas de Letras el ahorrador perdió poder adquisitivo tras pagar IRPF.»
- «Los hogares pasaron de 17 millones a 24.428 millones de euros en Letras (dic. 2021 – dic. 2023).»
- «De 2021 a 2024, al menos 2.202 millones de IRPF por intereses que no ganaron a la inflación.»
- «55 de cada 100 declaraciones con intereses son de rentas de 30.000 € o menos.»
- «Una pensionista con 20.000 € en un depósito en 2024 cobra 418 €, paga 79 € y la inflación se come 554 €: pierde 215 €.»
- «Entre el 48 % y el 87 % de las plusvalías inmobiliarias declaradas en 2024 sería inflación.»

## Formato del informe

1. Una tabla de hallazgos con:
   - gravedad (crítico / importante / menor);
   - archivo y línea;
   - qué falla;
   - cómo reproducirlo;
   - qué corrección propones.
2. Una lista de las cifras verificadas sin incidencias.
3. Un veredicto: ¿se puede publicar tal cual?
