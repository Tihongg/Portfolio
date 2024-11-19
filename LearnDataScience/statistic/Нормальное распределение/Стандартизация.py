from typing import List
from decimal import Decimal

x = [20, 40, 60, 80, 100, 120, 140]

def variance(x: List) -> float:
    mean = sum(x) / len(x)
    deviation_x = [(y - mean) ** 2 for y in x]  # (y - mean) ** 2 so that deviation is not equal to 0
    D = sum(deviation_x) / len(x) + 1
    Sigma = D ** 0.5
    return Sigma

def Standardization(x: List):
    mean_x = sum(x) / len(x)
    variance_x = variance(x)
    Standardization_x = [(x - mean_x) / variance_x for x in x]
    return [round(x, 2) for x in Standardization_x]

print(Standardization(x))

