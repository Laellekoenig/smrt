import pandas as pd
import matplotlib.pyplot as plt
import functions.filter as f
import functions.get_map as get_map
import functions.get_bounds as bounds
import functions.plot_stations as stations
import functions.plot_streets as streets
import functions.temperature_grid as tg
import functions.vehicle_grid as vg

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

# get map and bounding box
basel = get_map.get_basel_square(bw=True)
box = bounds.get_bounds()

# plot temp every station
print("Plotting temperature stations...")
plt.figure(figsize=(10, 10), dpi=160)
stations.plot_stations(luft, "Koordinaten", label="Temperature measuring Stations", zorder=2, color="darkgreen", size=60)
streets.plot_streets(zorder=1)
plt.legend()
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Temperature measuring Stations in Basel from {start} to {end}")
plt.savefig("final_plots/temperature_measuring_stations.png")

# vehicle stations
print("Plotting vehicle counting stations...")
plt.figure(figsize=(10, 10), dpi=160)
stations.plot_stations(verkehr, "Geo Point", label="Vehicle couting Stations", zorder=2, color="orange", size=60, marker=",")
streets.plot_streets(zorder=1)
plt.legend()
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Vehicle counting Stations in Basel from {start} to {end}")
plt.savefig("final_plots/vehicle_counting_stations.png")

# both
print("Plotting measuring stations...")
plt.figure(figsize=(10, 10), dpi=160)
stations.plot_stations(luft, "Koordinaten", label="temperature measuring stations", zorder=2, color="darkgreen", size=60)
stations.plot_stations(verkehr, "Geo Point", label="vehicle couting stations", zorder=2, color="orange", size=60, marker=",")
streets.plot_streets(zorder=1)
plt.legend()
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Measuring Stations in Basel from {start} to {end}")
plt.savefig("final_plots/measuring_stations.png")

# plot average temperature over time frame
print("Calculating average temperature grid...")
avg_temp_grid = tg.temperature_grid(luft, 50, interpolate=True)

print("Plotting average temperature...")
plt.figure(figsize=(10, 10), dpi=160)
plt.imshow(avg_temp_grid, extent=box, zorder=2, alpha=.8, cmap=plt.cm.get_cmap('plasma', 15), origin="lower")
plt.colorbar(label="°C", fraction=0.046, pad=0.04)
plt.clim(5, 20)
streets.plot_streets(zorder=1)
stations.plot_stations(luft, "Koordinaten", label="temperature measuring stations", zorder=3, color="black", size=60, alpha=.7)
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.title(f"Average Temperature in Basel from {start} to {end}")
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
plt.colorbar(label="Average amount of vechicles counted per hour", fraction=0.046, pad=0.04)
plt.clim(100, 400)
streets.plot_streets(zorder=1)
stations.plot_stations(verkehr, "Geo Point", label="vehicle counting stations", zorder=3, marker=",", color="black", size=60, alpha=.7)
plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
plt.title(f"Average amount of vehicles counted per hour in Basel from {start} to {end}")
plt.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("final_plots/avg_vehicles.png")
