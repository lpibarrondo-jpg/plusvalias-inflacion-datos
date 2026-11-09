# Encargo de auditoría independiente (solo lectura)

Auditoría del repositorio de un artículo divulgativo sobre cómo el IRPF grava como ganancia la parte de las plusvalías y los intereses que solo es inflación. El objetivo es que cada cifra publicada sea correcta, reproducible e imparcial.

**No modifiques ningún archivo del repositorio. Entrega solo un informe.** Si necesitas ejecutar algo, hazlo en una copia temporal fuera del repositorio.

## 1. Reproducibilidad

Ejecuta `scripts/descargar_ipc.py`, `scripts/construir_hoja_ipc.py` y `scripts/graficos.py` en una copia temporal y compara sus salidas con las de `data/processed/` y `graficos/`.

## 2. Datos frente a la fuente oficial

- **IPC:** vuelve a descargar la serie IPC290751 de la API del INE y compárala con `data/raw/ine_ipc_indice_general_mensual.csv`.
- **Banco de España:** compara `data/raw/bde_tipos_depositos_hogares_mensual.csv` con `be1907.csv` y `be1910.csv` de bde.es.
- **Agencia Tributaria:** compara `data/raw/aeat_irpf2024_transmisiones_por_activo.csv` con las tablas del bloque V de la Estadística de los declarantes del IRPF 2024.
- **BOE:** comprueba en `data/raw/boe/` los umbrales de la escala del ahorro (6.000 € desde 2010, 50.000 € desde 2015, 200.000 € desde 2021, 300.000 € desde 2023) y los tipos 19/21/23/27/30 %.
- **STC 67/2023:** comprueba que lo que el README dice de la sentencia coincide con `data/raw/sentencias/BOE-A-2023-16398.xml`.

## 3. Cálculos

Revisa:

- la cuota de la escala del ahorro;
- el tipo efectivo sobre la ganancia real (gráfico 2);
- la rentabilidad real de los depósitos antes y después del IRPF (gráfico 3);
- los umbrales actualizados y el caso de 2002 (gráfico 4);
- la estimación del componente de inflación en las plusvalías inmobiliarias de 2024 (gráfico 5): mes medio de compra, coeficiente y rango del 19-23 %.

Recalcula a mano al menos tres casillas del gráfico 2 y los totales del gráfico 5.

## 4. Metodología y sesgo

Valora si los supuestos documentados en el README son razonables y están bien explicados:

- índice medio anual frente al mensual;
- depósito a 1 año;
- IRPF al 19 % en depósitos;
- 17,7 años de tenencia de los Registradores aplicados a inmuebles que no son vivienda;
- valor de adquisición con gastos;
- exclusión de exenciones y de pérdidas.

Señala cualquier supuesto que exagere o infravalore el resultado.

## 5. Afirmaciones

Comprueba que cada título y subtítulo de los gráficos y cada cifra del README se sostienen exactamente con los datos. Por ejemplo: «559 €», «16 de 23 años», «381 € frente a 25.499 €», «87 %», «unos 2.400 millones».

## Formato del informe

1. Una tabla de hallazgos con:
   - gravedad (crítico / importante / menor);
   - archivo y línea;
   - qué falla;
   - cómo reproducirlo;
   - qué corrección propones.
2. Una lista de las cifras verificadas sin incidencias.
3. Un veredicto: ¿se puede publicar tal cual?
