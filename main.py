from spacepy import pycdf, time as sptime
import matplotlib.pyplot as plt
import os

#importing the cdf file
cdf = pycdf.CDF("./data/AL1_ASW91_L2_TH1_20250620_UNP_9999_999999_V02.cdf")
print(cdf)
"""
#epoch is encrypted timestamps  
epoch_array = cdf['epoch_for_cdf_mod'][...]
ticktock = sptime.Ticktock(epoch_array, 'CDF')
#timestamps after decryption are stored in datetime_list
datetime_list = ticktock.UTC
"""

"""
def plot_stacked_cdf_vars(cdf_path, save_dir="plots"):
    # Open CDF file
    cdf = pycdf.CDF(cdf_path) 

    # Convert CDF_EPOCH to datetime
    epoch_array = cdf['epoch_for_cdf_mod'][...]
    time = sptime.Ticktock(epoch_array, 'CDF').UTC

    # Variables to stack in one figure
    variables_to_plot = [
        'proton_bulk_speed',
        'proton_density',
        'alpha_bulk_speed',
        'alpha_density'
    ]

    # Create output directory if needed
    os.makedirs(save_dir, exist_ok=True)

    # Set up stacked plots
    num_vars = len(variables_to_plot)
    fig, axes = plt.subplots(num_vars, 1, figsize=(12, 3 * num_vars), sharex=True)

    # If only one subplot, make axes a list
    if num_vars == 1:
        axes = [axes]

    # Plot each variable
    for ax, var in zip(axes, variables_to_plot):
        data = cdf[var][...]
        ax.plot(time, data, label=var.replace('_', ' ').title(), color='tab:blue')
        ax.set_ylabel(var.replace('_', ' ').title())
        ax.legend(loc='upper right')
        ax.grid(True)

    axes[-1].set_xlabel("Time")
    fig.suptitle("Stacked Plot of Selected CDF Variables", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save the figure
    output_path = os.path.join(save_dir, "stacked_plot.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"✅ Stacked plot saved to {output_path}")

    cdf.close()

if __name__ == "__main__":
    # Replace this path with your actual file
    cdf_file = "./data/AL1_ASW91_L2_BLK_20250620_UNP_9999_999999_V02.cdf"
    plot_stacked_cdf_vars(cdf_file)
"""