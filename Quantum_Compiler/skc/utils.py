# Utilities for Solovay-Kitaev compiler

import math
import numpy
import random
import scipy.linalg

TOLERANCE = 1e-15
TOLERANCE2 = 1e-14
TOLERANCE3 = 1e-13
TOLERANCE4 = 1e-12
TOLERANCE5 = 1e-11
TOLERANCE6 = 1e-10
TOLERANCE7 = 1e-9
TOLERANCE8 = 1e-8
TOLERANCE9 = 1e-7
TOLERANCE10 = 1e-6

TOLERANCE_GREATER_THAN = 1e4

PI = math.pi
PI_HALF = PI / 2
THREE_PI_HALF = 1.5*PI
TWO_PI = 2*PI

self_adjoint_operators = []

##############################################################################
def dagger_and_simplify(name):
	len_name = len(name)
	if ((len_name < 1) or (name in self_adjoint_operators)):
		return name
	if (name[len_name-1] == 'd'):
		return name[0:len_name-1]
	else:
		return name+'d'

##############################################################################
def matrixify(array):
	return numpy.matrix(array, dtype=numpy.complex)

##############################################################################
def trace_norm(M):
	trace = numpy.trace(M * M.H)
	return math.sqrt(trace)
	
##############################################################################
def operator_norm(M):
	eig_vals = scipy.linalg.eigvals(M)
	eig_vals = [numpy.abs(x) for x in eig_vals]
	return numpy.max(eig_vals)
	
##############################################################################
def trace_distance(matrix_A, matrix_B):
	matrix_diff = matrix_A - matrix_B
	matrix_diff_dag = numpy.transpose(numpy.conjugate(matrix_diff))
	product = matrix_diff * matrix_diff_dag
	#print "prod= " + str(product)	
	trace_vals = scipy.linalg.eigvals(product);
	return scipy.linalg.norm(trace_vals)
	
##############################################################################
def fowler_distance(matrix_A, matrix_B):
	d = matrix_A.shape[0]
	assert(matrix_A.shape == matrix_B.shape)
	matrix_adjoint = numpy.transpose(numpy.conjugate(matrix_A))
	prod = matrix_adjoint * matrix_B
	trace = numpy.trace(prod)
	frac = (1.0*(d - numpy.abs(trace))) / d
	# Because frac can be negative due to floating point error, take the
	# absolute value before taking square root, since we expect real numbers
	return math.sqrt(numpy.abs(frac))

##############################################################################
def list_as_string(list_A):
	if (len(list_A) == 0):
		return ""
	string = list_A[0]
	for ancestor in list_A[1:]:
	       	string += "-" + ancestor
	return string

##############################################################################
def assert_and_print(bool_condition, arg_to_stringify, msg_prefix=""):
	if (not bool_condition):
		print "[ASSERTION FAILED] " + msg_prefix + ": " + str(arg_to_stringify)
	assert(bool_condition)

##############################################################################
def assert_approx_not_equals_tolerance(value1, value2, tolerance, message=""):
	diff = abs(value1 - value2)
	assert_and_print(diff >= tolerance, diff, message)
	
##############################################################################
def assert_in_range(value, lower, upper, message=""):
	assert_and_print(lower < value, value, "Lower bound= " + str(lower))
	assert_and_print(value < upper, value, "Upper bound= " + str(upper))

##############################################################################
def assert_approx_equals_tolerance(value1, value2, tolerance, message=""):
	diff = abs(value1 - value2)
	assert_and_print(diff < tolerance, diff, message) 
	
##############################################################################
def assert_approx_equals(value1, value2, message=""):
	assert_approx_equals_tolerance(value1, value2, TOLERANCE2, message)

##############################################################################
def assert_approx_not_equals(value1, value2, message=""):
	assert_approx_not_equals_tolerance(value1, value2, TOLERANCE2, message=message)

##############################################################################
def approx_equals_tolerance(value1, value2, tolerance):
	return (abs(value1 - value2) < tolerance)
	
##############################################################################
def approx_equals(value1, value2):
	return (abs(value1 - value2) < TOLERANCE)

