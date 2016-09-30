# Test whether we can recover the angle of rotation from a random unitary in SU(d)

from skc_diagonalize import *
from skc_basis import *
from skc_utils import *
from skc_compose import *
from skc_decompose import *

import numpy
import math

def test_decomposing_unitary(d):
	print "*******************************************************************"
	print "TESTING DECOMPOSITION OF UNITARY IN SU("+str(d)+")"
	B = get_hermitian_basis(d)
	
	(matrix_U, components, angle) = get_random_unitary(B)
	
	print "U= " + str(matrix_U)
	
	# Get the components of H in basis B
	(components2, K, matrix_H) = unitary_to_axis(matrix_U, B)
	print "H= " + str(matrix_H)
	
	print "K= " + str(K)
	print "angle= " + str(angle)
	assert_approx_equals_tolerance(numpy.abs(K), numpy.abs(2*angle), TOLERANCE4)

	#id_comp = numpy.trace(matrix_U).real / d
	#print "id_comp= " + str(id_comp)
	#angle2 = math.acos(id_comp)
	#print "acos(id_comp)= " + str(angle2)
	#assert_approx_equals(abs(angle), abs(angle2))
	
	#print "Renormalizing... "
	# Renormalize components
	#for key,value in components2.items():
	#	components2[key] = value / K
	#	print "("+str(key)+")= " + str(components2[key])
	
	# Assert that the components are now normalized
	norm = scipy.linalg.norm(components.values())
	norm2= scipy.linalg.norm(components2.values())
	print "norm= " + str(norm)
	print "norm2= " + str(norm2)
	assert_approx_equals(norm2, 1)
		
	for key in components2.keys():
		print str(key)
		print "  actual= " + str(components[key])
		print "  comput= " + str(components2[key])
		ratio = abs(components[key]) / abs(components2[key])
		#print "  ratio= " + str(ratio)
		assert_approx_equals_tolerance(ratio, 1, TOLERANCE5)

	# Check that we are truly normalized
	assert_approx_equals(scipy.linalg.norm(components2.values()), 1)
	print "norm3= " + str(scipy.linalg.norm(components2.values()))

	# Recompose unitary from recovered hermitian and angle
	H2 = matrix_from_components(components2, B)
	# Scale Hermitian by angle (but only for SU(4)?)
	if (d==4):
		H2 = H2 / angle
	assert_matrix_hermitian(H2)
	print "H2= " + str(H2)
	dist = fowler_distance(H2, matrix_H)
	print "dist(H2,H)= " + str(dist)
	assert_approx_equals_tolerance(dist, 0, TOLERANCE10)
	dist = trace_distance(H2, matrix_H)
	assert_approx_equals_tolerance(dist, 0, TOLERANCE5)
	
	U2 = exp_hermitian_to_unitary(matrix_H=matrix_H, angle=angle, basis=B)
	print "U2= " + str(U2)
	dist = fowler_distance(matrix_U, U2)
	print "dist(U2,U)= " + str(dist)
	assert_approx_equals_tolerance(dist, 0, TOLERANCE10)

test_decomposing_unitary(d=2)
test_decomposing_unitary(d=4)
#test_decomposing_unitary(d=8)
