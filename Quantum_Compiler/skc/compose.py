# Module for composing / constructing matrices from a given basis
# Either random or non-random, unitary or hermitian

import random
import scipy.linalg
import numpy

from skc.utils import *
from skc.diagonalize import *

##############################################################################
def get_random_hermitian(basis):
	# Vector of elements corresponding to components from basis
	components = {}
	for k,v in basis.items_minus_identity():
		components[k] = random.random()
		
	norm = scipy.linalg.norm(components.values())

	for k in components:
		components[k] /= norm
		
	# Check that we have actually normalized this vector
	assert_approx_equals(scipy.linalg.norm(components.values()), 1)
	
	d = basis.d
	sum = matrixify(numpy.zeros([d,d]))
	
	for k,v in basis.items_minus_identity():
		#print str(k) + " => " + str(v)
		sum = sum + (components[k] * basis.get(k).matrix)
	#print str(sum)
		
	assert_matrix_hermitian(sum)
	
	return (sum, components)

##############################################################################
def exp_hermitian_to_unitary(matrix_H, angle, basis):
	#print "exp_hermitian_to_unitary angle= " + str(angle)
	(matrix_V, matrix_W) = diagonalize(matrix_H, basis)
	Udiag = matrix_exp_diag(-1j*angle*matrix_W)
	assert_matrix_unitary(Udiag)
	# Now translate it back to its non-diagonal form
	U = matrix_V * Udiag * matrix_V.I
	assert_matrix_unitary(U)
	return U
	
##############################################################################
# Compose a random unitary by first creating a random Hermitian
# from the given Hermitian basis, and exponentiating it.
# Return the unitary matrix and its original Hermitian components
# This works for general SU(d), where d is given by the hermitian basis.
def get_random_unitary(basis_H, angle_lower=-PI_HALF, angle_upper=PI_HALF):
	(matrix_H, components_H) = get_random_hermitian(basis_H)
	# Choose a random angle between the angle_lower and angle_upper
	angle_range = angle_upper - angle_lower
	angle = (random.random() * angle_range) + angle_lower
	
	matrix_U = exp_hermitian_to_unitary(matrix_H, angle, basis_H)
	return (matrix_U, components_H, angle)
	
##############################################################################
# Compose a matrix given components from a basis
# Does not check whether components are normalized, or even from the basis
def matrix_from_components(components, basis):
	assert_approx_equals(scipy.linalg.norm(components.values()), 1)
	d = basis.d
	sum = matrixify(numpy.zeros([d,d]))
	for k,v in components.items():
		#print str(k) + " => " + str(v)
		sum = sum + (v * basis.get(k).matrix)
	#print str(sum)
	return sum

##############################################################################
def axis_to_unitary(axis_components, angle, basis):
	# Check that the axis is normalized
	assert_approx_equals(scipy.linalg.norm(axis_components.values()), 1)
	matrix_H = matrix_from_components(axis_components, basis)
	matrix_U = exp_hermitian_to_unitary(matrix_H, angle, basis)
	return matrix_U
	
##############################################################################
def get_random_axis(basis):
	for k,v in basis.items_minus_identity():
		components[k] = random.random()
		
	norm = scipy.linalg.norm(components.values())

	for k in components:
		components[k] /= norm
		
	# Check that we have actually normalized this vector
	assert_approx_equals(scipy.linalg.norm(components.values()), 1)
	return components