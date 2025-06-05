# sorting_threads.py

import pandas as pd
import time
import threading
import json
import os

# --- 1. Lectura de datos --------------------------------------------------

def load_csv_cantidad(path_csv: str, column: str = "CANTIDAD", n: int | None = None) -> list[int]:
    """
    Lee las primeras `n` filas del CSV (o todas si n=None) y devuelve la columna `column` como lista de enteros.
    """
    if n is not None:
        df = pd.read_csv(path_csv, usecols=[column], nrows=n)
    else:
        df = pd.read_csv(path_csv, usecols=[column])
    return df[column].astype(int).tolist()

def load_json_cantidad(path_json: str, column: str = "CANTIDAD", n: int | None = None) -> list[int]:
    """
    Lee un JSON en formato lista de objetos y devuelve la columna `column` como lista de enteros,
    limitando a las primeras `n` entradas si n no es None.
    """
    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Si n está definido, tomar solo los primeros n objetos
    if n is not None:
        data = data[:n]
    return [int(item[column]) for item in data]


# --- 2. Algoritmos de ordenamiento -----------------------------------------

def quick_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def counting_sort(arr: list[int]) -> list[int]:
    if not arr:
        return []
    max_val = max(arr)
    if max_val < 0:
        raise ValueError("Counting Sort solo admite enteros no negativos.")
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    sorted_arr = []
    for i, freq in enumerate(count):
        sorted_arr.extend([i] * freq)
    return sorted_arr

def radix_sort(arr: list[int]) -> list[int]:
    if not arr:
        return []
    max_val = max(arr)
    exp = 1
    data = arr.copy()

    def counting_for_radix(a: list[int], exp: int) -> list[int]:
        n = len(a)
        output = [0] * n
        count = [0] * 10  # dígitos 0-9

        for i in range(n):
            index = (a[i] // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            index = (a[i] // exp) % 10
            output[count[index] - 1] = a[i]
            count[index] -= 1
        return output

    while max_val // exp > 0:
        data = counting_for_radix(data, exp)
        exp *= 10

    return data


# --- 3. Función auxiliar para medir tiempo y guardar resultado ---------------

def timed_sort(name: str, func: callable, data: list[int], results: dict):
    """
    Ejecuta `func(data)` y mide el tiempo. Guarda en `results[name]`.
    """
    start = time.time()
    sorted_data = func(data)
    end = time.time()
    results[name] = {
        "time": end - start,
        "sorted": sorted_data
    }
    print(f"[{name}] terminado en {end - start:.4f} segundos")


# --- 4. Ejecutar hilos sobre un solo conjunto de datos -----------------------

def run_sorts_in_threads(data: list[int], prefix: str) -> dict:
    """
    Lanza 4 hilos para ordenar la lista `data` con cada algoritmo:
    Quick Sort, Merge Sort, Counting Sort y Radix Sort.
    `prefix` se usa solo para distinguir en la salida (p.ej. "CSV" o "JSON").
    Retorna un diccionario con los tiempos y resultados de cada algoritmo.
    """
    results = {}
    threads = []

    # Definir cada hilo con su nombre y su función
    algos = {
        f"{prefix}_QuickSort": quick_sort,
        f"{prefix}_MergeSort": merge_sort,
        f"{prefix}_CountingSort": counting_sort,
        f"{prefix}_RadixSort": radix_sort
    }

    for name, func in algos.items():
        t = threading.Thread(target=timed_sort, args=(name, func, data.copy(), results))
        threads.append(t)

    # Iniciar todos los hilos
    for t in threads:
        t.start()
    # Esperar a que terminen
    for t in threads:
        t.join()

    return results


# --- 5. Función principal ----------------------------------------------------

def main():
    # Rutas a tus archivos (ajusta si es necesario)
    path_csv = "ventas.csv"
    path_json = "ventas.json"
    n_limit = 1000000  # Por ejemplo, leer solo las primeras 10 000 filas

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
        print(f"  • {name}: {info['time']:.4f} s (primeros 5 ordenados: {info['sorted'][:5]})")

    # 3) Ejecutar ordenamientos en hilos para JSON
    print("\nIniciando ordenamientos en paralelo sobre JSON...\n")
    results_json = run_sorts_in_threads(data_json, prefix="JSON")

    print("\nResultados (JSON):")
    for name, info in results_json.items():
        print(f"  • {name}: {info['time']:.4f} s (primeros 5 ordenados: {info['sorted'][:5]})")


if __name__ == "__main__":
    main()
