import pandas as pd
import matplotlib.pyplot as plt
import imageio
import datetime as dt
import functions.temperature_grid as tg
import functions.plot_stations as stations
import functions.plot_streets as streets
import functions.get_map as get_map
import functions.get_bounds as bounds
import functions.filter as f

# define time frame
start = "2021-05-03"
end = "2021-05-03"

# load data sets
print("Loading data frames...")
verkehr = pd.read_csv("datasets/verkehrszählungen_reformatted.csv")
luft = pd.read_csv("datasets/luftklima_reformatted.csv")

# filter dates
print("Filtering data frames...")
verkehr = f.filter_date(verkehr, start, end)
luft = f.filter_date(luft, start, end)

# remove wrong measuring station
luft = luft[luft.Name != "Basel_Fenster_Test"]

# get map and bounding box
basel = get_map.get_basel_square(bw=True)
box = bounds.get_bounds()

# create heat map gif over time frame
img_count = 0
current_date = dt.datetime.strptime(start, "%Y-%m-%d")
current_hour = 0
end_date = dt.datetime.strptime(end, "%Y-%m-%d") + dt.timedelta(days=1)

while current_date < end_date:
    # advance counter
    img_count += 1

    # filter data by date and hour
    current_date_string = current_date.strftime("%Y-%m-%d")
    current_df = luft[(luft.Datum == current_date_string) & (luft.Stunde == current_hour)]

    # plot data
    grid = tg.temperature_grid(current_df, 50, interpolate=True)
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, extent=box, zorder=2, alpha=.8, cmap=plt.cm.get_cmap("YlOrRd", 15), origin="lower")
    plt.colorbar(label="°C", fraction=0.046, pad=0.04)
    plt.clim(0, 30)
    streets.plot_streets(zorder=1, color="black", linewidth=2)
    streets.plot_streets(zorder=1, color="white", linewidth=.75, label=None, fstr="--", dashes=(3, 7))
    stations.plot_stations(luft, "Koordinaten", label="temperature measuring station", zorder=3, color="#484141", size=40, alpha=1, marker="s")
    plt.imshow(basel, extent=box, aspect=1.4, zorder=0)
    plt.title(f"Average Temperature in Basel\n{current_date_string} {current_hour}:00", fontsize=17, pad=20, linespacing=1.5)
    plt.legend()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(f"final_plots/temperature_gif/temp_{img_count}.png")

    # advance date and hour
    current_hour += 1
    if current_hour == 24:
        current_hour = 0
        current_date += dt.timedelta(days=1)

# create gif
img_count = 24
imgs = []
for i in range(1, img_count + 1):
    imgs.append(imageio.imread(f"final_plots/temperature_gif/temp_{i}.png"))
imageio.mimsave("final_plots/temp.gif", imgs, duration=5/24)
