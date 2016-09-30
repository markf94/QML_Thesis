from skc_diagonalize import *
from skc_basis import *
from skc_compose import *
from skc_dawson_factor import *
from skc_group_factor import *

import numpy

d=4
H4 = get_hermitian_basis(d=d)
H2 = get_hermitian_basis(d=2)
X_AXIS = cart3d_to_h2(x=1, y=0, z=0)

basis = H4
axis = pick_random_axis(H4)

(matrix_U, components, angle) = get_random_unitary(basis)
print "matrix_U= " + str(matrix_U)

(matrix_V, matrix_W) = aram_diagonal_factor(matrix_U, H4)

matrix_U2 = get_group_commutator(matrix_V, matrix_W)

print "matrix_U2= " + str(matrix_U2)