# input: the start date as string (yyyy-mm-dd) and the end date as string, as well as the radius in km you want to have around the vehicle stations
#        vehicles, temperature are two dataframes
# returns a tuple with a list of the x coordinates of the vstations, a list of the y coordinates of the vstations and a list of the correlations to the vstations
def get_temp_for_vstation(time_from, time_to, radius, vehicles, temperature):
    startTime = time.time()
    vehicles["hour"] = pd.to_datetime(vehicles["TimeFrom"], format="%H:%M").dt.strftime("%H").astype(int)
    vehicles["Datum"] = pd.to_datetime(vehicles["Date"], format="%d.%m.%Y").dt.strftime("%Y-%m-%d")
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
            #if math.sqrt((vx[i] - tx[j])**2 + (vy[i] - ty[j])**2) < radius:
                stats_v.append((tx[j], ty[j]))
        stats.append(stats_v)
    
    time_from = dt.datetime.strptime(time_from, "%Y-%m-%d")
    time_to = dt.datetime.strptime(time_to, "%Y-%m-%d")
    delta_days = (time_to - time_from).days
    
    corr = []
    for s in stats:
        v = 0
        num = 0
        date = time_from
        corr_v = []
        corr_t = []
        for i in range(delta_days):
            for h in range(24):
                
                hourly_stats_temp = temp_here[(temp_here.Datum == date.strftime("%Y-%m-%d")) & (temp_here.Stunde == h)]
                hourly_stats_veh = veh_here[(veh_here.Datum == date.strftime("%Y-%m-%d")) & (veh_here.hour == h)]

                temp = 0
                for stat in s:
                    #print(stat[0])
                    p = str(stat[1]) + "," + str(stat[0])
                    station = hourly_stats_temp[hourly_stats_temp["Koordinaten"] == p]
                    #print(station)
                    t = station["Lufttemperatur"].tolist()
                    #print(t.head())
                    if len(t) != 0:
                        temp += t[0]
                num += 1
                if len(s) > 0:
                    temp /= len(s)
                #print(temp, flush=True)

                p = str(vy[v]) + "," + str(vx[v])
                vc = hourly_stats_veh[hourly_stats_veh["Geo Point"] == p]
                vcs = vc["Total"].tolist()
                #print(vc)
                if len(vcs) != 0:
                    v_num = 0
                    v_count = 0
                    for k in range(len(vcs)):
                        v_count += vcs[k]
                        v_num += 1
                    v_count /= v_num
                else:
                    v_count = 0
                #print(v_count)
                
                corr_v.append(v_count)
                corr_t.append(temp)
                
        corr_v = np.array(corr_v)        
        corr_t = np.array(corr_t)      
        c = np.corrcoef(np.vstack([corr_v, corr_t]))
        corr.append(c[0][1])
            
        v += 1

    #print(corr)
    #print("TIME NEEDED: ", time.time() - startTime)
    return(vx, vy, corr)