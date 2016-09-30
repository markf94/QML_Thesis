from skc_dawson_factor import *
from skc_decompose import *
from skc_operator import *
from skc_utils import *
from skc_basis import *

B2 = get_hermitian_basis(d=2)
#(matrix_U, components, angle) = get_random_unitary(B2)

axis_U = cart3d_to_h2(x=1, y=1, z=1)
angle_U = math.pi / 12

matrix_U = axis_to_unitary(axis_U, angle_U/2.0, B2)

print "U= " + str(matrix_U)

[matrix_A, matrix_B] = dawson_x_group_factor(matrix_U, B2)

print "A="
print str(matrix_A)

matrix_A_true = numpy.matrix([
	[ 0.96674550+0.24723584j, -0.01620469-0.06336385j],
	[ 0.01620469-0.06336385j,  0.96674550-0.24723584j]])
assert_matrices_approx_equal(matrix_A, matrix_A_true, trace_distance)

print "B="
print str(matrix_B)

matrix_B_true = numpy.matrix([
	[ 0.96674550+0.j,         -0.24776633+0.06336385j],
	[ 0.24776633+0.06336385j,  0.96674550+0.j        ]])
assert_matrices_approx_equal(matrix_B, matrix_B_true, trace_distance)