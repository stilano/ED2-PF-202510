import socket
import threading
import json

# Diccionario global para almacenar tiempos recibidos
resultados_recibidos = {}
resumen_mostrado = set()
lock = threading.Lock()  # Lock para sincronización

def manejar_cliente(conn, addr):
    try:
        # Recibir datos del cliente
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

        # Parsear JSON recibido
        mensaje = json.loads(data.decode("utf-8"))
        origen = mensaje["origen"]       # "CSV" o "JSON"
        algoritmo = mensaje["algoritmo"]    # "QuickSort", etc.
        tiempo = mensaje["tiempo"]       # float

        with lock:
            # Guardar en resultados_recibidos
            if origen not in resultados_recibidos:
                resultados_recibidos[origen] = {}
            resultados_recibidos[origen][algoritmo] = tiempo

            print(f"[Servidor] Recibido de {addr}: {origen} - {algoritmo} en {tiempo:.4f} s")

            # Mostrar resumen si se recibieron los 4 algoritmos
            if len(resultados_recibidos[origen]) == 4 and origen not in resumen_mostrado:
                mostrar_resumen(origen, resultados_recibidos[origen])
                resumen_mostrado.add(origen)

        # Responder un ACK
        respuesta = {"status": "OK", "recibido": True}
        conn.send(json.dumps(respuesta).encode("utf-8"))

    except Exception as e:
        print("[Servidor] Error al manejar cliente:", e)
    finally:
        conn.close()

def mostrar_resumen(origen, resultados):
    """
    Genera un resumen organizado para un origen específico (CSV o JSON).
    """
    print(f"\n>>> Todos los resultados para {origen} ya llegaron:")
    for algo, t in sorted(resultados.items()):  # Ordenar algoritmos alfabéticamente
        print(f"    • {algo}: {t:.4f} s")
    print(f">>> Fin del resumen para {origen}\n")

def iniciar_servidor(host="0.0.0.0", port=5000):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind((host, port))
    serv.listen()

    print(f"[Servidor] Escuchando en {host}:{port} ...")
    while True:
        conn, addr = serv.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.daemon = True
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
