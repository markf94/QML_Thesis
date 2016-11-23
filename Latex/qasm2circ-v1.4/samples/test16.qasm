# 
# File:	  test16.qasm
# Date:	  24-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - example from Nielsen
# paper on cluster states

	qubit	q0,\psi
	qubit	q1,\psi
	qubit	q2,\phi
	qubit	q3,0

	nop	q0
	nop	q0
	slash	q0
	nop	q1
	ZZ	q1,q2
	cnot	q2,q3
	nop	q2
	discard	q2
	dmeter	q3
