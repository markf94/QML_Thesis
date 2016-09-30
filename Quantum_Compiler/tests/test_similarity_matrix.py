from skc.dawson.factor import *
from skc.basis import *
from skc.operator import *
from skc.utils import *

import math
import unittest

# Maximum dimension (2**D) to test
D = 1

##############################################################################
def test_similarity(matrix_U1, matrix_U2, basis):
	
	#print "U1= " + str(matrix_U1)
	
	#print "U2= " + str(matrix_U2)

	# Test finding similarity matrix
	matrix_S = find_similarity_matrix(matrix_U1, matrix_U2, basis)
	
	#print "S= "
	#print str(matrix_S)
	
	(axis_S, K, matrix_H) = unitary_to_axis(matrix_S, basis)
	angle_S = K/2.0
	
	#print "axis_S: " + str(axis_S)
	#print "angle_S: " + str(angle_S)
	
	# S * U2 * S^\dagger
	matrix_U = matrix_S * matrix_U2 * matrix_S.H
	
	# Now let's conjugate this bitch
	#print "Conjugated U="
	#print str(matrix_U)
	
	distance = trace_distance(matrix_U1, matrix_U)
	#print "Distance from U= " + str(distance)
	assert_approx_equals(distance, 0)
	
	# Test that swapping U1 and U2 gives adjoint S
	matrix_S2 = find_similarity_matrix(matrix_U2, matrix_U1, basis)
	dist2 = trace_distance(matrix_S, matrix_S2.H)
	#print "Distance(S,S2_dag)= " + str(dist2)
	assert_approx_equals(dist2, 0)
	
	assert_matrix_unitary(matrix_S)
	
	#matrix_S_S_dag = matrix_S * matrix_S.H
	#assert_matrices_approx_equal(matrix_S_S_dag, basis.identity.matrix, trace_distance)
	return matrix_S

#############################################################################
# Some definitions common to all the tests below
B2 = get_hermitian_basis(d=2)
x_axis = cart3d_to_h2(x=1,y=0,z=0)
y_axis = cart3d_to_h2(x=0,y=1,z=0)
z_axis = cart3d_to_h2(x=0,y=0,z=1)

#############################################################################
# Start with something easy, which we've verified with Chris's C++ compiler
# x-axis to z-axis
def test_x_pi_z_pi():
	theta = math.pi
	
	unitary_U1 = axis_to_unitary(x_axis, theta/2.0, B2)
	assert_matrices_approx_equal(SX.matrix, unitary_U1, fowler_distance)
	unitary_U2 = axis_to_unitary(z_axis, theta/2.0, B2)
	assert_matrices_approx_equal(SZ.matrix, unitary_U2, fowler_distance)
	
	#print "======================"
	#print "SIMILARITY(X pi, Z pi)"
	matrix_S = test_similarity(unitary_U1, unitary_U2, B2)
	matrix_S_true = numpy.matrix([
		[ 0.70710678+0.j, -0.70710678+0.j],
		[ 0.70710678+0.j,  0.70710678+0.j]])
	assert_matrices_approx_equal(matrix_S, matrix_S_true, trace_distance)

#############################################################################
# Start with something easy, which we've verified with Chris's C++ compiler
# x-axis to y-axis
def test_x_pi_y_pi():
	theta = math.pi
	
	unitary_U1 = axis_to_unitary(x_axis, theta/2.0, B2)
	assert_matrices_approx_equal(SX.matrix, unitary_U1, fowler_distance)
	unitary_U2 = axis_to_unitary(y_axis, theta/2.0, B2)
	assert_matrices_approx_equal(SY.matrix, unitary_U2, fowler_distance)
	
	#print "======================"
	#print "SIMILARITY(X pi, Y pi)"
	matrix_S = test_similarity(unitary_U1, unitary_U2, B2)
	matrix_S_true = numpy.matrix([
		[ 0.70710678+0.70710678j,  0.00000000+0.j        ],
		[ 0.00000000+0.j,          0.70710678-0.70710678j]])
	assert_matrices_approx_equal(matrix_S, matrix_S_true, trace_distance)

#############################################################################
# Test something more complicated
def test_x_pi_12_y_pi_12():
	theta = math.pi / 12
	
	# First rotation is about axis (1,0,0)
	unitary_U = axis_to_unitary(x_axis, theta, B2)
	
	# Second rotation is about axis(0,1,0) of same angle
	unitary_U2 = axis_to_unitary(y_axis, theta, B2)
	
	#print "====="
	#print "SIMILARITY(X pi/12, Y pi/12)"
	matrix_S = test_similarity(unitary_U, unitary_U2, B2)
	matrix_S_true = numpy.matrix([
		[ 0.70710678+0.70710678j,  0.00000000+0.j        ],
 		[ 0.00000000+0.j,          0.70710678-0.70710678j]])
	assert_matrices_approx_equal(matrix_S, matrix_S_true, trace_distance) 		

##############################################################################
def create_test_case(d):
	basis = get_hermitian_basis(d=d)

	# Class for testing similarity matrices for various SU(d)
	class TestSimilarity(unittest.TestCase):
	
		def setUp(self):
			self.basis = basis
	
		def test_similarity(self):
			# Choose a unitary of some random axis and angle
			(matrix_U1, components1, angle) = get_random_unitary(basis)
			
			# Compose another unitary of the same angle around a
			# different random axis
			(H, components) = get_random_hermitian(basis)
			
			matrix_U2 = exp_hermitian_to_unitary(H, angle, basis)
			assert_matrix_unitary(matrix_U2)
	
			test_similarity(matrix_U1, matrix_U2, basis)
			
	return TestSimilarity

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	
	loader = unittest.TestLoader()

	for i in range(1,D+1):
		d = 2**i
		test_case = create_test_case(d)
		suite1 = loader.loadTestsFromTestCase(test_case)
		suite.addTest(suite1)
	
	suite.addTest(unittest.FunctionTestCase(test_x_pi_z_pi))
	suite.addTest(unittest.FunctionTestCase(test_x_pi_y_pi))
	suite.addTest(unittest.FunctionTestCase(test_x_pi_12_y_pi_12))
	return suite
	
##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
