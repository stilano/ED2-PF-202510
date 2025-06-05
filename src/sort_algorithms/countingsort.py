def counting_sort(arr: list[int]) -> list[int]:
    """
    Implementa Counting Sort para ordenar enteros no negativos.
    - arr: lista de enteros.
    Retorna la lista ordenada.
    """
    # Si la lista está vacía, no hay nada que ordenar
    if not arr:
        return []

    # Encuentra el valor máximo para determinar el rango del conteo
    max_val = max(arr)
    if max_val < 0:
        # Counting Sort no soporta valores negativos
        raise ValueError("Counting Sort solo admite enteros no negativos.")

    # Crea un arreglo de conteo de tamaño (max_val + 1), inicializado en 0
    count = [0] * (max_val + 1)

    # Se cuenta cada aparición de los números en 'arr'
    for num in arr:
        count[num] += 1

    # Reconstruye la lista ordenada usando los conteos
    sorted_arr = []
    for i, freq in enumerate(count):
        # Agregar 'i' exactamente 'freq' veces
        sorted_arr.extend([i] * freq)

    return sorted_arr