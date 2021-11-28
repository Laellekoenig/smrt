import functions.vals_to_boxes as vtb
import functions.get_bounds as gb
import numpy as np
from scipy.interpolate import griddata

# plots average temperature into boxes
# df:   temperature data frame
# date: date that should be plottet ("2021-05-23")
# hour: time in int 
# box:  bounding box of map
# col:  column that should be used as vals
# avg:  if average or total should be calculated
# interpolate:  if true, interpolates temperatures over grid
def temperature_grid(df, date, hour, n, box=None, col="Lufttemperatur", avg=True, interpolate=False):
    day = df[(df.Datum == date) & (df.Stunde == hour)]
    x = day.Längengrad.tolist()
    y = day.Breitengrad.tolist()
    vals = day[col].tolist()

    if box is None:
        box = gb.get_bounds()
    
    x_min = box[0]
    x_max = box[1]
    y_min = box[2]
    y_max = box[3]
    
    a = vtb.vals_to_boxes(x, y, vals, x_min, x_max, y_min, y_max, n, avg=avg)
    
    if interpolate:
        a = temp_interpolate(a)

    return a

def temp_interpolate(p):
    # normal cubic interpolation (but still has nan values on the edges)
    x = np.arange(0, p.shape[1])
    y = np.arange(0, p.shape[0])
    p = np.ma.masked_invalid(p)   # mask nans with --
    xx, yy = np.meshgrid(x, y)
    x1 = xx[~p.mask]
    y1 = yy[~p.mask]
    newarr = p[~p.mask]
    in_p = griddata((x1, y1), newarr.ravel(),(xx, yy), method='cubic')
    
    return in_p
