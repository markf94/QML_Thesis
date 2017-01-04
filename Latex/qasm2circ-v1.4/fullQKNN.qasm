#
# File:   fullQKNN.qasm
# Date:   22-Mar-04
# Author: Mark Fingerhuth

# Quantum circuit for qubit-based kNN algorithm

	def	C,0,'C(16 gates)'
	def	B,0,'B(25 gates)'
	def Td,0,'T^\dagger'

	qubit	a
	qubit	d
	qubit	c
	qubit	m

	H a
	H m
	C d
	cnot a,d
	B d
	cnot a,d
	Z a
	X a

	H d

	cnot a,d

	Td d

	cnot m,d

	T d

	cnot a,d

	Td d
	
	cnot m,d

	nop d

	T a

	cnot m,a

	Td a

	T m

	T d

	H d

	nop a
	nop d
	
	cnot m,a

	nop m 
	nop a
	
	cnot d,c

	nop c

	H a
	measure a
	measure c
