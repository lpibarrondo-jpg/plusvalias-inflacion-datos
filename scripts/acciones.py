"""Gráfico 9: invertir en el IBEX 35 y vender hoy: qué parte de la ganancia es inflación y cuánto IRPF se paga.

IBEX 35: valor a fin de mes, Banco de España, Boletín Estadístico, cuadro 22.25 (fuente: Sociedad Rectora de la
Bolsa de Madrid). Índice de precios, sin dividendos: es lo que determina la ganancia patrimonial al vender.
Cada año de compra = 50.000 € invertidos en 12 aportaciones iguales a fin de cada mes de ese año.
IPC: INE (IPC290751 desde 2002; antes, encadenado con la variación mensual oficial IPC290752, aproximado).

Uso: python scripts/acciones.py
"""
import csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graficos import plt, RAIZ, SALIDA, REPO, NARANJA, RAMPA, TINTA, TINTA2, MUTED, GRID, IDX, es, cuota_ahorro, pie

MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12}
INVERSION = 50_000
DESDE, HASTA = 1995, 2024

def ibex():
    filas = open(RAIZ / "data" / "raw" / "bde" / "be2225_indices_cotizacion_acciones.csv", encoding="latin-1").read().splitlines()
    cab = next(csv.reader([filas[3]]))
    col = next(i for i, c in enumerate(cab) if c.strip().endswith("IBEX-35") or "IBEX" in c.upper())
    out = {}
    for r in csv.reader(filas[6:]):
        if len(r) > col and r[0][:3] in MESES:
            try: out[f"{r[0][-4:]}-{MESES[r[0][:3]]:02d}"] = float(r[col])
            except ValueError: pass
    return out

def ipc_encadenado():
    var = {r["fecha"]: float(r["variacion_mensual_pct"]) / 100
           for r in csv.DictReader(open(RAIZ / "data" / "raw" / "ine_ipc_variacion_mensual.csv", encoding="utf-8"))}
    idx = dict(IDX)
    y, m = 2002, 1
    while (y, m) > (1961, 1):
        prev = (y, m - 1) if m > 1 else (y - 1, 12)
        idx[f"{prev[0]}-{prev[1]:02d}"] = idx[f"{y}-{m:02d}"] / (1 + var[f"{y}-{m:02d}"])
        y, m = prev
    return idx

