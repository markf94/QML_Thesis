from skc.utils import *
from skc.decompose import *
from skc.basis import *

import math
import numpy

##############################################################################
# The similarity matrix is the rotation to get from A to B?
def find_similarity_matrix_su2(components_A, components_B,
								angle_A, angle_B, basis):

	#print "*********************FIND_SIMILARITY_MATRIX_SU2"

	#print "components_a= " + str(components_A)
	#print "components_b= " + str(components_B)
	
	#angle_a = scale_A #/ 2.0
	#angle_b = scale_B #/ 2.0
	
	#print "angle_a= " + str(angle_a)
	#print "angle_b= " + str(angle_b)

	# angle_a and angle_b should be the same
	assert_approx_equals(numpy.abs(angle_a), numpy.abs(angle_b))

	vector_a = basis.sort_canonical_order(components_A)
	vector_b = basis.sort_canonical_order(components_B)
	#print "vector_a= " + str(vector_a)
	#print "vector_b= " + str(vector_b)
	
	norm_a = scipy.linalg.norm(vector_a)
	norm_b = scipy.linalg.norm(vector_b)
	
	# Rotation axes should be unit vectors
	assert_approx_equals(norm_a, 1)
	assert_approx_equals(norm_b, 1)

	# ab = a . b (vector dot product)
	ab_dot_product = numpy.dot(vector_a, vector_b)

	# s = b x a (vector cross product), perpendicular to both a & b
	vector_s = numpy.cross(vector_b, vector_a)
	#print "vector_s = " + str(vector_s)

	# what is the interpretation of the cross product here? did we need to
	# normalize this? oops
	norm_s = scipy.linalg.norm(vector_s)
	if (abs(norm_s) < TOLERANCE):
		# The vectors are parallel or anti parallel 
		# i am just pretending they are parallel so fix this.
		return basis.identity.matrix;

	#angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	# Occasionally the lengths of these vectors will drift, so renormalize here
	angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	
	assert((angle_s > 0) and (angle_s < PI))
	for i in range(len(vector_s)):
		vector_s[i] /= norm_s

	# compose angle and axis of rotation into a matrix
	components_S = basis.unsort_canonical_order(vector_s)
	#print "components_S = " + str(components_S)
	matrix_U = axis_to_unitary(components_S, angle_s/2.0, basis)
	#print "matrix_U= " + str(matrix_U)

	return matrix_U

##############################################################################
# The similarity matrix is the rotation to get from A to B?
def find_similarity_matrix(matrix_A, matrix_B, basis):

	#print "*********************FIND_SIMILARITY_MATRIX"

	#print "matrix_A= " + str(matrix_A)
	#print "matrix_B= " + str(matrix_B)

	(components_A, scale_A, hermitian_A) = unitary_to_axis(matrix_A, basis)
	(components_B, scale_B, hermitian_B) = unitary_to_axis(matrix_B, basis)
	#print "components_a= " + str(components_A)
	#print "components_b= " + str(components_B)
	
	angle_a = scale_A #/ 2.0
	angle_b = scale_B #/ 2.0
	
	#print "angle_a= " + str(angle_a)
	#print "angle_b= " + str(angle_b)

	# angle_a and angle_b should be the same
	assert_approx_equals(numpy.abs(angle_a), numpy.abs(angle_b))

	vector_a = basis.sort_canonical_order(components_A)
	vector_b = basis.sort_canonical_order(components_B)
	#print "vector_a= " + str(vector_a)
	#print "vector_b= " + str(vector_b)
	
	norm_a = scipy.linalg.norm(vector_a)
	norm_b = scipy.linalg.norm(vector_b)
	
	# Rotation axes should be unit vectors
	assert_approx_equals(norm_a, 1)
	assert_approx_equals(norm_b, 1)

	# ab = a . b (vector dot product)
	ab_dot_product = numpy.dot(vector_a, vector_b)

	# s = b x a (vector cross product), perpendicular to both a & b
	vector_s = numpy.cross(vector_b, vector_a)
	#print "vector_s = " + str(vector_s)

	# what is the interpretation of the cross product here? did we need to
	# normalize this? oops
	norm_s = scipy.linalg.norm(vector_s)
	if (abs(norm_s) < TOLERANCE):
		# The vectors are parallel or anti parallel 
		# i am just pretending they are parallel so fix this.
		return basis.identity.matrix;

	#angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	# Occasionally the lengths of these vectors will drift, so renormalize here
	angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	
	assert((angle_s > 0) and (angle_s < PI))
	for i in range(len(vector_s)):
		vector_s[i] /= norm_s

	# compose angle and axis of rotation into a matrix
	components_S = basis.unsort_canonical_order(vector_s)
	#print "components_S = " + str(components_S)
	matrix_U = axis_to_unitary(components_S, angle_s/2.0, basis)
	#print "matrix_U= " + str(matrix_U)

	return matrix_U

