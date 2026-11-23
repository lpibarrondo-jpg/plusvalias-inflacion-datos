# Informe de auditoría independiente (solo lectura) — Segunda ronda

- **Proyecto auditado:** Base de datos, cálculos, gráficos y calculadora del artículo sobre IRPF, plusvalías nominales, intereses e inflación.
- **Repositorio de referencia:** `https://github.com/lpibarrondo-jpg/plusvalias-inflacion-datos` (commit `bf58ea4`).
- **Material revisado:** `paquete_auditoria.txt` (encargo, `README.md`, scripts de `scripts/`, tablas procesadas de `data/processed/`, extractos de `data/raw/` y lógica de `calculadora/plantilla.html`) y `graficos.pdf` (13 gráficos).
- **Fecha del informe:** 23 de noviembre de 2026.
- **Alcance:** Auditoría independiente de datos, cálculos, coherencia gráfica, supuestos metodológicos e imparcialidad periodística, centrada en los gráficos 6 a 12 y la calculadora (con repaso general de los gráficos 1 a 5).

---

## 1. Veredicto: ¿se puede publicar tal cual?

**Sí, con dos ajustes menores recomendados antes de publicar (y sin ningún error crítico de cálculo).**

La base numérica, las fórmulas fiscales (escala del ahorro de 2026, exención proporcional por reinversión, encadenamiento del IPC) y la documentación metodológica son sólidas y coherentes entre los scripts, los archivos CSV procesados y los gráficos finales. No se ha detectado ninguna afirmación partidista ni petición de voto.

Antes de la publicación en semana electoral, conviene aplicar dos correcciones puntuales para evitar flancos de crítica técnica:

1. **Matizar el titular del Gráfico 11**, añadiendo la referencia a «de media» o «en años en que el depósito medio perdió frente a la inflación», para que no parezca que el 100 % de los 11.591 millones de euros (que incluyen Letras del Tesoro de 2023 y 2024) perdieron poder adquisitivo.
2. **Actualizar la nota metodológica del `README.md`** sobre las variaciones del IPC de 1961–2001, eliminando la frase que afirma que «no se usan en los cálculos», ya que sí se utilizan en el Gráfico 9 (1995–2001), la sensibilidad del Gráfico 5 y la calculadora.

---

## 2. Tabla de hallazgos

