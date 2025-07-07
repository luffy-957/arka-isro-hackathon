import pandas as pd
import numpy as np
import Scripts.Bulkparameters as Bulkparameters
import Scripts.TH_parameters as TH_parameters

def clean_dataframe(df, feature_cols, resample_interval='1H'):
    # Handle missing values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    # Remove outliers (using Z-score)
    for col in feature_cols:
        col_zscore = (df[col] - df[col].mean()) / df[col].std()
        df = df[(col_zscore > -3) & (col_zscore < 3)]

    # Resample to hourly intervals and interpolate missing data
    df = df.set_index('time').resample(resample_interval).mean().interpolate()

    # Add rolling statistics
    for col in feature_cols:
        df[f'{col}_rolling_mean'] = df[col].rolling(window=3, min_periods=1).mean()
        df[f'{col}_rolling_std'] = df[col].rolling(window=3, min_periods=1).std()

    # Normalize features (Min-Max scaling)
    for col in feature_cols:
        min_val, max_val = df[col].min(), df[col].max()
        df[f'{col}_normalized'] = (df[col] - min_val) / (max_val - min_val)

    df = df.reset_index()
    return df

def load_blk_data():
    # Load bulk solar wind parameters
    time, density, speed, thermal = Bulkparameters.loadfiles('../data/BLK/*cdf', -1e31)

    df = pd.DataFrame({
        'time': pd.to_datetime(time),
        'density': density,
        'speed': speed,
        'thermal': thermal
    })

    # Clean and preprocess data
    df = clean_dataframe(df, feature_cols=['density', 'speed', 'thermal'])

    return df

def load_th1_data():
    time, energy, flux = TH_parameters.loadfiles('../data/TH1/*cdf')

    energy = np.array(energy)
    flux = np.array(flux)

    # Average across energy channels
    avg_energy = np.mean(energy, axis=1)
    avg_flux = np.mean(flux, axis=1)

    df = pd.DataFrame({
        'time': pd.to_datetime(time),
        'energy': avg_energy,
        'flux': avg_flux
    })

    # Clean and preprocess data
    df = clean_dataframe(df, feature_cols=['energy', 'flux'])

    return df
