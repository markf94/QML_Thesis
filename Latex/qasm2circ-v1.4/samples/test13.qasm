# 
# File:	  test13.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - three-qubit phase
# estimation circuit with QFT and controlled-U

	defbox	CU,3,1,'U'
	defbox	CU2,3,1,'U^2'
	defbox	CU4,3,1,'U^4'
	def	c-S,1,'S'
	def	c-T,1,'T'

	qubit	j0,0	# QFT qubits
	qubit	j1,0
	qubit	j2,0
	qubit	s0	# U qubits
	qubit	s1

	h	j0	# equal superposition
	h	j1
	h	j2

	CU4	j0,s0,s1	# controlled-U
	CU2	j1,s0,s1
	CU	j2,s0,s1

	h	j0	# QFT
	c-S	j0,j1
	h	j1
	nop	j0
	c-T	j0,j2
	c-S	j1,j2
	h	j2
	nop	j0
	nop	j0
	nop	j1
	
	measure	j0	# final measurement
	measure	j1	
	measure	j2	
