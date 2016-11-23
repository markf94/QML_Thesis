# 
# File:	  test10.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - multi-qubit gates
# also demonstrates use of classical bits 

	qubit	q0	
	cbit	c1
	qubit	q2
	
	h	q0
	Utwo	q0,c1
	S	q2
	Utwo	c1,q2
