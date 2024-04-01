import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data from CSV
data = pd.read_csv(
    "simulation_data/"
<<<<<<< HEAD
    "small_footprint_two_level_15to1_simulations-2024-03-29-21-11"
=======
    "small_footprint_two_level_15to1_simulations-2024-03-30-07-42"
>>>>>>> 0bee96556c351a99215db789784de7c6c8ec3ac3
    ".csv"
)

# Set the plot style
sns.set(style="whitegrid")

# Create the plot
plt.figure(figsize=(10, 6))
plot = sns.scatterplot(data=data, x="qubits", y="error_rate")

# Set the y-axis to logarithmic scale
plt.yscale("log")

# Setting labels and title
plt.xlabel("Qubits")
plt.ylabel("Error Rate (log scale)")
plt.title("Qubits vs. Error Rate")

# Show the plot
plt.show()


# Clearing matplotlib figures
plt.close("all")
