import numpy as np
from spacepy.pycdf import CDF
import datetime as dt
import glob

def loadfiles(DATA_PATH):
    all_time = []
    all_energy = []
    all_flux = []
    for file in sorted(glob.glob(DATA_PATH)):
        with CDF(file) as cdf:
            try:
                time = np.array([dt.datetime.fromtimestamp(e.timestamp(), dt.UTC) for e in cdf['epoch_for_cdf_mod'][:]])
                energy = np.array(cdf['energy_center_mod'][:])
                flux = np.array(cdf['integrated_flux_mod'][:])
            except KeyError as e:
                print(f"Missing expected variable in {file}: {e}")
                continue

            all_time.extend(time)
            all_energy.extend(energy)
            all_flux.extend(flux)

    all_time = np.array(all_time)
    all_energy = np.array(all_energy)
    all_flux = np.array(all_flux)

    return all_time, all_energy, all_flux