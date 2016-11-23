# 
# File:	  test18.qasm
# Date:	  25-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - multiple-control bullet op

	def	MeasH,0,'\dmeter{H}'
	def	Z4,3,'bullet'	# handled specially

	qubit	q0,\psi
	qubit	q1,+
	qubit	q2,+
	qubit	q3,\phi

	nop	q0
	nop	q2
	Z4	q0,q1,q2,q3
	MeasH	q1
	MeasH	q2
