from skc.utils import *
from skc.dawson.factor import *
from skc.basis import *

##############################################################################
def get_group_commutator(matrix_V, matrix_W):
	return matrix_V * matrix_W * matrix_V.H * matrix_W.H

##############################################################################
def conjugate(matrix_A, matrix_B):
	return matrix_B * matrix_A * matrix_B.H

##############################################################################
def create_diagonal_submatrices(matrix_D, d):
	# Divide up matrix_D into 2x2 SU(2) unitaries, U_i
	submatrices_D = []
	print "D= " + str(matrix_D)
	for i in range(d/2):
		i2 = i*2
		i21 = (2*i)+1
		#print "i2= " + str(i2)
		#print "i21= " + str(i21)
		#print "D("+str(i2)+","+str(i2)+")= " + str(matrix_D[(i2,i2)])
		a11 = matrix_D[(i2,i2)]
		a12 = 0.0 #matrix_D[(i,i+1)]
		a21 = 0.0 #matrix_D[(i+1,i)]
		a22 = matrix_D[(i21,i21)]
		submatrix_D = matrixify([[a11,a12],[a21,a22]])
		print "D_"+str(i)+ "= " + str(submatrix_D)
		submatrices_D.append(submatrix_D)
		# These don't have to be unitary, but we'd like them close to I
		#assert_matrix_unitary(submatrix_D)
	return submatrices_D

##############################################################################
def reconstruct_diagonal_matrix(submatrices, d):
	matrix_D = matrixify(numpy.eye(d))
	
	for i in range(d/2):
		i2 = i*2
		i21 = (2*i)+1
		submatrix_D = submatrices[i]
		#print "U_"+str(i)+ "= " + str(submatrix_U)
		matrix_D[(i2,i2)] = submatrix_D[(0,0)]
		matrix_D[(i21,i21)] = submatrix_D[(1,1)]
		
	return matrix_D
	
##############################################################################
def create_group_commutator_submatrices(submatrices_D, basis, axis):
	submatrices_V = []
	submatrices_W = []
	
	for submatrix_U in submatrices_D:
		print "U_i= " + str(submatrix_U)
		(submatrix_V, submatrix_W) = \
			dawson_group_factor(submatrix_U, basis, axis)
		print "V_i= " + str(submatrix_V)
		print "W_i= " + str(submatrix_W)
		delta = get_group_commutator(submatrix_V, submatrix_W)
		print "delta= " + str(delta)
		dist = trace_distance(submatrix_U, delta)
		print "dist(U_i, delta)= " + str(dist)
		assert_approx_equals_tolerance(dist, 0, 1)
		#assert_matrices_approx_equal(submatrix_U, delta, trace_distance)
		# Write an assert_group_factor method here from skc_group_factor
		submatrices_V.append(submatrix_V)
		submatrices_W.append(submatrix_W)
		
	return (submatrices_V, submatrices_W)
	
##############################################################################
# We don't currently use axis, I need to find a better way to make this
# interoperable with dawson_group_factor
def aram_diagonal_factor(matrix_U, basis, axis):
	# Get the SU(d) unitary matrix_U in diagonal form (matrix_D)
	(matrix_P, matrix_D) = diagonalize(matrix_U, basis)

	submatrices_U = create_diagonal_submatrices(matrix_D, basis.d)
	
	matrix_U2 = reconstruct_diagonal_matrix(submatrices_U, basis.d)
	trace_dist = trace_distance(matrix_D, matrix_U2)
	assert_approx_equals(trace_dist, 0)
	
	# Find balanced group commutator for each submatrix
	
	# We pass in the basis and x-axis for SU(2) here, since that was the whole
	# point of this diagonalization scheme
	submatrices_V, submatrices_W = \
		create_group_commutator_submatrices(submatrices_U, H2, X_AXIS)	
	
	# Construct the big group commutator from the subcommutators
	matrix_V = reconstruct_diagonal_matrix(submatrices_V, basis.d)
	matrix_W = reconstruct_diagonal_matrix(submatrices_V, basis.d)
	
	matrix_D2 = get_group_commutator(matrix_V, matrix_W)
	trace_dist = trace_distance(matrix_D, matrix_D2)
	print "dist(D,D2)= " + str(trace_dist)
	
	# Undiagonalize
	matrix_Vt = conjugate(matrix_V, matrix_P)
	matrix_Wt = conjugate(matrix_W, matrix_P)
	
	# Verify that we can multiply it all back again
	matrix_U3 = get_group_commutator(matrix_Vt, matrix_Wt)
	trace_dist = trace_distance(matrix_U, matrix_U3)
	print "dist(U,U3)= " + str(trace_dist)
	return (matrix_Vt, matrix_Wt)