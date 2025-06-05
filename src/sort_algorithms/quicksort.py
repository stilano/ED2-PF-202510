def quick_sort(arr: list[int]) -> list[int]:
    """
    Implementa Quick Sort de manera recursiva usando un pivote en el medio.
    - Separa la lista en elementos 'left' (< pivote), 'middle' (== pivote) y 'right' (> pivote).
    - Ordena recursivamente 'left' y 'right' y concatena.
    Retorna la lista ordenada.
    """
    # Caso base: lista de tamaño 0 o 1 ya está ordenada
    if len(arr) <= 1:
        return arr

    # Elegimos el pivote como el elemento medio
    pivot = arr[len(arr) // 2]

    # Listas auxiliares para elementos menores, iguales y mayores que el pivote
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Ordenamos recursivamente 'left' y 'right', luego concatenar
    return quick_sort(left) + middle + quick_sort(right)