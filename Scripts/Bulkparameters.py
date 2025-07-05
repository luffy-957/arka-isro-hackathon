import numpy as np
from spacepy.pycdf import CDF
import datetime as dt
import glob

def loadfiles(DATA_PATH, INVALID):
    all_time = []
    all_density = []
    all_bulk_speed = []
    all_thermal_speed = []

    for file in sorted(glob.glob(DATA_PATH)):
        with CDF(file) as cdf:
            try:
                time = np.array([dt.datetime.fromtimestamp(e.timestamp(), dt.UTC) for e in cdf['epoch_for_cdf_mod'][:]])
                density = np.array(cdf['proton_density'][:])
                bulk_speed = np.array(cdf['proton_bulk_speed'][:])
                thermal_speed = np.array(cdf['proton_thermal'][:])
            except KeyError as e:
                print(f"Missing expected variable in {file}: {e}")
                continue

            # Filter invalid values
            valid_mask = (
                (density != INVALID) &
                (bulk_speed != INVALID) &
                (thermal_speed != INVALID)
            )

            # Apply mask and extend global lists
            all_time.extend(time[valid_mask])
            all_density.extend(density[valid_mask])
            all_bulk_speed.extend(bulk_speed[valid_mask])
            all_thermal_speed.extend(thermal_speed[valid_mask])

    all_time = np.array(all_time)
    all_density = np.array(all_density)
    all_bulk_speed = np.array(all_bulk_speed)
    all_thermal_speed = np.array(all_thermal_speed)

    return all_time, all_density, all_bulk_speed, all_thermal_speed