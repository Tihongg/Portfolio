import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
from tensorflow import keras
import numpy as np

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train, X_test = X_train / 255, X_test / 255
y_train, y_test = keras.utils.to_categorical(y_train, 10), keras.utils.to_categorical(y_train, 10)

model = Sequential()
model.add(Flatten(input_shape=(28, 28, 1)))
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=32, epochs=5, validation_split=0.2)

n = 2
x = np.expand_dims(X_test[n], axis=0)
res = model.predict(x)
print(res)
print(f"Распознонная цифра: {np.argmax(res)}")

plt.imshow(X_test[n], cmap=plt.cm.binary)
plt.show()