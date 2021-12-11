import pandas as pd
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import functions.filter as f
import functions.get_map as get_map
import functions.get_bounds as bounds
import functions.plot_stations as stations
import functions.plot_streets as streets
import functions.temperature_grid as tg
import functions.vehicle_grid as vg
import functions.grid_correlation as gc
import functions.calc_corr as cc


print("Loading data frames...")
verkehr = pd.read_csv("datasets/verkehrszählungen_reformatted.csv")
luft = pd.read_csv("datasets/luftklima_reformatted.csv")

# define time frame
start = "2021-05-01"
end = "2021-05-31"

# define stuff for correlation calculation
radius = 0.4 # include temperature stations within this radius from a vehicle measurement station
hour_from = "9" # starting time in hours (addition to date)
hour_to = "9"
time_step = 1 # steps in hours of which you want tot ake measurements (e.g. every 2 hours)
half_day = True # if True, only take measurements from 9:00 to 18:00 from everyday (then function does not include the 3 arguments above)

# filter dates
print("Filtering data frames...")
verkehr = f.filter_date(verkehr, start, end)
luft = f.filter_date(luft, start, end)

# remove wrong measuring station
luft = luft[luft.Name != "Basel_Fenster_Test"]

# get map and bounding box
basel = get_map.get_basel_square(bw=True)
box = bounds.get_bounds()

# plot temp every station
print("Plotting temperature stations...")
plt.figure(figsize=(10, 10), dpi=160)
stations.plot_stations(luft, "Koordinaten", label="temperature measuring station", zorder=2, color="#567eff", size=120, marker='^', edgecolors="white")
streets.plot_streets(zorder=1, color="#2d4287", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, fstr="--", label=None, dashes=(3, 7))
plt.legend()
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Temperature measuring Stations in Basel\nfrom {start} to {end}", fontsize=17, pad=20)
plt.savefig("final_plots/temperature_measuring_stations.png")

# vehicle stations
print("Plotting vehicle counting stations...")
plt.figure(figsize=(10, 10), dpi=160)
stations.plot_stations(verkehr, "Geo Point", label="vehicle couting station", zorder=2, color="#ff5656", size=90, marker="s", edgecolors="white")
streets.plot_streets(zorder=1, color="darkred", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, fstr="--", label=None, dashes=(3, 7))
plt.legend()
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Vehicle counting Stations in Basel\nfrom {start} to {end}", fontsize=17, pad=20)
plt.savefig("final_plots/vehicle_counting_stations.png")

# both
print("Plotting measuring stations...")
plt.figure(figsize=(10, 10), dpi=160)
stations.plot_stations(luft, "Koordinaten", label="temperature measuring station", zorder=2, color="#567eff", size=120, marker="^", edgecolors="white")
stations.plot_stations(verkehr, "Geo Point", label="vehicle couting station", zorder=2, color="#ff5656", size=90, marker="s", alpha=1, edgecolors="white")
streets.plot_streets(zorder=1, color="#232323", linewidth=2)
streets.plot_streets(zorder=1, color="#e5e5e5", linewidth=.75, fstr="--", label=None, dashes=(3, 7))
plt.legend()
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Measuring Stations in Basel\nfrom {start} to {end}", fontsize=17, pad=20)
plt.savefig("final_plots/measuring_stations.png")

# plot average temperature over time frame
print("Calculating average temperature grid...")
avg_temp_grid = tg.temperature_grid(luft, 50, interpolate=True)

print("Plotting average temperature...")
plt.figure(figsize=(10, 10), dpi=160)
plt.imshow(avg_temp_grid, extent=box, zorder=2, alpha=.8, cmap=plt.cm.get_cmap('YlOrRd', 15), origin="lower")
plt.colorbar(label="°C", fraction=0.046, pad=0.04)
plt.clim(5, 20)
streets.plot_streets(zorder=1, color="black", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, fstr="--", label=None, dashes=(3, 7))
stations.plot_stations(luft, "Koordinaten", label="temperature measuring station", zorder=3, color="#484141", size=40, alpha=1, marker="s")
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.title(f"Average Temperature in Basel\nfrom {start} to {end}", fontsize=17, pad=20)
plt.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("final_plots/average_temperature.png")

# plot average amount of vehicles
print("Calulcating vehicle grid...")
sum_vehicle_grid = vg.vehicle_grid(verkehr, 7, avg=True)

