import pprint
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import random

read = pd.read_csv("Cancer_Data.csv")
dct = {}
X = np.array([[x[0], x[1]] for x in zip(read["texture_worst"], read["perimeter_worst"])])
Y = np.array(read['diagnosis'])

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=10)

model = KNeighborsClassifier(n_neighbors=5, weights='distance')
model.fit(X_train, y_train)

cmap_bold = ["darkorange", "darkblue"]

plt.figure(figsize=(10, 8))
sns.scatterplot(
    x=X_train[:, 0],
    y=X_train[:, 1],
    hue=y_train,
    palette=cmap_bold
)

plt.scatter(X_test[:, 0], X_test[:, 1], c='g', marker='*', s=100, label='test dots')
plt.legend()

pred = model.predict(X_test)
print(pred)
print(y_test)
print(f"error: {np.sum(pred != y_test)}")

plt.show()






