import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

def is_float(value):
    if value == 'nan':
        return False
    try:
        float(value)
        return True
    except:
        return False

r = pd.read_csv("gcar_data.csv")
clean_r = [x for x in tuple(zip(r['power_kw'], r['mileage_in_km'], r["price_in_euro"])) if str(x[0]).isdigit() and is_float(str(x[1])) and str(x[2]).isdigit()]
X = np.array([(int(x[0]), int(x[1])) for x in clean_r])
Y = np.array([int(x[2]) for x in clean_r])

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=5)

model = KNeighborsRegressor(n_neighbors=2, weights='uniform')
model.fit(X_train, y_train)

plt.figure(figsize=(10, 8))
sns.scatterplot(
    x=X_train[:, 0],
    y=X_train[:, 1],
    hue=y_train
)

print(f'y: {list(y_test)}\nPredict: {list(map(int, model.predict(X_test)))}')


plt.scatter(X_test[:, 0], X_test[:, 1], c='g', marker='*', s=100, label='test dots')
plt.legend()
plt.show()