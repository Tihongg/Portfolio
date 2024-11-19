from typing import List

lst = [1, 4, 8, 3, 6, 12, 9, 22]


def function_range(x: List) -> float:  # You can't call it a range
    return max(x) - min(x)


print(function_range(lst))
