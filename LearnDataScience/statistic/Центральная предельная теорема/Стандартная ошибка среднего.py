from typing import List

lst = [1, 5, 2, 7, 1, 9, 3, 8, 5, 9]

def variance(x: List) -> float:
    mean = sum(x) / len(x)
    deviation_x = [(y - mean) ** 2 for y in x]  # (y - mean) ** 2 so that deviation is not equal to 0
    D = sum(deviation_x) / len(x) + 1
    return D

def standard_deviation(x):
    return variance(x) ** 0.5

def standard_error(x):
    return standard_deviation(x) / (len(x) ** 0.5)

print(standard_error(lst))

