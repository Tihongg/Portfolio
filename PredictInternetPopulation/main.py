import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import interface

internet_users = {
    2005: 1023000000,
    2006: 1147000000,
    2007: 1367000000,
    2008: 1545000000,
    2009: 1727000000,
    2010: 1981000000,
    2011: 2174000000,
    2012: 2387000000,
    2013: 2562000000,
    2014: 2750000000,
    2015: 2954000000,
    2016: 3217000000,
    2017: 3444000000,
    2018: 3729000000,
    2019: 4119000000,
    2020: 4585000000,
    2021: 4901000000,
    2022: 5300000000,
    2023: 5400000000,
    2024: 5440000000
}

class Model():
    Training_data_model = None
    Model = None

    def Create_model(self, training_data: tuple, save=True, name_save=''):
        X = training_data[0]
        y = training_data[1]
        model = LinearRegression()
        model.fit(X, y)
        Training_data_model = training_data
        if save and name_save != '':
            pickle.dump(model, open(name_save + ".sav", 'wb'))
            self.Model = name_save + ".sav"
        else:
            self.Model = model
            return model

    def predict(self, X):
        if type(self.Model) == str:
            load_model = pickle.load(open(self.Model, 'rb'))
            y_pred = load_model.predict([[X]])
        else:
            y_pred = self.Model.predict([[X]])

        pred = round(y_pred[0, 0])
        if pred < 0:
            return 0
        else:
            return pred


X = np.array(list(internet_users.keys())).reshape(-1, 1)
y = np.array(list(internet_users.values())).reshape(-1, 1)
model = Model()
model.Create_model((X, y))

