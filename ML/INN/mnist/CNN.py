import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Conv2D
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
from tensorflow import keras
import numpy as np

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train, X_test = np.expand_dims(X_train, axis=3), np.expand_dims(X_test, axis=3)
y_train, y_test = keras.utils.to_categorical(y_train, 10), keras.utils.to_categorical(y_train, 10)

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2), strides=2))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D((2, 2), strides=2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=32, epochs=5, validation_split=0.2)