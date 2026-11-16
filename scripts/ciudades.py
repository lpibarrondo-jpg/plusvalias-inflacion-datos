"""Gráfico 8: lo que se lleva el IRPF de la ganancia real al vender un piso de 80 m² en las grandes ciudades.

Precio de compra y de venta = valor tasado medio de la vivienda libre (€/m²) del municipio, Ministerio de
Vivienda y Agenda Urbana (tabla 35103500, municipios de más de 25.000 habitantes), por 80 m².
Compra = media de los cuatro trimestres del año; venta = último trimestre publicado.

Uso: python scripts/ciudades.py   (antes: descargar data/raw/mivau/valor_tasado_municipios_35103500.xls
y convertirlo con la función convertir() de este script)
"""
import csv, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graficos import (plt, RAIZ, SALIDA, REPO, RAMPA, NARANJA, TINTA, TINTA2, MUTED, SUP, IDX, es, cuota_ahorro, pie)
from matplotlib.patches import Patch

MIVAU = RAIZ / "data" / "raw" / "mivau"
M2 = 80
ANIOS = [2007, 2010, 2013, 2016, 2019, 2022]
CIUDADES = ["Madrid", "Barcelona", "Palma de Mallorca", "Málaga", "Valencia", "Coruña (A)", "Santander",
            "Sevilla", "Granada", "Vigo", "Palmas de Gran Canaria (Las)", "Alicante/Alacant", "Zaragoza",
            "Valladolid", "Murcia"]
NOMBRES = {"Palma de Mallorca": "Palma", "Coruña (A)": "A Coruña", "Palmas de Gran Canaria (Las)": "Las Palmas de G. C.",
           "Alicante/Alacant": "Alicante"}
GRIS = "#d9d8d2"

