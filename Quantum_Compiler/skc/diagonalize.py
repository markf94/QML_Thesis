# Functions for diagonalizing matrices

import scipy.linalg
import numpy

from skc.utils import *

##############################################################################
# Diagonalize the given unitary in the given basis, returning the
# diagonal matrix W, and the unitary matrix V such that
#  V * U * V^{-1} = W
# Equivalently, you can call conjugate(W, V) to recover U
# from skc_group_factor
def diagonalize(matrix_U, basis):
	d = basis.d
	#print "U= " + str(matrix_U)
	
	(eig_vals, eig_vecs) = scipy.linalg.eig(matrix_U)
	
	#print "eig_vals= " + str(eig_vals)
	#print "eig_vecs= " + str(eig_vecs)
	
	eig_length = len(eig_vecs)
	assert(len(eig_vals) == eig_length)
	
	# Create the diagonalization matrix V
	matrix_V = numpy.matrix(eig_vecs) #numpy.matrix(rows)
	
	#print "V= " + str(matrix_V)
	
	# Get adjoint
	#matrix_V_dag = numpy.transpose(numpy.conjugate(matrix_V))
	
	# Eigenvector matrix should be unitary if we are to have
	# V dagger be the same as V inverse
	#assert_matrix_unitary(matrix_V, TOLERANCE6, message=str())
	
	
	# Multiply V^{-1} * U * V to diagonalize
	matrix_W = matrix_V.I * matrix_U * matrix_V

	# Assert that we can recover matrix U
	#matrix_U2 = matrix_V * matrix_W * matrix_V.I
	#assert_matrices_approx_equal(matrix_U, matrix_U2, trace_distance)
	
	#print "W= " + str(matrix_W)
	
	# Construct the diagonalized matrix that we want
	matrix_diag = numpy.matrix(numpy.eye(d), dtype=numpy.complex)
	for i in range(eig_length):
		matrix_diag[(i,i)] = eig_vals[i]
	
	# Verify that off-diagonal elements are close to zero
	for i in range(eig_length):
		for j in range(eig_length):
			if (i != j):
				assert_approx_equals(matrix_W[(i,j)], 0)
				
	for i in range(eig_length):
		assert_approx_equals(matrix_W[(i,i)], eig_vals[i])

	return (matrix_V, matrix_W)

##############################################################################
# Return a diagonal matrix whose diagonal elements are natural logarithms
# of the corresponding diagonal elements in the input matrix
def get_matrix_logarithm(matrix_diag):
	d = matrix_diag.shape[0]
	# Copy the matrix
	matrix_ln = numpy.matrix(numpy.zeros([d,d], dtype=numpy.complex))
	
	# Substitute diagonal elements for their natural logarithm
	for i in range(d):
		matrix_ln[(i,i)] = numpy.log(matrix_diag[(i,i)])
		
	return matrix_ln
