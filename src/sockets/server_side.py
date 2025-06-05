import socket
import threading
import json

# Diccionario global para almacenar tiempos recibidos:
# { "CSV": { "QuickSort": 0.0234, "MergeSort": 0.0117, … },
#   "JSON": { … } }
resultados_recibidos = {}

def manejar_cliente(conn, addr):
    try:
        # Esperar a que el cliente envíe todos los datos (hasta EOF)
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

        # Parsear JSON recibido
        mensaje = json.loads(data.decode("utf-8"))
        origen    = mensaje["origen"]       # "CSV" o "JSON"
        algoritmo = mensaje["algoritmo"]    # "QuickSort", etc.
        tiempo    = mensaje["tiempo"]       # float

        # Guardar en resultados_recibidos
        if origen not in resultados_recibidos:
            resultados_recibidos[origen] = {}
        resultados_recibidos[origen][algoritmo] = tiempo

        print(f"[Servidor] Recibido de {addr}: {origen} - {algoritmo} en {tiempo:.4f} s")

        # Opcional: responder un ACK
        respuesta = { "status": "OK", "recibido": True }
        conn.send(json.dumps(respuesta).encode("utf-8"))

        # (Opcional) Si ya recibimos los 4 algoritmos de este origen, podemos mostrar un resumen:
        if len(resultados_recibidos[origen]) == 4:
            print(f"\n>>> Todos los resultados para {origen} ya llegaron:")
            for algo, t in resultados_recibidos[origen].items():
                print(f"    • {algo}: {t:.4f} s")
            print(">>> Fin del resumen para", origen, "\n")

    except Exception as e:
        print("[Servidor] Error al manejar cliente:", e)
    finally:
        conn.close()

def iniciar_servidor(host="0.0.0.0", port=5000):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind((host, port))
    serv.listen()

    print(f"[Servidor] Escuchando en {host}:{port} ...")
    while True:
        conn, addr = serv.accept()
        # Atender cada cliente en un hilo separado
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.daemon = True
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
