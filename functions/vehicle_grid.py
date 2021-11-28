import functions.vals_to_boxes as vtb
import functions.get_bounds as gb
import datetime as dt

# plots a heat map of vehicle data frame
# df:   vehicle data frame
# date: date that should be plotted (eg "2021-05-23")
# n:    number of rows and cols in final grid
# col:  name of column that should be used
# box:  bounding box of final plot
def vehicle_grid(df, n, date=None, hour=None, col="Total", box=None, avg=False):
    #df.Date = df.Date.apply(lambda x: dt.datetime.strptime(x, "%d.%m.%Y"))
    df.TimeFrom = df.TimeFrom.apply(lambda x: int(x.split(":")[0]))
    
    if date is not None and hour is not None:
        day = df[(df.Date == date) & (df.TimeFrom == hour)]
    elif date is not None:
        day = df[df.Date == date]
    elif hour is not None:
        day = df[df.TimeFrom == hour]
    else:
        day = df
    
    x = day.Longitude.tolist()
    y = day.Latitude.tolist()
    vals = day[col].tolist()

    if box is None:
        box = gb.get_bounds()
    
    x_min = box[0]
    x_max = box[1]
    y_min = box[2]
    y_max = box[3]

    a = vtb.vals_to_boxes(x, y, vals, x_min, x_max, y_min, y_max, n, avg=avg)

    return a
