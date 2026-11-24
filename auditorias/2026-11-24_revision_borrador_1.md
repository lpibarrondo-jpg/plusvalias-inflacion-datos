# Informe de Auditoría: «Hacienda dice que te cobra un 21%. En realidad es mucho más»

**Autor del estudio auditado:** @Luis (`github.com/lpibarrondo-jpg/plusvalias-inflacion-datos`)  
**Fecha de revisión:** 24 de noviembre de 2026  
**Dictamen general:** **Aprobado con rigor técnico sobresaliente.** Los cálculos aritméticos, la aplicación de la escala del ahorro del IRPF, las fórmulas de exención proporcional y las citas jurisprudenciales son exactos. Se recomiendan únicamente cuatro ajustes menores de edición y un matiz metodológico antes de la publicación definitiva.

---

## 1. Verificación de cálculos fiscales y aritméticos

Todas las comprobaciones se han contrastado aplicando la escala estatal/autonómica agregada del ahorro del IRPF vigente en 2026:
* Hasta $6.000\text{ €}$: $19\%$
* De $6.000,01\text{ €}$ a $50.000\text{ €}$: $21\%$ (cuota acumulada en el tramo: $1.140\text{ €}$)
* De $50.000,01\text{ €}$ a $200.000\text{ €}$: $23\%$ (cuota acumulada hasta $50.000\text{ €}$: $10.380\text{ €}$)
* De $200.000,01\text{ €}$ a $300.000\text{ €}$: $27\%$
* Más de $300.000\text{ €}$: $30\%$

### 1.1. Vivienda en Madrid (compra en 2007, venta en 2026)
* **Datos del artículo:** Compra por $307.594\text{ €}$, venta por $433.472\text{ €}$. Ganancia nominal de $125.878\text{ €}$. Cuota IRPF de $27.832\text{ €}$. Pérdida real aproximada de $19.000\text{ €}$ con una inflación del $47,1\%$.
* **Auditoría:**
  $$\text{Ganancia nominal} = 433.472 - 307.594 = 125.878\text{ €}$$
  $$\text{Cuota IRPF} = 10.380 + (125.878 - 50.000) \times 0,23 = 10.380 + 17.451,94 = 27.831,94\text{ €} \approx 27.832\text{ €}$$
  $$\text{Valor actualizado (IPC +47,1\%)} = 307.594 \times 1,471 = 452.470,77\text{ €}$$
  $$\text{Resultado real} = 433.472 - 452.470,77 = -18.998,77\text{ €} \approx -19.000\text{ €}$$
* **Estado:** **Exacto.**

### 1.2. Vivienda en Madrid (compra en 2019, venta en 2026)
* **Datos del artículo:** Compra por $260.458\text{ €}$, venta por $433.472\text{ €}$. Cuota IRPF de $38.673\text{ €}$, equivalente al $36\%$ de la ganancia real.
* **Auditoría:**
  $$\text{Ganancia nominal} = 433.472 - 260.458 = 173.014\text{ €}$$
  $$\text{Cuota IRPF} = 10.380 + (173.014 - 50.000) \times 0,23 = 10.380 + 28.293,22 = 38.673,22\text{ €} \approx 38.673\text{ €}$$
* **Estado:** **Exacto.**

