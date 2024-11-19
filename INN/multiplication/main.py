import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras import backend as K
import numpy as np
import random

def set_seed(seed):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    random.seed(seed)

set_seed(1)

X = np.array([1, 3, 2, 10, 4, 7, 8]).T
y = np.array([[3, 9, 6, 30, 12, 21, 24]]).T

model = Sequential()
model.add(Input(shape=(1, )))
model.add(Dense(1, activation='linear'))

def r2_score(y_true, y_pred):
    y_true = K.cast(y_true, dtype='float32')
    ss_res = K.sum(K.square(y_true - y_pred))
    ss_tot = K.sum(K.square(y_true - K.mean(y_true)))
    r2 = 1 - ss_res / (ss_tot + K.epsilon())
    return r2

n = 12

model.compile(optimizer='sgd', loss='mse', metrics=[r2_score])
model.fit(X, y, epochs=100)
print(print(model.predict(np.array([n]))[0][0]))