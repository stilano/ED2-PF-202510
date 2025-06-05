import time
import threading
from sort_algorithms.sort import algorithms
from sockets.client_side import send_result
from typing import List, Dict, Callable

def timed_sort(
    name: str,
    func: Callable[[List[int]], List[int]],
    data: List[int],
    results: Dict[str, dict],
    server_host: str,
    server_port: int
) -> None:
    """
    Ejecuta func(data), mide el tiempo, guarda en results[name], y envía
    {"origen", "algoritmo", "tiempo"} al servidor de sockets.
    - name:    "<prefix>_<AlgorithmName>" (p.ej. "CSV_QuickSort")
    - func:    función de ordenamiento
    - data:    copia de la lista original
    - results: diccionario compartido donde se guarda la salida
    - server_host, server_port: para connectar al servidor
    """

    # 1) Separar <prefix> y <AlgorithmName> de name
    if "_" in name:
        origen, algoritmo = name.split("_", 1)
    else:
        # Si no se encuentra "_", asumimos que el caller solo pasó "QuickSort" (sin prefijo).
        # En ese caso, dejamos origen como "UNKNOWN" o como el mismo name, según prefieras.
        origen = "UNKNOWN"
        algoritmo = name

    # 2) Medir el tiempo de ordenamiento
    start = time.time()
    sorted_data = func(data)
    end = time.time()
    elapsed = end - start

    # 3) Guardar localmente en el diccionario results
    results[name] = {
        "time": elapsed,
        "sorted": sorted_data
    }
    print(f"[Thread:{name}] → Tiempo: {elapsed:.4f} s")

    # 4) Enviar el resultado al servidor via sockets
    #    (sólo enviamos el tiempo, no la lista completa para no saturar el socket)
    send_result(
        origen=origen,
        algoritmo=algoritmo,
        tiempo=elapsed,
        server_host=server_host,
        server_port=server_port
    )

def run_sorts_in_threads(
    data: List[int],
    prefix: str,
    server_host: str = "127.0.0.1",
    server_port: int = 5000
) -> Dict[str, dict]:
    """
    Lanza 4 hilos para ordenar `data` con cada algoritmo:
      - QuickSort
      - MergeSort
      - CountingSort
      - RadixSort

    Cada hilo invoca a `timed_sort(name, func, data.copy(), results, server_host, server_port)`.
    `prefix` se usa para nombrar cada hilo (“CSV” o “JSON”).
    Retorna `results`, un diccionario con la forma:
      {
        "CSV_QuickSort":   { "time": ..., "sorted": [...] },
        "CSV_MergeSort":   { "time": ..., "sorted": [...] },
        "CSV_CountingSort":{ "time": ..., "sorted": [...] },
        "CSV_RadixSort":   { "time": ..., "sorted": [...] }
      }
    """

    results: Dict[str, dict] = {}
    threads: List[threading.Thread] = []

    # 2) Crear un hilo por cada algoritmo
    for algo_name, func in algorithms.items():
        # Combinar el prefijo y el nombre del algoritmo
        full_name = f"{prefix}_{algo_name}"
        copia_data = data.copy()
        hilo = threading.Thread(
            target=timed_sort,
            args=(full_name, func, copia_data, results, server_host, server_port)
        )
        threads.append(hilo)


    # 3) Iniciar todos los hilos
    for hilo in threads:
        hilo.start()

    # 4) Esperar a que terminen
    for hilo in threads:
        hilo.join()

    return results

