from skc_dawson_factor import *
from skc_decompose import *
from skc_operator import *
from skc_utils import *
from skc_basis import *
from skc_group_factor import *

import math

B2 = get_hermitian_basis(d=2)
#(matrix_U, components, angle) = get_random_unitary(B2)

axis_U = cart3d_to_h2(x=1, y=1, z=1)
angle_U = math.pi / 12

matrix_U = axis_to_unitary(axis_U, angle_U/2.0, B2)

print "U= " + str(matrix_U)

X_AXIS = cart3d_to_h2(x=1, y=0, z=0)
#############################################################################
# Test balanced group commutator factoring
[matrix_V, matrix_W] = dawson_group_factor(matrix_U, B2, X_AXIS)

V = matrix_V
W = matrix_W
V_dag = numpy.transpose(numpy.conjugate(V))
W_dag = numpy.transpose(numpy.conjugate(W))

delta = get_group_commutator(matrix_V, matrix_W) #V * W * V_dag * W_dag

print "Delta= " + str(delta)

distance = trace_distance(delta, matrix_U)
print "Trace Distance(Delta, U): " + str(distance)
assert_approx_equals(distance, 0)