##############################################################################
# Indented printing based on depth
def print_indented(message, depth):
	print (" " * (depth * 2)) + message

##############################################################################
# Chain the tensor product of multiple operators
def tensor_chain(op_vector):
	if (len(op_vector) == 0):
		raise RuntimeError("Cannot chain empty list of operators")
	product = None
	for op in op_vector:
		#print "op= " + str(op)
		#print "product= " + str(product)
		if (product == None):
			product = op
		else:
			product = numpy.kron(product, op)
	return product

##############################################################################
def vector_distance(vector_A, vector_B):
	vector_diff = vector_A - vector_B
	return scipy.linalg.norm(vector_diff)

##############################################################################	
def matrix_direct_sum(matrix_A, matrix_B):
  direct_sum = numpy.zeros( numpy.add(matrix_A.shape, matrix_B.shape) )
  direct_sum = matrixify(direct_sum)
  direct_sum[:matrix_A.shape[0],:matrix_A.shape[1]] = matrix_A
  direct_sum[matrix_A.shape[0]:,matrix_A.shape[1]:] = matrix_B
  return direct_sum
  
##############################################################################
def assert_matrices_approx_equal(matrix1, matrix2, distance=trace_distance,
		tolerance=TOLERANCE3):
	dist = distance(matrix1, matrix2)
	msg = "Matrices not-equal:\n" + str(matrix1) + "\n" +  str(matrix2)
	assert_approx_equals_tolerance(dist, 0, tolerance=tolerance, message=msg)

##############################################################################
def assert_matrices_approx_not_equal(matrix1, matrix2, distance=trace_distance,
		tolerance=TOLERANCE3, message=""):
	dist = distance(matrix1, matrix2)
	msg = "Matrices equal:\n" + str(matrix1) + "\n" +  str(matrix2)
	assert_approx_not_equals_tolerance(dist, 0, tolerance=tolerance, \
		message=message)
	
##############################################################################
def assert_matrix_hermitian(matrix):
	adjoint = numpy.transpose(numpy.conjugate(matrix))
	assert_matrices_approx_equal(matrix, adjoint, trace_distance)
	
##############################################################################
def assert_matrix_unitary(matrix, tolerance=TOLERANCE3):
	d = matrix.shape[0]
	identity = matrixify(numpy.eye(d))
	adjoint = numpy.transpose(numpy.conjugate(matrix))
	product = matrix * adjoint	
	assert_matrices_approx_equal(product, identity, trace_distance, tolerance)

##############################################################################
def assert_matrix_nonempty(matrix):	
	abs_trace = numpy.abs(numpy.trace(matrix*matrix.H))
	if (abs_trace < TOLERANCE3):
		print "abs_trace= " + str(abs_trace)
		print "Matrix is empty \n" + str(matrix)
	assert(abs_trace > TOLERANCE3)
	
##############################################################################
def matrix_exp_diag(matrix):
	d = matrix.shape[0]
	matrix_exp = matrixify(numpy.eye(d))
	for i in range(d):
		matrix_exp[(i,i)] = numpy.exp(matrix[(i,i)])
	return matrix_exp
	
##############################################################################
# Taylor series approximation
def matrix_exp(matrix, steps):
	d = matrix.shape[0]
	identity = matrixify(numpy.eye(d))
	sum = identity
	product = identity
	denom = 1
	for i in range(steps):
		product = product * matrix
		denom = denom * (i+1)
		#print "prod/denom= " + str(product / denom)
		sum = sum + (product / denom)
		#print "sum= " + str(product / denom)
	return sum
	
##############################################################################
def n_from_eps(eps, eps_0, c_approx):
	c_approx_sq = c_approx**2
	denom = numpy.log(3.0/2)
	eps_c_approx_sq = eps * c_approx_sq
	eps_0_c_approx_sq = eps_0 * c_approx_sq
	eps_ln = numpy.log(1.0 / eps_c_approx_sq)
	eps_0_ln = numpy.log(1.0 / eps_0_c_approx_sq)
	big_ln = numpy.log(eps_ln / eps_0_ln) / denom
	return numpy.ceil(big_ln)
	
