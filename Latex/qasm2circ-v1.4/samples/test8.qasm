# 
# File:	  test8.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - stage in
# simplification of quantum teleportation

	def	c-Z,1,'Z'

	qubit	q0,\psi
	qubit	q1,0
	qubit	q2,0

	H	q1
	cnot	q0,q1
	cnot	q1,q2
	cnot	q0,q1
	cnot	q1,q2
	H	q0
	c-Z	q2,q0
	H	q0
	H	q0
