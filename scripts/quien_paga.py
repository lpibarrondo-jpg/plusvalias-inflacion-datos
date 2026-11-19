"""Gráfico 12: quién declara intereses en el IRPF, por tramo de renta (2024).

AEAT, Estadística de los declarantes del IRPF 2024, partidas 027 (intereses de cuentas, depósitos y activos
financieros) y 030 (Letras del Tesoro), por tramos de rendimientos e imputaciones del declarante (total nacional,
territorio de régimen común).

Uso: python scripts/quien_paga.py
"""
import csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graficos import plt, RAIZ, SALIDA, REPO, NARANJA, RAMPA, TINTA, TINTA2, MUTED, GRID, es, pie

ETQ = {"(0 - 1,5]": "Hasta\n1.500 €", "(1,5 - 6]": "1.500-\n6.000 €", "(6 - 12]": "6.000-\n12.000 €", "(12 - 21]": "12.000-\n21.000 €",
       "(21 - 30]": "21.000-\n30.000 €", "(30 - 60]": "30.000-\n60.000 €", "(60 - 150]": "60.000-\n150.000 €",
       "(150 - 601]": "150.000-\n601.000 €", "Mayor de 601": "Más de\n601.000 €"}
HASTA30 = ["Negativo y Cero", "(0 - 1,5]", "(1,5 - 6]", "(6 - 12]", "(12 - 21]", "(21 - 30]"]
MEDIOS = ["(12 - 21]", "(21 - 30]"]  # aquí el mínimo personal ya lo absorbe la base general: el 19 % se paga
CLARO = "#f4b393"
num = lambda s: float(s.replace(".", "").replace(",", "."))

def tabla():
    r = [x for x in csv.DictReader(open(RAIZ / "data" / "raw" / "aeat_irpf2024_intereses_por_tramos_renta.csv", encoding="utf-8")) if x["partida"] == "027"]
    fil = []
    for t in ETQ:
        rows = [x for x in r if x["tramo"] == t or (t == "(0 - 1,5]" and x["tramo"] == "Negativo y Cero")]
        n = sum(num(x["liquidaciones_partida"]) for x in rows); imp = sum(num(x["importe_eur"]) for x in rows)
        fil.append(dict(tramo=t, personas=int(n), intereses_eur=round(imp), interes_medio=round(imp / n), irpf_19_medio=round(imp / n * 0.19)))
    tot = [x for x in r if x["tramo"] == "Total"][0]
    resumen = dict(total_personas=num(tot["liquidaciones_partida"]), total_importe=num(tot["importe_eur"]),
                   hasta30_personas=sum(num(x["liquidaciones_partida"]) for x in r if x["tramo"] in HASTA30),
                   hasta30_importe=sum(num(x["importe_eur"]) for x in r if x["tramo"] in HASTA30),
                   medios_personas=sum(num(x["liquidaciones_partida"]) for x in r if x["tramo"] in MEDIOS),
                   medios_importe=sum(num(x["importe_eur"]) for x in r if x["tramo"] in MEDIOS))
    with open(RAIZ / "data" / "processed" / "grafico12_intereses_por_tramo_renta_2024.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fil[0].keys()); w.writeheader(); w.writerows(fil)
    return fil, resumen

def grafico(fil, res):
    fig, ax = plt.subplots(figsize=(12.5, 8.6), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.73, bottom=0.27)
    x = range(len(fil))
    for i, f in zip(x, fil):
        bajo = f["tramo"] in HASTA30
        ax.bar(i, f["personas"] / 1e6, width=0.7, color=(NARANJA if f["tramo"] in MEDIOS else CLARO) if bajo else RAMPA[1], zorder=3)
        ax.text(i, f["personas"] / 1e6 + 0.03, f"{es(f['personas'] / 1e6, 2)} M", ha="center", va="bottom", fontsize=11,
                color=TINTA, fontweight="bold" if bajo else "normal")
        sub = f"{es(f['interes_medio'])} €" + (f"\n{es(f['irpf_19_medio'])} € IRPF" if f["tramo"] not in ("(0 - 1,5]", "(1,5 - 6]", "(6 - 12]") else "\nIRPF: depende")
        ax.text(i, -0.135, sub, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=10, color=MUTED, linespacing=1.3)
    ax.set_xticks(list(x), [ETQ[f["tramo"]] for f in fil], fontsize=10.2)
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Declaraciones con intereses (millones)", fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: es(v, 1)))
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.text(2.5, max(f["personas"] for f in fil) / 1e6 * 0.98, "Renta de 30.000 € o menos", ha="center", fontsize=11.5, color=NARANJA, fontweight="bold")
    pp = res["hasta30_personas"] / res["total_personas"]; pi = res["hasta30_importe"] / res["total_importe"]
    fig.text(0.04, 0.955, f"No es cosa de ricos: {es(pp * 100)} de cada 100 declaraciones con intereses son de rentas de 30.000 € o menos",
             fontsize=16.5, fontweight="bold", ha="left", va="top")
    fig.text(0.04, 0.905,
             f"En 2024, {es(res['total_personas'] / 1e6, 1)} millones de declaraciones del IRPF incluyeron intereses de cuentas y depósitos. "
             f"{es(res['hasta30_personas'] / 1e6, 1)} millones eran de rentas totales de 30.000 € o menos.\n"
             f"Solo en las de 12.000 a 30.000 € ({es(res['medios_personas'] / 1e6, 2)} millones de declaraciones), los intereses sumaron {es(res['medios_importe'] / 1e6)} millones "
             f"y el IRPF, al menos {es(res['medios_importe'] * 0.19 / 1e6)} millones,\nen un año en que el depósito a plazo medio pagaba un 2,09 % "
             "con la inflación en el 2,8 %. Bajo cada tramo: interés medio declarado e IRPF al 19 %.",
             fontsize=11.5, color=TINTA2, ha="left", va="top", linespacing=1.5)
    pie(fig, "Fuente: AEAT, Estadística de los declarantes del IRPF 2024, partida 027 (intereses de cuentas, depósitos y activos financieros en general), por tramos\n"
             "de rendimientos e imputaciones del declarante; territorio de régimen común. No incluye Letras del Tesoro (partida 030) ni a quienes no declaran.\n"
             "IRPF al 19 %, tipo mínimo del ahorro; por debajo de 12.000 € el mínimo personal puede reducirlo o anularlo. Depósitos a plazo: Banco de España (saldos\n"
             f"vivos de hogares); IPC medio de 2024: INE. Datos y código: {REPO}")
    fig.savefig(SALIDA / "12_quien_paga_intereses_por_renta.png")
    plt.close(fig)

if __name__ == "__main__":
    f, r = tabla(); grafico(f, r); print(r); [print(x) for x in f]
