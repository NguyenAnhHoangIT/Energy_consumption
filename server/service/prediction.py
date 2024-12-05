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

# Global variable to track feature columns
FEATURE_COLUMNS = None

def load_and_preprocess_data(file_path):
    """Load data and preprocess columns."""
    df = pd.read_csv(file_path)
    df['interval_start_utc'] = pd.to_datetime(df['interval_start_utc'])
    df['interval_end_utc'] = pd.to_datetime(df['interval_end_utc'])
    
    # Extract datetime components
    for prefix, column in [('start', 'interval_start_utc'), ('end', 'interval_end_utc')]:
        df[f'{prefix}_year'] = df[column].dt.year
        df[f'{prefix}_month'] = df[column].dt.month
        df[f'{prefix}_day'] = df[column].dt.day
        df[f'{prefix}_hour'] = df[column].dt.hour
        df[f'{prefix}_minute'] = df[column].dt.minute
    
    return df

def add_features(df, energy_columns, prediction_horizon):
    """Add lag, rolling mean features, and create future targets."""
    global FEATURE_COLUMNS  # Track the exact feature names used
    for col in energy_columns:
        df[f'{col}_lag_1'] = df[col].shift(1)
        df[f'{col}_rolling_mean_3'] = df[col].rolling(window=3).mean()
        df[f'{col}_future_{prediction_horizon}h'] = df[col].shift(-prediction_horizon)
    
    # Drop rows with NaN created by lagging, rolling, and future target
    df = df.dropna()
    
    # Save the final feature columns for consistency, excluding datetime columns
    FEATURE_COLUMNS = df.drop(
        columns=energy_columns + [f'{col}_future_{prediction_horizon}h' for col in energy_columns] + ['interval_start_utc', 'interval_end_utc']
    ).columns
    return df

def scale_data(train, test, feature_columns):
    """Scale train and test data using MinMaxScaler."""
    # Exclude datetime columns if they are mistakenly included in feature_columns
    numerical_columns = [col for col in feature_columns if not pd.api.types.is_datetime64_any_dtype(train[col])]
    
    scaler = MinMaxScaler()
    train[numerical_columns] = scaler.fit_transform(train[numerical_columns])
    test[numerical_columns] = scaler.transform(test[numerical_columns])
    return train, test, scaler

def prepare_features_and_target(df, energy_columns, prediction_horizon):
    """Prepare feature matrix X and target matrix y."""
    target_columns = [f'{col}_future_{prediction_horizon}h' for col in energy_columns]
    X = df.drop(columns=energy_columns + ['interval_start_utc', 'interval_end_utc'] + target_columns)
    y = df[target_columns]
    return X, y

def train_model(X_train, y_train):
    """Train a RandomForestRegressor model."""
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_future(df, model, scaler, prediction_horizon):
    """Predict energy values for the next time steps."""
    global FEATURE_COLUMNS  # Use the tracked feature columns
    last_known_data = df.iloc[-1:][FEATURE_COLUMNS]  # Select only the FEATURE_COLUMNS
    last_known_data_scaled = scaler.transform(last_known_data)  # Use the same feature columns for scaling
    predictions = model.predict(last_known_data_scaled)
    return predictions

def save_predictions_to_file(predictions, energy_columns, prediction_horizon, file_path):
    """Save future predictions to a text file."""
    with open(file_path, 'w') as f:
        for i, col in enumerate(energy_columns):
            f.write(f"{col} Predictions for Next {prediction_horizon} Hours:\n")
            for hour in range(1, prediction_horizon + 1):
                f.write(f"Hour {hour}: {predictions[0, i]:.2f}\n")
            f.write("\n")
    print(f"Predictions saved to {file_path}")

def main():
    data = getData()  # Correct dataset filename
    output_file = 'future_predictions.txt'
    
    # Define energy columns and prediction horizon
    energy_columns = [
        'solar', 'wind', 'geothermal', 'biomass', 'biogas', 'small_hydro',
        'coal', 'nuclear', 'natural_gas', 'large_hydro', 'batteries', 'imports', 'other'
    ]
    prediction_horizon = 48  # 2 days
    
    # Load and preprocess data
    df = load_and_preprocess_data(data)
    
    # Add lag, rolling features, and future target columns
    df = add_features(df, energy_columns, prediction_horizon)
    
    # Split data into train and test
    train_size = int(len(df) * 0.8)
    train = df[:train_size]
    test = df[train_size:]
    
    # Scale data
    train, test, scaler = scale_data(train, test, FEATURE_COLUMNS)
    
    # Prepare features and targets
    X, y = prepare_features_and_target(df, energy_columns, prediction_horizon)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Predict the future
    predictions = predict_future(df, model, scaler, prediction_horizon)
    
    # Save predictions to a file
    save_predictions_to_file(predictions, energy_columns, prediction_horizon, output_file)

if __name__ == "__main__":
    main()