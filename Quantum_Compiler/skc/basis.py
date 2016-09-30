# Module for constructing complete, standard, orthogonal unitary bases
# for arbitrary SU(d)
# (Generalized Pauli matrices)

import numpy
import math
import random

from skc.utils import *
from skc.operator import *

##############################################################################
# A complete basis for d x d matrices.
# May be Hermitian, Unitary, or neither.
class Basis:

	def __init__(self, d, basis_dict, identity_key):
		self.d = d
		self.basis_dict = basis_dict
		self.keys_minus_identity = list(basis_dict.keys())
		self.keys_minus_identity.remove(identity_key)
		self.identity_key = identity_key
		self.identity = basis_dict[identity_key]
		assert(self.identity != None)
	
	def is_hermitian(self):
		return ('hermitian' in dir(self))

	def is_unitary(self):
		return ('unitary' in dir(self))
		
	def items(self):
		return self.basis_dict.items()

	def items_minus_identity(self):
		no_id = dict(self.basis_dict)
		del no_id[self.identity_key]
		return no_id.items()
		
	def get(self, key):
		return self.basis_dict[key]
		
	def map(self, map_function):
		for gate in self.basis_dict.values():
			map_function(gate.matrix)
			
	# Return a list of the given component dictionary values
	# ordered in the canonical key order of this basis
	def sort_canonical_order(self, components):
		array = []
		for key in self.keys_minus_identity:
			array.append(components[key])
		return array
		
	# Return a dictionary of the given list of values,
	# assuming they are in the same key order as this basis
	def unsort_canonical_order(self, array):
		dict = {}
		keys = self.keys_minus_identity
		array_len = len(array)
		for i in range(array_len):
			dict[keys[i]] = array[i]
		return dict

	def print_string(self):
		print "SU("+str(self.d)+") Basis"
		for gate in self.basis_dict.values():
			print str(gate)
			print str(gate.matrix)

##############################################################################
# Get the standard vector basis for R^n, that is, n n-dimensional vectors
# { v[i] } where v[i] has a 1 in the ith component and 0 everywhere else
def get_standard_vector_basis(d):

	# Get standard basis orthonormal basis vectors for Z_d
	# v[i] will have 1 in the ith component, zero everywhere else
	v = []
	for i in range(d):
		new_vec = numpy.zeros(d)
		# Set one of the components to be 1, the rest stay zeros
		new_vec[i] = 1
		v.append(new_vec)
		#print "v["+str(i)+"]= " + str(new_vec)
	return v

##############################################################################
# Returns a dictionary of generalized hermitian
# Pauli matrices as a basis for SU(d), i.e. Gell-Mann matrices
# i.e. d x d orthonormal matrices that are a complete basis for C^{dxd}
# From http://en.wikipedia.org/wiki/Generalizations_of_Pauli_matrices#Construction
def get_hermitian_basis(d):

	#print "Getting Hermitian basis for SU("+str(d)+")"
	
	range_d = range(d)
	
	# Base case of recursion, just pass back h_{1,1}
	if (d==1):
		return {('h', (1,1)):matrixify(1)}
	
	# Returned basis is a dictionary of key tuples like
	# ('h',(1,d)), ... , ('h', (d,d)),
	# ('f',(k,j)) where k < j
	# ('f',(j,k)) where k > j
	B = {}
	
	# Recursively get the hermitian basis for d-1
	B1 = get_hermitian_basis(d-1)
	
	# Generate the h functions
	# h_{1,d} is always I_d
	op_matrix = matrixify(numpy.eye(d))
	op_name = "h_{1,"+str(d)+"}"
	B[('h',(1,d))] = Operator(name=op_name, matrix=op_matrix)
	
	# h_{k,d} for 1 < k < d
	for k in range(2,d):
		h_k_d1 = B1.get(('h',(k,d-1)))
		op_matrix = matrix_direct_sum(h_k_d1.matrix, matrixify(0))
		op_name = "h_{"+str(k)+","+str(d)+"}"
		B[('h', (k,d))] = Operator(name=op_name, matrix=op_matrix)
	
	# h_{d,d}
	scale = math.sqrt(2.0/(d*(d-1)))
	#print "scale= " + str(scale)
	Id1 = matrixify(numpy.eye(d-1))
	op_matrix = scale * matrix_direct_sum(Id1, matrixify(1-d))
	op_name = "h_{"+str(d)+","+str(d)+"}"
	B[('h',(d,d))] = Operator(name=op_name, matrix=op_matrix)
	#print op_name + "= " + str(op_matrix)
	
	# It is easier to generate Ejk with outer product of standard vector basis
	v = get_standard_vector_basis(d)
	
	# Generate the f functions
	# First, for 1 < k < j <= d
	# subtract one from vector indices since math indices begin at 1
	# but computer indices begin at 0
	for j in range(1,(d+1)):
		for k in range(1,j):
			E_kj = matrixify(numpy.outer(v[k-1],v[j-1]))
			E_jk = matrixify(numpy.outer(v[j-1],v[k-1]))
			op_matrix = E_kj + E_jk
			op_name = "f_{"+str(k)+","+str(j)+"}"
			B[('f',(k,j))] = Operator(name=op_name, matrix=op_matrix)
			
	# Next, for 1 < k < j <= d
	# subtract one from vector indices since math indices begin at 1
	# but computer indices begin at 0
	for k in range(1,(d+1)):
		for j in range(1,k):
			E_kj = matrixify(numpy.outer(v[k-1],v[j-1]))
			E_jk = matrixify(numpy.outer(v[j-1],v[k-1]))
			op_matrix = -1j*(E_jk - E_kj)
			op_name = "f_{"+str(k)+","+str(j)+"}"
			B[('f',(k,j))] = Operator(name=op_name, matrix=op_matrix)			
			
	basis = Basis(d = d, basis_dict = B, identity_key = ('h',(1,d)))
	
	# Sanity check that all returned elements are indeed Hermitian
	for gate in B.values():
		assert_matrix_hermitian(gate.matrix)
		assert_matrix_nonempty(gate.matrix)

	# We use this to check whether the basis is Hermitian		
	basis.hermitian = True

	return basis
	
