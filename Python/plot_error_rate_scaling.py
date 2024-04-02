import pandas as pd
import numpy as np
import plotly.express as px
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Load the data from CSV
df = pd.read_csv(
    "simulation_data/"
    "small_footprint_one_level_15to1_varying_pphys-2024-04-02-12-17"
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
    def power_law_func(x, a, b):
        return a * np.power(x, b)

    # Fitting the data to the power law function
    power_params, _ = curve_fit(power_law_func, x_data, y_data)

    # Predicting y values with the fitted parameters for the power law
    y_pred_power_law = power_law_func(x_data, *power_params)

    # Calculating the R^2 value for the power law fit
    r_squared_power_law = r2_score(y_data, y_pred_power_law)

    # Rounding the R^2 value to two significant figures for the power law fit
    r_squared_power_law_rounded = round(r_squared_power_law, 2)

    print(power_params, r_squared_power_law_rounded)
