from skc.operator import *

import math
import unittest

class TestOperator(unittest.TestCase):

	# Test that hash value implies equality
	def test_hash(self):
		hash1 = I2.__hash__()
		hash2 = H.__hash__()
		hash3 = T.__hash__()
		msg = "hash(I2)= " + str(hash1) + " hash(H)= " + str(hash2)
		self.assertNotEquals(hash1, hash2, msg)
		msg = "hash(H)= " + str(hash2) + " hash(T)= " + str(hash3)
		self.assertNotEquals(hash2, hash3, msg)
		msg = "hash(I2)= " + str(hash1) + " hash(T)= " + str(hash3)
		self.assertNotEquals(hash1, hash3, msg)
		
	def test_ancestors_as_string(self):
		op = Operator("", None)
		op.ancestors = ['A', 'B', 'C']
		string = op.ancestors_as_string()
		self.assertEquals(string, "A-B-C", "Ancestor string incorrect " + string)

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestOperator)
	suite.addTest(suite1)
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
