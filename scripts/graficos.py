"""Genera los gráficos del artículo a partir de los datos de data/raw.

Uso: python scripts/graficos.py
Requiere matplotlib. Salida en graficos/ (PNG) y data/processed/ (tablas de los gráficos).
"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
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

# ---------- Gráfico 3: depósitos, rentabilidad real antes y después del IRPF ----------
NARANJA = "#eb6834"
TIPO_AHORRO_MIN = 0.19  # primer tramo de la escala del ahorro

def tabla_depositos():
    dep = list(csv.DictReader(open(RAIZ / "data" / "raw" / "bde_tipos_depositos_hogares_mensual.csv")))
    def media(y, col):
        v = [float(r[col]) for r in dep if r["fecha"].startswith(str(y))]
        return sum(v) / len(v)
    filas = []
    ultimo_completo = int(ULT_FECHA[:4]) - 1
    for y in range(2003, ultimo_completo + 1):
        i = media(y, "plazo_hasta1a_nuevas") / 100
        p = media_anual(y) / media_anual(y - 1) - 1
        filas.append(dict(anio=y, tipo_deposito_1a=round(i, 6), inflacion_media=round(p, 6),
                          real_antes_irpf=round((1 + i) / (1 + p) - 1, 6),
                          real_despues_irpf=round((1 + i * (1 - TIPO_AHORRO_MIN)) / (1 + p) - 1, 6)))
    with open(RAIZ / "data" / "processed" / "grafico3_depositos_real.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas

def grafico_depositos(filas):
    import numpy as np
    x = np.arange(len(filas)); w = 0.4
    pre = [100 * f["real_antes_irpf"] for f in filas]; post = [100 * f["real_despues_irpf"] for f in filas]
    n_neg = sum(v < 0 for v in post)
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.76, bottom=0.17)
    ax.bar(x - w / 2 - 0.01, pre, w, color=AZUL, label="Antes del IRPF", zorder=3)
    ax.bar(x + w / 2 + 0.01, post, w, color=NARANJA, label="Después del IRPF (19 %)", zorder=3)
    ax.axhline(0, color=EJE, lw=1, zorder=2)
    k = [f["anio"] for f in filas].index(2022)
    ax.annotate(f"2022: {es(post[k], 1)} %", (k - w, post[k]), xytext=(-6, 0), textcoords="offset points",
                ha="right", va="center", fontsize=11, color=TINTA)
    ax.set_xticks(x, [str(f["anio"]) if f["anio"] % 2 == 1 else "" for f in filas])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{es(v)} %"))
    ax.set_ylim(-8.5, 3.5)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ("top", "right", "left", "bottom"): ax.spines[sp].set_visible(False)
    ax.tick_params(length=0, labelsize=11)
    ax.legend(loc="upper right", frameon=False, fontsize=11, ncol=2)
    fig.text(0.04, 0.93, f"En {n_neg} de {len(filas)} años, un depósito perdió poder adquisitivo después del IRPF",
             fontsize=20, fontweight="bold", ha="left")
    fig.text(0.04, 0.87, "Rentabilidad real anual de un depósito a plazo de hasta 1 año: el interés pagado por el banco, "
             "descontada la inflación.\nEl IRPF grava el interés nominal aunque, descontada la inflación, el ahorrador pierda dinero.",
             fontsize=12, color=TINTA2, ha="left", va="top", linespacing=1.45)
    pie(fig, "Fuente: Banco de España, Boletín Estadístico, cuadro 19.7 (TEDR de nuevas operaciones de depósitos a plazo de hogares "
             "hasta 1 año, media anual)\ne INE (IPC, media anual). IRPF al 19 % (primer tramo de la base del ahorro). "
             f"Cálculo propio. Datos y código: {REPO}")
    fig.savefig(SALIDA / "03_depositos_rentabilidad_real.png")
    plt.close(fig)
    return n_neg

# ---------- Bloque 6: escala del ahorro congelada y gráfico 4 ----------
# Umbrales de la escala del ahorro y norma que los fijó (BOE, versiones de los arts. 66 y 76 LIRPF)
UMBRALES = [(6_000, 2010, "Ley 26/2009 (BOE-A-2009-20765)"), (50_000, 2015, "Ley 26/2014 (BOE-A-2014-12327)"),
            (200_000, 2021, "Ley 11/2020 (BOE-A-2020-17339)"), (300_000, 2023, "Ley 31/2022 (BOE-A-2022-22128)")]
TIPOS = [t for _, t in ESCALA]

def cuota_con(base, limites):
    cuota, prev = 0.0, 0.0
    for lim, t in zip(list(limites) + [float("inf")], TIPOS):
        if base <= prev:
            break
        cuota += (min(base, lim) - prev) * t
        prev = lim
    return cuota

def tabla_escala():
    filas = []
    for u, y, norma in UMBRALES:
        coef = ULT / media_anual(y)
        filas.append(dict(umbral_legal=u, vigente_desde=y, norma=norma, coef_ipc=round(coef, 4),
                          umbral_actualizado=round(u * coef)))
    with open(RAIZ / "data" / "processed" / "tabla_escala_ahorro_actualizada.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return [f["umbral_actualizado"] for f in filas]

def grafico_medidas(lim_act, filas_mapa):
    caso = next(f for f in filas_mapa if f["anio_compra"] == 2002 and f["rentabilidad_real_anual"] == 0.005)
    legal = [u for u, _, _ in UMBRALES]
    actual = cuota_con(caso["ganancia_nominal"], legal)
    escala = cuota_con(caso["ganancia_nominal"], lim_act)
    base = cuota_con(caso["ganancia_real"], legal)
    etiquetas = ["Hoy (ley vigente)", "Actualizando los tramos\nde la escala con el IPC", "Descontando la inflación\nde la ganancia"]
    vals = [actual, escala, base]
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
    fig.subplots_adjust(left=0.25, right=0.9, top=0.72, bottom=0.2)
    y = list(range(len(vals)))[::-1]
    ax.barh(y, vals, height=0.55, color=[AZUL, AZUL, "#86b6ef"], zorder=3)
    for yi, v in zip(y, vals):
        ax.text(v + 400, yi, f"{es(v)} €", va="center", fontsize=13, fontweight="bold", color=TINTA)
    ax.set_yticks(y, etiquetas); ax.tick_params(length=0, labelsize=12, colors=TINTA2)
    ax.set_xlim(0, max(vals) * 1.15); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    fig.text(0.04, 0.92, f"Actualizar la escala ahorra {es(actual - escala)} €; descontar la inflación, {es(actual - base)} €",
             fontsize=20, fontweight="bold", ha="left")
    fig.text(0.04, 0.86, f"IRPF a pagar en un mismo caso: piso comprado en 2002 por {es(PRECIO)} € y vendido en {ULT_TXT} por "
             f"{es(caso['precio_venta'])} €\n(un 0,5 % anual por encima de la inflación). El problema no está en los tipos, "
             "sino en gravar como ganancia lo que es inflación.", fontsize=12, color=TINTA2, ha="left", va="top", linespacing=1.45)
    pie(fig, "Fuente: BOE (arts. 66 y 76 LIRPF, versiones vigentes desde 2010) e INE (IPC). Tramos actualizados con el IPC "
             "desde el año en que se fijaron.\nCálculo propio, mismo caso que el gráfico 2. "
             f"Datos y código: {REPO}")
    fig.savefig(SALIDA / "04_que_arregla_cada_medida.png")
    plt.close(fig)
    return actual, escala, base

# ---------- Bloque 7: cuánto de lo gravado en 2024 fue inflación (inmuebles) ----------
# AEAT, Estadística de declarantes del IRPF 2024, bloque V; Registradores, Anuario ERI 2024 (periodo medio de posesión 17,7 años)
TENENCIAS = [10, 15, 17.7]
TIPOS_REF = (0.19, 0.21, 0.23)

def tabla_inflacion_inmuebles():
    aeat = list(csv.DictReader(open(RAIZ / "data" / "raw" / "aeat_irpf2024_transmisiones_por_activo.csv")))
    g = lambda a, s, p: int(next(x["importe_eur"] for x in aeat if x["activo"] == a and x["seccion"] == s and x["partida"] == p))
    adq = g("inmuebles", "Operaciones sin beneficio fiscal", "Valor de Adquisición")
    gan = g("inmuebles", "Operaciones sin beneficio fiscal", "Resultado positivo")
    i2024 = media_anual(2024)
    filas = []
    for h in TENENCIAS:
        t = 2024.5 - h                      # ventas repartidas a lo largo de 2024: fecha media de compra
        anio, mes = int(t), int((t - int(t)) * 12) + 1
        mes = min(mes, 12)
        coef = i2024 / IDX[f"{anio}-{mes:02d}"]
        infl = adq * (coef - 1)
        filas.append(dict(anios_tenencia=h, mes_compra_medio=f"{anio}-{mes:02d}", coef_ipc=round(coef, 4),
                          valor_adquisicion=adq, ganancia_gravada=gan, componente_inflacion=round(infl),
                          ganancia_real=round(gan - infl), pct_inflacion=round(infl / gan, 4),
                          irpf_sobre_inflacion_19=round(infl * .19), irpf_sobre_inflacion_21=round(infl * .21),
                          irpf_sobre_inflacion_23=round(infl * .23)))
    with open(RAIZ / "data" / "processed" / "grafico5_inflacion_plusvalias_inmuebles_2024.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas

def grafico_inflacion_inmuebles(filas):
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
    fig.subplots_adjust(left=0.28, right=0.95, top=0.68, bottom=0.2)
    gan = filas[0]["ganancia_gravada"] / 1e9
    y = list(range(len(filas)))[::-1]
    for yi, f in zip(y, filas):
        inf_ = f["componente_inflacion"] / 1e9; real = f["ganancia_real"] / 1e9
        ax.barh(yi, inf_, height=0.55, color=NARANJA, zorder=3)
        ax.barh(yi, real, left=inf_ + 0.06, height=0.55, color=AZUL, zorder=3)
        ax.text(inf_ / 2, yi, f"Inflación: {es(f['pct_inflacion'] * 100)} %", ha="center", va="center", color="#ffffff",
                fontsize=12, fontweight="bold")
        ax.text(gan + 0.25, yi, f"{es(real, 1)} mil M€ reales", ha="left", va="center", color=TINTA2, fontsize=11)
    etiq = [f"{es(f['anios_tenencia'], 1).rstrip('0').rstrip(',')} años de tenencia" + (" (media oficial)" if f["anios_tenencia"] == 17.7 else "") for f in filas]
    ax.set_yticks(y, etiq); ax.tick_params(length=0, labelsize=11.5, colors=TINTA2)
    ax.set_xlim(0, gan * 1.32); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    c = filas[-1]
    fig.text(0.04, 0.92, f"El {es(c['pct_inflacion'] * 100)} % de las plusvalías inmobiliarias gravadas en 2024 sería inflación",
             fontsize=20, fontweight="bold", ha="left")
    fig.text(0.04, 0.86, f"Ganancias por venta de inmuebles declaradas en el IRPF de 2024 sin exenciones: {es(gan, 1)} mil millones de €. "
             "\nEn naranja, la parte que solo compensa la subida de precios desde la compra, según los años de tenencia.\n"
             f"Con la tenencia media oficial, el IRPF cobró unos {es(c['irpf_sobre_inflacion_21'] / 1e9, 1)} mil millones de € sobre esa parte.",
             fontsize=12, color=TINTA2, ha="left", va="top", linespacing=1.45)
    pie(fig, "Fuente: AEAT, Estadística de los declarantes del IRPF 2024, bloque V (inmuebles, operaciones sin beneficio fiscal); "
             "Colegio de Registradores, Anuario ERI 2024\n(periodo medio de posesión 17,7 años); INE (IPC). IRPF estimado al 21 % (rango 19-23 %). "
             f"Cálculo propio. Datos y código: {REPO}")
    fig.savefig(SALIDA / "05_inflacion_en_plusvalias_inmuebles_2024.png")
    plt.close(fig)

if __name__ == "__main__":
    v = grafico_poder_adquisitivo()
    filas = tabla_tipo_efectivo()
    M = grafico_mapa_calor(filas)
    print("Gráfico 1: valor real hoy de 1.000 € de enero 2002 =", round(v, 2))
    print("Gráfico 2: mínimo", round(M.min(), 3), "máximo", round(M.max(), 3))
    print("Gráfico 3: años con pérdida real tras IRPF =", grafico_depositos(tabla_depositos()))
    lim = tabla_escala()
    print("Umbrales actualizados:", lim)
    print("Gráfico 4 (actual, escala, base):", [round(v) for v in grafico_medidas(lim, filas)])
    fi = tabla_inflacion_inmuebles(); grafico_inflacion_inmuebles(fi)
    for f in fi: print("Gráfico 5:", f)
