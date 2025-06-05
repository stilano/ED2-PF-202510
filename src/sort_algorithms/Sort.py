# Importamos cada algoritmo de ordenamiento desde su respectivo módulo.
from sort_algorithms.quicksort import quick_sort       # QuickSort recursivo
from sort_algorithms.mergesort import merge_sort       # MergeSort recursivo
from sort_algorithms.countingsort import counting_sort # Counting Sort para enteros no negativos
from sort_algorithms.radixsort import radix_sort       # Radix Sort para enteros no negativos

# Creamos un diccionario que asocia el nombre de cada algoritmo (clave)
# con la función que lo implementa (valor). Esto permite elegir dinámicamente
# qué algoritmo ejecutar a partir de su nombre.
algorithms = {
    "QuickSort": quick_sort,
    "MergeSort": merge_sort,
    "RadixSort": radix_sort,
    "CountingSort": counting_sort,
}