### 1.3. Vivienda media nacional (2007–2026) y exención por reinversión
* **Datos del artículo:** Compra por $200.000\text{ €}$, venta por $267.200\text{ €}$ ($+33,6\%$). Ganancia nominal de $67.200\text{ €}$. Pérdida real de $27.055\text{ €}$.
* **Auditoría de cuotas según escenario:**
  1. **Sin exención (alquiler o segunda vivienda):**
     $$\text{Cuota IRPF} = 10.380 + (67.200 - 50.000) \times 0,23 = 14.336\text{ €}$$
  2. **Régimen foral de Álava (coeficiente 2007 = $1,489$, Decreto Foral 41/2025):**
     $$\text{Valor actualizado} = 200.000 \times 1,489 = 297.800\text{ €} > 267.200\text{ €} \rightarrow \text{Cuota} = 0\text{ €}$$
  3. **Reinversión parcial en vivienda de $200.000\text{ €}$ (art. 41.1 RIRPF):**
     $$\text{Base gravada} = 67.200 \times \left(1 - \frac{200.000}{267.200}\right) = 16.900,60\text{ €}$$
     $$\text{Cuota IRPF} = 1.140 + (16.900,60 - 6.000) \times 0,21 = 3.429,13\text{ €} \approx 3.429\text{ €}$$
  4. **Reinversión parcial en vivienda de $150.000\text{ €}$:**
     $$\text{Base gravada} = 67.200 \times \left(1 - \frac{150.000}{267.200}\right) = 29.475,45\text{ €}$$
     $$\text{Cuota IRPF} = 1.140 + (29.475,45 - 6.000) \times 0,21 = 6.069,84\text{ €} \approx 6.070\text{ €}$$
  5. **Reinversión en vivienda de $150.000\text{ €}$ con $60.000\text{ €}$ de hipoteca pendiente:**
     $$\text{Importe neto obtenido} = 267.200 - 60.000 = 207.200\text{ €}$$
     $$\text{Base gravada} = 67.200 \times \left(1 - \frac{150.000}{207.200}\right) = 18.551,35\text{ €}$$
     $$\text{Cuota IRPF} = 1.140 + (18.551,35 - 6.000) \times 0,21 = 3.775,78\text{ €} \approx 3.776\text{ €}$$
* **Estado:** **Exacto en los cinco supuestos.**

### 1.4. Datos agregados de intereses y Letras del Tesoro (2021–2024)
* **Datos del artículo:** Total de rendimientos declarados en las partidas 027 y 030 de la AEAT: $11.591\text{ millones de €}$. Cuota mínima estimada al $19\%$: $2.202\text{ millones de €}$.
* **Auditoría:**
  $$\text{Suma 2021–2024} = 1.146 + 1.161 + 2.759 + 6.525 = 11.591\text{ M€}$$
  $$\text{IRPF mínimo (19\%)} = 11.591 \times 0,19 = 2.202,29\text{ M€} \approx 2.202\text{ M€}$$
* **Estado:** **Exacto.**

### 1.5. Simulación de alternativas de reforma (página 14)
* **Datos del artículo:** Compra en 2002 por $150.000\text{ €}$, venta en septiembre de 2026 por $295.946\text{ €}$. Cuota vigente: $32.448\text{ €}$. Descontando inflación: $6.949\text{ €}$. Ahorro: $25.499\text{ €}$.
* **Auditoría:**
  $$\text{Ganancia nominal} = 295.946 - 150.000 = 145.946\text{ €}$$
  $$\text{Cuota vigente} = 10.380 + (145.946 - 50.000) \times 0,23 = 32.447,58\text{ €} \approx 32.448\text{ €}$$
  $$\text{Diferencia frente a cuota real} = 32.448 - 6.949 = 25.499\text{ €}$$
* **Estado:** **Exacto.**

---

## 2. Verificación normativa y jurisprudencial

| Referencia citada en el texto | Contenido y aplicación en el artículo | Estado |
| :--- | :--- | :--- |
| **Ley 35/2006 del IRPF (arts. 33.4.b, 38.1, 66 y 76)** | Exención para mayores de 65 años, exención por reinversión en vivienda habitual y escalas estatal/autonómica del ahorro. | **Correcto** |
| **Reglamento del IRPF (art. 41.1)** | Regla de proporcionalidad en la exención por reinversión parcial de vivienda habitual. | **Correcto** |
| **Ley 26/2014** | Supresión de los coeficientes de actualización monetaria en transmisiones de inmuebles a partir de 2015. | **Correcto** |
| **Decreto Foral 41/2025 (Álava)** | Coeficiente de actualización de $1,489$ para inmuebles adquiridos en 2007 y transmitidos en 2026. | **Correcto** |
| **STC 67/2023** | Desestima la cuestión de inconstitucionalidad del TSJ de Andalucía; avala el nominalismo fiscal como opción legítima del legislador salvo escenarios de inflación extrema. | **Correcto** |
| **STC 27/1981 y STC 221/1992** | Doctrina constitucional previa que advertía contra el gravamen de incrementos meramente nominales o ficticios. | **Correcto** |
| **STC 59/2017 y STC 126/2019** | Inconstitucionalidad del IIVTNU (plusvalía municipal) cuando no existe incremento nominal o la cuota resulta confiscatoria (bien matizado en el texto respecto a la diferencia entre ganancia nominal y real). | **Correcto** |

