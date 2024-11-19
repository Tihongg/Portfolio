from typing import List

all_height = [180, 170, 172, 176, 189, 189, 174, 188, 187, 162, 174, 179, 181, 182, 185, 187, 189]

def mean(x: List) -> float:
    return sum(x) / len(x)

print("Mean: " + str(mean(all_height)))

# Свойства

# 1. Если к кажому эл. добавить n число, то mean = mean + n
all_height = [180, 170, 172, 176, 189, 189, 174, 188, 187, 162, 174, 179, 181, 182, 185, 187, 189]
N = 5
all_height = [x + N for x in all_height]
print("The mean is if the number N is added to each element: " + str(mean(all_height)))

# 2. Если каждый эл. умножить на n число, то mean = mean * n
all_height = [180, 170, 172, 176, 189, 189, 174, 188, 187, 162, 174, 179, 181, 182, 185, 187, 189]
N = 2
all_height = [x * N for x in all_height]
print("The mean if each element is multiplied by N: " + str(mean(all_height)))

# 3. Если из каждого эл. вычти среднее арифметическое число, то сумма этих элементов = 0
all_height = [180, 170, 172, 176, 189, 189, 174, 188, 187, 162, 174, 179, 181, 182, 185, 187, 189]
all_height = [x - mean(all_height) for x in all_height.copy()]
print("The sum of all elements if the mean is subtracted from each element: 0" + f"  # python calculation = {sum(all_height)}, it may differ due to the inaccuracy of python")
