import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
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
    daily_median = daily_median.drop(columns=['id', 'interval_start_utc', 'interval_end_utc'])
    return daily_median

def daily():
    df = analyzeData()
    df['date'] = pd.to_datetime(df.index)  # Convert the index to datetime

    # Filter for the last 7 days
    last_7_days = df[df['date'] >= pd.Timestamp.today() - pd.Timedelta(days=7)]

    # Return data as a JSON
    return last_7_days.reset_index().to_json(orient='records', date_format='iso')

def monthly():
    df = analyzeData()  # Analyze or load data

    # Ensure the index is converted to DatetimeIndex
    df.index = pd.to_datetime(df.index)

    # Filter data from the start of the current year
    start_of_year = pd.Timestamp.today().replace(month=1, day=1)
    this_year = df[df.index >= start_of_year]

    # Resample by month-end ('ME') and calculate the median
    monthly_data = this_year.resample('ME').median()

    # Return data as a JSON
    return monthly_data.reset_index().to_json(orient='records', date_format='iso')

def yearly():
    df = analyzeData()  # Analyze or load data

    # Ensure the index is converted to DatetimeIndex
    df.index = pd.to_datetime(df.index)

    # Filter data from the last 5 years
    start_of_period = pd.Timestamp.today() - pd.DateOffset(years=5)
    five_years_data = df[df.index >= start_of_period]

    # Resample by year-end ('A') and calculate the sum
    yearly_data = five_years_data.resample('A').sum()

    # Return data as a JSON
    return yearly_data.reset_index().to_json(orient='records', date_format='iso')

def runphantich():
    while True:
        daily_data = daily()  # Get daily data
        monthly_data = monthly()  # Get monthly data
        yearly_data = yearly()  # Get yearly data
        time.sleep(300)

runphantich()