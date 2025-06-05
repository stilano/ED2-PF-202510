def counting_sort(arr: list[int]) -> list[int]:
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