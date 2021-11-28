import pandas as pd 
import matplotlib.pyplot as plt 

# df:       data frame containing coorinates
# col_name: name of column containing coordinates in format "latitude,longitude"
def plot_stations(df, col_name, size=10, zorder=0, alpha=1.0, label="Measuring Stations", marker="o", color="Blue"):
    uni = df[col_name].unique()
    x = []
    y = []

    for point in uni:
        split = point.split(",")
        x.append(float(split[1]))
        y.append(float(split[0]))

    plt.scatter(x, y, label=label, c=color, s=size, zorder=zorder, alpha=alpha, marker=marker)
