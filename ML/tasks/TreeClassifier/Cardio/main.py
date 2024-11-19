from sklearn.datasets import fetch_california_housing
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt

full_df = pd.read_csv('cardio.csv', sep=';')
full_features = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo',
                 'cholesterol', 'gluc', 'smoke', 'alco', 'active']
target = ['cardio']
full_df['age'] = round(full_df['age'] / 365)

features = ['age', 'ap_hi']
df = full_df[features + target]
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=10, random_state=1)

tree = DecisionTreeClassifier(random_state=1)
tree.fit(X_train, y_train)
plt.figure(figsize=(8, 6))
plot_tree(tree, feature_names=features, filled=True)

print(list(y_test['cardio']))
print(list(tree.predict(X_test)))