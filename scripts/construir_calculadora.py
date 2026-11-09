"""Genera calculadora/index.html con el IPC mensual del INE incrustado.

Desde enero de 2002 usa el índice oficial (base 2025). Antes, lo reconstruye hacia atrás con la variación
mensual oficial (redondeada a un decimal), por lo que esos años son aproximados.
Uso: python scripts/construir_calculadora.py
"""
import csv, json, pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
idx = {r["fecha"]: float(r["indice_base2025"])
       for r in csv.DictReader(open(RAIZ / "data" / "raw" / "ine_ipc_indice_general_mensual.csv", encoding="utf-8"))}
var = {r["fecha"]: float(r["variacion_mensual_pct"]) / 100
       for r in csv.DictReader(open(RAIZ / "data" / "raw" / "ine_ipc_variacion_mensual.csv", encoding="utf-8"))}
ultimo = max(idx)
serie = dict(idx)
y, m = 2002, 1
while (y, m) > (1961, 1):
    f = f"{y}-{m:02d}"
    y2, m2 = (y, m - 1) if m > 1 else (y - 1, 12)
    serie[f"{y2}-{m2:02d}"] = serie[f] / (1 + var[f])
    y, m = y2, m2
serie = {k: round(v, 4) for k, v in sorted(serie.items())}
html = (RAIZ / "calculadora" / "plantilla.html").read_text(encoding="utf-8")
html = html.replace("__IPC__", json.dumps(serie, separators=(",", ":"))).replace("__ULTIMO__", json.dumps(ultimo))
(RAIZ / "calculadora" / "index.html").write_text(html, encoding="utf-8")
print(f"calculadora/index.html: {len(serie)} meses ({min(serie)} a {ultimo})")
