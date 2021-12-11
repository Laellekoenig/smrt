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

from functions import vals_to_boxes as boxes
from dateutil.relativedelta import *

# returns tuple with 3 elements (lists),
    # 1. x positions of vehicle stations
    # 2. y positions of vehicle stations
    # 3. correlations of the corresponding stations
def get_corr_for_vstation(temperature, vehicles, radius, time_from, time_to, hour_from, hour_to, time_step = 1, half_day=False):
    startTime = time.time()
    
    date_and_hour_start = dt.datetime.strptime(time_from + " " + hour_from, "%Y-%m-%d %H")
    date_and_hour_start2 = dt.datetime.strptime(time_from + " 9", "%Y-%m-%d %H")
    date_and_hour_end = dt.datetime.strptime(time_to + " " + hour_to, "%Y-%m-%d %H")
    time_from = dt.datetime.strptime(time_from, "%Y-%m-%d")
    time_to = dt.datetime.strptime(time_to, "%Y-%m-%d")
    delta_days = (time_to - time_from).days
    vehicles["hour"] = pd.to_datetime(vehicles["TimeFrom"], format="%H:%M").dt.strftime("%H").astype(int)
    vehicles["Datum"] = pd.to_datetime(vehicles["Date"], format="%d.%m.%Y")#.dt.strftime("%Y-%m-%d")
    temperature["Datum"] = pd.to_datetime(temperature["Datum"], format="%Y-%m-%d")#.dt.strftime("%Y-%m-%d")
    temp = temperature[(temperature.Datum >= time_from) & (temperature.Datum <= time_to)]
    temp_here = temperature[(temperature.Datum >= time_from) & (temperature.Datum <= time_to)]
    veh = vehicles[(vehicles.Datum >= time_from) & (vehicles.Datum <= time_to)]
    veh_here = vehicles[(vehicles.Datum >= time_from) & (vehicles.Datum <= time_to)]
        
    veh_stats = veh["Geo Point"].unique()
    temp_stats = temp["Koordinaten"].unique()
    vx = []
    vy = []
    tx = []
    ty = []
    for point in veh_stats:
        vx.append(float(point.split(",")[1]))
        vy.append(float(point.split(",")[0]))
        
    for point in temp_stats:
        tx.append(float(point.split(",")[1]))
        ty.append(float(point.split(",")[0]))
        
    vn = len(veh_stats)
    tn = len(temp_stats)
    #print(vn)
    #print(tn)
    
    stats = [] # includes a set of nearby temp. measure stations for every vehicle count station
    
    for i in range(vn):
        stats_v = []
        for j in range(tn):
            if haversine(vx[i], vy[i], tx[j], ty[j]) < radius:
                stats_v.append((tx[j], ty[j]))
        stats.append(stats_v)
        
    temp_here["Datum"] = pd.to_datetime(temp_here["Datum"], format="%Y-%m-%d").dt.strftime("%Y-%m-%d")
    veh_here["Datum"] = pd.to_datetime(veh_here["Datum"], format="%Y-%m-%d").dt.strftime("%Y-%m-%d")
    
    
    if half_day: # only take measurements, that were made between 09:00 and 18:00
        corr = []
        v = 0
        for s in stats:
            date_start = date_and_hour_start2
            corr_v = []
            corr_t = []
            while(True):
                date = date_start.strftime("%Y-%m-%d")
                hour = int(date_start.strftime("%H"))

                hourly_stats_temp = temp_here[(temp_here.Datum == date) & (temp_here.Stunde == hour)]
                hourly_stats_veh = veh_here[(veh_here.Datum == date) & (veh_here.hour == hour)]
                temp = 0
                for stat in s:
                    p = str(stat[1]) + "," + str(stat[0])
                    station = hourly_stats_temp[hourly_stats_temp["Koordinaten"] == p]
                    t = station["Lufttemperatur"].tolist()
                    if len(t) != 0:
                        temp += t[0]
                    else:
                        date_start += dt.timedelta(hours=1)
                
                        if int(date_start.strftime("%H")) > 18:
                            date_start += dt.timedelta(hours=14)

                        if date_start > date_and_hour_end:
                            break
                        continue

                if len(s) > 0:
                    temp /= len(s)

                p = str(vy[v]) + "," + str(vx[v])
                vc = hourly_stats_veh[hourly_stats_veh["Geo Point"] == p]
                vcs = vc["Total"].tolist()
                if len(vcs) != 0:
                    v_num = 0
                    v_count = 0
                    for k in range(len(vcs)):
                        v_count += vcs[k]
                        v_num += 1
                    v_count /= v_num
                else:
                    date_start += dt.timedelta(hours=1)
                
                    if int(date_start.strftime("%H")) > 18:
                        date_start += dt.timedelta(hours=14)

                    if date_start > date_and_hour_end:
                        break
                    continue

                corr_v.append(v_count)
                corr_t.append(temp)
                
                date_start += dt.timedelta(hours=1)
                
                if int(date_start.strftime("%H")) > 18:
                    date_start += dt.timedelta(hours=14)
                    
                if date_start > date_and_hour_end:
                    break

            corr_v = np.array(corr_v)        
            corr_t = np.array(corr_t)      
            c = np.corrcoef(np.vstack([corr_v, corr_t]))
            corr.append(c[0][1])

            v += 1  
            #print("DONE: " + str(v), flush=True)
            
    else:
        corr = []
        v = 0
        for s in stats:
            date_start = date_and_hour_start
            corr_v = []
            corr_t = []
            while(True):
                date = date_start.strftime("%Y-%m-%d")
                hour = int(date_start.strftime("%H"))

                hourly_stats_temp = temp_here[(temp_here.Datum == date) & (temp_here.Stunde == hour)]
                hourly_stats_veh = veh_here[(veh_here.Datum == date) & (veh_here.hour == hour)]
                temp = 0
                for stat in s:
                    p = str(stat[1]) + "," + str(stat[0])
                    station = hourly_stats_temp[hourly_stats_temp["Koordinaten"] == p]
                    t = station["Lufttemperatur"].tolist()
                    if len(t) != 0:
                        temp += t[0]
                    else:
                        date_start += dt.timedelta(hours=time_step)
                        if date_start > date_and_hour_end:
                            break
                        continue

                if len(s) > 0:
                    temp /= len(s)

                p = str(vy[v]) + "," + str(vx[v])
                vc = hourly_stats_veh[hourly_stats_veh["Geo Point"] == p]
                vcs = vc["Total"].tolist()
                if len(vcs) != 0:
                    v_num = 0
                    v_count = 0
                    for k in range(len(vcs)):
                        v_count += vcs[k]
                        v_num += 1
                    v_count /= v_num
                else:
                    date_start += dt.timedelta(hours=time_step)
                    if date_start > date_and_hour_end:
                        break
                    continue

                corr_v.append(v_count)
                corr_t.append(temp)
                
                date_start += dt.timedelta(hours=time_step)
                if date_start > date_and_hour_end:
                    break

            corr_v = np.array(corr_v)        
            corr_t = np.array(corr_t)      
            c = np.corrcoef(np.vstack([corr_v, corr_t]))
            corr.append(c[0][1])

            v += 1  
            #print("DONE: " + str(v), flush=True)

    #print(corr)
    #print("TIME NEEDED: ", time.time() - startTime)
    return(vx, vy, corr)

