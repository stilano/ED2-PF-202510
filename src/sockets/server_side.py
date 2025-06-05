import socket
import threading
import json

# --- Función para manejar la conexión de cada cliente ---
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        print(f"Connection from {self.clientAddress}")
        try:
            # Recibir el nombre del algoritmo (p.ej., "QuickSort")
            file_name = self.csocket.recv(1024).decode()
            if not file_name:
                print("[ERROR] Nombre del algoritmo vacío")
                return
            
            # Recibir los datos (tiempo y resultados ordenados) en fragmentos
            data = b""
            while True:
                part = self.csocket.recv(1024)  # Leer por partes
                data += part
                if len(part) < 1024:  # Si el paquete recibido es menor de 1024, es el final
                    break

            if not data:
                print("[ERROR] Datos vacíos recibidos")
                return

            # Verificar los datos recibidos
            print(f"[DEBUG] Datos recibidos completos: {data.decode()}")  # Imprime los datos completos

            # Convertir los datos a diccionario
            results = json.loads(data.decode())

            # Guardar los resultados en un archivo por algoritmo
            with open(f"{file_name}_results.json", "a") as f:
                json.dump(results, f)
                f.write("\n")

            print(f"[INFO] Recibido y almacenado los resultados de {file_name}.")
        
        except Exception as e:
            print(f"[ERROR] Ocurrió un error: {e}")
        finally:
            self.csocket.close()
            print(f"Client at {self.clientAddress} disconnected")




# --- Configuración del servidor ---
def start_server():
    LOCALHOST = "0.0.0.0"  # Aceptar conexiones desde cualquier IP
    PORT = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("Server started")
    print("Waiting for client request...")

    while True:
        # Esperando por conexiones
        server.listen(3)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()

if __name__ == "__main__":
    start_server()
