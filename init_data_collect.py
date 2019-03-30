from scipy.spatial import distance as d
import numpy as np
import pandas as pd


def init_data_collect(atomdict, df):
    """
    This is a helper function for 'opt2hes', it calculates bond angles and
    bond lengths for molecules.
    """
    #Initializing a bunch of values to zero for different reasons
    xsum, ysum, zsum, n = 0, 0, 0, 0
    r2                  = 100

    #Iterate through atom dictionary and generate a martix of positions
    for k, value in atomdict.iteritem():
        key   = np.fromstring(value.split()[0], dtype=np.float64)
        x     = np.fromstring(value.split()[2], dtype=np.float64)
        y     = np.fromstring(value.split()[3], dtype=np.float64)
        z     = np.fromstring(value.split()[4], dtype=np.float64)
        xsum += x
        ysum += y               #Sums are for finding molecule centroid
        zsum += z
        n    += 1

        matrix[key] = np.array([x, y, z])

    xcen = xsum / n
    ycen = ysum / n             #Coordinate points of centroid, from formula
    zcen = zsum / n

    centroid = np.array([xcen, ycen, zcen])

    #Iterate through the matrix dictionary to find center atom
    for key, value in matrix.iteritem():
        r1 = d.euclidean(value, centroid)

        if r1 < r2:
            r2     = r1
            center = (key, value)