| Gravedad | Archivo o gráfico | Qué falla | Cómo comprobarlo / reproducirlo | Corrección propuesta |
| :--- | :--- | :--- | :--- | :--- |
| **Importante** | `graficos.pdf` (Gráfico 11, p. 12) y afirmación del artículo | El titular afirma: *«Al menos 2.202 millones de IRPF por intereses **que no ganaron a la inflación** (2021-2024)»*. Esa cifra ($11.591\text{ M€} \times 19\text{ \%}$) incluye 720 M€ de Letras del Tesoro en 2024 y 124 M€ en 2023, pero el propio Gráfico 10 muestra que en 10 de las 41 subastas las Letras sí superaron a la inflación. Además, incluye intereses de rentas inferiores a 12.000 € donde el mínimo personal puede reducir o anular la cuota (como advierte el Gráfico 12). | Comparar `grafico11_intereses_irpf_inflacion.csv` (suma de partidas 027 y 030) con `grafico10_letras_12m.csv` (10 subastas con ganancia real tras impuestos) y `grafico12_intereses_por_tramo_renta_2024.csv` (tramos por debajo de 12.000 €). | Reformular el titular a: *«Al menos 2.202 millones de IRPF por intereses en años en que el depósito medio perdió frente a la inflación (2021-2024)»* (manteniendo el matiz «de media» que ya recoge correctamente el subtítulo). |
| **Importante** | `README.md` (sección *Notas de metodología*) | Afirma que las variaciones mensuales del IPC de 1961–2001 *«se incluyen como contexto y **no se usan en los cálculos**»*. En esta segunda ronda esa frase ha quedado desactualizada: sí se usan en el Gráfico 9 (compras de 1995–2001), en el análisis de sensibilidad del Gráfico 5 y en la calculadora. | Contrastar el penúltimo párrafo de `README.md` con las funciones `ipc_encadenado()` en `scripts/acciones.py`, `sensibilidad_tenencia()` en `scripts/graficos.py` y el bucle de encadenado en `scripts/construir_calculadora.py`. | Actualizar la nota del `README.md` para explicar que esas variaciones se usan de forma aproximada en el Gráfico 9 (1995–2001), la sensibilidad del Gráfico 5 y la calculadora. |
| **Menor** | `graficos.pdf` (Gráfico 12, p. 13) | El titular *«No es cosa de ricos: 55 de cada 100 declaraciones con intereses son de rentas de 30.000 € o menos»* es exacto en número de declaraciones, pero el gráfico no muestra que ese bloque concentra el **26,5 % del importe total** de intereses (1.540 M€ de 5.806 M€). Un lector crítico podría señalar el contraste entre número de declarantes y volumen de intereses. | Sumar `importe_eur` de los tramos hasta 30.000 € en `aeat_irpf2024_intereses_por_tramos_renta.csv`: $1.540.312.214 / 5.805.582.799 = 26,53\text{ \%}$. | Mantener el titular (es riguroso y fiel al dato), pero incluir expresamente el dato del 26,5 % del importe en el cuerpo del artículo para blindar el argumento. |
| **Menor** | `graficos.pdf` (Gráfico 11, p. 12) y `scripts/intereses_agregado.py` | En la anotación inferior del año **2023** figura `Depósito: 1,10 %`, cuando la media exacta de `plazo_pond_saldos` en 2023 es **1,1051 %** (que redondea a **1,11 %**). Se debe a un doble redondeo: `round(tipo, 3)` produce `1.105` y el formateo posterior a 2 decimales aplica el redondeo bancario de Python a `1,10`. | Promediar los 12 meses de 2023 de `plazo_pond_saldos` en `bde_tipos_depositos_hogares_mensual.csv` ($13,2612 / 12 = 1,1051$). | Formatear el tipo sin redondeo previo intermedio en `intereses_agregado.py` (impacto de 0,01 puntos porcentuales; no altera ninguna conclusión). |
| **Menor** | Afirmación del artículo (sección 5 del encargo) sobre el Gráfico 9 | La frase propuesta para el artículo dice: *«En 5 de 30 años de compra del IBEX el IRPF supera toda la ganancia real»*. En 2 de esos 5 años (2000 y 2007) no hay ganancia real, sino **pérdida real** (−2.237 € y −9.598 €). El subtítulo del Gráfico 9 sí es exacto (*«supera toda la ganancia real o se paga con pérdida real»*). | Revisar los años 1998, 1999, 2000, 2006 y 2007 en `grafico9_ibex_por_anio_compra.csv`. | Replicar en el texto del artículo la redacción exacta del subtítulo del gráfico: *«supera toda la ganancia real o se paga con pérdida real»*. |
| **Menor** | Afirmación del artículo (sección 5 del encargo) sobre el ejemplo de la pensionista | *«Una pensionista con 20.000 € en un depósito en 2024 cobra 418 €, paga 79 € y la inflación se come 554 €: pierde 215 €»*. Usa una aproximación lineal ($418 - 79 - 554 = -215\text{ €}$); con la fórmula exacta de Fisher usada en los gráficos 3 y 10, la pérdida real en euros de 2024 es de **209,5 €** (diferencia de ~5 €). | Calcular $20.000 \times 0,02091 = 418,2\text{ €}$; IRPF al 19 % $= 79,46\text{ €}$; IPC 2,77 % $= 554\text{ €}$; Fisher: $20.000 \times [(1 + 0,02091 \times 0,81) / 1,0277 - 1] = -209,5\text{ €}$. | Aceptable en divulgación porque el desglose cuadra a la vista ($418 - 79 - 554 = -215$), aunque conviene indicar que es una aproximación en euros corrientes. |

---

## 3. Cifras verificadas sin incidencias

Todas las cifras siguientes han sido recalculadas manualmente a partir de las tablas procesadas, los extractos de datos brutos y las fórmulas de los scripts, y coinciden con los valores mostrados en `graficos.pdf`:

### Gráfico 5 (repaso)
- **Porcentaje de inflación en plusvalías inmobiliarias de 2024:** rango verificado del **48,46 %** (10 años de tenencia) al **87,20 %** (17,7 años, media oficial de Registradores).

