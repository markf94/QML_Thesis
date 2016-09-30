from skc.simplify import *

import math
import unittest

##############################################################################
class TestSimplifyEngine(unittest.TestCase):

	def setUp(self):
		rules = [AdjointRule(), DoubleIdentityRule('Q'), IdentityRule(),
			GeneralRule(['X','Y','Z'])]
		self.engine = SimplifyEngine(rules)
		
	def test_min_arg_count(self):
		self.assertEquals(self.engine.max_arg_count, 3)

	def test_simplest(self):
		# This should simplify to I
		sequence = ['I', 'I']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['I'])
		self.assertEqual(simplify_length, 1)

	def test_repeated_identity(self):
		# This should simplify to I
		sequence = ['I', 'I', 'I', 'I', 'I']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['I'])
		self.assertEqual(simplify_length, 4)

	def test_general_identity_not_enough(self):
		# This should simplify QIQ to nothing
		sequence = ['D', 'A', 'B']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['D', 'A', 'B'])
		self.assertEqual(simplify_length, 0)

	def test_general_identity(self):
		# This should simplify QIQ to nothing
		sequence = ['D', 'X', 'Y', 'Z', 'X', 'Y', 'Z']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['D'])
		self.assertEqual(simplify_length, 6)

	def test_general_identity_beginning(self):
		# This does not simplify XYZ because it works from the end
		sequence = ['X', 'Y', 'Z', 'D']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['X', 'Y', 'Z', 'D'])
		self.assertEqual(simplify_length, 0)

	def test_general_identity_ending(self):
		# This should simplify QIQ to nothing
		sequence = ['D','X', 'Y', 'Z']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['D'])
		self.assertEqual(simplify_length, 3)

	def test_identity_middle(self):
		# This should simplify QIQ to nothing
		sequence = ['X', 'Q', 'I', 'Q', 'Z']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['X', 'Q', 'I', 'Q', 'Z'])
		self.assertEqual(simplify_length, 0)

	def test_identity(self):
		# This should simplify QIQ to nothing
		sequence = ['X', 'Q', 'I', 'Q']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['X'])
		self.assertEqual(simplify_length, 3)
		
		
	def test_double_q_middle(self):
		# This should simplify 3 Q's down to just Q
		sequence = ['X', 'Q', 'Q', 'Q', 'Z']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['X', 'Q', 'Q', 'Q', 'Z'])
		self.assertEqual(simplify_length, 0)

	def test_double_q(self):
		# This should simplify 3 Q's down to just Q
		sequence = ['X', 'Q', 'Q', 'Q']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['X', 'Q'])
		self.assertEqual(simplify_length, 2)
		
	def test_none_obtains(self):
		# This should simplify to I
		sequence = ['X', 'Q', 'Y', 'Q', 'Z']
		(simplify_length, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['X', 'Q', 'Y', 'Q', 'Z'])
		self.assertEqual(simplify_length, 0)

##############################################################################
class TestDoubleIdentityRule(unittest.TestCase):

	def setUp(self):
		self.rule = DoubleIdentityRule('I')

	def test_simplest(self):
		# This should simplify to I
		sequence = ['I', 'I']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])

	def test_simplest_not(self):
		# This should simplify to I
		sequence = ['X', 'Z']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['X', 'Z'])

##############################################################################
class TestIdentityRule(unittest.TestCase):

	def setUp(self):
		self.rule = IdentityRule()

	def test_simplest(self):
		# This should simplify to I
		sequence = ['I', 'I']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])

	def test_simplest2(self):
		# This should simplify to Q
		sequence = ['Q', 'I']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['Q'])

	def test_simplest3(self):
		# This should simplify to Q
		sequence = ['I', 'Q']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['Q'])

	def test_simplest_not(self):
		# This should not simplify
		sequence = ['X', 'Z']
		(obtains,sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['X', 'Z'])

##############################################################################
class TestGeneralRule(unittest.TestCase):

	def setUp(self):
		self.rule = GeneralRule(sequence=['A','B','C'], new_sym='I4')

	def test_simplest(self):
		msg = "Incorrect number of args: " + str(self.rule.arg_count)
		self.assertEqual(self.rule.arg_count, 3, msg)
		# This should simplify to I
		sequence = ['A', 'B', 'C']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I4'])

	def test_simplest2(self):
		# This should simplify to Q
		sequence = ['A', 'B', 'C']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I4'])

	def test_simplest_not(self):
		# This should not simplify
		sequence = ['A', 'I', 'Z']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['A', 'I', 'Z'])

##############################################################################
class TestAdjointRule(unittest.TestCase):

	def setUp(self):
		self.rule = AdjointRule()

	# Test that adjoint rule obtains for simplest case
	def test_simplest(self):
		# This should simplify to I
		sequence = ['Q', 'Qd']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])

	def test_simplest_reverse(self):
		# This should also simplify to I
		sequence = ['Qd', 'Q']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])
		
	def test_different_prefixes(self):
		sequence = ['X', 'Zd']
		# This should not simplify
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['X', 'Zd'])

	def test_equal_length(self):
		# This should not simplify
		sequence = ['Ydd', 'Xdd']
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['Ydd', 'Xdd'])

	def test_repeated_d(self):
		sequence = ['Qddd', 'Qdd']
		# This should simplify to I
		(obtains, sequence) = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])
		
##############################################################################		
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestAdjointRule)
	suite.addTest(suite1)
	suite2 = loader.loadTestsFromTestCase(TestIdentityRule)
	suite.addTest(suite2)
	suite3 = loader.loadTestsFromTestCase(TestDoubleIdentityRule)
	suite.addTest(suite3)
	suite4 = loader.loadTestsFromTestCase(TestGeneralRule)
	suite.addTest(suite4)
	suite5 = loader.loadTestsFromTestCase(TestSimplifyEngine)
	suite.addTest(suite5)
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
