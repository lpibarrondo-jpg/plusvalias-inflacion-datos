"""Gráfico 10: Letras del Tesoro a 12 meses: rentabilidad real antes y después del IRPF, y el boom de ahorradores.

Tipos: Banco de España, cuadro ti_1_4 (mercado primario, Letras a 12 meses, tipo marginal de cada subasta).
Tenencias de hogares: Banco de España, Boletín Estadístico, cuadro 22.3 (Letras, cartera firme por tenedores,
hogares e ISFLSH, valor facial). Inflación: INE, IPC del mes de la subasta al mismo mes del año siguiente.
IRPF: 19 % (primer tramo de la base del ahorro). Rendimiento de la letra = tipo × 364/360.

Uso: python scripts/letras.py
"""
import csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graficos import plt, RAIZ, SALIDA, REPO, NARANJA, RAMPA, TINTA, TINTA2, MUTED, GRID, IDX, es, pie
import matplotlib.dates as mdates
from datetime import date

BDE = RAIZ / "data" / "raw" / "bde"
MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12}
TIPO_IRPF = 0.19
DESDE = date(2022, 5, 1)  # primera subasta a 12 meses con tipo positivo tras años de tipos negativos

def subastas():
    filas = open(BDE / "ti_1_4_letras_subastas_tipo_marginal.csv", encoding="latin-1").read().splitlines()
    out = []
    for r in csv.reader(filas[6:]):
        if len(r) > 4 and r[0][:2].isdigit():
            try: v = float(r[4])
            except ValueError: continue
            d, m, y = r[0].split(); out.append((date(int(y), MESES[m], int(d)), v))
    return out

def hogares():
    filas = open(BDE / "be2203_letras_tenedores.csv", encoding="latin-1").read().splitlines()
    cab = next(csv.reader([filas[3]]))
    col = next(i for i, c in enumerate(cab) if "Hogares" in c)
    out = []
    for r in csv.reader(filas[6:]):
        if len(r) > col and r[0][:3] in MESES:
            try: out.append((date(int(r[0][-4:]), MESES[r[0][:3]], 15), float(r[col]) / 1e9))
            except ValueError: pass
    return out

def mes_mas(d, k):
    t = d.year * 12 + d.month - 1 + k
    return f"{t // 12}-{t % 12 + 1:02d}"

def tabla():
    filas = []
    for d, tipo in subastas():
        fin = mes_mas(d, 12)
        if d < DESDE or fin not in IDX: continue
        infl = IDX[fin] / IDX[f"{d.year}-{d.month:02d}"] - 1
        rend = tipo / 100 * 364 / 360
        antes = (1 + rend) / (1 + infl) - 1
        despues = (1 + rend * (1 - TIPO_IRPF)) / (1 + infl) - 1
        cat = ("pérdida real antes de impuestos" if antes <= 0 else
               "ganancia real convertida en pérdida por el IRPF" if despues <= 0 else "ganancia real tras impuestos")
        filas.append(dict(fecha_subasta=d.isoformat(), tipo_marginal=tipo, rendimiento=round(rend, 5), inflacion_12m=round(infl, 5),
                          real_antes_irpf=round(antes, 5), real_despues_irpf=round(despues, 5),
                          irpf_sobre_ganancia_real=round(rend * TIPO_IRPF / antes, 3) if antes > 0 else None, categoria=cat))
    with open(RAIZ / "data" / "processed" / "grafico10_letras_12m.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas

def grafico(filas, hog):
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(13, 10.5), dpi=150, gridspec_kw=dict(height_ratios=[2.3, 1], hspace=0.38), sharex=True)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.75, bottom=0.145)
    xs = [date.fromisoformat(f["fecha_subasta"]) for f in filas]
    tipo = [f["rendimiento"] * 100 for f in filas]
    neto = [f["rendimiento"] * (1 - TIPO_IRPF) * 100 for f in filas]
    infl = [f["inflacion_12m"] * 100 for f in filas]
    ax.fill_between(xs, neto, infl, where=[i > n for i, n in zip(infl, neto)], color=NARANJA, alpha=0.18, lw=0, step="mid",
                    label="Pierde poder adquisitivo después del IRPF")
    ax.step(xs, infl, where="mid", color=NARANJA, lw=2.4, label="Inflación durante la vida de la letra")
    ax.step(xs, tipo, where="mid", color=RAMPA[1], lw=2.2, label="Lo que paga la letra")
    ax.step(xs, neto, where="mid", color=RAMPA[3], lw=2.2, ls=(0, (4, 2)), label="Lo que queda tras el IRPF (19 %)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{es(v)} %"))
    ax.set_ylim(0, max(infl + tipo) * 1.3)
    ax.set_xlim(date(2022, 3, 1), date(2026, 11, 1))
    ax.grid(axis="y", color=GRID, lw=0.8); ax.tick_params(labelsize=10.5)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(loc="upper left", frameon=False, fontsize=10.2, ncol=2)
    ax.set_title("Letras a 12 meses, por fecha de subasta", loc="left", fontsize=12, color=TINTA2, pad=8)
    hx = [d for d, v in hog if d >= date(2022, 3, 1)]; hv = [v for d, v in hog if d >= date(2022, 3, 1)]
    ax2.bar(hx, hv, width=25, color=RAMPA[2])
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{es(v)} mm €"))
    ax2.grid(axis="y", color=GRID, lw=0.8); ax2.tick_params(labelsize=10.5)
    for s in ("top", "right"): ax2.spines[s].set_visible(False)
    ax2.set_title("Letras en manos de los hogares (miles de millones de euros, valor facial)", loc="left", fontsize=12, color=TINTA2, pad=8)
    ax2.xaxis.set_major_locator(mdates.YearLocator()); ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    n = len(filas)
    n_antes = sum(f["categoria"].startswith("pérdida") for f in filas)
    n_conv = sum(f["categoria"].startswith("ganancia real convertida") for f in filas)
    h21 = next(v for d, v in hog if d.year == 2021 and d.month == 12)
    h23 = next(v for d, v in hog if d.year == 2023 and d.month == 12)
    fig.text(0.04, 0.955, f"Letras del Tesoro: en {n_antes + n_conv} de {n} subastas el ahorrador perdió poder adquisitivo tras pagar IRPF",
             fontsize=19, fontweight="bold", ha="left", va="top")
    fig.text(0.04, 0.905,
             f"Subastas a 12 meses desde mayo de 2022 (primer tipo positivo). En {n_antes} la letra ya pagaba menos que la inflación y aun así tributó; "
             f"en otras {n_conv},\nel IRPF convirtió una pequeña ganancia real en pérdida. "
             f"Mientras, los hogares pasaron de tener {es(h21 * 1000)} millones de euros en Letras (diciembre de 2021)\na "
             f"{es(h23)} mil millones (diciembre de 2023). El Estado es a la vez quien paga ese interés y quien lo grava.",
             fontsize=11.5, color=TINTA2, ha="left", va="top", linespacing=1.5)
    pie(fig, "Fuente: Banco de España (tipo marginal de las subastas de Letras a 12 meses, cuadro ti_1_4; Letras por tenedores, Boletín Estadístico, cuadro 22.3); "
             "INE (IPC, del mes de la\nsubasta al mismo mes del año siguiente). IRPF del 19 % (primer tramo del ahorro). "
             f"Sin comisiones; tipo marginal, muy próximo al medio.\nDatos y código: {REPO}")
    fig.savefig(SALIDA / "10_letras_tesoro_real.png")
    plt.close(fig)
    return n, n_antes, n_conv, h21, h23

if __name__ == "__main__":
    filas = tabla(); print(grafico(filas, hogares()))
