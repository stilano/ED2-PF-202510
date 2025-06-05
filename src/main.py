from export.csv_export import export_csv
from export.json_export import export_json
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

if __name__ == "__main__":
    #comparar_exportaciones()
    comparar_sorts()
    print("\n✅ Comparación completada.")
