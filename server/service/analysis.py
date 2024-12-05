import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append("..")
from server.database_api.api import *

def analyzeData():
    data = getAll('energy_data')

    data.fillna(value=0, inplace=True) #neu co null, NaN thay the = 0

    # Convert 'interval_start_utc' to a datetime format
    data['interval_start_utc'] = pd.to_datetime(data['interval_start_utc'])

    # Group by day and compute the median for each day and energy source
    data['date'] = data['interval_start_utc'].dt.date
    daily_median = data.groupby('date').median()

    return daily_median

