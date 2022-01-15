import numpy as np

mapdata = np.genfromtxt('Data/testmap.csv', delimiter = ',')
print (len(mapdata))
twoblocks = np.genfromtxt('Data/2 blocks.csv', delimiter = ',')

buildertest = np.genfromtxt('Data/testmap2.csv', delimiter = ',')
