from typing import List

all_height = [180, 172, 176, 189, 189, 174, 188, 187, 162, 174, 179, 181, 182, 185, 187, 189]

def median(x: List) -> int:
    x = sorted(x)
    if len(x) % 2 != 0:
        Centre_x = len(x) // 2
        return x[Centre_x]
    else:
        Centre_x = len(x) // 2
        before_Centre = (len(x) // 2) - 1
        mean = (x[Centre_x] + x[before_Centre]) / 2
        return mean

print("Median: " + str(median(all_height)))
