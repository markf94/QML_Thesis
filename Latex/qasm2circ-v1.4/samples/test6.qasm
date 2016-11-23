# 
# File:	  test6.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - demonstrate
# multiple-qubit controlled single-q-gates

	def	c-U,3,'U'

	qubit	j0
	qubit	j1
	qubit	j2
	qubit	j3

	toffoli	j0,j1,j2
	X	j0
	c-U	j2,j3,j0,j1
	H	j2
	measure	j3
