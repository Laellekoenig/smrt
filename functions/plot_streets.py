import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast

def plot_streets(label="speed limit ≥ 50km/h", rainbow=False, zorder=0, alpha=1.0, color="indigo"):
    df = pd.read_csv("datasets/strassen.csv", delimiter=";")
    streets = df["Geo Shape"]

    # get point from pandas series
    start = streets[0].find("[")
    streets = streets.apply(lambda x: x[start:-1])

    #plot
    label=""
    for street in streets:
        npa = np.array(ast.literal_eval(street)).T
        x = npa[0,:]
        y = npa[1,:]

        if rainbow:
            plt.plot(x, y, zorder=zorder, alpha=alpha, label=label)
            label = None
        else:
            plt.plot(x, y, zorder=zorder, c=color, alpha=alpha, label=label)

