from skc.basic_approx.generate import *

from skc.operator import *
from skc.simplify import *
from skc.basic_approx import *
from skc.basis import *

import numpy

iset2 = [H, T, T_inv, S, S_inv, SX, SY, SZ]

for insn in iset2:
	print str(insn)

# Simplifying rules
identity_rule = IdentityRule()
double_H_rule = DoubleIdentityRule('H')
adjoint_rule = AdjointRule()
T8_rule = GeneralRule(['T','T','T','T','T','T','T','T'], 'I')
double_H_rule2 = GeneralRule(['H','H'], 'I')
Td8_rule = GeneralRule(['Td','Td','Td','Td','Td','Td','Td','Td'], 'I')
# We should also add a rule for 8T gates -> I

#new stuff
S4_rule = GeneralRule(['S','S','S','S'], 'I')
Sd4_rule = GeneralRule(['Sd','Sd','Sd','Sd'], 'I')
double_SX_rule = DoubleIdentityRule('SX')
double_SY_rule = DoubleIdentityRule('SY')
double_SZ_rule = DoubleIdentityRule('SZ')



simplify_rules = [
	identity_rule,
	double_H_rule,
	double_H_rule2,
	adjoint_rule,
	T8_rule,
	Td8_rule,
	#new stuff
	S4_rule,
	Sd4_rule,
	double_SX_rule,
	double_SY_rule,
	double_SZ_rule
	]
#simplify_rules = []

H2 = get_hermitian_basis(d=2)

print "BASIS H2"
for (k,v) in H2.items_minus_identity():
	print str(k) + " => " + str(v.matrix)

set_filename_prefix("pickles/su2_all_gates/gen")

settings = BasicApproxSettings()
settings.set_iset(iset2)
settings.init_simplify_engine(simplify_rules)
settings.set_identity(I2)
settings.basis = H2

generate_approxes(16, settings)
