from skc.operator import *
from skc.dawson.factor import *
from skc.dawson import *
from skc.compose import *
from skc.basis import *
from skc.simplify import *
import skc.utils
import math

H2 = get_hermitian_basis(d=2)
theta = math.pi / 4 # 45 degrees
axis = cart3d_to_h2(x=1, y=1, z=1)

print "Identity Name: " + H2.identity.name

# Compose a unitary to compile
#matrix_U = axis_to_unitary(axis, theta, H2)
#matrix_U = matrixify([[1,0], [0,numpy.exp(1j * math.pi / 8)]])
matrix_U = matrixify([[0.83147 + 0.55557j,0], [0,0.83147 - 0.55557j]])
op_U = Operator(name="U", matrix=matrix_U)

n = 3
print "U= " + str(matrix_U)

##############################################################################
# Prepare the simplify engine
# Simplifying rules
identity_rule = IdentityRule(id_sym=H2.identity.name)
double_H_rule = DoubleIdentityRule('H', id_sym=H2.identity.name)
double_I_rule = DoubleIdentityRule(H2.identity.name, id_sym=H2.identity.name)
#H_non_dagger_rule = NonDaggerRule('H')
#I_non_dagger_rule = NonDaggerRule(H2.identity.name)
H_non_dagger_rule = DoubleIdentityRule('H', id_sym=H2.identity.name)
I_non_dagger_rule = DoubleIdentityRule('I', id_sym=H2.identity.name)
adjoint_rule = AdjointRule()
T8_rule = GeneralRule(['T','T','T','T','T','T','T','T'], H2.identity.name)
Td8_rule = GeneralRule(['Td','Td','Td','Td','Td','Td','Td','Td'], H2.identity.name)
# We should also add a rule for 8T gates -> I
#new stuff
S4_rule = GeneralRule(['S','S','S','S'], H2.identity.name)
Sd4_rule = GeneralRule(['Sd','Sd','Sd','Sd'], H2.identity.name)
#double_X_rule = DoubleIdentityRule('X', id_sym=H2.identity.name)
#double_Y_rule = DoubleIdentityRule('Y', id_sym=H2.identity.name)
#double_Z_rule = DoubleIdentityRule('Z', id_sym=H2.identity.name)

simplify_rules = [
	identity_rule,
	double_H_rule,
	double_I_rule,
	adjoint_rule,
	T8_rule,
	Td8_rule,
	H_non_dagger_rule,
	I_non_dagger_rule,
	S4_rule,
	Sd4_rule
	#double_X_rule,
	#double_Y_rule,
	#double_Z_rule
	]

simplify_engine = SimplifyEngine(simplify_rules)

skc.utils.self_adjoint_operators = ['H', H2.identity.name]

# Prepare the compiler
sk_set_factor_method(dawson_group_factor)
sk_set_basis(H2)
sk_set_axis(X_AXIS)
sk_set_simplify_engine(simplify_engine)
#sk_build_tree("su2", 11)
sk_build_tree("su2_all_gates", 9)

Un = solovay_kitaev(op_U, n)
print "Approximated U: " + str(Un)

print "Un= " + str(Un.matrix)

print "trace_dist(U,Un)= " + str(trace_distance(Un.matrix, op_U.matrix))
print "fowler_dist(U,Un)= " + str(fowler_distance(Un.matrix, op_U.matrix))
print "sequence length= " + str(len(Un.ancestors))
print "n= " + str(n)
