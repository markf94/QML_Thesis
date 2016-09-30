from skc.basic_approx.generate import *

from skc.operator import *
from skc.simplify import *
from skc.basic_approx import *
from skc.basis import *

import numpy

iset2 = [H, T, T_inv, S, S_inv] #SX, SY, SZ]

for insn in iset2:
	print str(insn)

# Simplifying rules
identity_rule = IdentityRule()
double_H_rule = DoubleIdentityRule('H')
adjoint_rule = AdjointRule()
T8_rule = GeneralRule(['T','T','T','T','T','T','T','T'], 'I')
Td8_rule = GeneralRule(['Td','Td','Td','Td','Td','Td','Td','Td'], 'I')
# We should also add a rule for 8T gates -> I

#new stuff
S4_rule = GeneralRule(['S','S','S','S'], 'I')
Sd4_rule = GeneralRule(['Sd','Sd','Sd','Sd'], 'I')
#double_X_rule = DoubleIdentityRule('X')
#double_Y_rule = DoubleIdentityRule('Y')
#double_Z_rule = DoubleIdentityRule('Z')



simplify_rules = [
	identity_rule,
	double_H_rule,
	adjoint_rule,
	T8_rule,
	Td8_rule,
	#new stuff
	S4_rule,
	Sd4_rule
	#double_X_rule,
	#double_Y_rule,
	#double_Z_rule
	]
#simplify_rules = []

H2 = get_hermitian_basis(d=2)

print "BASIS H2"
for (k,v) in H2.items_minus_identity():
	print str(k) + " => " + str(v.matrix)

set_filename_prefix("pickles/su2/gen")

settings = BasicApproxSettings()
settings.set_iset(iset2)
settings.init_simplify_engine(simplify_rules)
settings.set_identity(I2)
settings.basis = H2

generate_approxes(16, settings)
