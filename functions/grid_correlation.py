import functions.vals_to_boxes as vtb
import functions.get_bounds as gb
import datetime as dt
import numpy as np

def handle(x, y):
    done = False
    start = 0
    while (not done):
        altered = False

        for i in range(start, len(x)):
            if np.isnan(x[i]) or np.isnan(y[i]):
                del x[i]
                del y[i]
                altered = True
                break
        
        if not altered:
            return
        
def correlation_grid(vdf, tdf, start_date, end_date, n, drop_empty=True, box=None, ignore_nan=True):
    # reformat vehicle data frame
    #vdf.Date = vdf.Date.apply(lambda x: dt.datetime.strptime(x, "%d.%m.%Y"))
    vdf.TimeFrom = vdf.TimeFrom.apply(lambda x: int(x.split(":")[0]))

    # select time frame from data frames
    tdf = tdf[(tdf.Datum >= start_date) & (tdf.Datum <= end_date)]
    vdf = vdf[(vdf.Date >= start_date) & (vdf.Date <= end_date)]
    # due to bad formatting of data
    vdf["hour"] = vdf.DateTimeFrom.apply(lambda x: dt.datetime.fromisoformat(x).hour)
    
    # convert input dates to dt.datetime
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
    
    delta_days = (end_date - start_date).days
    a1_lst = []
    a2_lst = []

    # bounding box
    if box is None:
        box = gb.get_bounds()

    x_min = box[0]
    x_max = box[1]
    y_min = box[2]
    y_max = box[3]
    
    date = start_date
    for i in range(delta_days):
        for hour in range(24):
    
            now1 = tdf[(tdf.Datum == date.strftime("%Y-%m-%d")) & (tdf.Stunde == hour)]
            x = now1.Längengrad.tolist()
            y = now1.Breitengrad.tolist()
            vals = now1.Lufttemperatur.tolist()
            
            a1 = vtb.vals_to_boxes(x, y, vals, x_min, x_max, y_min, y_max, n, remove_empty=drop_empty, avg=True)
            a1_lst.append(a1)
            
            now2 = vdf[(vdf.Date == date.strftime("%Y-%m-%d")) & (vdf.hour == hour)]
            x = now2.Longitude.tolist()
            y = now2.Latitude.tolist()
            vals = now2.Total.tolist()
            
            a2 = vtb.vals_to_boxes(x, y, vals, x_min, x_max, y_min, y_max, n, remove_empty=drop_empty, avg=True)
            a2_lst.append(a2)
        
        # advance one day
        date += dt.timedelta(days=1)
    
    corr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x = []
            for a1 in a1_lst:
                x.append(a1[i][j])
            y = []
            for a2 in a2_lst:
                y.append(a2[i][j])
            
            if ignore_nan:
                handle(x, y)
            
            x = np.array(x)
            y = np.array(y)
            
            corr_mat = np.corrcoef(np.vstack([x, y]))
            corr[i][j] = corr_mat[0][1]
    
    return corr