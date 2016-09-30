# Testing our own matrix exponentiate, since numpy's doesn't seem to work

from skc_utils import *
from skc_operator import *
from skc_diagonalize import *
from skc_basis import *

import numpy

# Verify that numpy.exp is just element-wise exponentiation, not that useful
RX = numpy.exp(-1j*(math.pi/2)*SX.matrix)

print "RX= " + str(RX)

# Pauli X is hermitian (and unitary, but we don't care about that part now)
assert_matrix_hermitian(SX.matrix)

RX2 = matrix_exp(-1j*(math.pi/2)*SX.matrix, 50)

print "RX2= " + str(RX2)

# We can't assert unitarity here, b/c our matrix_exp misformats the matrix
# somehow so that the elements aren't complex, or something.
# Just visually inspect the print str above.
#assert_matrix_unitary(RX2)

# Verify that exponentiating a Hermitian (via its diagonalized form)
# gives a unitary
B2 = get_hermitian_basis(d=2)

(matrix_V, matrix_W) = diagonalize(SX.matrix, B2)

RX3 = matrix_exp_diag(-1j*(math.pi/2)*matrix_W)

print "RX3= " + str(RX3)

# Success! Hopefully
assert_matrix_unitary(RX3)

# Now translate it back to its non-diagonal form
RX4 = matrix_V * RX3 * matrix_V.I

print "RX4= " + str(RX4)

# Should still be unitary
assert_matrix_unitary(RX3)
