import json
import socket

def send_result(
    origen: str,
    algoritmo: str,
    tiempo: float,
    server_host: str = "127.0.0.1",
    server_port: int = 5000
) -> None:
    """
    Crea un socket hacia (server_host, server_port) y envía un JSON con:
      { "origen": origen, "algoritmo": algoritmo, "tiempo": tiempo }s
    Luego opcionalmente espera un ACK y cierra la conexión.
    """
    paquete = {
        "origen": origen,
        "algoritmo": algoritmo,
        "tiempo": tiempo
    }
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_host, server_port))
        mensaje = json.dumps(paquete).encode("utf-8")
        sock.sendall(mensaje)

    except Exception as e:
        print(f"[Client] Error al enviar resultado: {e}")
    finally:
        sock.close()