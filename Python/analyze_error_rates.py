import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv(
    "simulation_data/"
    "small_footprint_one_level_15to1_simulations-2024-04-01-10-42"
    ".csv"
)

# Filter the DataFrame where 'error_rate' is less than 10^-10
filtered_df = df[df["error_rate"] < 10**-6]
filtered_df = filtered_df[filtered_df["error_rate"] > 10**-7]

breakpoint()
