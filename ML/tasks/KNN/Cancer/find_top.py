import pprint
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import random

def find_top_corr(read):
    lst = list(read)
    lst.remove("id")
    lst.remove('diagnosis')
    lst.remove('Unnamed: 32')
    dct = {}
    for x in lst:
        for y in lst:
            if x != y:
                dct[f"{x}-{y}"] = np.corrcoef(read[x], read[y])[0, 1]

    top = sorted(dct.items(), key=lambda x: x[1], reverse=True)
    return top


read = pd.read_csv("Cancer_Data.csv")
dct = {}
find_top_corr = find_top_corr(read)
i = 0
for top in find_top_corr:
    e = 0
    X = np.array([[x[0], x[1]] for x in zip(read[top[0].split("-")[0]], read[top[0].split("-")[1]])])
    Y = np.array(read['diagnosis'])
    for _ in range(25):
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=10)
        model = KNeighborsClassifier(n_neighbors=15, weights='distance')
        model.fit(X_train, y_train)

        pred = model.predict(X_test)
        print("\r", end='', flush=True)
        print(f"{i}/{len(find_top_corr)}", end="", flush=True)

        e += np.sum(pred != y_test)
    i += 1
    dct[top[0]] = e

dct = sorted(dct.items(), key=lambda x: x[1], reverse=True)
print("-----------------------------------------")
pprint.pprint(dct)