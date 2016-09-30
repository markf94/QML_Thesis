# Functions for searching basic approximations
from skc.decompose import *
from skc.basic_approx.file import *
from skc.basic_approx.process import *
from skc.operator import *

import time

def load_kdtree(base_dir, filename_suffix):
	filename = base_dir+"/kdt-"+filename_suffix+".pickle"
	tree = read_from_file(filename)
	return tree

def search_kdtree(tree, search_U, basis):
	
	begin_time = time.time()
	
	try:
		(components, K, matrix_H) = unitary_to_axis(search_U, basis)
	except ValueError:
		print "ValueError"
		# too close to identity, decomposition failed, just return identity
		return basis.identity

	# Re-center angles from 0 to 2pi, instead of -pi to pi
	if (K < 0):
		for (k,v) in components.items():
			components[k] = v * -1
		K *= -1
	search_op = Operator(name="Search", matrix=search_U)
	search_op.dimensions = components_to_kdpoint(components, basis, K)
	print "search.dimensions= " + str(search_op.dimensions)
	
	nearest = tree.query(search_op, t=1) # find nearest 4 points
	
	end_time = time.time()
	print "Search time: " + str(end_time - begin_time)
	return nearest[0]

##############################################################################
# Find the closest basic approximation in approxes to arbitrary unitary u
# Based on operator norm distance
def find_basic_approx(approxes, u, distance):
    min_dist = numpy.finfo(numpy.float32).max # set to max float value at first
    closest_approx = None
    found = False
    for approx in approxes:
        #print "approx= " + str(approx)
        #print "u= " + str(u)
        current_dist = distance(approx.matrix,u.matrix)
        #print "current_dist= " + str(current_dist)
        #print "min_dist= " + str(min_dist)
        if (current_dist < min_dist):
            found = True
            min_dist = current_dist
            closest_approx = approx
            
    if (not found):
        raise RuntimeError("No closest approximation found.")
    
    return (closest_approx, min_dist)
