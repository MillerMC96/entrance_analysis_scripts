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

def plot_pmf_window(time_step):
    # pull indicators

    transparency = 0.7
    text_spacing = bottom * 0.02
    offset_from_indicator = 0.2

    # time step indicator
    plt.axvline(time_step, alpha=transparency)
    plt.text(time_step + offset_from_indicator, bottom + text_spacing, str(time_step), rotation=90)


class atom:
    def __init__(self, x_coor, y_coor, z_coor):
        self.x = float(x_coor)
        self.y = float(y_coor)
        self.z = float(z_coor)

parser = argparse.ArgumentParser(description = 'plotting the short axis distance.')
# xvg option not usable now, but PMF is working fine
parser.add_argument('xvg', metavar='file', nargs='+', type=open, \
                    help='the xvg file containing short axis atoms')
parser.add_argument('-pmf', metavar=('b', 'e'), nargs=2, action='store', \
                    type=int, help='plot the pmf windows')
args = parser.parse_args()

# customize pmf window beginning and ending points
pmf_begin = args.pmf[0]
pmf_end = args.pmf[1]

# read file from command line
xvg_file = open(sys.argv[1], 'r')
lines = xvg_file.readlines()

# customize title
# fig_title = sys.argv[2]

# distance array
dist = []

# time array
time = []

# unit conversion
nm_to_angstrom = 10

# data entry
for line in lines:
    line_entry = line.split()
    # skip comments
    first_charactor = line_entry[0]
    if first_charactor[0] != '#' and first_charactor[0] != '@':
        # read data
        time.append(float(line_entry[0]))
        ALA63_1 = atom(line_entry[1], line_entry[2], line_entry[3])
        ALA63_2 = atom(line_entry[4], line_entry[5], line_entry[6])
        ALA63_3 = atom(line_entry[7], line_entry[8], line_entry[9])
        PHE28 = atom(line_entry[10], line_entry[11], line_entry[12])
        dist1 = find_distance_between(ALA63_1, PHE28)
        dist2 = find_distance_between(ALA63_2, PHE28)
        dist3 = find_distance_between(ALA63_3, PHE28)
        dist.append((dist1 + dist2 + dist3) / 3 * nm_to_angstrom)

# plot parameters
spacing = np.amax(dist) * 0.02
top = np.amax(dist) + spacing
bottom = np.amin(dist) - spacing

# window
N = 100

# moving mean
move_mean = np.convolve(dist, np.ones((N,))/N, mode = 'same')

# moving standard deviation
dist_pd = pd.Series(dist)
move_std = dist_pd.rolling(N).std()

plt.scatter(time, dist, s = 2)
plt.hlines(6.526, time[0], time[-1], colors = 'k', linestyles = '--', label = "crystal structure")
# plt.axvline(x=110, color = 'k', linestyle = '--', label = 'PMF starting point')

# plotting moving mean
plt.plot(time[N-1:-N], move_mean[N-1:-N], 'r', label = "moving average over " + str(N) + " points")

# plotting moving std
dist_upper_bound = list()
dist_lower_bound = list()

for dist_point, std in zip(move_mean, move_std):
    dist_upper_bound.append(dist_point + std)
    dist_lower_bound.append(dist_point - std)
# plotting error band
plt.fill_between(time[N-1:-N], dist_upper_bound[N-1:-N], dist_lower_bound[N-1:-N], alpha = 0.4, label = "error band")

# customizable pmf windows

for i in np.linspace(pmf_begin, pmf_end, 11):
    plot_pmf_window(i)

# self adapting ylim
plt.ylim(bottom, top)
plt.xlabel("time [ps]")
plt.ylabel("distance [Å]")
plt.title("distance along the short axis over time")
plt.legend(loc = 'best')
plt.show()
