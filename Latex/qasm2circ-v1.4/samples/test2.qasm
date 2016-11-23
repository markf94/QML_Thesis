# 
# File:   test2.qasm
# Date:   22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - simple teleportation circuit
#
        qubit 	q0
        qubit 	q1
	qubit 	q2

	h	q1	# create EPR pair
	cnot	q1,q2
	cnot	q0,q1	# Bell basis measurement
	h	q0
	nop	q1
	measure	q0	
	measure	q1
	c-z	q1,q2	# correction step
	c-x	q0,q2
