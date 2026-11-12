"""Gráfico 6: vivienda comprada en 2007 (o 2008) y vendida en 2026: ganancia en euros, pérdida en poder adquisitivo.

Compara, por comunidad autónoma, la variación nominal del Índice de Precios de Vivienda (INE, IPV) entre la
media anual del año de compra y el último trimestre publicado con la inflación (IPC) del mismo periodo.
Calcula además un ejemplo de IRPF en territorio común frente a Álava (que actualiza el valor de adquisición).

Uso: python scripts/vender_con_perdidas.py   (requiere haber ejecutado antes scripts/graficos.py una vez)
"""
import csv, json, collections, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graficos import (plt, RAIZ, SALIDA, REPO, AZUL, NARANJA, RAMPA, TINTA, TINTA2, MUTED, GRID, EJE,
                      IDX, es, cuota_ahorro, pie)

RAW = RAIZ / "data" / "raw"
IPV_A = json.load(open(RAW / "ine_ipv" / "ipv_80271_medias_anuales.json", encoding="utf-8"))
IPV_T = json.load(open(RAW / "ine_ipv" / "ipv_80270_trimestral.json", encoding="utf-8"))
ETDP = json.load(open(RAW / "ine_etdp" / "ETDP1826_compraventas_viviendas_nacional_mensual.json", encoding="utf-8"))

FORALES = {"País Vasco": "actualiza el valor de compra con coeficientes", "Navarra, Comunidad Foral de": "régimen foral propio"}
# Álava, Decreto Foral 41/2025 (BOTHA n.º 146, 26-12-2025), coeficientes IRPF para transmisiones de 2026
COEF_ALAVA = {2007: 1.489, 2008: 1.430}
TRIM_MESES = {"T1": (1, 2, 3), "T2": (4, 5, 6), "T3": (7, 8, 9), "T4": (10, 11, 12)}
NOMBRES = {"Navarra, Comunidad Foral de": "Navarra", "Asturias, Principado de": "Asturias", "Rioja, La": "La Rioja",
           "Madrid, Comunidad de": "Madrid", "Murcia, Región de": "Murcia", "Balears, Illes": "Illes Balears",
           "Castilla - La Mancha": "Castilla-La Mancha", "Nacional": "ESPAÑA"}

def ipc_anual(y):
    v = [IDX[f"{y}-{m:02d}"] for m in range(1, 13)]
    return sum(v) / 12

def series():
    gen_t = {s["Nombre"].split(".")[0]: s["Data"] for s in IPV_T if s["Nombre"].strip().endswith("General. Índice.")}
    gen_a = {s["Nombre"].split(".")[0]: {d["Anyo"]: d["Valor"] for d in s["Data"]}
             for s in IPV_A if "Media anual. General" in s["Nombre"]}
    ult = gen_t["Nacional"][0]
    assert all(d[0]["Anyo"] == ult["Anyo"] and d[0]["T3_Periodo"] == ult["T3_Periodo"] for d in gen_t.values())
    ipc_t = sum(IDX[f"{ult['Anyo']}-{m:02d}"] for m in TRIM_MESES[ult["T3_Periodo"]]) / 3
    return gen_t, gen_a, ult, ipc_t