def convertir():
    """XLS del Ministerio (una hoja por trimestre) -> JSON {municipio: {AAAATn: €/m²}} con la columna Total."""
    import xlrd
    b = xlrd.open_workbook(MIVAU / "valor_tasado_municipios_35103500.xls")
    data = {}
    for name in b.sheet_names():
        m = re.match(r"T(\d)A(\d{4})", name.strip()); q = f"{m.group(2)}T{m.group(1)}"
        sh = b.sheet_by_name(name)
        hdr = next(r for r in range(sh.nrows) if "Municipio" in [str(x).strip() for x in sh.row_values(r)])
        cm = [str(x).strip() for x in sh.row_values(hdr)].index("Municipio")
        ct = next(i for i, c in enumerate(sh.row_values(hdr + 1)) if str(c).strip() == "Total")
        for r in range(hdr + 2, sh.nrows):
            row = sh.row_values(r); mun = str(row[cm]).strip(); v = row[ct]
            if mun and isinstance(v, float):
                data.setdefault(mun, {})[q] = v
    json.dump(data, open(MIVAU / "valor_tasado_municipios.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return data

def ipc_medio(meses):
    return sum(IDX[m] for m in meses) / len(meses)

def tabla():
    data = convertir()
    ult = max(data["Madrid"])
    a, t = int(ult[:4]), int(ult[-1])
    ipc_v = ipc_medio([f"{a}-{m:02d}" for m in range(3 * t - 2, 3 * t + 1)])
    filas = []
    for c in CIUDADES:
        s = data[c]
        for y in ANIOS:
            qs = [s[f"{y}T{i}"] for i in range(1, 5)]
            compra = sum(qs) / 4 * M2; venta = s[ult] * M2
            infl = ipc_v / ipc_medio([f"{y}-{m:02d}" for m in range(1, 13)])
            g = venta - compra; real = venta - compra * infl; cuota = cuota_ahorro(max(g, 0))
            if g <= 0: cat = "sin ganancia"
            elif real <= 0: cat = "paga con pérdida real"
            else: cat = "ganancia real"
            filas.append(dict(ciudad=c, anio_compra=y, venta=ult, eur_m2_compra=round(compra / M2, 1), eur_m2_venta=s[ult],
                              precio_compra=round(compra), precio_venta=round(venta), inflacion=round(infl - 1, 4),
                              ganancia_nominal=round(g), ganancia_real=round(real), irpf=round(cuota),
                              pct_ganancia_inflacion=round((compra * (infl - 1)) / g, 4) if g > 0 else None,
                              irpf_sobre_ganancia_real=round(cuota / real, 4) if real > 0 else None, categoria=cat))
    with open(RAIZ / "data" / "processed" / "grafico8_ciudades.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas, ult

CORTES = [(0.35, RAMPA[0], "Menos del 35 %"), (0.50, RAMPA[1], "35-50 %"), (1.00, RAMPA[2], "50-100 %"),
          (99, RAMPA[3], "100 % o más")]

def color(f):
    if f["categoria"] == "sin ganancia": return GRIS, TINTA2
    if f["categoria"] == "paga con pérdida real": return NARANJA, "#ffffff"
    v = f["irpf_sobre_ganancia_real"]
    for lim, c, _ in CORTES:
        if v < lim: return c, (TINTA if c == RAMPA[0] else "#ffffff")

def grafico(filas, ult):
    fig, ax = plt.subplots(figsize=(12, 11.5), dpi=150)
    fig.subplots_adjust(left=0.2, right=0.97, top=0.745, bottom=0.14)
    nf, nc = len(CIUDADES), len(ANIOS)
    for i, c in enumerate(CIUDADES):
        for j, y in enumerate(ANIOS):
            f = next(f for f in filas if f["ciudad"] == c and f["anio_compra"] == y)
            bg, fg = color(f)
            ax.add_patch(plt.Rectangle((j - 0.48, i - 0.46), 0.96, 0.92, color=bg, lw=0))
            if f["categoria"] == "sin ganancia": txt = "sin ganancia"
            elif f["categoria"] == "paga con pérdida real": txt = f"pierde y paga\n{es(f['irpf'])} €"
            elif f["irpf_sobre_ganancia_real"] >= 1: txt = "IRPF mayor que\nla ganancia real"
            else: txt = f"{es(f['irpf_sobre_ganancia_real'] * 100)} %"
            ax.text(j, i, txt, ha="center", va="center", fontsize=11 if "\n" not in txt else 9.5, color=fg,
                    fontweight="bold" if f["categoria"] == "paga con pérdida real" else "normal", linespacing=1.2)
    ax.set_xlim(-0.5, nc - 0.5); ax.set_ylim(nf - 0.5, -0.5)
    ax.set_xticks(range(nc), [str(y) for y in ANIOS]); ax.xaxis.tick_top()
    ax.set_xlabel("Año de compra", fontsize=11.5, labelpad=10); ax.xaxis.set_label_position("top")
    ax.set_yticks(range(nf), [NOMBRES.get(c, c) for c in CIUDADES])
    ax.tick_params(length=0, labelsize=11.5, colors=TINTA2)
    for s in ax.spines.values(): s.set_visible(False)
    mad = {f["anio_compra"]: f for f in filas if f["ciudad"] == "Madrid"}
    fig.text(0.04, 0.955, "Sobre el papel, el IRPF cobra un 19-23 %. Sobre lo que de verdad ganas, mucho más",
             fontsize=19.5, fontweight="bold", ha="left", va="top")
    fig.text(0.04, 0.905,
             f"IRPF dividido entre la ganancia real (descontada la inflación) al vender hoy un piso de {M2} m² al precio medio tasado de cada ciudad.\n"
             "Naranja: el precio sube en euros pero no tanto como la inflación; el vendedor pierde poder adquisitivo y paga IRPF igual.\n"
             f"Madrid, comprado en 2019 por {es(mad[2019]['precio_compra'])} € y vendido por {es(mad[2019]['precio_venta'])} €: "
             f"el IRPF ({es(mad[2019]['irpf'])} €) se lleva el {es(mad[2019]['irpf_sobre_ganancia_real'] * 100)} % de lo ganado de verdad.\n"
             f"Madrid, comprado en 2007 por {es(mad[2007]['precio_compra'])} € y vendido por {es(mad[2007]['precio_venta'])} €: "
             f"pierde poder adquisitivo y paga {es(mad[2007]['irpf'])} € de IRPF.",
             fontsize=11.5, color=TINTA2, ha="left", va="top", linespacing=1.5)
    hand = [Patch(facecolor=c, label=l) for _, c, l in CORTES] + [Patch(facecolor=NARANJA, label="Pierde y paga"),
                                                                    Patch(facecolor=GRIS, label="Sin ganancia en euros")]
    ax.legend(handles=hand, loc="upper left", bbox_to_anchor=(-0.17, -0.01), ncol=6, frameon=False, fontsize=10,
              handlelength=1.2, handleheight=1.2, columnspacing=1.2)
    pie(fig, f"Fuente: Ministerio de Vivienda y Agenda Urbana, valor tasado medio de la vivienda libre en municipios de más de 25.000 habitantes "
             f"(compra: media del año;\nventa: {ult[:4]} T{ult[-1]}); INE (IPC). Valor de tasación, no precio de venta; media de cada ciudad, no de cada piso. "
             "IRPF: escala del ahorro 2026, sin gastos\nni exenciones (reinversión en vivienda habitual, mayores de 65). "
             f"Datos y código: {REPO}")
    fig.savefig(SALIDA / "08_ciudades_irpf_sobre_ganancia_real.png")
    plt.close(fig)

if __name__ == "__main__":
    filas, ult = tabla(); grafico(filas, ult)
    for f in filas:
        if f["anio_compra"] in (2007, 2019): print(f["ciudad"], f["anio_compra"], f["precio_compra"], f["precio_venta"],
                                                   f["categoria"], f["irpf"], f["irpf_sobre_ganancia_real"], f["pct_ganancia_inflacion"])
