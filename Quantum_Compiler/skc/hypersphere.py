from skc.decompose import *
import numpy

# acos and asin restrict the last hyperspherical coordinate (\phi_{n-1}) to
# [0,pi] and [-pi/2,+pi/2] respectively
# whereas \phi_{n-1} should range from [0 to 2pi]
# This method fixes up phi_n1 to be from this true range, based on the signs
# of the product of sines (of \phi_1 up to \phi_{n-2})
def fix_last_hsphere_coord(product, c_n, c_n1):
	# Handle degenerate cases
	if (approx_equals(product, 0)):
		# If all other angles zero, just return angle of 0, since it could be
		# anything in [0,2pi]
		assert_approx_equals(c_n, 0)
		assert_approx_equals(c_n1, 0)
		return 0
	if (approx_equals(c_n1, 0)):
		# If c_n1 close to 0, cos(phi_n1) close to 0, sin(phi_n1) close to 1 
		assert_approx_equals(c_n, product)
		assert_approx_equals(c_n1, 0)
		return PI_HALF
	if (approx_equals(c_n, 0)):
		# If c_n close to 0, cos(phi_n1) close to 1, sin(phi_n1) close to 0
		assert_approx_equals(c_n1, product)
		assert_approx_equals(c_n, 0)
		return 0
	
	# Now it's time to get the raw angles, restricted by acos and asin
	
	# acos restricts the angle from [0,pi]
	phi_n1_acos = math.acos(c_n1 / product)
	# asin restricts the angle from [-pi/2,+pi/2]
	phi_n1_asin = math.asin(c_n / product)

	#-------------------------------------------------------------------------
	# CASE 1: \phi_{n-1} \in [0, PI_HALF]
	# If sign(product) == sign(c_n1) == sign(c_n)
	if (((product > 0) and (c_n1 > 0) and (c_n > 0)) or
	    ((product < 0) and (c_n1 < 0) and (c_n < 0))):
		assert_approx_equals(phi_n1_acos, phi_n1_asin)
		assert_in_range(phi_n1_acos, 0, PI_HALF) # cos(\phi_n1) > 0
		assert_in_range(phi_n1_asin, 0, PI_HALF) # sin(\phi_n1) > 0
		# The angle is correct, we can return either one
		return phi_n1_acos
	#-------------------------------------------------------------------------
	# CASE 3: \phi_{n-1} \in [PI, THREE_PI_HALF]
	# else if sign(product) has different sign, but sign(c_n1) == sign(c_n)
	elif (((product > 0) and (c_n1 < 0) and (c_n < 0)) or
	      ((product < 0) and (c_n1 > 0) and (c_n > 0))):
		assert_in_range(phi_n1_acos, PI_HALF, PI) # cos(\phi_n1) < 0
		assert_in_range(phi_n1_asin, -PI_HALF, 0) # sin(\phi_n1) < 0

		# Choose the acos angle after fixing it up
		phi_n1_acos = TWO_PI - phi_n1_acos
		assert_in_range(phi_n1_acos, PI, THREE_PI_HALF)
		new_c_n1 = math.cos(phi_n1_acos) * product
		assert_approx_equals(c_n1, new_c_n1)

		# but check that the asin one shifted returns the correct sine
		phi_n1_asin = -phi_n1_asin + PI
		assert_in_range(phi_n1_asin, PI, THREE_PI_HALF)
		new_c_n = math.sin(phi_n1_asin) * product
		assert_approx_equals(c_n, new_c_n)

		# Sanity check that we have the same angle in both cases
		assert_approx_equals(phi_n1_acos, phi_n1_asin)
		return phi_n1_acos
	#-------------------------------------------------------------------------
	# CASE 2: \phi_{n-1} \in [PI_HALF, PI]
	# else if sign(product) == sign(c_n) but != sign(c_n1)
	elif (((product > 0) and (c_n1 < 0) and (c_n > 0)) or
	      ((product < 0) and (c_n1 > 0) and (c_n < 0))):
		assert_in_range(phi_n1_acos, PI_HALF, PI) # cos(\phi_n1) < 0
		assert_in_range(phi_n1_asin, 0, PI_HALF)  # sin(\phi_n1) > 0
		
		# Choose the acos angle because it is in the correct range
		# but check that the asin phi shifted returns the correct sine
		phi_n1_asin = PI - phi_n1_asin
		assert_in_range(phi_n1_asin, PI_HALF, PI)
		new_c_n = math.sin(phi_n1_asin) * product
		assert_approx_equals(c_n, new_c_n)
		
		# Sanity check that we have the same angle in both cases
		assert_approx_equals(phi_n1_acos, phi_n1_asin)
		return phi_n1_acos
	#-------------------------------------------------------------------------
	# CASE 4: \phi_{n-1} \in [THREE_PI_HALF, TWO_PI]
	# else if sign(product) == sign(c_n1) but != sign(c_n)
	elif (((product < 0) and (c_n1 < 0) and (c_n > 0)) or
	      ((product > 0) and (c_n1 > 0) and (c_n < 0))):
		assert_in_range(phi_n1_acos, 0, PI_HALF) # cos(\phi_n1) > 0
		assert_in_range(phi_n1_asin, -PI_HALF, 0) # sin(\phi_n1) < 0

		# Choose the acos angle but fix it up first
		phi_n1_acos = TWO_PI - phi_n1_acos
		assert_in_range(phi_n1_acos, THREE_PI_HALF, TWO_PI)
		new_c_n1 = math.cos(phi_n1_acos) * product
		assert_approx_equals(c_n1, new_c_n1)
		
		# then check that asin phi shifted returns the correct sine
		phi_n1_asin = -phi_n1_asin + THREE_PI_HALF
		assert_in_range(phi_n1_asin, THREE_PI_HALF, TWO_PI)
		new_c_n = math.sin(phi_n1_asin) * product
		assert_approx_equals(c_n, new_c_n)
		
		# Sanity check that we have the same angle in both cases
		assert_approx_equals(phi_n1_acos, phi_n1_asin)
		return phi_n1_acos

	# When all else fails...
	else:
		raise RuntimeError("Signs of cartesian coords inconsistent!")

