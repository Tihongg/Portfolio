import sklearn
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

def random_regression():
    r_data, r_values = make_regression(n_samples=500, n_features=1, n_informative=2, noise=1)
    return (r_data, r_values)

r = random_regression()
plt.scatter(r[0][:, 0], r[1])
model = LinearRegression()
model.fit(r[0], np.array(r[1]).reshape(-1, 1))

# MAE
different = [abs(np.diff([model.predict([[x]])[0, 0], y]))[0] for x, y in zip(r[0][:, 0], r[1])]
print(f"""MAE: 
my: {float(sum(different) / len(different))}
sklearn: {mean_absolute_error(r[1], model.predict(r[0]))}
""")

# MSE
different = [np.diff([model.predict([[x]])[0, 0], y])[0] ** 2 for x, y in zip(r[0][:, 0], r[1])]
print(f"""MSE: 
my: {float(sum(different) / len(different))}
sklearn: {mean_squared_error(r[1], model.predict(r[0]))}
sqrt (RMSE): {np.sqrt(float(sum(different) / len(different)))}
""")

# R2
different = [np.diff([model.predict([[x]])[0, 0], y])[0] ** 2 for x, y in zip(r[0][:, 0], r[1])]
R2 = 1 - float(sum(different) / len(different)) / np.var(r[1])
print(f"""R2: 
my: {R2}
sklearn: {r2_score(r[1], model.predict(r[0]))}
""")

plt.plot(r[0][:, 0], model.predict(r[0]), color='red')
plt.show()