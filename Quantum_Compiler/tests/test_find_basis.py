# Test file to try and find an orthonormal,traceless basis for SU(D)

import numpy
import unittest
import types

from skc.utils import *
from skc.operator import *
from skc.basis import *

# Maximum dimension (2**D) to test
D=3

def test_unitary_identity(basis_dict):

	# Extract the dimension of the matrices, based on (0,0) identity element
	element00 = basis_dict[(0,0)]
	d = element00.matrix.shape[0]

#def test_orthogonality(basis):
	# I think this property only holds for Pauli matrices and SU(2)
	#print "TESTING SELF-PRODUCT TRACE"
	# Assert that all basis elements have a trace self-product of d
	#for gate in basis_dict.values():
	#	print "Testing " + str(gate) +"\n" + str(gate.matrix)
	#	abs_trace = numpy.abs(numpy.trace(gate.matrix*gate.matrix))
	#	assert_approx_equals(abs_trace, d)

def create_basis_test_case(basis):
	class TestBasis(unittest.TestCase):
	
		def setUp(self):
			self.basis = basis
	
		# Test that the basis identity matrix is equal to standard identity		
		def test_identity_matrix(self):
			identity_element = self.basis.identity
			d = self.basis.d
			# identity element should be equal to eye(d)
			identity = numpy.matrix(numpy.eye(d), dtype=numpy.complex)
			id_distance = trace_distance(identity, identity_element.matrix)
			assert_approx_equals(id_distance, 0)
	
		# Test that each basis element is self-traceless
		def test_self_traceless(self):
			identity_element = self.basis.identity
			for gate in self.basis.basis_dict.values():
				if (gate == identity_element):
					# Skip the identity, it is not traceless
					continue
				#print "Testing \n" + str(gate)
				assert_approx_equals(numpy.trace(gate.matrix), 0)
	
		# Test that every basis element is orthogonal to every other	
		def test_orthogonal(self):
			for gate in self.basis.basis_dict.values():
				# Remove the gate from the second list copy to avoid self-multiplication
				basis2 = list(self.basis.basis_dict.values())
				#print "Removing \n" + str(gate)
				#print "From \n" + str(basis2)
				basis2.remove(gate)
				for gate2 in basis2:
					#print "Testing \n" + str(gate) + "\n " + str(gate.matrix)
					#print "  vs. \n" + str(gate2) + "\n " + str(gate2.matrix)
					inner_product = hs_inner_product(gate.matrix, gate2.matrix)
					assert_approx_equals(inner_product, 0)
	return TestBasis

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	
	loader = unittest.TestLoader()

	# Add hermitian basis tests up to D
	for i in range(1,D+1):
		d = 2**i
		
		# Add the Hermitian basis test case for SU(d)
		basis_H = get_hermitian_basis(d=d)
		test_case_H = create_basis_test_case(basis_H)
		suite_H = loader.loadTestsFromTestCase(test_case_H)
		suite.addTest(suite_H)

		# Add the unitary basis test case for SU(d)
		basis_U = get_unitary_basis(d=d)
		test_case_U = create_basis_test_case(basis_U)
		suite_U = loader.loadTestsFromTestCase(test_case_U)
		suite.addTest(suite_U)
		
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
