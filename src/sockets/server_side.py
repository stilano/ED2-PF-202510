import socket          # Para crear sockets de red
import threading       # Para manejar múltiples hilos de ejecución
import json            # Para codificar/decodificar mensajes JSON

# Diccionario para almacenar los tiempos recibidos de cada origen (CSV o JSON).
resultados_recibidos = {}

# Conjunto para llevar registro de qué origenes ya se han resumido (evita resúmenes duplicados).
resumen_mostrado = set()

# Lock para sincronizar el acceso a 'resultados_recibidos' y 'resumen_mostrado' entre hilos
lock = threading.Lock()


def manejar_cliente(conn, addr):
    """
    Función que se ejecuta en un hilo separado para atender a un cliente específico.
    - conn: socket de conexión con el cliente.
    - addr: dirección del cliente (tupla (IP, puerto)).
    Se encarga de:
      1) Recibir el JSON con los datos de origen, algoritmo y tiempo.
      2) Almacenar el tiempo en 'resultados_recibidos' de forma sincronizada.
      3) Mostrar un resumen si ya se recibieron los 4 algoritmos de ese origen.
      4) Enviar un ACK al cliente.
    """
    try:
        # 1. Recibimos todos los datos enviados por el cliente.
        data = b""
        while True:
            packet = conn.recv(4096)  # Se reciben hasta 4096 bytes
            if not packet:
                # Si no hay más datos, rompemos el bucle de recepción
                break
            data += packet

        # 2. Se convierten los bytes recibidos a cadena y parsear JSON
        mensaje = json.loads(data.decode("utf-8"))
        origen = mensaje["origen"]         # "CSV" o "JSON"
        algoritmo = mensaje["algoritmo"]   # Nombre del algoritmo (ej. "QuickSort")
        tiempo = mensaje["tiempo"]         # Tiempo de ejecución del algoritmo en segundos

        # 3. Bloqueamos acceso a variables compartidas para evitar condiciones de carrera
        with lock:
            # Si es la primera vez que recibimos datos para este origen, creamos la clave
            if origen not in resultados_recibidos:
                resultados_recibidos[origen] = {}
            # Guardamos el tiempo del algoritmo dentro del diccionario
            resultados_recibidos[origen][algoritmo] = tiempo

            # Se muestra en consola que recibimos los datos de este cliente
            print(f"[Servidor] Recibido de {addr}: {origen} - {algoritmo} en {tiempo:.4f} s")

            # 4) Si ya tenemos los 4 algoritmos para este mismo origen y aún no mostramos el resumen:
            if len(resultados_recibidos[origen]) == 4 and origen not in resumen_mostrado:
                # Generar y mostrar el resumen de tiempos para este origen
                mostrar_resumen(origen, resultados_recibidos[origen])
                # Marcar que ya mostramos el resumen para este origen
                resumen_mostrado.add(origen)

    except Exception as e:
        # Si ocurre cualquier error (JSON mal formado, error de socket, etc.), lo imprimimos
        print("[Servidor] Error al manejar cliente:", e)

    finally:
        # 6. Cerrar la conexión en cualquier caso para liberar recursos
        conn.close()


def mostrar_resumen(origen, resultados):
    """
    Imprime en consola un resumen ordenado de los tiempos
    de los cuatro algoritmos para un origen dado (CSV o JSON).
    - origen: cadena "CSV" o "JSON"
    - resultados: diccionario { "QuickSort": 0.03, "MergeSort": 0.04, ... }
    """
    print(f"\n>>> Todos los resultados para {origen} ya llegaron:")
    # Ordenamos los algoritmos alfabéticamente para consistencia
    for algo, t in sorted(resultados.items()):
        print(f"    • {algo}: {t:.4f} s")
    print(f">>> Fin del resumen para {origen}\n")


def iniciar_servidor(host="0.0.0.0", port=5000):
    """
    Función principal para iniciar el servidor:
      1) Crea un socket TCP y lo configura.
      2) Se queda en un bucle aceptando clientes entrantes.
      3) Para cada cliente aceptado, arranca un hilo con 'manejar_cliente'.
    Parámetros opcionales:
      - host: dirección IP donde escucha (por defecto 0.0.0.0 para escuchar en todas las interfaces).
      - port: puerto TCP donde escucha (por defecto 5000).
    """
    # 1. Creamos el socket
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Se permite reutilizar la dirección inmediatamente tras cerrar (evita 'Address already in use')
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Asignamos el socket a (host, port)
    serv.bind((host, port))
    # Ponemos el socket en modo escucha, sin límite estricto de cola
    serv.listen()

    print(f"[Servidor] Escuchando en {host}:{port} ...")

    # 2. Bucle principal: se aceptan conexiones entrantes
    while True:
        conn, addr = serv.accept()  # Espera bloqueante hasta que un cliente se conecte
        # 3. Para cada cliente, se arranca un hilo que ejecute 'manejar_cliente'
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.daemon = True  # Se marca el hilo para que no bloquee el cierre del programa
        hilo.start()        # Iniciamos el hilo


if __name__ == "__main__":
    # Solo se ejecuta si el archivo se invoca directamente (no si se importa como módulo)
    iniciar_servidor()

