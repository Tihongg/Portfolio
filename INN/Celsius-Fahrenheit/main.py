import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense
import numpy as np

c = np.array(range(-1000, 1001))
f = np.array([round(f*1.8 + 32, 1) for f in c])

model = keras.Sequential()
model.add(Dense(units=1, input_shape=(1, ), activation='linear'))

model.compile(optimizer=keras.optimizers.Adam(0.1), loss='mse', metrics=['mae'])

model.fit(c, f, epochs=80)

find_c = 123456

print("НС:" + str(model.predict(np.array([find_c]))[0, 0]) + "\nОтвет: " + str(round(find_c*1.8 + 32, 2)))