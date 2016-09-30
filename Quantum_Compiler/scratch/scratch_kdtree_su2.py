from skc.kdtree import *
from skc.basic_approx.file import *
from skc.compose import *
from skc.decompose import *
from skc.basis import *
from skc.basic_approx.process import *
from skc.basic_approx.search import *

import time

# Really, we should save the basis to a file with the instruction set, maybe
basis = get_hermitian_basis(d=2)

base_dir = "pickles/su2"
file_upper = 16

tree = build_kdtree(base_dir+"/gen-g", file_upper, "-1.pickle")

#process_kdtree(base_dir, file_upper)

#tree = load_kdtree(base_dir, str(file_upper))

# This is the random matrix that we are looking for
(search_U, components, angle) = get_random_unitary(basis)
op = search_kdtree(tree, search_U, basis)

print "op= " + str(op)
#print "op.dims= " + str(op.dimensions)
print "fowler_dist(op,U)= " + str(fowler_distance(op.matrix, search_U))
print "trace_dist(op,U)= " + str(trace_distance(op.matrix, search_U))
