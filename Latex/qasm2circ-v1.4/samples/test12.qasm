# 
# File:	  test12.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - multi-qubit controlled
# multi-qubit operations

	defbox	CU2,3,1,'U'
	defbox	CV2,3,1,'V'

	qubit	q0
	qubit	q1
	qubit	q2
	
	h	q0
	CU2	q0,q1,q2
	h	q0
	CV2	q2,q0,q1
	