##############################################################################
# Convert hyperspherical coordinates in a certain basis to a unitary
# Dual of unitary_to_hspherical below.
def hspherical_to_unitary(hsphere_coords, basis):
	print "**********************HSPHERICAL_TO_UNITARY"

	# For SU(d), we require (d^2) - 1 hyperspherical coordinates
	d21 = (basis.d**2) - 1
	d2 = (basis.d**2)

	angle = hsphere_coords[0]

	cartesian_coords = range(d2)
	
	#Remember that all non-identity components are scaled by sin(theta)
	for i in range(1,d2):
		cartesian_coords[i] = 1.0 / math.sin(angle)
	
	 # This is the identity component, which we discard
	cartesian_coords[0] = 1.0
	
	print "angle= " + str(angle)

	# Flag that tells us whether to fill in cartesian coords
	# for degenerate hspherical coords
	zero_from_now_on = False
	
	for i in range(0,d21):
		# If the current hsphere coord is zero, then all other
		# hsphere coords degenerate to zero, and we're done
		if (approx_equals(hsphere_coords[i], 0)):
			print "hsphere_coords["+str(i)+"] is zero, all others degenerate"
			for j in range(i+1,d21):
				assert_approx_equals(0, hsphere_coords[j])
			zero_from_now_on = True
		
		# Otherwise, proceed with taking successive sines and cosines
		# Find product of all previous sines of hsphere coords
		product = 1
		for j in range(0,i):
			print "sin(hsphere_coords["+str(j)+"])= " + \
				str(math.sin(hsphere_coords[j]))
			product *= math.sin(hsphere_coords[j])
		print "product of sines from 0 to " + str(i) + "= " + str(product)
		print "hsphere_coord[" + str(i) + "]= " + str(hsphere_coords[i])
		cartesian_coords[i] *= math.cos(hsphere_coords[i]) * product
		print "cartesian_coord["+str(i)+"]= " + str(cartesian_coords[i])
		
		# If this is the next to last hsphere_coord, take the last sine
		if (i == (d21-1)):
			cartesian_coords[d21] *= math.sin(hsphere_coords[d21-1])*product
			print "cartesian_coord["+str(d21)+"]= " + str(cartesian_coords[d21])
		
	components = basis.unsort_canonical_order(cartesian_coords[1:d2])
	
	print "axis= " + str(components)
	matrix_U2 = axis_to_unitary(components, angle, basis)		

	return matrix_U2

