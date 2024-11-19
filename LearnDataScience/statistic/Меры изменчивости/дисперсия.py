from typing import List

# Дисперсия - это мера, которая показывает разброс между результатами.

lst = [1, 5, 2, 7, 1, 9, 3, 8, 5, 9]


def variance(x: List) -> float:
    mean = sum(x) / len(x)
    deviation_x = [(y - mean) ** 2 for y in x]  # (y - mean) ** 2 so that deviation is not equal to 0
    D = sum(deviation_x) / len(x) + 1
    return D

def standard_deviation(x: List) -> float:
    return variance(x) ** 0.5

# Свойства

# 1. Если к каждому элементу списка добавить число n, то Дисперсия не измениться
lst = [x + 2 for x in lst]

print(standard_deviation(lst))

# 2. Если каждый элемент умножить в n раз, то и дисперсия увеличиться в n раз.
lst = [x * 3 for x in lst]

print(standard_deviation(lst))

