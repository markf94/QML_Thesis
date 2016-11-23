# 
# File:	  test17.qasm
# Date:	  24-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - example from Nielsen
# paper on cluster states

	def	MeasH,0,'\dmeter{H}'

	qubit	q0,\psi
	qubit	q1,+
	qubit	q2,+
	qubit	q3,\phi

	nop	q0
	nop	q2
	ZZ	q0,q1
	ZZ	q2,q3
	ZZ	q1,q2
	MeasH	q1
	MeasH	q2
