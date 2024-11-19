import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import numpy as np
import tensorflow as tf
import random
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras import Input
from tensorflow.keras import backend as K

def r2_score(y_true, y_pred):
    y_true = K.cast(y_true, dtype='float32')
    ss_res = K.sum(K.square(y_true - y_pred))
    ss_tot = K.sum(K.square(y_true - K.mean(y_true)))
    r2 = 1 - ss_res / (ss_tot + K.epsilon())
    return r2

def set_seed(seed):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    random.seed(seed)

set_seed(1)

x1 = np.random.randint(1, 10, size=50)
x2 = np.random.randint(1, 10, size=50)
y = np.array((x1 + x2)[None]).T

X = np.vstack([x1, x2]).T

norm = MinMaxScaler()
X = norm.fit_transform(X)


model = Sequential()
model.add(Input(shape=(2, )))
model.add(Dense(3, activation='linear'))
model.add(Dense(1, activation='linear'))

model.compile(optimizer='sgd', loss='mse', metrics=[r2_score])
model.fit(X, y, epochs=300)


test = [[137, 234]]
norm_test = norm.transform(test)
print(f"{test[0][0]} + {test[0][1]} = {round(model.predict(norm_test)[0, 0])}")