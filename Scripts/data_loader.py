import pandas as pd
import Scripts.Bulkparameters as Bulkparameters
import Scripts.TH_parameters as TH_parameters

def load_blk_data():
    # Assuming the function returns: time, density, speed, thermal
    time, density, speed, thermal = Bulkparameters.loadfiles('../data/BLK/*cdf', -1e31)

    df = pd.DataFrame({
        'time': pd.to_datetime(time),
        'density': density,
        'speed': speed,
        'thermal': thermal
    })

    return df

def load_th1_data():
    # Load time, energy (2D), flux (2D) from TH_parameters
    time, energy, flux = TH_parameters.loadfiles('../data/TH1/*cdf')

    # Convert to numpy arrays if not already
    import numpy as np
    energy = np.array(energy)
    flux = np.array(flux)

    # Take average across the 50 energy channels (axis=1)
    avg_energy = np.mean(energy, axis=1)
    avg_flux = np.mean(flux, axis=1)

    # Create a DataFrame
    df = pd.DataFrame({
        'time': pd.to_datetime(time),
        'energy': avg_energy,
        'flux': avg_flux
    })

    return df

