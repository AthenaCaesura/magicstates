import pandas as pd
import numpy as np
import plotly.express as px
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# Load the data from CSV
df = pd.read_csv(
    "simulation_data/"
    "small_footprint_one_level_15to1_varying_pphys-2024-04-02-16-18"
    ".csv"
)

unique_combinations = df[["dx", "dz", "dm"]].drop_duplicates()
for combo in unique_combinations.itertuples(index=False, name=None):
    this_df = df[
        (df["dx"] == combo[0]) & (df["dz"] == combo[1]) & (df["dm"] == combo[2])
    ]

    # Extracting data for fitting
    x_data = this_df["pphys"].to_numpy()
    y_data = this_df["error_rate"].to_numpy()

    # Defining the power law function
    def power_law_func(x, a, b, c):
        return a * np.power(x, b) + c

    # Fitting the data to the power law function
    power_params, _ = curve_fit(power_law_func, x_data, y_data, p0=[10000, 1, 0])

    x_fit = np.arange(0, 1, 0.0000001)
    y_fit = power_law_func(x_fit, *power_params)

    # Predicting y values with the fitted parameters for the power law
    y_pred_power_law = power_law_func(x_data, *power_params)

    # Calculating the R^2 value for the power law fit
    r_squared_power_law = r2_score(y_data, y_pred_power_law)

    print(power_params, r_squared_power_law)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(this_df["pphys"], this_df["error_rate"], color="blue", alpha=0.5)
    plt.plot(x_fit, y_fit, linestyle="-", color="blue", alpha=0.7)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Physical Parameter vs Error Rate")
    plt.xlabel("Physical Parameter (pphys)")
    plt.ylabel("Error Rate (%)")
    plt.grid(True)
    # plt.show()
