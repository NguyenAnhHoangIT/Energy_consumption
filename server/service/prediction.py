import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import sys
sys.path.append("..")
from server.database_api.api import *

def predictData(col_name):
        data = getAll('energy_data')

        data.fillna(value=0, inplace=True) #neu co null, NaN thay the = 0

        # Convert 'interval_start_utc' to a datetime format
        data['interval_start_utc'] = pd.to_datetime(data['interval_start_utc'])

        # Group by day and compute the median for each day and energy source
        data['date'] = data['interval_start_utc'].dt.date
        cleaned_data = data.groupby('date').median()

        cleaned_data.fillna(0, inplace=True)

        cleaned_data = cleaned_data.filter(['date', col_name], axis=1)

        s = cleaned_data.values
        observed_size = 7
        overlap_size = 2
        predict_distance = 1

        samples = int((len(s) - observed_size) / (observed_size - overlap_size))
        X = np.stack([s[i * (observed_size - overlap_size):i * (observed_size - overlap_size) + observed_size] for i in range(samples)])
        Y = np.stack([s[i * (observed_size - overlap_size) + observed_size + predict_distance] [-1]for i in range(samples)])

        X.shape
        Y.shape

        X = X.reshape(X.shape[0], -1)

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

        regr = RandomForestRegressor(max_depth=2, random_state=0)
        regr.fit(X_train, y_train)

        regr.score(X_test, y_test)

        single_data = X_test[11]
        single_data

        predicted_temp = regr.predict(single_data.reshape(1, -1))

        return predicted_temp