#############################################################################
def dawson_x_group_factor_su2(matrix_U, basis):

	#print "*********************DAWSON_X_GROUP_FACTOR_SU2"

	(components_U, scale_U, hermitian_U) = unitary_to_axis(matrix_U, basis)
	
	angle_u = scale_U #/ 2.0

	#print "angle_u= " + str(angle_u)
	
	# st = pow(0.5 - 0.5*sqrt(1 - a[1]*a[1]),0.25);
	# a[0] = cos(phi/2), from the I component above
	# st = sin(theta/2) = 4th root of (1/2 - 1/2 * cos(phi/2))
	ni = math.cos(angle_u/2)
	st = math.pow(0.5 - 0.5*ni, 0.25);
	# ct = cos(theta/2), from cos^2 + sin^2 = 1
	ct = math.sqrt(1-(st**2));
	# This converts to spherical coordinations, theta = pitch, alpha = yaw
	theta = 2*math.asin(st);
	alpha = math.atan(st);
	
	#print "st= " + str(st)
	#print "ct= " + str(ct)
	#print "theta= " + str(theta)
	#print "alpha= " + str(alpha)

	ax = st*math.cos(alpha); # x component
	bx = ax
	ay = st*math.sin(alpha); # y component
	by = ay
	az = ct; # z components
	bz = -az; # a and b have opposite z components
	
	components_a = cart3d_to_h2(x=ax, y=ay, z=az)
	components_b = cart3d_to_h2(x=bx, y=by, z=bz)
	#print "vector_a= " + str(components_a)
	#print "vector_b= " + str(components_b)
	
	#matrix_A = axis_to_unitary(vector_a, theta, basis)
	#matrix_B = axis_to_unitary(vector_b, theta, basis)
	
	# Find similarity between A and B^\dagger
	matrix_C = find_similarity_matrix(components_A, components_B,
		angle_A, -angle_B, basis)

	return [matrix_B, matrix_C]

#############################################################################
def dawson_x_group_factor(matrix_U, basis):

	#print "*********************DAWSON_X_GROUP_FACTOR"

	(components_U, scale_U, hermitian_U) = unitary_to_axis(matrix_U, basis)
	
	angle_u = scale_U #/ 2.0

	#print "angle_u= " + str(angle_u)
	
	# st = pow(0.5 - 0.5*sqrt(1 - a[1]*a[1]),0.25);
	# a[0] = cos(phi/2), from the I component above
	# st = sin(theta/2) = 4th root of (1/2 - 1/2 * cos(phi/2))
	ni = math.cos(angle_u/2)
	st = math.pow(0.5 - 0.5*ni, 0.25);
	# ct = cos(theta/2), from cos^2 + sin^2 = 1
	ct = math.sqrt(1-(st**2));
	# This converts to spherical coordinations, theta = pitch, alpha = yaw
	theta = 2*math.asin(st);
	alpha = math.atan(st);
	
	#print "st= " + str(st)
	#print "ct= " + str(ct)
	#print "theta= " + str(theta)
	#print "alpha= " + str(alpha)

	ax = st*math.cos(alpha); # x component
	bx = ax
	ay = st*math.sin(alpha); # y component
	by = ay
	az = ct; # z components
	bz = -az; # a and b have opposite z components
	
	vector_a = cart3d_to_h2(x=ax, y=ay, z=az)
	vector_b = cart3d_to_h2(x=bx, y=by, z=bz)
	#print "vector_a= " + str(vector_a)
	#print "vector_b= " + str(vector_b)
	
	if (approx_equals(theta, 0)):
		# Too close to zero, just return two identities
		return [basis.identity.matrix, basis.identity.matrix]
		#raise RuntimeError("Theta too close to zero!")
	
	matrix_A = axis_to_unitary(vector_a, theta/2.0, basis)
	matrix_B = axis_to_unitary(vector_b, theta/2.0, basis)
	
	# Find similarity between A and B^\dagger
	matrix_C = find_similarity_matrix(matrix_A, matrix_B.H, basis)

	return [matrix_B, matrix_C]

#############################################################################
def dawson_group_factor(matrix_U, basis, x_axis):

	dist = fowler_distance(matrix_U, basis.identity.matrix)
	if (approx_equals_tolerance(dist, 0, TOLERANCE10)):
		# Too close to identity, just return a pair of identities
		return [basis.identity.matrix, basis.identity.matrix]

	#print "*********************DAWSON_GROUP_FACTOR"

	# U is a rotation about some axis, find out by how much, then make
	# that a rotation about the X-axis.
	#print "matrix_U= " + str(matrix_U)
	
	(components_U, scale_U, hermitian_U) = unitary_to_axis(matrix_U, basis)
	angle_u = scale_U / 2.0;
	
	# do the same rotation about the x axis (n is an angle)
	matrix_XU = axis_to_unitary(x_axis, angle_u, basis)
	
	#print "matrix_XU= " + str(matrix_XU)

	# oh!! the similarity matrix is what S stands for!
	# and it is the rotation to get from U to XU
	matrix_S = find_similarity_matrix(matrix_U, matrix_XU, basis);
	matrix_S_dag = numpy.conjugate(numpy.transpose(matrix_S))

	#print "matrix_S= " + str(matrix_S)
	
	# now then wtf is this?! the real bgc-decompose
	[matrix_A, matrix_B] = dawson_x_group_factor(matrix_XU, basis);
	
	#print "matrix_A= " + str(matrix_A)
	#print "matrix_B= " + str(matrix_B)

	V = matrix_S * matrix_A * matrix_S_dag	
	W = matrix_S * matrix_B * matrix_S_dag	
	
	return [ V,W ]
