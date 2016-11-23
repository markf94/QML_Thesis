# 
# File:	  test4.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - quantum
# fourier transform on three qubits

	def	c-S,1,'S'
	def	c-T,1,'T'

	qubit	j0
	qubit	j1
	qubit	j2

	h	j0	
	c-S	j1,j0
	c-T	j2,j0
	nop	j1
	h	j1
	c-S	j2,j1
	h	j2
	swap	j0,j2
