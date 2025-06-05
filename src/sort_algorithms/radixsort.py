def radix_sort(arr: list[int]) -> list[int]:
    """
    Implementa Radix Sort para enteros no negativos.
    - Ordena por dígitos: desde el menos significativo al más significativo.
    Retorna la lista ordenada.
    """
    # Si la lista está vacía, no hay nada que ordenar
    if not arr:
        return []

    # Encouentra el valor máximo para saber cuántas pasadas de dígitos hacer
    max_val = max(arr)
    exp = 1  # exponent (1 → dígito de las unidades, 10 → decenas, etc.)
    data = arr.copy()  # Copiar la lista original para no modificarla in situ

    def counting_for_radix(a: list[int], exp: int) -> list[int]:
        """
        Counting Sort auxiliar que ordena 'a' según el dígito en la posición 'exp'.
        - a: lista de enteros
        - exp: potencia de 10 que indica el dígito actual (1, 10, 100, ...)
        Retorna la lista parcialmente ordenada por ese dígito.
        """
        n = len(a)
        output = [0] * n       # Lista de salida del mismo tamaño
        count = [0] * 10       # Arreglo de conteo para dígitos 0-9

        # Se cuentan apariciones del dígito actual para cada elemento
        for i in range(n):
            index = (a[i] // exp) % 10
            count[index] += 1

        # Se acumulan conteos para convertirlos en posiciones finales
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Se construye la lista de salida en orden inverso para mantener estabilidad
        for i in range(n - 1, -1, -1):
            index = (a[i] // exp) % 10
            output[count[index] - 1] = a[i]
            count[index] -= 1

        return output

    # Repite la ordenación de dígitos mientras queden dígitos en el número máximo
    while max_val // exp > 0:
        data = counting_for_radix(data, exp)
        exp *= 10  # Pasa al siguiente dígito (decenas, centenas, ...)

    return data