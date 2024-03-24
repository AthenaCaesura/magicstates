import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load data from CSV
data = pd.read_csv(
    "simulation_data/"
    "small_footprint_two_level_15to1_simulations-2024-03-24-10-25.csv"
)

# Ensure data is sorted by 'qubits'
data = data.sort_values(by="qubits")

# Set the style of seaborn
sns.set_theme(style="whitegrid")

# Create the plot
plt.figure(figsize=(10, 6))
plot = sns.lineplot(data=data, x="qubits", y="error_rate", marker="o", color="b")

# Setting the scale of y-axis to logarithmic
plt.yscale("log")

# De-cluttering the x-axis
plot.xaxis.set_major_locator(
    ticker.MaxNLocator(integer=True)
)  # This might adjust depending on your data
plt.xticks(rotation=45)  # Rotate labels to avoid overlap

plt.xlabel("Qubits")
plt.ylabel("Error Rate")
plt.title("Error Rate vs Qubits on a Log-Linear Scale")
plt.tight_layout()  # Adjust layout for rotated x-axis labels
plt.show()
