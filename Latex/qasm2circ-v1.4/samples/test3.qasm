# 
# File:   test3.qasm
# Date:   22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - swap circuit
#
        qubit 	q0
        qubit 	q1

	cnot	q0,q1
	cnot	q1,q0
	cnot	q0,q1