def tabla(anio_compra):
    gen_t, gen_a, ult, ipc_t = series()
    infl = ipc_t / ipc_anual(anio_compra) - 1
    filas = []
    for reg, data in gen_t.items():
        nom = data[0]["Valor"] / gen_a[reg][anio_compra] - 1
        real = (1 + nom) / (1 + infl) - 1
        if reg in FORALES:
            cat = "régimen foral"
        elif nom <= 0:
            cat = "pérdida nominal: no tributa"
        elif real < 0:
            cat = "ganancia nominal y pérdida real: tributa"
        else:
            cat = "ganancia real"
        filas.append(dict(territorio=reg, anio_compra=anio_compra, periodo_venta=f"{ult['Anyo']}{ult['T3_Periodo']}",
                          var_nominal=round(nom, 4), inflacion=round(infl, 4), var_real=round(real, 4), categoria=cat))
    with open(RAIZ / "data" / "processed" / f"grafico6_compra_{anio_compra}_venta_hoy.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas

def ejemplo(anio_compra, precio=200_000, gastos_compra=0.10, gastos_venta=0.03):
    """Vivienda media nacional comprada en anio_compra por `precio` y vendida al precio que marca el IPV."""
    gen_t, gen_a, ult, ipc_t = series()
    venta = precio * gen_t["Nacional"][0]["Valor"] / gen_a["Nacional"][anio_compra]
    infl = ipc_t / ipc_anual(anio_compra)
    out = {}
    for etiqueta, gc, gv in (("sin gastos", 0, 0), ("con gastos", gastos_compra, gastos_venta)):
        adq = precio * (1 + gc); trans = venta * (1 - gv)
        g_nom = trans - adq
        out[etiqueta] = dict(precio_compra=precio, valor_adquisicion=round(adq), precio_venta=round(venta),
                             valor_transmision=round(trans), ganancia_nominal=round(g_nom),
                             resultado_real=round(trans - adq * infl), irpf_comun=round(cuota_ahorro(max(g_nom, 0))),
                             alava_valor_actualizado=round(adq * COEF_ALAVA[anio_compra]),
                             alava_resultado=round(trans - adq * COEF_ALAVA[anio_compra]), irpf_alava=0)
        assert out[etiqueta]["alava_resultado"] < 0  # en Álava es pérdida: no hay cuota
    with open(RAIZ / "data" / "processed" / f"grafico6_ejemplo_compra_{anio_compra}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["variante"] + list(out["sin gastos"].keys())); w.writeheader()
        for k, v in out.items(): w.writerow(dict(variante=k, **v))
    return out

def compraventas_por_anio():
    t = collections.Counter(); n = collections.Counter()
    for d in ETDP["Data"]:
        t[d["Anyo"]] += d["Valor"]; n[d["Anyo"]] += 1
    return {y: int(v) for y, v in t.items() if n[y] == 12}

def grafico(filas, ej, ventas):
    filas = sorted(filas, key=lambda f: f["var_real"])
    nac = next(f for f in filas if f["territorio"] == "Nacional")
    fig, ax = plt.subplots(figsize=(12, 11.2), dpi=150)
    fig.subplots_adjust(left=0.19, right=0.78, top=0.745, bottom=0.14)
    y = list(range(len(filas)))[::-1]
    ax.axvline(0, color=TINTA2, lw=1.2, zorder=2)
    for yi, f in zip(y, filas):
        nom, real = f["var_nominal"] * 100, f["var_real"] * 100
        foral = f["categoria"] == "régimen foral"
        alerta = f["categoria"].startswith("ganancia nominal y pérdida real")
        if alerta:
            ax.axhspan(yi - 0.45, yi + 0.45, color="#fdeee7", zorder=0, lw=0)
        ax.plot([real, nom], [yi, yi], color=NARANJA if not foral else EJE, lw=4, solid_capstyle="butt", zorder=3, alpha=0.9)
        ax.scatter([nom], [yi], s=70, color=RAMPA[0] if not foral else EJE, zorder=4, edgecolor="white", lw=1)
        ax.scatter([real], [yi], s=70, color=RAMPA[3] if not foral else MUTED, zorder=4, edgecolor="white", lw=1)
        etq = "Paga IRPF y pierde" if alerta else ("Régimen foral" if foral else
              ("Ganancia real" if f["var_real"] > 0 else "Sin ganancia: no tributa"))
        ax.text(1.02, yi, etq, transform=ax.get_yaxis_transform(), va="center", ha="left", fontsize=10.5,
                color=NARANJA if alerta else MUTED, fontweight="bold" if alerta else "normal")
    ax.set_yticks(y, [NOMBRES.get(f["territorio"], f["territorio"]) for f in filas])
    for lab, f in zip(ax.get_yticklabels(), filas):
        if f["territorio"] == "Nacional": lab.set_fontweight("bold"); lab.set_color(TINTA)
    ax.tick_params(axis="y", length=0, labelsize=11.5, colors=TINTA2)
    ax.tick_params(axis="x", labelsize=10.5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{es(v)} %"))
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.set_ylim(-0.7, len(filas) - 0.3)
    n_alerta = sum(f["categoria"].startswith("ganancia nominal y pérdida real") and f["territorio"] != "Nacional" for f in filas)
    n_comun = sum(f["categoria"] != "régimen foral" and f["territorio"] != "Nacional" for f in filas)
    a = filas[0]["anio_compra"]; e = ej["sin gastos"]
    fig.text(0.04, 0.955, f"Compró su casa en {a} y la vende hoy: pierde poder adquisitivo y paga IRPF igual",
             fontsize=19.5, fontweight="bold", ha="left", va="top")
    sub = [f"Precio de la vivienda: media de {a} frente a {filas[0]['periodo_venta'][:4]} ({filas[0]['periodo_venta'][4:]}). Punto claro: variación en euros. "
           f"Punto oscuro: descontada la inflación ({es(nac['inflacion'] * 100, 1)} %).",
           f"La barra naranja es lo que se come la inflación. En {n_alerta} de los {n_comun} territorios de régimen común el precio sube en euros",
           "pero baja en términos reales, y aun así el IRPF grava la diferencia nominal como ganancia.",
           f"Ejemplo, España: casa de {es(e['precio_compra'])} € vendida hoy por {es(e['precio_venta'])} € → {es(e['irpf_comun'])} € de IRPF "
           f"con una pérdida real de {es(-e['resultado_real'])} €.",
           "La misma operación en Álava, que actualiza el valor de compra con la inflación, no paga nada."]
    fig.text(0.04, 0.905, "\n".join(sub), fontsize=11.5, color=TINTA2, ha="left", va="top", linespacing=1.5)
    pie(fig, "Fuente: INE, Índice de Precios de Vivienda (base 2015) e IPC; Decreto Foral 41/2025 de Álava (coeficientes 2026). Índices medios a calidad constante:\n"
             "cada vivienda concreta puede variar. IRPF: escala del ahorro 2026 de territorio común, sin gastos ni exenciones (reinversión en vivienda habitual, mayores de 65).\n"
             f"Compraventas de vivienda registradas en España: {es(ventas[2007])} en 2007 y {es(ventas[2008])} en 2008 (INE, ETDP). Datos y código: {REPO}")
    fig.savefig(SALIDA / f"06_compra_{a}_vende_hoy.png")
    plt.close(fig)

if __name__ == "__main__":
    ventas = compraventas_por_anio()
    for a in (2007, 2008):
        filas = tabla(a); ej = ejemplo(a)
        grafico(filas, ej, ventas)
        cats = collections.Counter(f["categoria"] for f in filas if f["territorio"] != "Nacional")
        print(a, dict(cats)); print("  ejemplo:", ej)
    print("compraventas 2007-2008:", ventas[2007], ventas[2008], ventas[2007] + ventas[2008])
