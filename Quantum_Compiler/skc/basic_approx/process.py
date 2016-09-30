from skc.basic_approx.file import *
from skc.decompose import *
from skc.operator import *
from skc.kdtree import *

def components_to_kdpoint(components, basis, angle):
	point = basis.sort_canonical_order(components)
	point.append(angle) # add the angle as the last component
	return point

def unitary_to_kdpoint(matrix_U):
	(components, K, matrix_H) = unitary_to_axis(matrix_U, basis)
	return components_to_kdpoint(components, basis, K)

# Load the sequences from files beginning with filename_prefix and ending with
# filename_suffix with the numbers 1 to filename_upper (inclusive) in between.
# Constructs a kdtree from all the loaded sequences and returns it for searching. 
def build_kdtree(filename_prefix, filecount_upper, filename_suffix):
	filenames = []
	for i in range(1,filecount_upper+1):
		filenames.append(filename_prefix+str(i)+filename_suffix)
	
	# This is the data that we load from a file
	sequences = []
	for filename in filenames:
		new_sequences = read_from_file(filename)
		sequences.extend(new_sequences)
	
	data = []
	# Process this to produce the format the kdtree expects, namely a list of components in each dimension
	for operator in sequences:
		#print "op= " + str(operator)
		#print "matrix= " + str(operator.matrix)
		#operator.dimensions = unitary_to_kdpoint(operator.matrix)
		#print "dimensions= " + str(operator.dimensions)
		# Now dimensions is in R^{d^2}
		data.append(operator)
		
	
	# Build it! Kablooey
	tree = KDTree.construct_from_data(data)
	return tree

def process_kdtree(base_dir, filecount_upper):
	# Start the generate timer
	begin_time = time.time()
	
	tree = build_kdtree(base_dir+"/gen-g", filecount_upper, "-1.pickle")
	
	set_filename_prefix(base_dir+"/kdt")
	set_filename_suffix(str(filecount_upper))
	
	build_time = time.time() - begin_time
	print "Build time: " + str(build_time)
	
	dump_to_file(tree)

