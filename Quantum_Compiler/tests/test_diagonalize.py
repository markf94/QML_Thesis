# Test file to see if we can recover hermitian H from unitary U
# By constructing diagonal form explicitly from eigenvalues
import scipy.linalg

from skc.utils import *
from skc.basis import *
from skc.operator import *
from skc.compose import *
import unittest

# Maximum dimension (2**D) to test
D=4

##############################################################################
def test_diagonalize(d):
	B = get_hermitian_basis(d) # SU(2) basis
	
	(matrix_U, components) = get_random_hermitian(B)
	
	#print "U= " + str(matrix_U)
	
	(eig_vals, eig_vecs) = scipy.linalg.eig(matrix_U)
	
	#print "eig_vals= " + str(eig_vals)
	#print "eig_vecs= " + str(eig_vecs)
	
	# Create rows of the matrix from elements of the eigenvectors, to
	# fake creating a matrix from column vectors
	eig_length = len(eig_vecs)
	assert(len(eig_vals) == eig_length)
	
	# Verify eigenvalues and eigenvectors, via Av = \lambdav (eigenvalue eqn)
	for i in range(eig_length):
		col_vec = numpy.matrix(eig_vecs[:,i]).transpose()
		scaled_vec1 = matrix_U * col_vec
		#print "scaled_vec1= " + str(scaled_vec1)
		scaled_vec2 = col_vec * eig_vals[i]
		#print "scaled_vec2= " + str(scaled_vec2)
		dist = vector_distance(scaled_vec1, scaled_vec2)
		assert_approx_equals(dist, 0)
		
	# Create the diagonalization matrix V
	matrix_V = numpy.matrix(eig_vecs) #numpy.matrix(rows)
	
	#print "V= " + str(matrix_V)
	
	# Get adjoint
	matrix_V_dag = numpy.transpose(numpy.conjugate(matrix_V))
	
	# Eigenvector matrix should be unitary if we are to have
	# V be its own inverse
	assert_matrix_unitary(matrix_V)

	# Conjugate with U to see what we get
	#matrix_W = matrix_V * matrix_U * matrix_V_dag
	matrix_W = matrix_V.I * matrix_U * matrix_V
	
	#print "W= " + str(matrix_W)
	
	# Construct the diagonalized matrix that we want
	matrix_diag = numpy.matrix(numpy.eye(d), dtype=numpy.complex)
	for i in range(0,eig_length):
		matrix_diag[(i,i)] = eig_vals[i]
	
	#print "diag= " + str(matrix_diag)
	
	dist = trace_distance(matrix_diag, matrix_W)
	
	#print "dist(diag,W)= " + str(dist)
	assert_approx_equals(dist, 0)

	# Verify that off-diagonal elements are close to zero
	for i in range(eig_length):
		for j in range(eig_length):
			if (i != j):
				assert_approx_equals(matrix_W[(i,j)], 0)
				
	for i in range(0,eig_length):
		diff = abs(matrix_W[(i,i)] - eig_vals[i])
		assert_approx_equals(diff, 0)
		#print "eig_val("+str(i)+") diff= " + str(diff)

##############################################################################
# Class for testing matrix diagonalization for various SU(d)
class TestDiagonalize(unittest.TestCase):

	def test_diagonalize(self):
		for i in range(1,D+1):
			d = 2**i
			test_diagonalize(d=d)

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestDiagonalize)
	suite.addTest(suite1)
	return suite

if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)