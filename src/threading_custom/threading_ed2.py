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
    Ejecuta un algoritmo de ordenamiento sobre `data`, mide el tiempo que tarda,
    almacena el resultado en el diccionario `results[name]` y envía un mensaje al
    servidor de sockets con la información de origen, algoritmo y tiempo.

    Parámetros:
    - name:         Cadena con el formato "<prefix>_<AlgorithmName>" (p.ej. "CSV_QuickSort").
                    Usamos el prefijo para distinguir si viene de CSV o JSON.
    - func:         Función de ordenamiento (QuickSort, MergeSort, etc.).
    - data:         Lista de enteros que se va a ordenar. Se pasa una copia para no
                    alterar `data` en otros hilos.
    - results:      Diccionario compartido (global) donde guardaremos:
                        results[name] = { "time": <float>, "sorted": <lista ordenada> }.
                    Nota: dicho diccionario NO es thread-safe; estamos asumiendo
                    que no habrá conflictos de escritura concurrente en claves diferentes.
    - server_host:  IP o hostname del servidor de sockets.
    - server_port:  Puerto donde el servidor está escuchando.
    """

    # 1. Separamos el prefijo (origen) y el nombre del algoritmo
    #    Si name = "CSV_QuickSort", split obtiene ["CSV", "QuickSort"].
    if "_" in name:
        origen, algoritmo = name.split("_", 1)
    else:
        # Si no se encuentra "_", dejamos origen en "UNKNOWN"
        origen = "UNKNOWN"
        algoritmo = name

    # 2. Medimos tiempo de ejecución del algoritmo
    start = time.time()
    sorted_data = func(data)  # Ejecuta el algoritmo sobre la copia de la lista
    end = time.time()
    elapsed = end - start

    # 3. Guardamos localmente en el diccionario `results`
    #    Al terminar, results[name] contendrá {"time": elapsed, "sorted": sorted_data}.
    #    Esto permite consultar más tarde los tiempos y los datos ordenados.
    results[name] = {
        "time": elapsed,
        "sorted": sorted_data
    }
    print(f"[Thread:{name}] → Tiempo: {elapsed:.4f} s")

    # 4. Enviamos al servidor de sockets solo la información necesaria:
    #    origen (CSV/JSON), algoritmo ("QuickSort", ...), y tiempo (float).
    #    NO enviamos la lista completa para no saturar la red con datos grandes.
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
    Lanza múltiples hilos para ordenar la misma lista `data` con cada uno de los algoritmos
    disponibles: QuickSort, MergeSort, CountingSort y RadixSort. Cada hilo invoca a timed_sort().

    Parámetros:
    - data:         Lista de enteros a ordenar.
    - prefix:       Cadena que indica el origen de los datos ("CSV" o "JSON"), se utilizará para
                    nombrar los hilos y distinguir los resultados.
    - server_host:  IP o hostname del servidor de sockets (por defecto "127.0.0.1").
    - server_port:  Puerto donde el servidor está escuchando (por defecto 5000).

    Retorna:
    - results: Diccionario con la siguiente estructura:
        {
            "CSV_QuickSort":    { "time": <float>, "sorted": <list[int]> },
            "CSV_MergeSort":    { ... },
            "CSV_CountingSort": { ... },
            "CSV_RadixSort":    { ... }
        }
      donde cada clave es "<prefix>_<AlgorithmName>".
    """

    # Este diccionario contendrá el tiempo y array ordenado de cada hilo.
    results: Dict[str, dict] = {}

    # Lista para almacenar los objetos Thread creados
    threads: List[threading.Thread] = []

    # 1. Por cada algoritmo disponible en el diccionario `algorithms`:
    #    - Construimos un nombre completo: "<prefix>_<algo_name>"
    #    - Creamos una copia de `data` para que cada hilo trabaje en su propia lista.
    #    - Instanciamos un Thread que llame a timed_sort con los parámetros necesarios.
    for algo_name, func in algorithms.items():
        full_name = f"{prefix}_{algo_name}"
        copia_data = data.copy()  # Copia superficial de la lista original
        hilo = threading.Thread(
            target=timed_sort,
            args=(full_name, func, copia_data, results, server_host, server_port)
        )
        threads.append(hilo)

    # 2. Iniciamos todos los hilos
    for hilo in threads:
        hilo.start()

    # 3. Esperamos a que cada hilo termine su ejecución antes de continuar
    for hilo in threads:
        hilo.join()

    # 4. Al salir de aquí, `results` contendrá todos los tiempos y arrays ordenados
    return results


