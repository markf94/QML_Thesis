from skc.simplify import *

class BasicApproxSettings:
	
	def __init__(self):
		self.identity = None
		self.iset = []
		self.iset_dict = {}
		self.simplify_engine = None  # simplify engine

	def set_iset(self, new_iset):
		self.check_iset(new_iset)
		self.iset = new_iset
		for insn in new_iset:
			self.iset_dict[insn.name] = insn
			
	def set_identity(self, new_identity):
		self.identity = new_identity
		self.iset_dict[new_identity.name] = new_identity

	def print_iset(self):
		print "INSTRUCTION SET"
		for insn in self.iset:
			print str(insn)

	##############################################################################
	# Verify that all operators in iset are the same size and shape
	def check_iset(self, iset):
		m = len(iset)
		print str(m) + " instructions found"
		
		first_op = iset[0] # Python uses 0-based indexing
		first_shape = first_op.matrix.shape
	
		if (len(first_shape) != 2):
			msg = "First operator is not a matrix! Shape = " +str(shape)
			raise RuntimeError(msg)
			
		d = first_shape[0] # d=2 for qubits
		if (d != first_shape[1]):
			msg = "First operator is not a square matrix! Shape = " + str(shape)
			raise RuntimeError(msg)
	
		for i in range(m):
			i_shape = iset[i].matrix.shape
			if (i_shape != first_shape):
				msg = "Operator " + str(i) + "'s shape does not match first shape: " + str(i_shape)
				raise RuntimeError(msg)
			
	def simplify(self, sequence):
		return self.simplify_engine.simplify(sequence)

	# Initialize the global simplify engine with the given rules for all
	# subsequent generation of basic approximations
	def init_simplify_engine(self, rules):
		self.simplify_engine = SimplifyEngine(rules)