print("Plotting vehicle avg grid...")
plt.figure(figsize=(10, 10), dpi=160)
plt.imshow(sum_vehicle_grid, extent=box, zorder=2, alpha=.8, cmap=plt.cm.get_cmap('Greens', 6), origin="lower")
plt.colorbar(label="average amount of vechicles counted per hour", fraction=0.046, pad=0.04)
plt.clim(100, 400)
streets.plot_streets(zorder=1, color="black", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, label=None, fstr="--", dashes=(3, 7))
stations.plot_stations(verkehr, "Geo Point", label="vehicle counting station", zorder=3, marker="^", color="white", size=50, alpha=1, edgecolors="#484141")
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.title(f"Average Amount of Vehicles counted per Hour\nfrom {start} to {end}", fontsize=17, pad=20)
plt.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("final_plots/avg_vehicles.png")

# reload data frames for grid correlation to work, not ideal
print("reloading verkehrszählungen data set for correlation...")
verkehr = pd.read_csv("datasets/verkehrszählungen_reformatted.csv")
verkehr = f.filter_date(verkehr, start, end)

# plot grid correlation plot
print("Calculating correlation")
grid = gc.correlation_grid(verkehr, luft, start, end, 7)

print("Plotting correlation grid...")
plt.figure(figsize=(10, 10), dpi=160)
plt.imshow(grid, extent=box, zorder=2, alpha=.8, origin="lower", cmap=plt.cm.get_cmap("Reds", 10))
plt.colorbar(label="correlation", fraction=0.046, pad=0.04)
plt.clim(0, 1)
streets.plot_streets(zorder=1, color="black", linewidth=2)
streets.plot_streets(zorder=1, color="white", linewidth=.75, label=None, fstr="--", dashes=(3, 7))
stations.plot_stations(verkehr, "Geo Point", zorder=4, label="vehicle counting station", marker="^", size=50, alpha=1, color="white", edgecolors="#484141")
stations.plot_stations(luft, "Koordinaten", zorder=3, label="temperature measuring station", marker="s", color="#484141", size=40, alpha=1)
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.title(f"Correlation between Temperature and Vechicle Count\nfrom {start} to {end}", fontsize=17, pad=20)
plt.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("final_plots/grid_correlation.png")

# calculate correltation and ellipses
print("Calculating new correlation...")
temperature = pd.read_csv("datasets/luftklima_reformatted.csv")
vehicles = pd.read_csv("datasets/verkehrszählungen_reformatted.csv")
corr = cc.get_corr_for_vstation(temperature, vehicles, radius, start, end, hour_from, hour_to, time_step, half_day)
el = cc.calc_ellipse_dists(corr[0], corr[1], radius)

# plot correlation (new variant)
print("Plotting new correlation...")
fig, ax = plt.subplots(figsize=(7, 7), dpi=160)
cmap = matplotlib.cm.get_cmap('Greens', 10)
norm = matplotlib.colors.Normalize(vmin=0.0, vmax=1.0)
ellipses = []
for i in range(len(corr[2])):
    if corr[2][i] > -999999999999: #get rid of NaN
        ell = Ellipse((corr[0][i], corr[1][i]), el[0][i], el[1][i], 0, color=cmap(norm(corr[2][i])), fill = True, alpha=.7)
        #cir = plt.Circle((corr[0][i], corr[1][i]), 0.004, color=cmap(norm(corr[2][i])), fill = True, alpha=.7)
        ellipses.append(ell)
for e in ellipses:
     ax.add_artist(e)

streets.plot_streets(zorder=1, color="indigo")        
stations.plot_stations(vehicles, "Geo Point", zorder=3, size=25, color="firebrick", alpha=.9, label="Vehicle counting Station", marker=",")
stations.plot_stations(temperature, "Koordinaten", zorder=3, size=25, color="darkgoldenrod", alpha=.9, label="Temperature measuring station", marker="^")
#plt.scatter(corr[0], corr[1], marker="o", zorder=1, c=corr[2], s=600)
plt.imshow(basel, extent=box, zorder=0, aspect=1.4, alpha=.7, cmap = matplotlib.cm.get_cmap('Greens', 10))
plt.colorbar(label="correlation", fraction=0.046, pad=0.04)
plt.clim((0, 1))
plt.title("Correlation between Temperature and counted Vehicles, from " + start + " to " + end + ", pad=20")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc='lower right')
plt.show()

img_name = "test_images/corr.png"
fig.savefig(img_name)
plt.close()