def tabla():
    ix, ipc = ibex(), ipc_encadenado()
    venta = max(k for k in ix if k in ipc)
    filas = []
    for y in range(DESDE, HASTA + 1):
        meses = [f"{y}-{m:02d}" for m in range(1, 13)]
        aport = INVERSION / 12
        valor = sum(aport / ix[m] for m in meses) * ix[venta]
        coste_actualizado = sum(aport * ipc[venta] / ipc[m] for m in meses)
        g = valor - INVERSION; real = valor - coste_actualizado; cuota = cuota_ahorro(max(g, 0))
        filas.append(dict(anio_compra=y, venta=venta, inversion=INVERSION, valor_venta=round(valor), ganancia_nominal=round(g),
                          inflacion_acumulada=round(coste_actualizado / INVERSION - 1, 4), ganancia_real=round(real),
                          parte_inflacion=round(min((g - real) / g, 1), 4) if g > 0 else None, irpf=round(cuota),
                          irpf_sobre_ganancia_real=round(cuota / real, 4) if real > 0 else None,
                          dt9_abatimiento=y < 1995))
    with open(RAIZ / "data" / "processed" / "grafico9_ibex_por_anio_compra.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas, venta, ix

def grafico(filas, venta, ix):
    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.72, bottom=0.17)
    x = [f["anio_compra"] for f in filas]
    for f in filas:
        g = f["ganancia_nominal"] / INVERSION * 100; r = f["ganancia_real"] / INVERSION * 100
        infl = g - r if r > 0 else g
        ax.bar(f["anio_compra"], infl, color=NARANJA, width=0.78, zorder=3)
        if r > 0:
            ax.bar(f["anio_compra"], r, bottom=infl, color=RAMPA[1], width=0.78, zorder=3)
            lab = f"{es(f['irpf_sobre_ganancia_real'] * 100)} %" if f["irpf_sobre_ganancia_real"] < 1 else ">100 %"
        else:
            ax.bar(f["anio_compra"], r, color="none", edgecolor=NARANJA, hatch="///", lw=0, width=0.78, zorder=3)
            lab = "pierde"
        top = max(g, 0)
        ax.text(f["anio_compra"], top + 4, lab, ha="center", va="bottom", fontsize=8.6, rotation=0,
                color=NARANJA if r <= 0 or f["irpf_sobre_ganancia_real"] >= 0.5 else TINTA2,
                fontweight="bold" if r <= 0 or f["irpf_sobre_ganancia_real"] >= 0.5 else "normal", linespacing=1.0)
    ax.axhline(0, color=TINTA2, lw=1, zorder=4)
    ax.set_xticks(x[::1], [str(v) if v % 2 == 1 else "" for v in x], fontsize=10)
    ax.set_xlim(DESDE - 0.7, HASTA + 0.7)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{es(v)} €"))
    ax.set_ylabel("Ganancia al vender por cada 100 € invertidos", fontsize=11)
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10.5)
    y07 = next(f for f in filas if f["anio_compra"] == 2007)
    rango = [f["irpf_sobre_ganancia_real"] for f in filas if f["irpf_sobre_ganancia_real"] and f["anio_compra"] <= 2015]
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=NARANJA, label="Parte de la ganancia que solo es inflación"),
                       Patch(facecolor=RAMPA[1], label="Ganancia real"),
                       Patch(facecolor="none", edgecolor=NARANJA, hatch="///", label="Pérdida real")],
              loc="upper right", frameon=False, fontsize=10.5)
    mes = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril", "05": "mayo", "06": "junio", "07": "julio",
           "08": "agosto", "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"}[venta[5:]]
    n_mitad = sum(1 for f in filas if f["irpf_sobre_ganancia_real"] is None or f["irpf_sobre_ganancia_real"] > 0.5)
    n_todo = sum(1 for f in filas if f["irpf_sobre_ganancia_real"] is None or f["irpf_sobre_ganancia_real"] >= 1)
    fig.text(0.04, 0.955, f"En bolsa, igual: en {n_mitad} de {len(filas)} años de compra, el IRPF se lleva más de la mitad de la ganancia real",
             fontsize=19.5, fontweight="bold", ha="left", va="top")
    fig.text(0.04, 0.905,
             f"50.000 € invertidos en el IBEX 35 a lo largo de cada año y vendidos a cierre de {mes} de {venta[:4]}. "
             "Encima de cada barra: IRPF dividido entre la ganancia real.\n"
             f"En {n_todo} años (1998-2000, burbuja puntocom, y 2006-2007) el impuesto supera toda la ganancia real o se paga con pérdida real: "
             f"quien invirtió en 2007\ngana un {es(y07['ganancia_nominal'] / INVERSION * 100)} % en euros, pierde un "
             f"{es(-y07['ganancia_real'] / INVERSION * 100)} % en poder adquisitivo y paga {es(y07['irpf'])} € de IRPF. "
             "Sobre el papel, el tipo es del 19 % al 23 %;\nsobre la ganancia real nunca baja del 23 %, y para quien compró cerca de una burbuja se dispara.",
             fontsize=11.5, color=TINTA2, ha="left", va="top", linespacing=1.5)
    pie(fig, "Fuente: Banco de España, Boletín Estadístico, cuadro 22.25 (IBEX 35 a fin de mes; Sociedad Rectora de la Bolsa de Madrid); INE (IPC; antes de 2002, encadenado\n"
             "con la variación mensual oficial). Índice de precios sin dividendos (los dividendos tributan cada año aparte). 12 aportaciones iguales por año. "
             "IRPF: escala del ahorro 2026,\nsin gastos ni comisiones. Compras anteriores a 1995 excluidas (régimen transitorio de abatimiento). "
             f"Datos y código: {REPO}")
    fig.savefig(SALIDA / "09_ibex_inflacion_por_anio_compra.png")
    plt.close(fig)

if __name__ == "__main__":
    filas, venta, ix = tabla(); grafico(filas, venta, ix)
    print("venta", venta, ix[venta])
    for f in filas: print(f["anio_compra"], f["ganancia_nominal"], f["ganancia_real"], f["parte_inflacion"], f["irpf"], f["irpf_sobre_ganancia_real"])
