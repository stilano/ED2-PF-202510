from export.csv_export import export_csv
from export.json_export import export_json
import os
import json
import pandas as pd
from typing import Dict, List

# 1. Importamos los loaders para CSV y JSON, ajustando la ruta al nombre real de tus módulos
from load.loadcsv import load_csv_cantidad
from load.loadjson import load_json_cantidad

# 2. Importamos run_sorts_in_threads (el que arranca los hilos y envía por sockets)
from threading_custom.threading_ed2 import run_sorts_in_threads

def comparar_exportaciones():
    """
    Compara los resultados de exportar datos en formato CSV y JSON.
    Llama a las funciones `export_csv()` y `export_json()` para obtener los resultados de exportación en ambos formatos.
    Imprime en consola el formato, el tiempo de exportación y el tamaño del archivo generado para cada uno.
    Retorna:
        None
    """
    csv_resultado = export_csv()
    json_resultado = export_json()

    print("\n📊 RESULTADOS DE EXPORTACIÓN:")
    for resultado in [csv_resultado, json_resultado]:
        print(f"\nFormato: {resultado['formato']}")
        print(f"  ⏱ Tiempo: {resultado['tiempo']:.4f} segundos")
        print(f"  📦 Tamaño: {resultado['tamano_kb']:.2f} KB")

def comparar_sorts():
    """
    Compara el rendimiento de diferentes algoritmos de ordenamiento sobre datos de cantidad de ventas cargados desde archivos CSV y JSON.
    Esta función realiza los siguientes pasos:
    1. Verifica la existencia de los archivos 'ventas.csv' y 'ventas.json' en el directorio actual.
    2. Carga hasta 1,000,000 de registros de la columna "CANTIDAD" de cada archivo.
    3. Ejecuta múltiples algoritmos de ordenamiento en hilos paralelos sobre los datos cargados de ambas fuentes (CSV y JSON).
    4. Imprime el tiempo de ejecución de cada algoritmo de ordenamiento para ambas fuentes de datos.
    Dependencias:
        - load.loadcsv.load_csv_cantidad: Función para cargar la columna "CANTIDAD" de un archivo CSV.
        - load.loadjson.load_json_cantidad: Función para cargar la columna "CANTIDAD" de un archivo JSON.
        - threading_custom.threading_ed2.run_sorts_in_threads: Función para ejecutar algoritmos de ordenamiento en hilos paralelos.
    Retorna:
        Nada.
    """
    
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

    # 1. Se lee columna "cantidad" de cada archivo, limitando a n_limit
    print("Leyendo CSV (primeras filas)...")
    data_csv = load_csv_cantidad(path_csv, column="CANTIDAD", n=n_limit)
    print(f"Se obtuvieron {len(data_csv)} registros del CSV.\n")

    print("Leyendo JSON (primeras filas)...")
    data_json = load_json_cantidad(path_json, column="CANTIDAD", n=n_limit)
    print(f"Se obtuvieron {len(data_json)} registros del JSON.\n")

    # 2) Se ejecutan ordenamientos en hilos para CSV
    print("Iniciando ordenamientos en paralelo sobre CSV...\n")
    results_csv = run_sorts_in_threads(data_csv, prefix="CSV")

    print("\nResultados (CSV):")
    for name, info in results_csv.items():
        print(f"  • {name}: {info['time']:.4f} s")

    # 3. Se ejecutan ordenamientos en hilos para JSON
    print("\nIniciando ordenamientos en paralelo sobre JSON...\n")
    results_json = run_sorts_in_threads(data_json, prefix="JSON")

    print("\nResultados (JSON):")
    for name, info in results_json.items():
        print(f"  • {name}: {info['time']:.4f} s")
        
