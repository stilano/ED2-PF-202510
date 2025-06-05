def merge_sort(arr: list[int]) -> list[int]:
    """
    Implementa Merge Sort de manera recursiva.
    - Divide la lista en mitades, ordena cada mitad y las combina.
    Retorna la lista ordenada.
    """
    # Caso base: lista de tamaño 0 o 1 ya está ordenada
    if len(arr) <= 1:
        return arr

    # Encuentra el punto medio para dividir la lista
    mid = len(arr) // 2
    # Ordena recursivamente la mitad izquierda
    left = merge_sort(arr[:mid])
    # Ordena recursivamente la mitad derecha
    right = merge_sort(arr[mid:])

    # Combina ambas mitades ordenadas
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """
    Función auxiliar para Merge Sort: combina dos listas ordenadas.
    - left: lista ordenada
    - right: lista ordenada
    Retorna una lista fusionada y ordenada.
    """
    result = []
    i = j = 0

    # Mientras haya elementos en ambas listas, compara y anexa el menor
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Si quedaron elementos en 'left', se agregar al final
    result.extend(left[i:])
    # Si quedaron elementos en 'right', se agregan al final
    result.extend(right[j:])
    return result