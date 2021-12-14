import numpy as np
import matplotlib.pyplot as plt
import functions.get_map as get_map
import functions.get_bounds as bounds
import functions.plot_streets as streets
import functions.plot_stations as stations
import pandas as pd

def fill(g, n):

    for i in range(n):
        for j in range(n):
            if i % 2 == 0 and j % 2 == 0:
                g[i][j] = 1
            elif i % 2 != 0 and j % 2 != 0:
                g[i][j] = 0
            elif i % 2 == 0 and j % 2 != 0:
                g[i][j] = .25
            else:
                g[i][j] = .5

df = pd.read_csv("datasets/luftklima_reformatted.csv")


box = bounds.get_bounds()
basel = get_map.get_basel_square(bw=False)
basel_bw = get_map.get_basel_square(bw=True)

#7
g = np.zeros((7, 7))
fill(g, 7)

print("Plotting random grid 7x7")
plt.figure(figsize=(10, 10), dpi=160)
plt.imshow(g, extent=box, zorder=2, alpha=.35, cmap=plt.cm.get_cmap('binary', 4))
streets.plot_streets(zorder=1, color="black", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, fstr="--", label=None, dashes=(3, 7))
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.title(f"Dividing Basel into a 7x7 grid", fontsize=17, pad=20)
plt.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("final_plots/7x7grid.png")

# with stations
print("Plotting random grid 7x7")
plt.figure(figsize=(10, 10), dpi=160)
plt.imshow(g, extent=box, zorder=2, alpha=.35, cmap=plt.cm.get_cmap('binary', 4))
streets.plot_streets(zorder=1, color="black", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, fstr="--", label=None, dashes=(3, 7))
stations.plot_stations(df, "Koordinaten", label="temperature measuring station", zorder=3, color="red", size=100, marker='^', edgecolors="darkred")
plt.imshow(basel_bw, extent=box, aspect=1.4, zorder=0)
plt.title(f"Dividing Basel into a 7x7 grid", fontsize=17, pad=20)
plt.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("final_plots/7x7grid_stations.png")

#50
g = np.zeros((50, 50))
fill(g, 50)

print("Plotting random grid 50x50")
plt.figure(figsize=(10, 10), dpi=160)
plt.imshow(g, extent=box, zorder=2, alpha=.35, cmap=plt.cm.get_cmap('binary', 4))
streets.plot_streets(zorder=1, color="black", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, fstr="--", label=None, dashes=(3, 7))
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.title(f"Dividing Basel into a 50x50 grid", fontsize=17, pad=20)
plt.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("final_plots/50x50grid.png")