### Gráfico 6 — Compra en 2007/2008 y venta en 2026 T2
- **Variación real con inflación del 47,13 % (2007 a 2026 T2):**
  - **España:** $(1,336 / 1,4713) - 1 = -9,19\text{ \%}$.
  - **Comunidad de Madrid:** $(1,4083 / 1,4713) - 1 = -4,28\text{ \%}$.
  - **Cataluña:** $(1,1832 / 1,4713) - 1 = -19,58\text{ \%}$.
  - **Andalucía:** $(1,5061 / 1,4713) - 1 = +2,37\text{ \%}$.
- **Recuento territorial:** **13 de 17** territorios de régimen común en 2007 (y **12 de 17** en 2008) registran subida nominal y pérdida real.
- **Ejemplo nacional de 200.000 € (2007, sin gastos):** venta por **267.200 €**, ganancia nominal de **67.200 €**, IRPF de **14.336 €** ($6.000 \times 19\text{ \%} + 44.000 \times 21\text{ \%} + 17.200 \times 23\text{ \%}$), pérdida real de **27.055 €** (con coeficiente exacto $1,471275$) y cuota de **0 €** en Álava (valor actualizado de 297.800 €).

### Gráfico 7 — Exención por reinversión en vivienda habitual (art. 41.1 RIRPF)
- **Reinvierte 200.000 €:** fracción exenta **74,85 %**, base gravada **16.901 €**, IRPF **3.429 €**.
- **Reinvierte 150.000 €:** fracción exenta **56,14 %**, base gravada **29.475 €**, IRPF **6.070 €**.
- **Reinvierte 150.000 € con 60.000 € de hipoteca pendiente:** importe obtenido **207.200 €**, fracción exenta **72,39 %**, base gravada **18.551 €**, IRPF **3.776 €**.

### Gráfico 8 — Grandes ciudades (piso de 80 m², valor tasado MIVAU)
- **Madrid 2007:** media 2007 $= 3.844,925\text{ €/m}^2 \rightarrow$ compra **307.594 €**; venta 2026 T2 ($5.418,4\text{ €/m}^2$) $= $ **433.472 €**; ganancia nominal 125.878 €; IRPF **27.832 €**; pérdida real **−19.083 €**.
- **Madrid 2019:** media 2019 $= 3.255,725\text{ €/m}^2 \rightarrow$ compra **260.458 €**; venta **433.472 €**; IRPF **38.673 €**; ganancia real 106.571 €; IRPF sobre ganancia real **36,29 %** (36 % en el gráfico).
- **Barcelona 2019:** compra **271.940 €**, venta **368.144 €**, IRPF **21.007 €**, ganancia real 26.832 €, IRPF/ganancia real **78,29 %** (78 %).
- **Valencia 2007:** compra **175.910 €**, venta **237.824 €**, IRPF **13.120 €**, pérdida real **−20.988 €**.

### Gráfico 9 — IBEX 35 por año de compra (1995–2024)
- **Compra en 2007:** ganancia nominal 15.290 € (**+31 %**), pérdida real −9.598 € (**−19 %**), IRPF **3.091 €**.
- **Compra en 1999:** ganancia nominal 46.690 €, ganancia real 281 €, IRPF **9.685 €** (`>100 %` de la ganancia real).
- **Recuento:** **5** años con IRPF $\ge 100\text{ \%}$ de la ganancia real o con pérdida real (1998–2000, 2006–2007); **8** años por encima del 50 % (añadiendo 2001, 2005 y 2008); mínimo de la serie **23,08 %** (2024).
- **Encadenamiento del IPC anterior a 2002:** la fórmula inversa $I_{t-1} = I_t / (1 + v_t)$ está correctamente implementada en todos los scripts.

### Gráfico 10 — Letras del Tesoro a 12 meses
- **Subastas recalculadas a partir de `ti_1_4` y el IPC mensual:**
  - `2025-09-05`: tipo marginal 1,996 %, rendimiento **2,018 %**, inflación 12m **4,916 %**, real tras IRPF **−3,128 %**.
  - `2024-06-07`: tipo marginal 3,423 %, rendimiento **3,461 %**, inflación 12m **2,286 %**, real tras IRPF **+0,506 %**.
  - `2025-01-10`: tipo marginal 2,384 %, rendimiento **2,410 %**, inflación 12m **2,290 %**, real tras IRPF **−0,329 %**.
