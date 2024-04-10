import plotly.graph_objects as go
import pandas as pd

# Load the data from CSV
df1 = pd.read_csv(
    "../factory_searching/simulation_data/"
    "small_footprint_one_level_15to1_simulations-2024-04-01-10-42"
    ".csv"
)
df2 = pd.read_csv(
    "../factory_searching/simulation_data/"
    "small_footprint_two_level_15to1_simulations-2024-04-02-03-31"
    ".csv"
)


# Generating hover text for each DataFrame
hovertext1 = [
    f"({dx}, {dz}, {dm})" for dx, dz, dm in zip(df1["dx"], df1["dz"], df1["dm"])
]
hovertext2 = [
    f"({dx}, {dz}, {dm}, {dx2}, {dz2}, {dm2})"
    for dx, dz, dm, dx2, dz2, dm2 in zip(
        df2["dx"],
        df2["dz"],
        df2["dm"],
        df2["dx2"],
        df2["dz2"],
        df2["dm2"],
    )
]

# Plotting both DataFrames with Plotly, using different colors
fig = go.Figure()

# Adding DataFrame 1
fig.add_trace(
    go.Scatter(
        x=df1["qubits"],
        y=df1["error_rate"],
        mode="markers",
        name="DF1 Error Rate",
        marker_color="blue",
        hovertext=hovertext1,
        hoverinfo="text",
    )
)

# Adding DataFrame 2
fig.add_trace(
    go.Scatter(
        x=df2["qubits"],
        y=df2["error_rate"],
        mode="markers",
        name="DF2 Error Rate",
        marker_color="red",
        hovertext=hovertext2,
        hoverinfo="text",
    )
)

selected_one_level_factories = df1[
    ((df1["dx"] == 5) & (df1["dz"] == 1) & (df1["dm"] == 3))
    | ((df1["dx"] == 7) & (df1["dz"] == 3) & (df1["dm"] == 3))
    | ((df1["dx"] == 9) & (df1["dz"] == 3) & (df1["dm"] == 3))
    | ((df1["dx"] == 3) & (df1["dz"] == 1) & (df1["dm"] == 1))
]

hovertext3 = [
    f"({dx}, {dz}, {dm}) - {error_rate:.2g}"
    for dx, dz, dm, error_rate in zip(
        selected_one_level_factories["dx"],
        selected_one_level_factories["dz"],
        selected_one_level_factories["dm"],
        selected_one_level_factories["error_rate"],
    )
]
# Adding Selected 1 Level Factories
fig.add_trace(
    go.Scatter(
        x=selected_one_level_factories["qubits"],
        y=selected_one_level_factories["error_rate"],
        name="Best Factories",
        mode="markers",
        marker_color="green",
        hovertext=hovertext3,
        hoverinfo="text",
    )
)

selected_two_level_factories = df2[
    (
        (df2["dx"] == 5)
        & (df2["dz"] == 1)
        & (df2["dm"] == 3)
        & (df2["dx2"] == 11)
        & (df2["dz2"] == 3)
        & (df2["dm2"] == 5)
    )
    | (
        (df2["dx"] == 5)
        & (df2["dz"] == 1)
        & (df2["dm"] == 1)
        & (df2["dx2"] == 11)
        & (df2["dz2"] == 5)
        & (df2["dm2"] == 5)
    )
    | (
        (df2["dx"] == 5)
        & (df2["dz"] == 1)
        & (df2["dm"] == 1)
        & (df2["dx2"] == 13)
        & (df2["dz2"] == 5)
        & (df2["dm2"] == 5)
    )
    | (
        (df2["dx"] == 5)
        & (df2["dz"] == 1)
        & (df2["dm"] == 3)
        & (df2["dx2"] == 15)
        & (df2["dz2"] == 5)
        & (df2["dm2"] == 5)
    )
    | (
        (df2["dx"] == 7)
        & (df2["dz"] == 1)
        & (df2["dm"] == 3)
        & (df2["dx2"] == 15)
        & (df2["dz2"] == 5)
        & (df2["dm2"] == 7)
    )
    | (
        (df2["dx"] == 3)
        & (df2["dz"] == 1)
        & (df2["dm"] == 1)
        & (df2["dx2"] == 11)
        & (df2["dz2"] == 3)
        & (df2["dm2"] == 5)
    )
]

hovertext4 = [
    f"({dx}, {dz}, {dm}, {dx2}, {dz2}, {dm2}) - {error_rate:.2g}"
    for dx, dz, dm, dx2, dz2, dm2, error_rate in zip(
        selected_two_level_factories["dx"],
        selected_two_level_factories["dz"],
        selected_two_level_factories["dm"],
        selected_two_level_factories["dx2"],
        selected_two_level_factories["dz2"],
        selected_two_level_factories["dm2"],
        selected_two_level_factories["error_rate"],
    )
]
# Adding Selected 1 Level Factories
fig.add_trace(
    go.Scatter(
        x=selected_two_level_factories["qubits"],
        y=selected_two_level_factories["error_rate"],
        name="Best Factories",
        mode="markers",
        marker_color="green",
        hovertext=hovertext4,
        hoverinfo="text",
    )
)


# Updating layout for log scale on y-axis and adding legend
fig.update_layout(
    title="Qubits vs. Error Rate from Two DataFrames",
    xaxis_title="Qubits",
    yaxis_title="Error Rate (log scale)",
    yaxis_type="log",
    legend_title="Data Source",
)

fig.show()
