import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation
import matplotlib.patches as ptc
import os
import ast
import datetime as dt
import time
import geopy
from geopy import distance
import geopy.distance

import imageio
from scipy.interpolate import griddata
from scipy.interpolate import interp2d

import math

#from functions import vals_to_boxes as boxes
from dateutil.relativedelta import *

import functions.get_map as get_map
import functions.get_bounds as bounds
import functions.plot_stations as stations
import functions.plot_streets as streets
import functions.temperature_grid as tg
import functions.vehicle_grid as vg
import functions.grid_correlation as gc
import functions.calc_corr as cc




date = dt.datetime(2020,8,1)
temperature = pd.read_csv("datasets/luftklima_reformatted.csv")
vehicles = pd.read_csv("datasets/verkehrszählungen_reformatted.csv")
basel = plt.imread("maps/basel_square_bw.jpg")
box = bounds.get_bounds()

for j in range(0, 12):
    date_start = date + relativedelta(months=+j)
    date_start = date_start.strftime("%Y-%m-%d")
    date_end = date + relativedelta(months=+(j+1)) - dt.timedelta(days=1)
    date_end = date_end.strftime("%Y-%m-%d")
    corr = cc.get_corr_for_vstation(temperature, vehicles, 0.4, date_start, date_end, "1", "1", 6, True)
    print(str(j+1) + " correlations calculated, now plotting...")
    el = cc.calc_ellipse_dists(corr[0], corr[1], 0.4)
    print("Plotting new correlation...")
    fig, ax = plt.subplots(figsize=(10, 10), dpi=160)
    #plt.figure(figsize=(7, 7), dpi=160)

    cmap = matplotlib.cm.get_cmap('Reds', 10)
    norm = matplotlib.colors.Normalize(vmin=0.0, vmax=1.0)
    ellipses = []
    for i in range(len(corr[2])):
        if corr[2][i] > -999999999999: #get rid of NaN
            ell = Ellipse((corr[0][i], corr[1][i]), el[0][i], el[1][i], 0, color=cmap(norm(corr[2][i])), fill = True, alpha=.7)
            #cir = plt.Circle((corr[0][i], corr[1][i]), 0.004, color=cmap(norm(corr[2][i])), fill = True, alpha=.7)
            ellipses.append(ell)
    for e in ellipses:
        ax.add_artist(e)

    streets.plot_streets(zorder=1, color="black", linewidth=2)
    streets.plot_streets(zorder=1, color="white", linewidth=.75, label=None, fstr="--", dashes=(3, 7))
    stations.plot_stations(vehicles, "Geo Point", zorder=4, label="vehicle counting station", marker="^", size=50, alpha=1, color="white", edgecolors="#484141")
    stations.plot_stations(temperature, "Koordinaten", zorder=3, label="temperature measuring station", marker="s", color="#484141", size=40, alpha=1)
    #plt.imshow(basel, extent=box, zorder=0, aspect=1.4, alpha=.7, cmap = matplotlib.cm.get_cmap('Greens', 10))
    ##plt.imshow(grid, extent=box, zorder=2, alpha=.8, origin="lower", cmap=matplotlib.cm.get_cmap("Reds", 10))
    plt.imshow(basel, extent=box, zorder=0, aspect=1.4, alpha=.7, cmap = matplotlib.cm.get_cmap('Reds', 10))
    plt.colorbar(label="correlation", fraction=0.046, pad=0.04)
    plt.clim(0, 1)
    plt.title(f"Correlation between Temperature and Vechicle Count\nfrom {date_start} to {date_end}", fontsize=17, pad=20)
    plt.legend()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    img_name = "final_plots/corr_part_" + str(100 + j) + ".png"
    fig.savefig(img_name)
    plt.close()
    print("DONE: " + str(j))
    