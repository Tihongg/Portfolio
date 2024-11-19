from sklearn.datasets import fetch_california_housing
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = fetch_california_housing()
X = data.data
features = data.feature_names
y = data.target

df = pd.DataFrame(X, columns=features)
df['target'] = y

X_train, X_test, y_train, y_test = train_test_split(
    df[features],
    df['target'],
    test_size=0.2,
    shuffle=True,
    random_state=3
)

tree = DecisionTreeRegressor(random_state=1, max_depth=14, min_samples_leaf=24, max_leaf_nodes=400)
tree.fit(X_train, y_train)

print(f'{[round(x, 2) for x in y_test]}')
print(f'{[round(x, 2) for x in tree.predict(X_test)]}')