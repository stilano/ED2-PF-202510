import socket
import time
import json

# --- Algoritmos de ordenamiento ---
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
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

def counting_sort(arr):
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

def radix_sort(arr):
    if not arr:
        return []
    max_val = max(arr)
    exp = 1
    data = arr.copy()

    def counting_for_radix(a, exp):
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


# --- Medir el tiempo y enviar resultados ---
def timed_sort(name, func, data):
    start = time.time()
    sorted_data = func(data)
    end = time.time()
    result = {
        "time": end - start,
        "sorted": sorted_data[:5]  # Solo los primeros 5 para mostrar en el ejemplo
    }
    print(f"[DEBUG] Resultado para {name}: {result}")  # Verifica el resultado antes de enviarlo
    return result

def send_results_to_server(file_name, data):
    try:
        # Verificar los datos antes de enviarlos
        if not data:
            print(f"[ERROR] Los datos para {file_name} están vacíos.")
        else:
            print(f"[DEBUG] Enviando datos para {file_name}: {data}")  # Imprime los datos antes de enviarlos

        # Conectar con el servidor
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 8080))  # Dirección IP y puerto del servidor

        # Enviar el nombre del archivo (algoritmo)
        client.send(file_name.encode())

        # Enviar los resultados (tiempos y datos ordenados) como JSON
        client.send(json.dumps(data).encode())

        print(f"[INFO] Resultados enviados para {file_name}")
        client.close()
    except Exception as e:
        print(f"[ERROR] Error al enviar los resultados: {e}")

def run_and_send_results(data, file_name):
    result = timed_sort(file_name, func=globals()[file_name], data=data)
    send_results_to_server(file_name, result)

# --- Ejecutar y enviar resultados ---
if __name__ == "__main__":
    data = [9, 7, 8, 3, 5, 1, 4, 6, 2]  # Datos de prueba

    algorithms = ["quick_sort", "merge_sort", "counting_sort", "radix_sort"]

    for algo in algorithms:
        print(f"[INFO] Ejecutando {algo}...")
        run_and_send_results(data, algo)
