from typing import List

all_height = [180, 170, 172, 176, 189, 189, 174, 188, 187, 162, 174, 179, 181, 182, 185, 187, 189]

def moda(x: List) -> int:
    Counter = {}
    for height in x:
        if height not in Counter:
            Counter[height] = 1
        else:
            Counter[height] += 1

    sorted_Counter = sorted(Counter.items(), key=lambda item: item[1], reverse=True)
    moda_Counter = [height for height, often in sorted_Counter if often == sorted_Counter[0][1]]
    if len(moda_Counter) == 1:
        moda_Counter = moda_Counter[0]

    return moda_Counter

print("Moda: " + str(moda(all_height)))