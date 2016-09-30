# Testing that we can compose a unitary by exponentiating a hermitian

from skc.operator import *
from skc.utils import *
from skc.basis import *
from skc.compose import *
from skc.decompose import *

import random
import unittest

# Maximum dimension (2**D) to test
D = 4

##############################################################################
def test_pauli_unitary():
	# Pauli matrices are unitary
	assert_matrix_unitary(SX.matrix)
	assert_matrix_unitary(SY.matrix)
	assert_matrix_unitary(SZ.matrix)
	assert_matrix_unitary(I2.matrix)

##############################################################################
def test_pauli_hermitian():
	# Test for Hermiticity just for good measure
	assert_matrix_hermitian(SX.matrix)
	assert_matrix_hermitian(SY.matrix)
	assert_matrix_hermitian(SZ.matrix)
	assert_matrix_hermitian(I2.matrix)

##############################################################################
def create_test_case(d):

	class TestComposeCase(unittest.TestCase):
	
		def setUp(self):
			self.basis = get_hermitian_basis(d=2)

		######################################################################
		def test_compose(self):
			# Get a random Hermitian
			(H, components) = get_random_hermitian(self.basis)
			
			#U = exp_hermitian_to_unitary(H, math.pi/2, self.basis)
			#print "U(pi/2)= " + str(U)
			#assert_matrix_unitary(U)
			angle = random.random() * math.pi
			U = exp_hermitian_to_unitary(H, angle, self.basis)
			#print "U("+str(angle)+")= " + str(U)
			assert_matrix_unitary(U)
			
		######################################################################
		# Test whether reversing the sign of the angle for the same axis
		# results in the adjoint of a unitary
		def test_unitary_reverse_angle(self):
			(H, components) = get_random_hermitian(self.basis)
			angle = random.random() * math.pi
			U = exp_hermitian_to_unitary(H, angle, self.basis)
			Udag = exp_hermitian_to_unitary(H, -angle, self.basis)
			U_Udag = U * Udag
			assert_matrices_approx_equal(U_Udag, self.basis.identity.matrix,
				trace_distance)

		######################################################################
		# Test whether reversing the sign of the hermitian for the same angle
		# results in the adjoint of a unitary
		def test_unitary_reverse_hermitian(self):
			(H, components) = get_random_hermitian(self.basis)
			angle = random.random() * math.pi
			U = exp_hermitian_to_unitary(H, angle, self.basis)
			Udag = exp_hermitian_to_unitary(-H, angle, self.basis)
			U_Udag = U * Udag
			assert_matrices_approx_equal(U_Udag, self.basis.identity.matrix,
				trace_distance)

		######################################################################
		# Test that reversing the sign of the Hermitian
		# gives you a non-equal matrix
		def test_unitary_reverse_hermitian(self):
			(H, components) = get_random_hermitian(self.basis)
			angle = random.random() * math.pi
			U = exp_hermitian_to_unitary(H, angle, self.basis)
			Udag = exp_hermitian_to_unitary(-H, angle, self.basis)
			dist = trace_distance(U, Udag)
			assert_approx_not_equals(dist, 0)
			
		######################################################################
		def test_axis_roundtrip(self):
			(matrix_U, components, angle) = get_random_unitary(self.basis)
			#print "components= " + str(components)
			(components2, K, matrix_H) = unitary_to_axis(matrix_U, self.basis)
			#print "components2= " + str(components2)
			msg = "test_axis_roundtrip(d="+str(self.basis.d)+") K=" + \
				str(K) + " angle=" + str(angle)
			assert_approx_equals_tolerance(K/2.0, abs(angle), TOLERANCE10,
				msg)
			matrix_U2 = axis_to_unitary(components2, K/2.0, self.basis)
			fowler_dist = fowler_distance(matrix_U, matrix_U2)
			assert_approx_equals_tolerance(fowler_dist, 0, TOLERANCE10)
			trace_dist = trace_distance(matrix_U, matrix_U2)
			assert_approx_equals(trace_dist, 0)
			
			# Check that we recovered the correct components (with sign)
			for k,v in components2.items():
				msg = "components not equal: " + \
					"k=" + str(k) + " v=" + \
					str(v) + " v2=" + str(components[k])
				# We just want to check that magnitude and sign is conserved
				assert_approx_equals(v, numpy.sign(angle)*components[k], message=msg)

		######################################################################
		def test_axis_recover_sign(self):
			(matrix_U, components, angle) = get_random_unitary(self.basis)
			#print "components= " + str(components)
			#print "angle= " + str(angle)
			(components2, K2, matrix_H2) = unitary_to_axis(matrix_U, self.basis)
			#print "components2= " + str(components2)
			
			# Reverse the sign of a random components
			random_key = random.choice(components2.keys())
			components2[random_key] *= -1
			#print "components2= " + str(components2)

			matrix_U2 = axis_to_unitary(components2, K2/2.0, self.basis)
			(components3, K3, matrix_H3) = unitary_to_axis(matrix_U2, self.basis)
			#print "components3= " + str(components3)

			msg = "angles not equal: K3=" + \
				str(K3) + " angle=" + str(angle)
			assert_approx_equals_tolerance(K3/2.0, abs(angle), TOLERANCE10,
				msg)
			
			angle_sign = numpy.sign(angle)
			for k,v in components3.items():
				msg = "components not equal: " + \
					"k=" + str(k) + " v=" + str(v) + \
					" v2=" + str(components[k])
				if (k == random_key):
					assert_approx_equals(v, -angle_sign*components[k], message=msg)
				else:
					assert_approx_equals(v, angle_sign*components[k], message=msg)
			
			trace_dist = trace_distance(matrix_U, matrix_U2)
			assert_approx_not_equals(trace_dist, 0)
			
	TestComposeCase.__name__ = "TestComposeCaseD"+str(d)

	return TestComposeCase

##############################################################################	
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()

	# Create one test case for every SU(d)
	for i in range(1,D+1):
		d = 2**i
		test_case = create_test_case(d)
		suite1 = loader.loadTestsFromTestCase(test_case)
		suite.addTest(suite1)
	
	# Add single function tests from above
	suite.addTest(unittest.FunctionTestCase(test_pauli_unitary))
	suite.addTest(unittest.FunctionTestCase(test_pauli_hermitian))
	return suite
	
##############################################################################	
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)