import numpy as np
import sys

class atom:
    def __init__(self, x_pos = 0, y_pos = 0, z_pos = 0):
        self.x = float(x_pos)
        self.y = float(y_pos)
        self.z = float(z_pos)
    # return a vector from another atom to this atom 
    def subtract(self, another_atom):
        dx = self.x - another_atom.x
        dy = self.y - another_atom.y
        dz = self.z - another_atom.z
        return atom(dx, dy, dz)

# convert methyl groups into single points
def convert_methyl_to_one_point(atom_list = [atom(), atom(), atom()]):
    x = (atom_list[0].x + atom_list[1].x + atom_list[2].x) / 3
    y = (atom_list[0].y + atom_list[1].y + atom_list[2].y) / 3
    z = (atom_list[0].z + atom_list[1].z + atom_list[2].z) / 3
    return atom(x, y, z)

# parse axis atoms
def read_axis_atoms(data_line):
    axis_atoms = []
    for i in range(0, 12, 3):
        axis_atoms.append(atom(data_line[i], data_line[i+1], data_line[i+2]))
    return axis_atoms

# parse short axis
def get_short_axis_segment(data_line):
    short_axis = read_axis_atoms(data_line[1:])
    return short_axis

# parse long axis
def get_long_axis_segment(data_line):
    long_axis = read_axis_atoms(data_line[13:])
    return long_axis

# read file from command line
xvg_file = open(sys.argv[1], 'r')
lines = xvg_file.readlines()

# data entry
for line in lines:
    line_entry = line.split()
    # skip comments
    first_charactor = line_entry[0]
    if first_charactor[0] != '#' and first_charactor[0] != '@':
        # read data
        short_axis = get_short_axis_segment(line_entry)
        long_axis = get_long_axis_segment(line_entry)

# vector calculation
short_axis_methyl = convert_methyl_to_one_point(short_axis[:-1])
long_axis_methyl = convert_methyl_to_one_point(long_axis[:-1])

# vectors
short_axis_vec = np.array([short_axis[3].subtract(short_axis_methyl).x, \
                           short_axis[3].subtract(short_axis_methyl).y, \
                           short_axis[3].subtract(short_axis_methyl).z])

long_axis_vec = np.array([long_axis[3].subtract(long_axis_methyl).x, \
                          long_axis[3].subtract(long_axis_methyl).y, \
                          long_axis[3].subtract(long_axis_methyl).z])

# final pulling vector
pulling_vector = np.cross(short_axis_vec, long_axis_vec)

print(pulling_vector)