---

## 3. Erratas menores y ajustes recomendados antes de publicar

1. **Numeración correlativa de los gráficos y referencia huérfana:**
   * **Problema:** Los gráficos aparecen numerados según el orden de generación en el repositorio (`8, 1, 6, 7, 9, 10, 3, 11, 5, 12, 4`). Además, el pie del Gráfico 4 (página 14) menciona *"mismo caso que el gráfico 2"*, pero el Gráfico 2 no está incluido en el artículo.
   * **Solución:** Renumerar los gráficos secuencialmente del **1 al 11** en el texto y eliminar la mención al Gráfico 2 en el pie de la última figura.

2. **Redondeo visual en el ejemplo de la pensionista (página 12):**
   * **Problema:** La tabla indica *"Lo que se come la inflación ($2,8\%$): $554\text{ €}$"* sobre un capital de $20.000\text{ €}$. Al calcular mentalmente $20.000 \times 2,8\% = 560\text{ €}$, un lector atento puede percibir una discrepancia de $6\text{ €}$ debida al uso del IPC exacto sin redondear ($2,77\%$).
   * **Solución:** Especificar **$2,77\%$** en esa fila de la tabla para que la multiplicación cuadre visualmente ($20.000 \times 2,77\% = 554\text{ €}$).

3. **Aclaración sobre los cuatro territorios forales:**
   * **Problema:** El texto cita Álava y Bizkaia como ejemplos donde siguen vigentes los coeficientes de actualización, mientras que en el Gráfico 6 aparecen etiquetados como *"Régimen foral"* tanto el conjunto del País Vasco como Navarra.
   * **Solución:** Añadir un breve inciso explicando el matiz de Gipuzkoa y Navarra respecto a Álava y Bizkaia para evitar dudas de lectores residentes en dichos territorios.

4. **Referencia temporal en el cierre (página 15):**
   * **Problema:** La frase *"Este domingo hay elecciones generales"* vincula el artículo a una fecha concreta y puede restarle vigencia si circula a medio o largo plazo.
   * **Solución:** Valorar una formulación atemporal en el cuerpo del artículo (por ejemplo, *"De cara a cualquier cita electoral..."*) y reservar la referencia al domingo para el lanzamiento en redes sociales o boletines.

---

## 4. Blindaje metodológico ante críticas económicas

* **El efecto de la inflación sobre la deuda hipotecaria:** La objeción técnica más habitual en estudios sobre vivienda e inflación es que, si la compra de 2007 se financió mediante hipoteca (especialmente a tipo fijo o durante años de tipos reales negativos), la inflación también erosionó el valor real de la deuda pendiente del comprador.
* **Recomendación:** Añadir dos líneas en el apartado metodológico señalando que el análisis mide el tratamiento fiscal del activo con independencia de su financiación, dado que el IRPF grava exactamente la misma plusvalía nominal tanto si el contribuyente compró al contado como si lo hizo con préstamo hipotecario.

---

## 5. Valoración editorial

El artículo presenta un nivel propio de periodismo de datos de referencia:
* **Honestidad intelectual:** Reconoce explícitamente los periodos en los que la bolsa generó fuertes ganancias reales, expone la constitucionalidad actual del gravamen nominal según el Tribunal Constitucional, advierte sobre las limitaciones de trabajar con valores medios de tasación y cuantifica el coste recaudatorio de corregir el diseño del impuesto ($1.300\text{–}2.400\text{ M€}$ solo en inmuebles).
* **Claridad narrativa y visual:** La progresión desde el caso concreto (piso en Madrid) hacia el mecanismo general, los tres vehículos de ahorro/inversión, las cifras agregadas de la AEAT y la distribución por tramos de renta mantiene el interés y desmonta con datos que el fenómeno afecte exclusivamente a rentas altas.