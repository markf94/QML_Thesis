import unittest

import test_recompose
import test_find_basis
import test_utils
import test_matrix_ln
import test_diagonalize
import test_compose
import test_similarity_matrix
import test_simplify
import test_operator
import test_hypersphere

loader = unittest.TestLoader()

suite = unittest.TestSuite()
suite.addTest(test_recompose.get_suite())
suite.addTest(test_find_basis.get_suite())
suite.addTest(test_utils.get_suite())
suite.addTest(test_matrix_ln.get_suite())
suite.addTest(test_diagonalize.get_suite())
suite.addTest(test_compose.get_suite())
suite.addTest(test_similarity_matrix.get_suite())
suite.addTest(test_simplify.get_suite())
suite.addTest(test_operator.get_suite())
suite.addTest(test_hypersphere.get_suite())
unittest.TextTestRunner(verbosity=2).run(suite)
