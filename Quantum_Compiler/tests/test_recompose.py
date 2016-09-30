from skc.basis import *
from skc.decompose import *
from skc.compose import *
from skc.utils import *

import unittest

# Maximum dimension (2**D) to test
D = 4

##############################################################################
# Test for recovering a sign change in the hermitian from a single
# component
def test_recover_sign(d):
	B = get_hermitian_basis(d=d)
	(H, components) = get_random_hermitian(B)
	
	#print "H= " + str(H)
	
	(components2, norm) = get_basis_components(H, B)
	random_key = random.choice(components2.keys())
	components2[random_key] *= -1
	
	H3 = matrix_from_components(components2, B)

	(components3, norm) = get_basis_components(H, B)
	
	for k,v in components3.items():
		if (k != random_key):
			assert_approx_equals(v, components2[k])
		else:
			assert_approx_equals(-v, components2[k])
	
##############################################################################
# Method for constructing a matrix from basis components
def test_redecompose(d):
	B = get_hermitian_basis(d=d)
	(H, components) = get_random_hermitian(B)
	
	#print "H= " + str(H)
	
	(components2, norm) = get_basis_components(H, B)
	
	H3 = matrix_from_components(components2, B)

	(components3, norm) = get_basis_components(H, B)
	
	for k,v in components3.items():
		assert_approx_equals(v, components2[k])

##############################################################################
# Method for constructing a matrix from basis components
def test_recompose(d):
	B = get_hermitian_basis(d=d)
	(H, components) = get_random_hermitian(B)
	
	#print "H= " + str(H)
	
	(components2, norm) = get_basis_components(H, B)
	
	H3 = matrix_from_components(components2, B)
	
	#print "H3= " + str(H3)
	
	dist = trace_distance(H, H3)
	assert_approx_equals(dist, 0)

##############################################################################
# Class for testing recompose for various SU(d)
class TestRecompose(unittest.TestCase):

	def test_recover_sign(self):
		for i in range(1,D+1):
			d = 2**i
			test_recover_sign(d=d)

	def test_recompose(self):
		for i in range(1,D+1):
			d = 2**i
			test_recompose(d=d)

	def test_redecompose(self):
		for i in range(1,D+1):
			d = 2**i
			test_redecompose(d=d)

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestRecompose)
	suite.addTest(suite1)
	return suite

if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
