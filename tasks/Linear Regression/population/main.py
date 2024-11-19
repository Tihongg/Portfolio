import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from sklearn.linear_model import LinearRegression
import numpy as np
import itertools

def read(country):
    data = {}
    f = pd.read_csv("Final.csv")
    for _, x in f.iterrows():
        if x['Entity'] not in data:
            data[x['Entity']] = {}
        data[x['Entity']][x['Year']] = x['No. of Internet Users']

    if country is None:
        return data
    else:
        return data[country]

def del_null_year(r):
    return {x: r[x] for x in r if r[x] != 0}

def create_model(r):
    model = LinearRegression()
    model.fit(np.array(list(r.keys())).reshape(-1, 1), np.array(list(r.values())).reshape(-1, 1))

    return model

def main(country, year, show=True):
    r = read(country)
    r = del_null_year(r)
    model = create_model(r)

    pr = int(model.predict(np.array(year).reshape(-1, 1))[0, 0])
    if pr < 0:
        print(0)
    else:
        print(pr)

    if show:
        for x in r:
            plt.scatter(x, r[x], color='red')

        plt.plot(list(r.keys()), model.predict(np.array(list(r.keys())).reshape(-1, 1)))
        plt.xlim(min(r.keys()), max(r.keys()))
        plt.ylim(0, max(r.values()))
        plt.show()

main("Russia", 2024)

