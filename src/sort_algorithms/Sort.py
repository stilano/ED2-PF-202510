from sort_algorithms.quicksort import quick_sort
from sort_algorithms.mergesort import merge_sort
from sort_algorithms.countingsort import counting_sort
from sort_algorithms.radixsort import radix_sort


# Diccionario que asocia los nombres de los algoritmos con sus funciones
algorithms = {
    f"{prefix}_QuickSort": quick_sort,
    f"{prefix}_MergeSort": merge_sort,
    f"{prefix}_CountingSort": counting_sort,
    f"{prefix}_RadixSort": radix_sort
}
