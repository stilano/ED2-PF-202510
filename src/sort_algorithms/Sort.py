import quicksort
import mergesort
import radixsort
import countingsort

# Diccionario que asocia los nombres de los algoritmos con sus funciones
algorithms = {
    "QuickSort": quicksort.quick_sort,
    "MergeSort": mergesort.merge_sort,
    "RadixSort": radixsort.radix_sort,
    "CountingSort": countingsort.counting_sort,
}