##############################################################################
# Returns a dictionary of generalized unitary
# Pauli matrices as a basis for SU(d)
# i.e. d x d orthonormal matrices that are a complete basis for C^{dxd}
def get_unitary_basis(d):

	range_d = range(d) # Just call it once here
	
	v = get_standard_vector_basis(d)
		
	zeta = numpy.exp(2j*math.pi / d)
	#print "zeta= " + str(zeta)
	
	S = {}
	for j in range_d:
		for k in range_d:
			sum = 0;
			for m in range_d:
				outer_prod = numpy.outer(v[m],v[(m+k) % d])
				#print "v["+str(m)+"]v["+str((m+k)%d)+"]= " + str(outer_prod)
				jkm_term = (zeta**(j*m)) * outer_prod
				#print "("+str(j)+","+str(k)+","+str(m)+")= " + str(jkm_term)
				sum += jkm_term
			sum = matrixify(sum)
			name = "S_{" + str(j) + "," + str(k) + "}"
			new_op = Operator(name=name, matrix=sum)
			S[(j,k)] = new_op
			# Add these special members here for excluding identity later
			#new_op.j = j
			#new_op.k = k
			#print str(new_op)
			#print str(new_op.matrix)
			
	basis = Basis(d = d, basis_dict = S, identity_key = (0,0))

	# Sanity check that all returned elements are indeed unitary
	for gate in S.values():
		assert_matrix_unitary(gate.matrix)
		assert_matrix_nonempty(gate.matrix)
		
	# How do we check if this basis is complete?

	# We use this to check whether the basis is Hermitian		
	basis.unitary = True
	
	return basis

##############################################################################
# Hilbert-Schmidt inner product
# For defining orthogonality on operators in Hilbert space
# From http://en.wikipedia.org/wiki/Hilbert%E2%80%93Schmidt_operator
def hs_inner_product(matrix_A, matrix_B):
	matrix_A_dag = numpy.transpose(numpy.conjugate(matrix_A))
	return numpy.trace(matrix_A_dag * matrix_B)

##############################################################################
# Perform equivalent of matrix inner product, for testing orthogonality
# i.e. sum of element-wise products
def matrix_inner_product(matrix_A, matrix_B):
	shape_A = matrix_A.shape
	shape_B = matrix_B.shape
	assert(shape_A == shape_B) # matrices should have same shape
	# Reshape matrices into one long array/vector
	matrix_length = shape_A[0] * shape_A[1]
	#print "matrix_length= " + str(matrix_length)
	reshaped_A = matrix_A.reshape(matrix_length)
	reshaped_B = matrix_B.reshape(matrix_length)
	#print "reshaped_A= " + str(reshaped_A)
	#print "reshaped_B= " + str(reshaped_B)
	# Now the reshaped_X look like matrix([[a,b],[c,d]])
	# Is there a better way than converting via a one-row array?
	array_A = numpy.asarray(reshaped_A)
	array_B = numpy.asarray(reshaped_B)
	#print "array_A= " + str(array_A)
	#print "array_B= " + str(array_B)
	# Now the array_X look like array([a,b,c,d])
	# Now we can just do normal vector inner product
	return numpy.dot(array_A, array_B)

##############################################################################
# Convert x,y,z 3D Cartesians coordinates to a dictionary of components
# from the Hermitian (Gell-Mann) basis for SU(2)
def cart3d_to_h2(x, y, z):
	components = {}
	components[('f',(1,2))] = x
	components[('f',(2,1))] = y
	components[('h',(2,2))] = z
	norm = scipy.linalg.norm(components.values())
	for k,v in components.items():
		components[k] /= norm
	return components
	
##############################################################################
# Currently this is only used in Dawson factoring to supply a random axis
def pick_random_axis(basis):
	(random_k,random_v) = random.choice(basis.items_minus_identity())
	components = {}
	for k,v in basis.items_minus_identity():
		if (k == random_k):
			components[k] = 1
		else:
			components[k] = 0
	return components

##############################################################################
# Module constants
H2 = get_hermitian_basis(d=2)
X_AXIS = cart3d_to_h2(x=1, y=0, z=0)
