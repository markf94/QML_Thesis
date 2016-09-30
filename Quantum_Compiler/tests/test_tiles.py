from skc_tile import *
import math

from skc_basic_approx import *
from skc_operator import *
from skc_utils import *
import numpy
#import cPickle
import time
import random

PI = math.pi
PI_HALF = math.pi / 2

ur_tile = Tile_SU2(psi = PI_HALF, theta = PI_HALF, phi = PI, width = PI)

# Global phase factor funniness
H = H.scale(-1j)
T = T.scale(numpy.exp(-1j*math.pi / 8))
T_inv = T_inv.scale(numpy.exp(1j*math.pi / 8))

iset = [H, T, T_inv]

# Do it!
basic_approxes = []

begin_time = time.time()

# Collect all basic approxes for sequences of length 1 up to length l_0
for i in range(7):
	i_approxes = gen_basic_approx(iset, i+1)
	for j in i_approxes:
		ur_tile.insert(j)
	basic_approxes.extend(i_approxes)
	#ur_tile.print_string(0)
	print "Number of basic approximations so far: " + str(len(basic_approxes))

gen_time = time.time() - begin_time
print "Generation time: " + str(gen_time)

# Compose a random unitary
angle = random.random() * math.pi / 2
nx = random.random()
ny = random.random()
nz = random.random()

axis = Cart3DCoords(1,0,0)
axis.x = nx
axis.y = ny
axis.z = nz
axis.normalize()

unitary = axis.to_unitary_rotation(angle)
matrix = unitary.to_matrix()
op = Operator("U", matrix)

begin_time = time.time()

(closest_approx, min_dist) = find_basic_approx(basic_approxes, op, trace_distance)

find_time = time.time() - begin_time
print "List search time: " + str(find_time)

begin_time = time.time()

(closest_approx, min_dist) = ur_tile.find_closest_point(op, trace_distance)

find_time = time.time() - begin_time
print "Tree search time: " + str(find_time)