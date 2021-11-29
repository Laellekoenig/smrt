# input: x = x-coordinate
#        y = y-coordinate
#        dist = distance around x and y point

# returns: widht and height of the corresponding ellipse
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