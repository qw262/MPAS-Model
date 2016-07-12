#!/usr/bin/env python
'''
Plots profiles for hydro-margin test case
'''
import numpy as np
import netCDF4
#import datetime
# import math
# from pylab import *
from optparse import OptionParser
import matplotlib.pyplot as plt
from matplotlib import cm
# from matplotlib.contour import QuadContourSet
# import time

secInYr = 3600.0 * 24.0 * 365.0  # Note: this may be slightly wrong for some calendar types!

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="file to visualize", metavar="FILE")
parser.add_option("-t", "--time", dest="time", help="time step to visualize (0 based)", metavar="TIME")
parser.add_option("-s", "--save", action="store_true", dest="saveimages", help="include this flag to save plots as files")
parser.add_option("-n", "--nodisp", action="store_true", dest="hidefigs", help="include this flag to not display plots (usually used with -s)")

options, args = parser.parse_args()

if not options.filename:
	print "No filename provided. Using output.nc."
        options.filename = "output.nc"

if not options.time:
	print "No time provided. Using time -1."
        time_slice = -1
else:
        time_slice = int(options.time)


fig = plt.figure(1, facecolor='w')

f = netCDF4.Dataset(options.filename,'r')
#xtime = f.variables['xtime'][:]
xCell = f.variables['xCell'][:]
yCell = f.variables['yCell'][:]
#xEdge = f.variables['xEdge'][:]
#yEdge = f.variables['yEdge'][:]
h = f.variables['waterThickness'][time_slice,:]
#u = f.variables['waterVelocityCellX'][time_slice,:]
P = f.variables['waterPressure'][time_slice,:]
#H = f.variables['thickness'][time_slice,:]

print "Attempting to read thickness field from landice_grid.nc."
fin = netCDF4.Dataset("landice_grid.nc",'r')
H = fin.variables['thickness'][0,:]


# Find center row  - currently files are set up to have central row at y=0
unique_ys=np.unique(yCell[:])
centerY=unique_ys[len(unique_ys)/2]
print "number of ys, center y index, center Y value", len(unique_ys), len(unique_ys)/2, centerY
ind = np.nonzero(yCell[:] == centerY)
x = xCell[ind]/1000.0

print "start plotting."

# water thickness
ax = fig.add_subplot(211)
#plt.plot(x, H[ind]*917.0*9.81/1.0e5, '.-')
plt.plot(x, h[ind], '.-')
plt.xlabel('X-position (km)')
plt.ylabel('water depth (m)')

# water pressure
ax = fig.add_subplot(212)
plt.plot(x, H[ind]*917.0*9.81, '.-')
plt.plot(x, P[ind], '.--')
plt.xlabel('X-position (km)')
plt.ylabel('water pressure (Pa)')

print "plotting complete"

plt.draw()
if options.saveimages:
        print "Saving figures to files."
        plt.savefig('GL-position.png')




if options.hidefigs:
     print "Plot display disabled with -n argument."
else:
     plt.show()

