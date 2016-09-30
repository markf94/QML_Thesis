from skc.basic_approx.generate import *

from skc.operator import *
from skc.simplify import *
from skc.basis import *
from skc.basic_approx import *

import numpy

##############################################################################
# Instruction set
H1_matrix = numpy.kron(H.matrix, I2.matrix)
H2_matrix = numpy.kron(I2.matrix, H.matrix)
H1 = Operator(name="H1", matrix=H1_matrix)
H2 = Operator(name="H2", matrix=H2_matrix)

T1_matrix = numpy.kron(T.matrix, I2.matrix)
T2_matrix = numpy.kron(I2.matrix, T.matrix)
T1 = Operator(name="T1", matrix=T1_matrix)
T2 = Operator(name="T2", matrix=T2_matrix)

Tinv1_matrix = numpy.kron(T_inv.matrix, I2.matrix)
Tinv2_matrix = numpy.kron(I2.matrix, T_inv.matrix)
Tinv1 = Operator(name="T1d", matrix=Tinv1_matrix)
Tinv2 = Operator(name="T2d", matrix=Tinv2_matrix)

CNot_matrix = matrixify([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CNot = Operator(name="CN", matrix=CNot_matrix)
# CNot is its own inverse, so we don't need to add a dagger for it

iset4 = [H1, H2, T1, T2, Tinv1, Tinv2, CNot]

print "ISET SU(4)"

for insn in iset4:
	print str(insn)

##############################################################################
# Hermitian basis

H4 = get_hermitian_basis(d=4)

print "BASIS H2"
for (k,v) in H4.items_minus_identity():
	print str(k) + " => " + str(v.matrix)

##############################################################################
# Simplifying rules
identity_rule = IdentityRule(H4.identity.name)
double_H1_rule = DoubleIdentityRule(symbol='H1', id_sym=H4.identity.name)
double_H2_rule = DoubleIdentityRule(symbol='H2', id_sym=H4.identity.name)
double_CN_rule = DoubleIdentityRule(symbol='CN', id_sym=H4.identity.name)

# H1 and H2 commute with a bunch of stuff, generate rules for them here

# First create a list of just iset labels, and don't include CNot
H_rule_iset = [x.name for x in iset4]
H_rule_iset.remove ('CN')

H_rules = []
for arg1 in ['H1','H2']:
	# defensive copy
	iset = list(H_rule_iset)
	# remove the current arg
	iset.remove(arg1)
	for arg2 in iset:
		new_rule = GeneralRule([arg1, arg2, arg1], arg2)
		print str(new_rule)
		H_rules.append(new_rule)

# Similarly, T1 commutes with T2 and H2 and likewise
# T2 commutes with T1 and H1

T_rules = []

T1_set = ['T1','T1d']
for arg1 in T1_set:
	T1_setd = list(T1_set)
	T1_setd.remove(arg1)
	arg1d = T1_setd[0]
	for arg2 in ['T2','T2d','H2']:
		new_rule = GeneralRule([arg1, arg2, arg1d], arg2)
		print str(new_rule)
		T_rules.append(new_rule)

T2_set = ['T2','T2d']
for arg1 in T2_set:
	T2_setd = list(T2_set)
	T2_setd.remove(arg1)
	arg1d = T2_setd[0]
	for arg2 in ['T1','T1d','H1']:
		new_rule = GeneralRule([arg1, arg2, arg1d], arg2)
		print str(new_rule)
		T_rules.append(new_rule)
		
adjoint_rule = AdjointRule(id_sym=H4.identity.name)

simplify_rules = [
	identity_rule,
	double_H1_rule,
	double_H2_rule,
	double_CN_rule,
	adjoint_rule
	]
simplify_rules.extend(H_rules)
simplify_rules.extend(T_rules)
#simplify_rules = []

##############################################################################
# Prepare settings
set_filename_prefix("pickles/su4/gen")

settings = BasicApproxSettings()
settings.set_iset(iset4)
settings.init_simplify_engine(simplify_rules)
settings.set_identity(H4.identity)
settings.basis = H4
