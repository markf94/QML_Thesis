from skc.basis import *
from skc.decompose import *
from skc.hypersphere import *

import math
import unittest

##############################################################################
def test_hsphere_coords_roundtrip(basis):

	(matrix_U, components, angle) = get_random_unitary(basis)
	
	axis = basis.sort_canonical_order(components)
	print "axis= " + str(axis)
	theta = math.pi / 12
	print "U=" + str(matrix_U)
	hsphere_coords = unitary_to_hspherical(matrix_U, basis)
	
	print str(hsphere_coords)
	
	matrix_U2 = hspherical_to_unitary(hsphere_coords, basis)
	print "U2=" + str(matrix_U2)
	
	assert_matrices_approx_equal(matrix_U, matrix_U2, trace_distance)

##############################################################################
def test_hsphere_coords_random(basis):

	(matrix_U, components, angle) = get_random_unitary(basis)
	theta = math.pi / 12
	print "U=" + str(matrix_U)
	hsphere_coords = unitary_to_hspherical(matrix_U, basis)
	
	print str(hsphere_coords)

##############################################################################
# Force negative angle to test that edge case
def test_hsphere_coords_random_negative(basis):

	(matrix_U, components, angle) = \
		get_random_unitary(basis, angle_lower = -PI_HALF, angle_upper = 0)
	theta = math.pi / 12
	print "U=" + str(matrix_U)
	hsphere_coords = unitary_to_hspherical(matrix_U, basis)
	
	print str(hsphere_coords)

##############################################################################
def test_hsphere_coords_random_axis(basis):
	theta = math.pi / 12

	axis = pick_random_axis(basis)
	test_hsphere_coords_axis(theta, axis, basis)
	
##############################################################################
def test_hsphere_coords_axis(angle, axis, basis):
	matrix_U = axis_to_unitary(axis, angle/2.0, basis)
	print "U=" + str(matrix_U)
	hsphere_coords = unitary_to_hspherical(matrix_U, basis)
	
	print str(hsphere_coords)
	
	matrix_U2 = hspherical_to_unitary(hsphere_coords, basis)
	print "U2=" + str(matrix_U2)
	
	assert_matrices_approx_equal(matrix_U, matrix_U2, trace_distance)

axis2 = cart3d_to_h2(x=1, y=1, z=1)
H2 = get_hermitian_basis(d=2)
H4 = get_hermitian_basis(d=4)

#test_hsphere_coords_axis(angle=math.pi/12, axis=axis2, basis=H2)
#test_hsphere_coords_random_axis(basis=H2)
#test_hsphere_coords_random(basis=H2)
#test_hsphere_coords_random_negative(basis=H2)
#test_hsphere_coords_roundtrip(basis=H2)
#test_hsphere_coords_random_axis(basis=H4)
#test_hsphere_coords_random(basis=H4)

##############################################################################
# Class for testing matrix logarithms for various SU(d)
class TestHSphereLastCoord(unittest.TestCase):

	# Degenerate case where phi_1 = phi_2 = 0, then phi_3 should = 0 too
	def test_fix_last_hsphere_coord_degen_1(self):
		c_n1 = 0
		c_n = c_n1
		product = 0
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals(phi_n1, 0)

	def test_fix_last_hsphere_coord_case_1(self):
		c_n1 = math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals_tolerance(phi_n1, 0.785398163397, 1e-12)

	# These hard-coded examples are taken from an SU(2) rotation of math.pi / 12
	# about an axis(1,1,1) normalized
	# This should return a phi_ni in the range [0, PI_HALF]
	def test_fix_last_hsphere_coord_case_1(self):
		c_n1 = math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals_tolerance(phi_n1, 0.785398163397, 1e-12)

	# This should return a phi_ni in the range [PI_HALF, PI]
	# by just flipping the sign of the phi_1 
	def test_fix_last_hsphere_coord_case_2(self):
		c_n1 = -math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = -c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		correct_phi_n1 = 0.785398163397 + PI_HALF
		#correct_phi_n1 = THREE_PI_HALF - 0.785398163397
		assert_approx_equals_tolerance(phi_n1, correct_phi_n1, 1e-12)

	# This should return a phi_ni in the range [PI, THREE_PI_HALF]
	# by just flipping the sign of the phi_1 
	def test_fix_last_hsphere_coord_case_3(self):
		c_n1 = math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = c_n1
		phi_1 = -math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals_tolerance(phi_n1, 0.785398163397 + PI, 1e-12)

	# This should return a phi_ni in the range [THREE_PI_HALF, TWO_PI]
	# by just flipping the sign of the phi_1 
	def test_fix_last_hsphere_coord_case_4(self):
		c_n1 = -math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = -c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = -math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		#correct_phi_n1 = 0.785398163397 + PI
		correct_phi_n1 = TWO_PI - 0.785398163397
		assert_approx_equals_tolerance(phi_n1, correct_phi_n1, 1e-12)

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestHSphereLastCoord)
	suite.addTest(suite1)
	return suite

if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)