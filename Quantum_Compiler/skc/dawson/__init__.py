# Solovay-Kitaev compiler using Dawson's group factor

from skc.operator import *
from skc.utils import *
from skc.basic_approx.search import *
import sys

##############################################################################
# Global variables
the_basis = None
# Not currently used with aram_diagonal_factor method
the_axis = None
the_factor_method = None
the_tree = None
the_simplify_engine = None

# Build the search tree. Kablooey!
def sk_build_tree(subdir, filecount_upper):
	global the_tree
	the_tree = build_kdtree("pickles/"+subdir+"/gen-g", filecount_upper, "-1.pickle")

def sk_search_tree(op_U):
	op = search_kdtree(the_tree, op_U.matrix, the_basis)
	return op

##############################################################################
def sk_set_simplify_engine(simplify_engine):
	global the_simplify_engine
	the_simplify_engine = simplify_engine

##############################################################################
def sk_set_axis(axis):
	global the_axis
	the_axis = axis
	print "the_axis= " + str(the_axis)

##############################################################################
# Not currently used with aram_diagonal_factor method
def sk_set_basis(basis):
	global the_basis
	the_basis = basis
	print "the_basis= " + str(the_basis)

##############################################################################
def sk_set_factor_method(factor_method):
	global the_factor_method
	the_factor_method = factor_method
	print "the_factor_method= " + str(the_factor_method.__name__)

##############################################################################
def solovay_kitaev(U, n, id="U", ancestry=""):
	print "*******************************************************************"
	print str(id)+"_"+str(n)
	print ancestry
	print "-------------------------------------------------------------------"
	
	if (n == 0):
		basic_approx = sk_search_tree(U)
		# discard min_dist for now. but just you wait...
		print "Returning basic approx: " + str(basic_approx)
		return basic_approx
	else:
	
		#dist = fowler_distance(U.matrix, the_basis.identity.matrix)
		#if (dist < TOLERANCE):
		#	return the_basis.identity
	
		print "Beginning level " + str(n)
		U_n1 = solovay_kitaev(U, n-1, 'U', ancestry+id) # U_{n-1}
		#print "U_"+str(n-1)+": " + str(U_n1)
		U_n1_dagger = U_n1.dagger()
		U_U_n1_dagger = U.multiply(U_n1_dagger).matrix
		V_matrix,W_matrix = the_factor_method(U_U_n1_dagger, the_basis, the_axis)
		#print "V: " + str(V_matrix)
		#print "W: " + str(W_matrix)
		V = Operator(name="V", matrix=V_matrix)
		W = Operator(name="W", matrix=W_matrix)
		V_n1 = solovay_kitaev(V, n-1, 'V', ancestry+id) # V_{n-1}
		#print "V_"+str(n-1)+": " + str(V_n1)
		V_n1_dagger = V_n1.dagger()
		W_n1 = solovay_kitaev(W, n-1, 'W', ancestry+id) # W_{n-1}
		#print "W_"+str(n-1)+": " + str(W_n1)
		
		W_n1_dagger = W_n1.dagger()
		V_n1_dagger_W_n1_dagger = V_n1_dagger.multiply(W_n1_dagger)
		(simplify_length, simplified_sequence) = \
			the_simplify_engine.simplify(V_n1_dagger_W_n1_dagger.ancestors)
		V_n1_dagger_W_n1_dagger.ancestors = simplified_sequence
		
		V_n1_W_n1 = V_n1.multiply(W_n1)
		(simplify_length, simplified_sequence) = \
			the_simplify_engine.simplify(V_n1_W_n1.ancestors)
		V_n1_W_n1.ancestors = simplified_sequence
		
		delta = V_n1_W_n1.multiply(V_n1_dagger_W_n1_dagger)
		(simplify_length, simplified_sequence) = \
			the_simplify_engine.simplify(delta.ancestors)
		delta.ancestors = simplified_sequence
		
		U_n = delta.multiply(U_n1)
		(simplify_length, simplified_sequence) = \
			the_simplify_engine.simplify(U_n.ancestors)
		U_n.ancestors = simplified_sequence
		#print "delta_"+str(n)+": " + str(U_n)
		print "Ending level " + str(n)
		return U_n
