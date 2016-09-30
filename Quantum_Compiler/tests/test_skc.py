from skc_operator import *
from skc_dawson import *
from skc_utils import *
from skc_compose import *
from skc_basis import *
import math

d = 4
basis = get_hermitian_basis(d=d)
theta = math.pi / 4 # 45 degrees

axis_U = cart3d_to_h2(x=1, y=1, z=1)
angle_U = math.pi / 12

#matrix_U = axis_to_unitary(axis_U, theta/2.0, basis)
(matrix_U, components, angle) = get_random_unitary(basis)

print "U= " + str(matrix_U)

load_basic_approxes("basic_approxes_su4.pickle")
set_basis(basis)

random_axis = pick_random_axis(basis)
set_axis(random_axis)

Uop = Operator(name="U", matrix=matrix_U)

Un = solovay_kitaev(Uop, 3)
print "Approximated U: " + str(Un)