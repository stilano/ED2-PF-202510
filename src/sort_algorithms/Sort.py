from sort_algorithms.quicksort import quick_sort
from sort_algorithms.mergesort import merge_sort
from sort_algorithms.radixsort import radix_sort
from sort_algorithms.countingsort import counting_sort


# Diccionario que asocia los nombres de los algoritmos con sus funciones
algorithms = {
    "QuickSort": quick_sort,
    "MergeSort": merge_sort,
    "RadixSort": radix_sort,
    "CountingSort": counting_sort,
}
