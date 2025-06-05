def radix_sort(arr: list[int]) -> list[int]:
    if not arr:
        return []
    max_val = max(arr)
    exp = 1
    data = arr.copy()

    def counting_for_radix(a: list[int], exp: int) -> list[int]:
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