- **Recuento:** **41** subastas en total (**23** con pérdida real antes de impuestos, **8** convertidas en pérdida por el IRPF y **10** con ganancia real tras impuestos).
- **Tenencias de hogares e ISFLSH (`be2203`):** **16,6 M€** (redondeado a 17 M€) en diciembre de 2021 a **24.428 M€** en diciembre de 2023.

### Gráfico 11 — Intereses agregados (2021–2024)
- **Suma de partidas 027 y 030 (tomando 0 € en 2022 para la 030):** **11.591.168.917 €** (11.591 M€).
- **IRPF al 19 % (cota inferior):** **2.202.322.094 €** (2.202 M€).

### Gráfico 12 — Intereses por tramo de renta (2024, partida 027)
- **Total de declaraciones:** **6.794.229**.
- **Rentas de 30.000 € o menos:** **3.719.116** declaraciones (**54,74 %** $\rightarrow$ 55 %).
- **Tramo de 12.000 a 30.000 €:** **2.062.034** declaraciones, **967.730.303 €** (968 M€) de intereses y **183.868.758 €** (184 M€) de IRPF al 19 %.

### Calculadora (`calculadora/plantilla.html`)
- **Escenario 1 (ejemplo por defecto, compra junio 2015 por 150.000 € + 10.000 € de gastos; venta septiembre 2026 por 250.000 € − 7.500 € de gastos):** ganancia nominal 82.500 € $\rightarrow$ IRPF actual **17.855 €**; ganancia real 31.970 € $\rightarrow$ IRPF descontando inflación **6.594 €**.
- **Escenario 2 (compra 2007 con ganancia nominal y pérdida real):** rama condicional, aviso de pérdida real y cálculo de cuota verificados sin errores.
- **Escenario 3 (pérdida nominal):** cuota 0 € y cálculo de pérdida real verificados sin errores.

---

## 4. Valoración de metodología, supuestos e imparcialidad

- **Transparencia metodológica:** Los supuestos del `README.md` y los pies de los gráficos explican con claridad las limitaciones de usar valores medios de tasación (Gráfico 8) o índices a calidad constante (Gráfico 6), el uso del IBEX 35 sin dividendos con aportaciones mensuales (Gráfico 9), el tipo marginal frente al medio en Letras (Gráfico 10), la exclusión de exenciones/gastos y la distinción entre declaraciones y personas (Gráfico 12).
- **Cautela en rentas bajas (Gráfico 12):** Es muy acertado excluir los tramos por debajo de 12.000 € de la atribución de cuota del 19 % por el efecto del mínimo personal y familiar.
- **Imparcialidad política:** No se observa sesgo partidista ni petición de voto en ninguno de los archivos revisados (`README.md`, `calculadora/plantilla.html` y los 13 gráficos de `graficos.pdf`). Las referencias normativas citan las leyes correspondientes (Ley 26/2009, Ley 26/2014, Ley 11/2020, Ley 31/2022, Ley 7/2024) de forma descriptiva y neutral.

---

## 5. Limitaciones de esta auditoría

Para que quede constancia exacta de lo verificado y lo no verificado en este pase:

1. **Sin ejecución de código ni redescarga directa:** No se han ejecutado los scripts de Python ni se han vuelto a descargar los ficheros originales desde INE, Banco de España, AEAT, Ministerio de Vivienda, BOE o BOTHA.
2. **Extractos parciales en `paquete_auditoria.txt`:** El paquete no incluye los ficheros brutos completos de `ine_ipv/`, `ine_etdp/`, la serie mensual completa del IBEX 35 ni `ine_ipc_variacion_mensual.csv`. En esos puntos se ha auditado la coherencia interna, las fórmulas de los scripts y el cuadre entre tablas procesadas y gráficos, pero no la transcripción dato a dato desde la fuente primaria.
3. **Borrador del artículo no incluido:** No se ha revisado el texto completo del artículo periodístico, por lo que corresponde al editor confirmar que el texto final menciona expresamente que la Ley 26/2014 suprimió los coeficientes de actualización y que las reformas de 2020, 2022 y 2024 subieron tipos sin corregir la base.