##############################################################################
# Convert a unitary rotation to hyperspherical coordinates
# Dual to hspherical_to_unitary above
def unitary_to_hspherical(matrix_U, basis):
	print "**********************UNITARY_TO_HSPHERICAL"
	(components, K, matrix_H) = unitary_to_axis(matrix_U, basis)
	angle = K/2.0
	
	print "angle= " + str(angle)
	ni = numpy.trace(matrix_U * basis.identity.matrix).real / basis.d
	print "ni= " + str(ni)
	
	cartesian_coords = basis.sort_canonical_order(components)
	
	for i in range(len(cartesian_coords)):
		cartesian_coords[i] *= math.sin(angle)
	
	# For SU(d), we require (d^2) - 1 hyperspherical coordinates
	d21 = (basis.d**2) - 1
	
	# Initialize hsphere_coords to contain initial angle
	hsphere_coords = [angle]
	print "hsphere_coords[0]= " + str(hsphere_coords[0])
	
	for i in range(1,d21):
		# If the current hsphere coord is zero, then all other
		# hsphere coords degenerate to zero, and we're done
		if (approx_equals(hsphere_coords[i-1], 0)):
			print "hsphere_coords["+str(i)+"] is zero, all others degenerate"
			for j in range(i,d21):
				hsphere_coords.append(0)
			break
		
		# Otherwise, proceed with taking succesive sines and cosines
		
		# Take sin of previous hsphere coord
		sin_i1 = math.sin(hsphere_coords[i-1])
		# Find product of all previous sines of hsphere coords
		product = 1
		for j in range(0,i):
			print "sin(hsphere_coords["+str(j)+"])= " + \
				str(math.sin(hsphere_coords[j]))
			product *= math.sin(hsphere_coords[j])
		print "product of sines from 0 to " + str(i) + "= " + str(product)
		print "cartesian_coord["+str(i-1)+"]= " + str(cartesian_coords[i-1])
		print "ratio= " + str(cartesian_coords[i-1] / product)
		angle_i = math.acos(cartesian_coords[i-1] / product)
		print "hsphere_coord[" + str(i) + "]= " + str(angle_i)
		hsphere_coords.append(angle_i)
		
		# If this is the next to last hsphere_coord, take the last arcsine
		# and verify it against the last hspherical coord
		if (i == (d21-1)):
			angle_i = math.asin(cartesian_coords[d21-1] / product)
			print "cartesian_coord["+str(d21-1)+"]= " + str(cartesian_coords[d21-1])
			#print "hsphere_coord[" + str(d21-1) + "]= " + str(angle_i)
			# The last two coords must give same angle from acos and asin
			# or be off by pi, since acos is restricted to [0,2pi] and
			# asin is restricted to [-pi/2,pi/2]
			angle_diff = abs(hsphere_coords[d21-1]- angle_i)
			angles_equal = approx_equals_tolerance(angle_diff, 0, TOLERANCE3)
			angles_off_by_pi = approx_equals_tolerance(angle_diff, PI, TOLERANCE3)
			if (not angles_equal and not angles_off_by_pi):
				print "angle_diff= " + str(angle_diff)
			assert(angles_equal or angles_off_by_pi)
	return hsphere_coords
