# Test whether we can recover the angle of rotation from a random unitary in SU(d)

from skc_diagonalize import *
from skc_basis import *
from skc_utils import *
from skc_compose import *
from skc_decompose import *

import numpy
import math

B = get_hermitian_basis(d=4)
	
(matrix_U, components, angle) = get_random_unitary(B)

for k,v in components.items():
	print str(k) + " => " + str(v)

sorted_components = B.sort_canonical_order(components)

for x in sorted_components:
	print str(x)

(matrix_U2, components2, angle2) = get_random_unitary(B)

sorted_components2 = B.sort_canonical_order(components2)

# Verify that order of components in both vectors correspond to canonical order
for key in components.keys():
	value = components[key]
	value2 = components2[key]
	
	index = sorted_components.index(value)
	index2 = sorted_components2.index(value2)
	
	assert(index == index2)
	
# Roundtrip by creating a dictionary from a vector in canonical order
component_dict = B.unsort_canonical_order(sorted_components)
component_dict2 = B.unsort_canonical_order(sorted_components2)

# Check that our dictionary is the same as before
for key,value in component_dict.items():
	value2 = components[key]
	assert_approx_equals(value, value2)
	
for key,value in component_dict2.items():
	value2 = components2[key]
	assert_approx_equals(value, value2)