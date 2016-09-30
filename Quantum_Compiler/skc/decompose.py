# Methods for decomposing unitaries

from skc.diagonalize import *
from skc.compose import *

##############################################################################
# Given a Hermitian matrix H which is the logarithm of the unitary U
# and a basis, return the different components of H in that basis
# Also return the global constant factor K
def get_basis_components(matrix_H, basis):
	d = basis.d

	# Create a dictionary with the same keys as basis_dict
	component_dict = {}	
	
	# Iterate over basis elements to pick out components in H
	# Don't include the identity element here
	for key,gate in basis.items_minus_identity():
		kc_alpha = numpy.trace(matrix_H * gate.matrix)
		component_dict[key] = kc_alpha.real
		#print str(key) + "=> " + str(kc_alpha)
		# Components should be real, with negligible imaginary parts
		msg = str(matrix_H)
		#assert_approx_equals(kc_alpha.imag, 0, message=msg)
	
	# Norm will always be positive, so we have to fix up the sign that
	# we return below, b/c it will be interpreted as (two times) an angle
	norm = scipy.linalg.norm(component_dict.values())
	#print "norm= " + str(norm)
	
	sign_plus = 0
	sign_minus = 0

	# Go through components, count how many are positive and negative
	# and scale by norm
	for key,value in component_dict.items():
		# If a value is close to zero, don't use it to determine sign
		if (numpy.abs(value) > TOLERANCE):
			if (value > 0):
				sign_plus += 1
			elif (value < 0):
				sign_minus += 1
		#value /= norm
		#print str(key) + " => " + str(value)
		component_dict[key] = value / norm
		
	# Take a majority vote on the sign of the angle
	if (sign_plus > sign_minus):
		sign = +1
	else:
		sign = -1

	# For now, angle is always positive, let's see how this breaks things
	sign = +1
	#print "sign_plus= " + str(sign_plus)
	#print "sign_minus= " + str(sign_minus)
		
	# Fix sign of components so that they are all positive
	#for k,v in component_dict.items():
	#	component_dict[k] = numpy.abs(v)
	#	assert(component_dict[k] >= 0)

	# Check that we really normalized the values
	assert_approx_equals(scipy.linalg.norm(component_dict.values()), 1)
	
	# Verify that we can compose the matrix again from these components
	M = matrix_from_components(component_dict, basis)
	dist = fowler_distance(M, matrix_H)
	#if (dist > TOLERANCE3):
		#print "dist= " + str(dist)
		#print "M= " + str(M)
	#assert_approx_equals(dist, 0)
	
	# Fix the scale factor to have the right sign
	K = sign*norm
	#print "sign= " + str(sign)

	return (component_dict, K)

##########################################################################
def unitary_to_axis(matrix_U, basis):
	(matrix_V, matrix_W) = diagonalize(matrix_U, basis)
	
	#print "V= " + str(matrix_V)
	#print "W= " + str(matrix_W)
	
	matrix_ln = get_matrix_logarithm(matrix_W)
	
	#print "matrix_ln= " + str(matrix_ln)
	
	# Reconjugate to transform into iH
	matrix_iH = matrix_V * matrix_ln * matrix_V.I
	
	# Factor out -i (since we used -i in exp_hermitian_to_unitary)
	matrix_H = (-1.0/1j) * matrix_iH
	
	#print "matrix_H= " + str(matrix_H)
	trace_norm = numpy.trace(matrix_H * matrix_H.H)
	#print "trace_norm(H)= " + str(trace_norm)
	
	# Compare the calculated components with our original
	(components2, K) = get_basis_components(matrix_H, basis)
	#print "K= " + str(K)
	#angle = K/2.0
	# Scale matrix by our calculated angle
	#matrix_H = matrix_H / angle
	return (components2, K, matrix_H)