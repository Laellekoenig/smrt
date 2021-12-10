import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import functions.filter as f
import functions.get_map as get_map
import functions.get_bounds as bounds
import functions.plot_stations as stations
import functions.plot_streets as streets
import functions.temperature_grid as tg
import functions.vehicle_grid as vg
import functions.grid_correlation as gc

print("Loading data frames...")
verkehr = pd.read_csv("datasets/verkehrszählungen_reformatted.csv")
luft = pd.read_csv("datasets/luftklima_reformatted.csv")

# define time frame
start = "2021-05-03"
end = "2021-05-09"

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
