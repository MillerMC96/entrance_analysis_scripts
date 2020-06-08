import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def find_distance_between(p0, p1):
    dx = p1.x - p0.x
    dy = p1.y - p0.y
    dz = p1.z - p0.z
    distance = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    return distance

class atom:
    def __init__(self, x_coor, y_coor, z_coor):
        self.x = float(x_coor)
        self.y = float(y_coor)
        self.z = float(z_coor)

# read file from command line
xvg_file = open(sys.argv[1], 'r')
lines = xvg_file.readlines()

# customize title
# fig_title = sys.argv[2]

# force constant (kJ/mol/A^2)
FC = 250

# time array
time = []

# unit conversion
nm_to_angstrom = 10

# data arrays for analysis
data_line = []

# data entry
for line in lines:
    line_entry = line.split()
    # skip comments
    first_charactor = line_entry[0]
    if first_charactor[0] != '#' and first_charactor[0] != '@':
        # read data
        data_line.append(line_entry[1:])
        time.append(float(line_entry[0]))

# numpy array of frames
frames_str = np.array(data_line)
frames = frames_str.astype(np.float)
# convert to Angstroms
frames = frames * 10
# frames = np.transpose(frames)
# find deviations
first_frame = frames[0]
deviations = frames - first_frame
# square deviations
deviations_squared = np.square(deviations)
# multiply by force constant to get energy
all_energies = deviations_squared * FC
# sum up the columns
energy_frames = all_energies.sum(axis=1)

# plot parameters
spacing = np.amax(energy_frames) * 0.02
top = np.amax(energy_frames) + spacing
bottom = np.amin(energy_frames) - spacing

# window
N = 100

# moving mean
move_mean = np.convolve(energy_frames, np.ones((N,))/N, mode = 'same')

# moving standard deviation
energy_frames_pd = pd.Series(energy_frames)
move_std = energy_frames_pd.rolling(N).std()

plt.scatter(time, energy_frames, s = 2)
# plt.hlines(6.526, time[0], time[-1], colors = 'k', linestyles = '--', label = "crystal structure")
# plt.axvline(x=110, color = 'k', linestyle = '--', label = 'PMF starting point')

# plotting moving mean
#plt.plot(time[N-1:-N], move_mean[N-1:-N], 'r', label = "moving average over " + str(N) + " points")

# plotting moving std
#energy_frames_upper_bound = list()
#energy_frames_lower_bound = list()

#for energy_frames_point, std in zip(move_mean, move_std):
#    energy_frames_upper_bound.append(energy_frames_point + std)
#    energy_frames_lower_bound.append(energy_frames_point - std)
# plotting error band
#plt.fill_between(time[N-1:-N], energy_frames_upper_bound[N-1:-N], \
#                 energy_frames_lower_bound[N-1:-N], alpha = 0.4, \
#                 label = "error band")

# self adapting ylim
plt.ylim(bottom, top)
plt.xlabel("time [ps]")
plt.ylabel("energy [kJ/mol]")
plt.title("elastic energy of heavy atoms over time")
plt.legend(loc = 'best')
plt.show()
