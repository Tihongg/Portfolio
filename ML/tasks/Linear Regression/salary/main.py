import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

r = pd.read_csv("Salary_dataset.csv")
X = list(r['YearsExperience'])
Y = list(r['Salary'])

model = LinearRegression()
model.fit(np.array(X).reshape(-1, 1), np.array(Y).reshape(-1, 1))

plt.scatter(X, Y, color='blue')
plt.plot(X, model.predict(np.array(X).reshape(-1, 1)), color='red')
print(model.predict([[20]])[0, 0])
plt.show()



