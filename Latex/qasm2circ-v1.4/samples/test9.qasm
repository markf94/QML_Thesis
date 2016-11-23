# 
# File:	  test9.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - two-qubit gate circuit
# implementation of Toffoli 

	def	c-X,1,'\sqrt{X}'
	def	c-Xd,1,'{\sqrt{X}}^\dagger'

	qubit	q0
	qubit	q1
	qubit	q2

	c-X	q1,q2
	cnot	q0,q1
	c-Xd	q1,q2
	cnot	q0,q1
	c-X	q0,q2
