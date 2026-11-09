"""Descarga la serie oficial del IPC del INE y la guarda en CSV.

Fuente: INE, API Tempus3. Serie IPC290751 «Nacional. Índice general. Índice», base 2025.
Uso: python scripts/descargar_ipc.py
"""
import csv, json, pathlib, urllib.request
from datetime import date

SERIE = "IPC290751"
URL = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{SERIE}?date=19610101:20991231&tip=A"
RAIZ = pathlib.Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "data" / "raw" / "ine_ipc_indice_general_mensual.csv"

def main():
    with urllib.request.urlopen(URL, timeout=60) as r:
        serie = json.load(r)
    datos = sorted(serie["Data"], key=lambda x: (x["Anyo"], x["T3_Periodo"]))
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "indice_base2025", "tipo_dato"])
        for d in datos:
            w.writerow([f'{d["Anyo"]}-{d["T3_Periodo"][1:]}', d["Valor"], d["T3_TipoDato"]])
    print(f"{serie['Nombre'].strip()} | {len(datos)} meses | "
          f"{datos[0]['Anyo']}-{datos[0]['T3_Periodo'][1:]} a {datos[-1]['Anyo']}-{datos[-1]['T3_Periodo'][1:]} | "
          f"descargado {date.today().isoformat()} -> {SALIDA.relative_to(RAIZ)}")

if __name__ == "__main__":
    main()
