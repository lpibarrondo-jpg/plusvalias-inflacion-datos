"""Genera los gráficos del artículo a partir de los datos de data/raw.

Uso: python scripts/graficos.py
Requiere matplotlib. Salida en graficos/ (PNG) y data/processed/ (tablas de los gráficos).
"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "graficos"; SALIDA.mkdir(exist_ok=True)
REPO = "github.com/lpibarrondo-jpg/plusvalias-inflacion-datos"

# ---------- Estilo (paleta validada: rampa azul ordinal 250-650) ----------
FUENTE = "Inter" if any("Inter" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
SUP, TINTA, TINTA2, MUTED, GRID, EJE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
AZUL = "#2a78d6"
RAMPA = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
plt.rcParams.update({"font.family": FUENTE, "text.color": TINTA, "axes.labelcolor": TINTA2,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": EJE,
                     "figure.facecolor": SUP, "axes.facecolor": SUP, "savefig.facecolor": SUP})

def es(x, dec=0):
    """Formato numérico español: 1.234,5"""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

# ---------- Datos ----------
ipc = [(r["fecha"], float(r["indice_base2025"]))
       for r in csv.DictReader(open(RAIZ / "data" / "raw" / "ine_ipc_indice_general_mensual.csv"))]
IDX = dict(ipc)
ULT_FECHA, ULT = ipc[-1]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
ULT_TXT = f"{MESES[int(ULT_FECHA[5:]) - 1]} {ULT_FECHA[:4]}"

def media_anual(y):
    v = [x for f, x in ipc if f.startswith(str(y))]
    return sum(v) / len(v)

# Escala del ahorro del IRPF 2025-2026 (estatal + autonómica, art. 66 y 76 LIRPF; Ley 7/2024)
ESCALA = [(6_000, .19), (50_000, .21), (200_000, .23), (300_000, .27), (float("inf"), .30)]

def cuota_ahorro(base):
    cuota, prev = 0.0, 0.0
    for lim, t in ESCALA:
        if base <= prev:
            break
        cuota += (min(base, lim) - prev) * t
        prev = lim
    return cuota

def pie(fig, texto):
    fig.text(0.04, 0.035, texto, fontsize=9.5, color=MUTED, ha="left", va="bottom", linespacing=1.5)

# ---------- Gráfico 1: poder adquisitivo de 1.000 € desde enero de 2002 ----------
def grafico_poder_adquisitivo():
    base = IDX["2002-01"]
    xs = [int(f[:4]) + (int(f[5:]) - 1) / 12 for f, _ in ipc]
    ys = [1000 * base / v for _, v in ipc]
    with open(RAIZ / "data" / "processed" / "grafico1_poder_adquisitivo_1000eur.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["fecha", "valor_real_1000eur_ene2002"])
        w.writerows([(fe, round(y, 2)) for (fe, _), y in zip(ipc, ys)])

    fig, ax = plt.subplots(figsize=(12, 6.75), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.95, top=0.80, bottom=0.17)
    ax.axvspan(2021 + 2 / 12, 2023 + 11 / 12, color=GRID, alpha=0.6, lw=0, zorder=0)
    ax.text(2022.55, 1015, "Brote inflacionario\n2021-2023", ha="center", va="top", fontsize=10, color=TINTA2)
    ax.plot(xs, ys, color=AZUL, lw=2.4, solid_capstyle="round", zorder=3)
    ax.scatter([xs[0], xs[-1]], [ys[0], ys[-1]], s=60, color=AZUL, edgecolor=SUP, linewidth=2, zorder=4)
    ax.annotate("1.000 € en enero de 2002", (xs[0], ys[0]), xytext=(12, 0), textcoords="offset points",
                fontsize=11, color=TINTA2, va="center")
    ax.annotate(f"{es(ys[-1])} €\n{ULT_TXT}", (xs[-1], ys[-1]), xytext=(12, 0), textcoords="offset points",
                fontsize=13, fontweight="bold", color=TINTA, ha="left", va="center")
    ax.set_xlim(2001.6, 2029.6); ax.set_ylim(500, 1040)
    ax.set_yticks(range(500, 1001, 100)); ax.set_yticklabels([f"{es(v)} €" for v in range(500, 1001, 100)])
    ax.set_xticks(range(2002, 2027, 4))
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(length=0, labelsize=11)
    perdida = 100 * (1 - ys[-1] / 1000)
    fig.text(0.04, 0.92, f"1.000 € guardados en 2002 hoy compran lo que {es(ys[-1])} € entonces",
             fontsize=20, fontweight="bold", ha="left")
    fig.text(0.04, 0.855, f"Poder adquisitivo de 1.000 € sin invertir, medido con el IPC. "
             f"Han perdido un {es(perdida)} % de su valor real.", fontsize=12.5, color=TINTA2, ha="left")
    pie(fig, f"Fuente: INE, IPC índice general nacional (serie IPC290751, base 2025), enero 2002 - {ULT_TXT}. "
             f"Cálculo propio.\nDatos y código: {REPO}")
    fig.savefig(SALIDA / "01_poder_adquisitivo_1000eur.png")
    plt.close(fig)
    return ys[-1]

# ---------- Gráfico 2: tipo efectivo sobre la ganancia real ----------
PRECIO = 150_000
ANIOS = list(range(2002, 2025, 2))
RENT = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05]
CORTES = [0, .35, .50, 1.00, 99]
ETIQ = ["Menos del 35 %", "35-50 %", "50-100 %", "100 % o más: el impuesto supera la ganancia real"]

def tabla_tipo_efectivo():
    venta_t = int(ULT_FECHA[:4]) + (int(ULT_FECHA[5:]) - 0.5) / 12
    filas = []
    for y in ANIOS:
        coef = ULT / media_anual(y)
        n = venta_t - (y + 0.5)
        for r in RENT:
            venta = PRECIO * coef * (1 + r) ** n
            g_nom = venta - PRECIO
            g_real = venta - PRECIO * coef
            cuota = cuota_ahorro(g_nom)
            filas.append(dict(anio_compra=y, rentabilidad_real_anual=r, coef_ipc=round(coef, 4),
                              anios_tenencia=round(n, 2), precio_venta=round(venta), ganancia_nominal=round(g_nom),
                              ganancia_real=round(g_real), cuota_irpf=round(cuota),
                              tipo_sobre_nominal=round(cuota / g_nom, 4), tipo_sobre_real=round(cuota / g_real, 4)))
    with open(RAIZ / "data" / "processed" / "grafico2_tipo_efectivo_real.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas

def grafico_mapa_calor(filas):
    import numpy as np
    M = np.array([[next(f["tipo_sobre_real"] for f in filas if f["anio_compra"] == y and f["rentabilidad_real_anual"] == r)
                   for r in RENT] for y in ANIOS])
    cmap = ListedColormap(RAMPA); norm = BoundaryNorm(CORTES, cmap.N)

    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.78, bottom=0.15)
    ax.imshow(M, cmap=cmap, norm=norm, aspect="auto")
    # separación de 2 px entre celdas
    for i in range(len(ANIOS) + 1): ax.axhline(i - 0.5, color=SUP, lw=2.5)
    for j in range(len(RENT) + 1): ax.axvline(j - 0.5, color=SUP, lw=2.5)
    for i in range(len(ANIOS)):
        for j in range(len(RENT)):
            v = M[i, j]; k = int(np.digitize(v, CORTES[1:-1]))
            txt = f"{es(v * 100)} %" if v < 10 else f"{es(v * 100, 0)} %"
            ax.text(j, i, txt, ha="center", va="center", fontsize=11.5,
                    color=TINTA if k == 0 else "#ffffff", fontweight="bold" if v >= 1 else "normal")
    ax.set_xticks(range(len(RENT)), [f"{es(r * 100, 1).rstrip('0').rstrip(',')} %" for r in RENT])
    ax.set_yticks(range(len(ANIOS)), [str(y) for y in ANIOS])
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
    ax.set_xlabel("Cuánto ha ganado el bien por encima de la inflación cada año (rentabilidad real anual)",
                  fontsize=11.5, labelpad=10)
    ax.set_ylabel("Año de compra", fontsize=11.5)
    ax.tick_params(length=0, labelsize=11.5)
    for s in ax.spines.values(): s.set_visible(False)
    fig.text(0.04, 0.945, "Al vender, el IRPF puede llevarse la mitad o más de lo que realmente ganaste", fontsize=20,
             fontweight="bold", ha="left")
    fig.text(0.04, 0.91, f"Cuota del IRPF dividida entre la ganancia real (descontada la inflación). "
             f"Bien comprado por {es(PRECIO)} € y vendido en {ULT_TXT}.\n"
             "Si la ley descontara la inflación, el tipo estaría entre el 19 % y el 30 % según el importe.",
             fontsize=12, color=TINTA2, ha="left", va="top", linespacing=1.45)
    ax.legend(handles=[Patch(facecolor=c, label=l) for c, l in zip(RAMPA, ETIQ)], loc="upper left",
              bbox_to_anchor=(-0.09, -0.015), ncol=4, frameon=False, fontsize=10.5, handlelength=1.2,
              handleheight=1.2, columnspacing=1.4)
    pie(fig, "Fuente: INE (IPC, serie IPC290751, base 2025) y escala del ahorro del IRPF 2026 (arts. 66 y 76 LIRPF). "
             "Cálculo propio: compra a mitad de año,\nsin gastos, exenciones ni reducciones; el precio de compra se actualiza "
             f"con el IPC medio del año de compra. Datos y código: {REPO}")
    fig.savefig(SALIDA / "02_tipo_efectivo_ganancia_real.png")
    plt.close(fig)
    return M

if __name__ == "__main__":
    v = grafico_poder_adquisitivo()
    filas = tabla_tipo_efectivo()
    M = grafico_mapa_calor(filas)
    print("Gráfico 1: valor real hoy de 1.000 € de enero 2002 =", round(v, 2))
    print("Gráfico 2: mínimo", round(M.min(), 3), "máximo", round(M.max(), 3))
