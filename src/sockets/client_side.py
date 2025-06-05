import json    # Para serializar el diccionario a formato JSON
import socket  # Para crear sockets y comunicarse con el servidor

def send_result(
    origen: str,
    algoritmo: str,
    tiempo: float,
    server_host: str = "127.0.0.1",
    server_port: int = 5000
) -> None:
    """
    Crea un socket  hacia (server_host, server_port) y envía un JSON con:
      {
        "origen": origen,       # Por ejemplo, "CSV" o "JSON"
        "algoritmo": algoritmo, # Por ejemplo, "QuickSort"
        "tiempo": tiempo        # Tiempo de ejecución en segundos
      }
    Luego cierra la conexión. Si ocurre un error, lo informa por pantalla.

    Parámetros:
    - origen: Identifica el formato de datos de origen (CSV o JSON).
    - algoritmo: Nombre del algoritmo de ordenamiento.
    - tiempo: Tiempo de ejecución en segundos (float).
    - server_host: Dirección IP o hostname del servidor (por defecto "127.0.0.1").
    - server_port: Puerto en el que el servidor está escuchando (por defecto 5000).
    """

    # 1. Empaquetamos los datos en un diccionario
    paquete = {
        "origen": origen,
        "algoritmo": algoritmo,
        "tiempo": tiempo
    }

    try:
        # 2. Creamos un socket 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 3. Conectamos al servidor especificado
        sock.connect((server_host, server_port))
        # 4. Convertir el diccionario a cadena JSON y luego a bytes UTF-8
        mensaje = json.dumps(paquete).encode("utf-8")
        # 5. Enviar todos los bytes al servidor
        sock.sendall(mensaje)

    except Exception as e:
        # Si ocurre cualquier excepción durante la conexión o el envío, se informa
        print(f"[Client] Error al enviar resultado: {e}")
    finally:
        # 6. Cerramos el socket para liberar recursos
        sock.close()



