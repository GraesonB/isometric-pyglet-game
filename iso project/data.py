import numpy as np
from variables import *

floor_4 = np.genfromtxt('Data/4x4floor.csv', delimiter = ',')

walls_16 = np.genfromtxt('Data/16x16walls.csv', delimiter = ',')
floor_16 = np.genfromtxt('Data/16x16floor.csv', delimiter = ',')

walls_32 = np.genfromtxt('Data/32x32walls.csv', delimiter = ',')
floor_32 = np.genfromtxt('Data/32x32floor.csv', delimiter = ',')

shrub_data = np.genfromtxt('Data/shrub.csv', delimiter = ',')


if map_size == 16:
    mapdata = [floor_4, walls_16]
if map_size == 32:
    mapdata = [floor_32, walls_32]







#twoblocks = np.genfromtxt('Data/2 blocks.csv', delimiter = ',')

#buildertest = np.genfromtxt('Data/testmap2.csv', delimiter = ',')
