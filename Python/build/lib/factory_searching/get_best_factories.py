import pandas as pd
from scipy.spatial import ConvexHull
import numpy as np

# Load the data from CSV
df = pd.read_csv(
    "simulation_data/"
    "small_footprint_two_level_15to1_simulations-2024-04-02-03-31"
    ".csv"
)


def polar_angle(p0, p1=None):
    if p1 is None:
        p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return np.arctan2(y_span, x_span)


def distance(p0, p1=None):
    if p1 is None:
        p1 = anchor
    return (p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2


def det(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


def graham_scan(df):
    global anchor

    # Find the anchor point (lowest y-coordinate and the leftmost if there are ties)
    anchor = df.sort_values(by=["qubits", "error_rate"], ascending=[True, True]).iloc[0]

    # Sort points by polar angle with the anchor
    sorted_points = sorted(points, key=lambda p: (polar_angle(p), -distance(p)))

    hull = [sorted_points[0], sorted_points[1]]

    for s in sorted_points[2:]:
        while det(hull[-2], hull[-1], s) <= 0:
            hull.pop()  # Remove the point if it turns clockwise
        hull.append(s)

    return np.array(hull)


# Sample DataFrame creation (replace this with your actual DataFrame)
data = {"error_rate": [0.1, 0.2, 0.15, 0.3, 0.25], "qubits": [5, 3, 8, 7, 9]}
df = pd.DataFrame(data)

# Perform Graham's scan
hull_points = graham_scan(df)

# Creating a DataFrame for the convex hull points
df_hull = pd.DataFrame(hull_points, columns=["error_rate", "qubits"])

print("Convex hull points:")
print(df_hull)