def conexion_cliente_servidor():
    """
    Realiza la conexión cliente-servidor para procesar y ordenar datos de ventas desde archivos CSV y JSON.
    Este procedimiento realiza las siguientes acciones:
    1. Verifica la existencia de los archivos 'ventas.csv' y 'ventas.json'.
    2. Carga la columna "CANTIDAD" de ambos archivos, con opción de limitar el número de registros.
    3. Ejecuta en paralelo cuatro algoritmos de ordenamiento sobre los datos de cada archivo y envía los tiempos de ejecución al servidor mediante sockets.
    4. Muestra un resumen de los tiempos de ejecución para cada algoritmo y archivo.
    5. Guarda las listas ordenadas en archivos separados (CSV y JSON).
    6. Retorna los resultados de los ordenamientos en memoria para su uso posterior.
    Returns:
        Tuple[Dict[str, dict], Dict[str, dict]]: 
            - Un diccionario con los resultados de los algoritmos sobre el archivo CSV.
            - Un diccionario con los resultados de los algoritmos sobre el archivo JSON.
    """

    path_csv  = "ventas.csv"
    path_json = "ventas.json"
    n_limit   = 10000

    # Verificamos que existan ambos archivos
    if not os.path.exists(path_csv) or not os.path.exists(path_json):
        print("Error: no se encontró 'ventas.csv' o 'ventas.json' en el directorio.")
        return {}, {}

    
    # 1. Cargamos la columna "cantidad" de cada archivo
    print("Leyendo CSV...")
    data_csv: List[int] = load_csv_cantidad(path_csv, column="CANTIDAD", n=n_limit)
    print(f"  → {len(data_csv)} registros cargados desde CSV.\n")

    print("Leyendo JSON...")
    data_json: List[int] = load_json_cantidad(path_json, column="CANTIDAD", n=n_limit)
    print(f"  → {len(data_json)} registros cargados desde JSON.\n")

    
    # 2. Ejecutamos los 4 algoritmos en paralelo sobre CSV y enviar tiempos por socket
    print("Medimos el tiempo de conexion al servidor para cada sort en CSV...\n")
    results_csv: Dict[str, dict] = run_sorts_in_threads(
        data=data_csv,
        prefix="CSV",
        server_host="127.0.0.1",  # Ajusta si tu servidor corre en otra IP
        server_port=5000          # Debe coincidir con el puerto en server_side.py
    )

    
    # 3. Ejecutamos los 4 algoritmos en paralelo sobre JSON y enviar tiempos por socket
    print("Medimos el tiempo de conexion al servidor para cada sort en JSON...\n")
    results_json: Dict[str, dict] = run_sorts_in_threads(
        data=data_json,
        prefix="JSON",
        server_host="127.0.0.1",
        server_port=5000
    )

    
    # 4. Se muestra un breve resumen de tiempos y tamaño de cada lista ordenada
    
    print("\n--- Resumen de tiempos (CSV) ---")
    for name, info in results_csv.items():
        print(f"  • {name}: {info['time']:.4f} s")

    print("\n--- Resumen de tiempos (JSON) ---")
    for name, info in results_json.items():
        print(f"  • {name}: {info['time']:.4f} s")

    
    # 5) Guardamos cada lista ordenada en disco
    
    for name, info in results_csv.items():
        # Guardar en CSV de una sola columna
        df_out = pd.DataFrame({"cantidad_ordenada": info["sorted"]})
        out_csv  = f"{name}_sorted.csv"
        df_out.to_csv(out_csv, index=False)

        print(f"  → Guardado: {out_csv}")

    for name, info in results_json.items():
        # Guardar en JSON de una sola columna
        out_json = f"{name}_sorted.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(info["sorted"], f, ensure_ascii=False)

        print(f"  → Guardado: {out_json}")

    
    # 6) Retornamos los resultados en memoria para cualquier uso posterior
    
    return results_csv, results_json
    
if __name__ == "__main__":
    comparar_exportaciones()
    comparar_sorts()
    results_csv, results_json = conexion_cliente_servidor()
