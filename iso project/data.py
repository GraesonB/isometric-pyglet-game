import numpy as np

test_walls = np.genfromtxt('Data/testmap.csv', delimiter = ',')
test_floor = np.genfromtxt('Data/floor.csv', delimiter = ',')

walls_32 = np.genfromtxt('Data/32_empty.csv', delimiter = ',')
floor_32 = np.genfromtxt('Data/32_floor.csv', delimiter = ',')

mapdata = [floor_32, walls_32]







#twoblocks = np.genfromtxt('Data/2 blocks.csv', delimiter = ',')

#buildertest = np.genfromtxt('Data/testmap2.csv', delimiter = ',')
