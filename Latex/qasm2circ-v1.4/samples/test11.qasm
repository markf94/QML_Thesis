# 
# File:	  test11.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - user-defined 
# multi-qubit ops

	defbox	fx,2,0,'U_{f(x)}'
	defbox	fxy,3,0,'U_{f(x,y)}'
  
	qubit	q0
	qubit	q1
	qubit	q2

	h	q0
	fx	q0,q1
	h	q1
	fxy	q0,q1,q2

