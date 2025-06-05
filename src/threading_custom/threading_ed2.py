import time
import threading
from sort_algorithms.sort import algorithms

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

def run_sorts_in_threads(data: list[int], prefix: str) -> dict:
    """
    Lanza 4 hilos para ordenar la lista `data` con cada algoritmo:
    Quick Sort, Merge Sort, Counting Sort y Radix Sort.
    `prefix` se usa solo para distinguir en la salida (p.ej. "CSV" o "JSON").
    Retorna un diccionario con los tiempos y resultados de cada algoritmo.
    """
    results = {}
    threads = []

    for name, func in algorithms.items():
        t = threading.Thread(target=timed_sort, args=(name, func, data.copy(), results))
        threads.append(t)

    # Iniciar todos los hilos
    for t in threads:
        t.start()
    # Esperar a que terminen
    for t in threads:
        t.join()

    return results

