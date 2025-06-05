from export.csv_export import export_csv
from export.json_export import export_json
import os
import json
import pandas as pd
from typing import Dict, List

# 1) Importa tus loaders para CSV y JSON, ajustando la ruta al nombre real de tus módulos
#    Por ejemplo, si tu loader CSV está en src/loaders/csv_loader.py:
from load.loadcsv import load_csv_cantidad
#    Y tu loader JSON está en src/loaders/json_loader.py:
from load.loadjson import load_json_cantidad

# 2) Importa run_sorts_in_threads (el que arranca los hilos y envía por sockets)
from threading_custom.threading_ed2 import run_sorts_in_threads

def comparar_exportaciones():
    csv_resultado = export_csv()
    json_resultado = export_json()

    print("\n📊 RESULTADOS DE EXPORTACIÓN:")
    for resultado in [csv_resultado, json_resultado]:
        print(f"\nFormato: {resultado['formato']}")
        print(f"  ⏱ Tiempo: {resultado['tiempo']:.4f} segundos")
        print(f"  📦 Tamaño: {resultado['tamano_kb']:.2f} KB")

def comparar_sorts():
    
    import os
    from load.loadcsv import load_csv_cantidad
    from load.loadjson import load_json_cantidad
    from threading_custom.threading_ed2 import run_sorts_in_threads

    path_csv = "ventas.csv"
    path_json = "ventas.json"
    n_limit = 1000000  # Limitar a 1 millón de registros

    if not os.path.exists(path_csv) or not os.path.exists(path_json):
        print("No se encontraron los archivos 'ventas.csv' y/o 'ventas.json' en el directorio.")
        return

    # 1) Leer columna "cantidad" de cada archivo, limitando a n_limit
    print("Leyendo CSV (primeras filas)...")
    data_csv = load_csv_cantidad(path_csv, column="CANTIDAD", n=n_limit)
    print(f"Se obtuvieron {len(data_csv)} registros del CSV.\n")

    print("Leyendo JSON (primeras filas)...")
    data_json = load_json_cantidad(path_json, column="CANTIDAD", n=n_limit)
    print(f"Se obtuvieron {len(data_json)} registros del JSON.\n")

    # 2) Ejecutar ordenamientos en hilos para CSV
    print("Iniciando ordenamientos en paralelo sobre CSV...\n")
    results_csv = run_sorts_in_threads(data_csv, prefix="CSV")

    print("\nResultados (CSV):")
    for name, info in results_csv.items():
        print(f"  • {name}: {info['time']:.4f} s")

    # 3) Ejecutar ordenamientos en hilos para JSON
    print("\nIniciando ordenamientos en paralelo sobre JSON...\n")
    results_json = run_sorts_in_threads(data_json, prefix="JSON")

    print("\nResultados (JSON):")
    for name, info in results_json.items():
        print(f"  • {name}: {info['time']:.4f} s")
        
def main():
    # -- Ajusta estas rutas a donde tengas 'ventas.csv' y 'ventas.json' --
    path_csv  = "ventas.csv"
    path_json = "ventas.json"
    # Si quieres limitar la cantidad de registros que lees, pon un número (p.ej. 10000).
    # Si prefieres leer el archivo completo, deja n_limit = None.
    n_limit   = 10000

    # Verifica que existan ambos archivos
    if not os.path.exists(path_csv) or not os.path.exists(path_json):
        print("Error: no se encontró 'ventas.csv' o 'ventas.json' en el directorio.")
        return {}, {}

    # ---------------------------
    # 1) Cargar la columna "cantidad" de cada archivo
    # ---------------------------
    print("Leyendo CSV...")
    data_csv: List[int] = load_csv_cantidad(path_csv, column="CANTIDAD", n=n_limit)
    print(f"  → {len(data_csv)} registros cargados desde CSV.\n")

    print("Leyendo JSON...")
    data_json: List[int] = load_json_cantidad(path_json, column="CANTIDAD", n=n_limit)
    print(f"  → {len(data_json)} registros cargados desde JSON.\n")

    # ---------------------------
    # 2) Ejecutar los 4 algoritmos en paralelo sobre CSV y enviar tiempos por socket
    # ---------------------------
    print("Ordenando CSV en paralelo y enviando resultados al servidor...\n")
    results_csv: Dict[str, dict] = run_sorts_in_threads(
        data=data_csv,
        prefix="CSV",
        server_host="127.0.0.1",  # Ajusta si tu servidor corre en otra IP
        server_port=5000          # Debe coincidir con el puerto en server_side.py
    )

    # ---------------------------
    # 3) Ejecutar los 4 algoritmos en paralelo sobre JSON y enviar tiempos por socket
    # ---------------------------
    print("\nOrdenando JSON en paralelo y enviando resultados al servidor...\n")
    results_json: Dict[str, dict] = run_sorts_in_threads(
        data=data_json,
        prefix="JSON",
        server_host="127.0.0.1",
        server_port=5000
    )

    # ---------------------------
    # 4) Mostrar un breve resumen de tiempos y tamaño de cada lista ordenada
    # ---------------------------
    print("\n--- Resumen de tiempos (CSV) ---")
    for name, info in results_csv.items():
        print(f"  • {name}: {info['time']:.4f} s  (n={len(info['sorted'])})")

    print("\n--- Resumen de tiempos (JSON) ---")
    for name, info in results_json.items():
        print(f"  • {name}: {info['time']:.4f} s  (n={len(info['sorted'])})")

    # ---------------------------
    # 5) (Opcional) Guardar cada lista ordenada en disco
    #    Por ejemplo: "CSV_QuickSort_sorted.csv" y "CSV_QuickSort_sorted.json"
    # ---------------------------
    for name, info in results_csv.items():
        # Guardar en CSV de una sola columna
        df_out = pd.DataFrame({"cantidad_ordenada": info["sorted"]})
        out_csv  = f"{name}_sorted.csv"
        df_out.to_csv(out_csv, index=False)

        # Guardar en JSON como array simple
        out_json = f"{name}_sorted.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(info["sorted"], f, ensure_ascii=False)

        print(f"  → Guardado: {out_csv}, {out_json}")

    for name, info in results_json.items():
        df_out = pd.DataFrame({"cantidad_ordenada": info["sorted"]})
        out_csv  = f"{name}_sorted.csv"
        df_out.to_csv(out_csv, index=False)

        out_json = f"{name}_sorted.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(info["sorted"], f, ensure_ascii=False)

        print(f"  → Guardado: {out_csv}, {out_json}")

    # ---------------------------
    # 6) Retornar los resultados en memoria para cualquier uso posterior
    # ---------------------------
    return results_csv, results_json

if __name__ == "__main__":
    #comparar_exportaciones()
    comparar_sorts()
    results_csv, results_json = main()
   
    # Ejemplo de cómo acceder a los resultados ordenados:
    #   results_csv["CSV_QuickSort"]["sorted"]  → lista completa ordenada por QuickSort (CSV)
    if "CSV_QuickSort" in results_csv:
        primeros_10 = results_csv["CSV_QuickSort"]["sorted"][:10]
        print("\nPrimeros 10 valores ordenados (QuickSort sobre CSV):", primeros_10)
