"""Gráfico 11: intereses declarados en el IRPF y lo que Hacienda cobró por ellos, frente a la inflación.

AEAT, Estadística de los declarantes del IRPF 2019-2024 (territorio de régimen común), partidas 027 (intereses de
cuentas, depósitos y activos financieros en general) y 030 (Letras del Tesoro), total nacional.
IRPF estimado al 19 % (tipo mínimo de la base del ahorro): es una cota inferior.
Tipo medio de los depósitos a plazo de hogares (saldos vivos): Banco de España, cuadro 19.10. Inflación: INE, IPC medio anual.

Uso: python scripts/intereses_agregado.py
"""
import csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graficos import plt, RAIZ, SALIDA, REPO, NARANJA, RAMPA, TINTA, TINTA2, MUTED, GRID, IDX, es, pie

T = 0.19

def datos():
    aeat = list(csv.DictReader(open(RAIZ / "data" / "raw" / "aeat_irpf_2019_2024_intereses_y_cuota_ahorro.csv", encoding="utf-8")))
    dep = list(csv.DictReader(open(RAIZ / "data" / "raw" / "bde_tipos_depositos_hogares_mensual.csv", encoding="utf-8")))
    filas = []
    for y in range(2019, 2025):
        imp = {r["partida"]: int(r["importe_eur"]) for r in aeat if r["ejercicio"] == str(y)}
        tipo = sum(float(r["plazo_pond_saldos"]) for r in dep if r["fecha"].startswith(str(y))) / 12
        ipc = (sum(IDX[f"{y}-{m:02d}"] for m in range(1, 13)) / sum(IDX[f"{y - 1}-{m:02d}"] for m in range(1, 13)) - 1) * 100
        intereses = imp["027"] + max(imp["030"], 0)
        filas.append(dict(ejercicio=y, intereses_027=imp["027"], letras_030=imp["030"], total_intereses=intereses,
                          irpf_19=round(intereses * T), cuota_ahorro_total=imp["540"] + imp["541"], base_liquidable_ahorro=imp["510"],
                          tipo_medio_ahorro=round((imp["540"] + imp["541"]) / imp["510"], 4),
                          tipo_depositos_plazo_saldos=round(tipo, 4), ipc_medio_anual=round(ipc, 2)))
    with open(RAIZ / "data" / "processed" / "grafico11_intereses_irpf_inflacion.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas

def grafico(filas):
    fig, ax = plt.subplots(figsize=(12.5, 9), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.68, bottom=0.235)
    x = [f["ejercicio"] for f in filas]
    a = [f["intereses_027"] / 1e6 for f in filas]; b = [max(f["letras_030"], 0) / 1e6 for f in filas]
    irpf = [f["irpf_19"] / 1e6 for f in filas]
    ax.bar(x, a, width=0.62, color=RAMPA[0], label="Intereses de cuentas, depósitos y otros activos", zorder=3)
    ax.bar(x, b, bottom=a, width=0.62, color=RAMPA[1], label="Letras del Tesoro", zorder=3)
    ax.bar(x, irpf, width=0.3, color=NARANJA, label="IRPF sobre esos intereses (al 19 %, mínimo)", zorder=4)
    for f, xi, tot, ir in zip(filas, x, [p + q for p, q in zip(a, b)], irpf):
        ax.text(xi, tot + 90, f"{es(tot)} M€", ha="center", va="bottom", fontsize=11, color=TINTA2)
        ax.text(xi, ir + 60, f"{es(ir)}", ha="center", va="bottom", fontsize=10.5, color=NARANJA, fontweight="bold")
        neg = f["tipo_depositos_plazo_saldos"] < f["ipc_medio_anual"]
        ax.text(xi, -0.075, f"Depósito: {es(f['tipo_depositos_plazo_saldos'], 2)} %\nIPC: {es(f['ipc_medio_anual'], 1)} %",
                transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=10,
                color=NARANJA if neg else MUTED, fontweight="bold" if neg else "normal", linespacing=1.3)
    ax.set_xticks(x, [str(v) for v in x], fontsize=12)
    ax.tick_params(axis="x", pad=2, length=0)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{es(v)} M€"))
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.set_ylim(0, max(p + q for p, q in zip(a, b)) * 1.12)
    ax.legend(loc="upper left", frameon=False, fontsize=10.5)
    p = [f for f in filas if f["ejercicio"] >= 2021]
    tot = sum(f["total_intereses"] for f in p) / 1e6; ir = sum(f["irpf_19"] for f in p) / 1e6
    fig.text(0.04, 0.955, f"2021-2024: al menos {es(ir)} millones de IRPF por intereses,\nen años en que el depósito medio perdió frente a la inflación",
             fontsize=19, fontweight="bold", linespacing=1.25, ha="left", va="top")
    fig.text(0.04, 0.86,
             f"Los declarantes del IRPF ingresaron {es(tot)} millones de euros en intereses y Letras del Tesoro en esos cuatro años. "
             "En todos ellos, el tipo medio\nde los depósitos a plazo de los hogares estuvo por debajo de la inflación: de media, "
             "ese dinero no hizo más que intentar compensar la subida de precios.\nY aun así tributó como si fuera renta. "
             "Debajo de cada año: tipo medio de los depósitos a plazo frente al IPC medio (en naranja, cuando pierde).",
             fontsize=11.5, color=TINTA2, ha="left", va="top", linespacing=1.5)
    pie(fig, "Fuente: AEAT, Estadística de los declarantes del IRPF 2019-2024, partidas 027 y 030, total del territorio de régimen común (sin País Vasco ni Navarra). "
             "IRPF estimado al\n19 %, el tipo mínimo del ahorro: cota inferior. No incluye las retenciones del 19 % de quienes no declaran. "
             "Tipo medio de los depósitos a plazo de hogares, saldos vivos\n(Banco de España, cuadro 19.10); IPC medio anual (INE). "
             f"Datos y código: {REPO}")
    fig.savefig(SALIDA / "11_intereses_irpf_inflacion.png")
    plt.close(fig)
    return tot, ir

if __name__ == "__main__":
    f = datos(); print(grafico(f))
    for r in f: print(r)
