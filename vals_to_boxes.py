import numpy as np

'''
returns a nXn array that can be plotted
boxes contain sum of values contained within
'''
def vals_to_boxes(x, y, vals,x_min, x_max, y_min, y_max, n):
    a = np.zeros((n, n))

    x_range = np.linspace(x_min, x_max, n + 1)
    y_range = np.linspace(y_min, y_max, n + 1)

    for i in range(len(y_range) - 1):
        for j in range(len(y_range) - 1):
            for k in range(len(vals)):
                lo = x[k]
                la = y[k]
                val = vals[k]

                if lo >= x_range[j] and lo < x_range[j + 1] and la >= y_range[i] and la < y_range[i + 1]:
                    a[i][j] += val
    
    return a