def calc_ellipse_dists(x, y, dist):
    w = []
    h = []

    for i in range(len(x)):
        long2 = geopy.distance.distance(kilometers=dist).destination((y[i], x[i]), bearing=90)
        long2 = long2[1]
        lat2 = geopy.distance.distance(kilometers=dist).destination((y[i], x[i]), bearing=0)
        lat2 = lat2[0]
        
        width = 2 * (x[i] - long2)
        height = 2 * (y[i] - lat2)
        
        w.append(width)
        h.append(height)
        
    return(w, h) # width and height of ellipses

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371*c
    return km


def plot_corr(corr, el, nr, date_start, date_end):
    fig, ax = plt.subplots(figsize=(7, 7), dpi=160)

    cmap = matplotlib.cm.get_cmap('Greens', 10)
    norm = matplotlib.colors.Normalize(vmin=0.0, vmax=1.0)
    ellipses = []
    for i in range(len(corr[2])):
        if corr[2][i] > -999999999999: #get rid of NaN
            ell = Ellipse((corr[0][i], corr[1][i]), el[0][i], el[1][i], 0, color=cmap(norm(corr[2][i])), fill = True, alpha=.7)
            ellipses.append(ell)
    for e in ellipses:
         ax.add_artist(e)

    plot_streets(zorder=1, color="indigo")        
    plot_stations(vehicles, "Geo Point", zorder=3, size=25, color="firebrick", alpha=.9, label="Vehicle counting Station", marker=",")
    plot_stations(temperature, "Koordinaten", zorder=3, size=25, color="darkgoldenrod", alpha=.9, label="Temperature measuring station", marker="^")
    plt.imshow(basel, extent=box, zorder=0, aspect=1.4, alpha=.7, cmap = matplotlib.cm.get_cmap('Greens', 10))
    plt.colorbar(label="correlation", fraction=0.046, pad=0.04)
    plt.clim((0, 1))
    plt.title("Correlation between Temperature and counted Vehicles, from " + date_start + " to " + date_end + ", pad=20")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend(loc='lower right')
    plt.show()

    img_name = "test_images/corr_try_" + str(nr) + ".png" 
    fig.savefig(img_name)
    plt.close()


