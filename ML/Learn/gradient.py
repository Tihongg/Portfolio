import numdifftools as nd
import matplotlib.pyplot as plt
import numpy as np
import random

def f(x):
    return x**2

def gr_f(x):
    return 2*x

D = 10
X = np.linspace(-D, +D, 100)
Y = list(map(f, X))

plt.plot(X, Y)

start_point = random.choice(X)
learning_rate = 0.1
esp = 0.0001
last = start_point
i = 0
while True:
    gr = gr_f(last)
    next = last - learning_rate * gr
    plt.scatter([last, next], [f(last), f(next)], color='red')
    plt.plot([last, next], [f(last), f(next)], color='red')

    if abs(last - next) <= esp:
        print(i)
        break

    last = next
    i += 1

plt.show()



