# Test generating random matrices

import numpy
from skc_utils import *
from skc_operator import *
from skc_basis import *

# Get SU(2) basis (I plus Pauli matrices)
B2 = get_basis(d=2)

random_U = get_random_unitary(B2)
print str(random_U)