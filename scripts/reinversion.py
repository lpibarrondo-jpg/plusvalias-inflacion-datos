"""Gráfico 7: ¿salva la exención por reinversión en vivienda habitual al vendedor que pierde por la inflación?

Art. 38.1 LIRPF y art. 41.1 RIRPF: si se reinvierte menos de lo obtenido, solo se exime la parte proporcional
de la ganancia (importe reinvertido / importe total obtenido). Si la vivienda se compró con préstamo, el importe
total obtenido es el valor de transmisión menos el principal pendiente.

Uso: python scripts/reinversion.py
"""
import csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graficos import plt, RAIZ, SALIDA, REPO, AZUL, NARANJA, RAMPA, TINTA, TINTA2, MUTED, GRID, es, cuota_ahorro, pie
from vender_con_perdidas import series, ipc_anual

def operacion(anio, precio=200_000):
    gen_t, gen_a, ult, ipc_t = series()
    venta = precio * gen_t["Nacional"][0]["Valor"] / gen_a["Nacional"][anio]
    return venta, venta - precio, venta - precio * ipc_t / ipc_anual(anio)

def irpf_reinversion(venta, ganancia, reinvertido, pendiente=0.0):
    obtenido = venta - pendiente
    frac = min(reinvertido / obtenido, 1.0)
    return frac, ganancia * (1 - frac), cuota_ahorro(ganancia * (1 - frac))

def escenarios():
    venta, g, real = operacion(2007)
    filas = []
    def add(nombre, reinv, pend=0.0, exento_65=False, anio=2007, v=venta, gg=g, rr=real):
        if exento_65:
            frac, base, cuota = 1.0, 0.0, 0.0
        else:
            frac, base, cuota = irpf_reinversion(v, gg, reinv, pend)
        filas.append(dict(escenario=nombre, anio_compra=anio, precio_compra=200_000, precio_venta=round(v),
                          ganancia_nominal=round(gg), resultado_real=round(rr), reinvertido=round(reinv),
                          prestamo_pendiente=round(pend), fraccion_exenta=round(frac, 4), base_gravada=round(base),
                          irpf=round(cuota)))
    add("No reinvierte: pasa a vivir de alquiler (menor de 65)", 0)
    add("Segunda vivienda: no hay exención", 0)
    add("Se muda a una vivienda de 200.000 €", 200_000)
    add("Se muda a una vivienda de 150.000 €", 150_000)
    add("Igual, con 60.000 € de hipoteca pendiente", 150_000, pend=60_000)
    add(f"Compra otra de {es(venta)} € o más", venta)
    add("Mayor de 65 que vende su vivienda habitual", 0, exento_65=True)
    v13, g13, r13 = operacion(2013)
    add("Contraste: compró en 2013 y compra otra más cara", v13, anio=2013, v=v13, gg=g13, rr=r13)
    with open(RAIZ / "data" / "processed" / "grafico7_reinversion.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    return filas

def grafico(filas):
    fig, ax = plt.subplots(figsize=(12, 8.6), dpi=150)
    fig.subplots_adjust(left=0.41, right=0.8, top=0.74, bottom=0.15)
    y = list(range(len(filas)))[::-1]
    tope = max(f["irpf"] for f in filas)
    for yi, f in zip(y, filas):
        contraste = f["anio_compra"] != 2007
        col = RAMPA[2] if contraste else (NARANJA if f["irpf"] > 0 else RAMPA[0])
        ax.barh(yi, f["irpf"], height=0.6, color=col, zorder=3)
        ax.text(f["irpf"] + tope * 0.015, yi, f"{es(f['irpf'])} €", va="center", ha="left", fontsize=12,
                fontweight="bold", color=TINTA)
        r = f["resultado_real"]
        txt = f"pierde {es(-r)} € reales" if r < 0 else f"gana {es(r)} € reales"
        ax.text(1.03, yi, txt, transform=ax.get_yaxis_transform(), va="center", ha="left", fontsize=11,
                color=NARANJA if r < 0 else RAMPA[2])
    ax.axhline(0.5, color=GRID, lw=1, ls="--")
    ax.set_yticks(y, [f["escenario"] for f in filas]); ax.tick_params(axis="y", length=0, labelsize=11.5, colors=TINTA2)
    ax.set_xlim(0, tope * 1.18); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.text(1.03, len(filas) - 0.35, "Resultado real", transform=ax.get_yaxis_transform(), fontsize=10.5, color=MUTED, va="bottom")
    ax.text(0, len(filas) - 0.35, "IRPF a pagar", fontsize=10.5, color=MUTED, va="bottom")
    b = filas[0]
    fig.text(0.04, 0.955, "La exención por reinversión salva al que sube de casa, no al que baja",
             fontsize=19.5, fontweight="bold", ha="left", va="top")
    fig.text(0.04, 0.9,
             f"Vivienda de 200.000 € comprada en 2007 y vendida hoy por {es(b['precio_venta'])} € (evolución media del INE). "
             f"Ganancia en euros: {es(b['ganancia_nominal'])} €.\nEn términos reales, una pérdida de {es(-b['resultado_real'])} €. "
             "Si reinvierte menos de lo obtenido, la ley solo exime la parte proporcional de la ganancia,\n"
             "así que quien se muda a una vivienda más barata sigue pagando IRPF por una ganancia que la inflación ya se ha comido.\n"
             f"Mientras, quien compró en 2013 gana {es(filas[-1]['resultado_real'])} € reales y, si compra otra más cara, no paga nada.",
             fontsize=11.5, color=TINTA2, ha="left", va="top", linespacing=1.5)
    pie(fig, "Fuente: INE (IPV e IPC); arts. 33.4.b y 38.1 de la Ley 35/2006 del IRPF y art. 41.1 de su Reglamento (BOE). Escala del ahorro 2026 de territorio común.\n"
             "Sin gastos de compraventa. Exención proporcional: base gravada = ganancia × (1 − reinvertido / importe obtenido); con préstamo, importe obtenido = venta − principal pendiente.\n"
             f"Requisitos: vivienda habitual (en general, 3 años de residencia) y reinversión en 2 años. Datos y código: {REPO}")
    fig.savefig(SALIDA / "07_reinversion_vivienda_habitual.png")
    plt.close(fig)

if __name__ == "__main__":
    filas = escenarios(); grafico(filas)
    for f in filas: print(f)
