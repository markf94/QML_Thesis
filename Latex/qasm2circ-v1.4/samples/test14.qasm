# 
# File:	  test14.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - three-qubit FT QEC
# circuit with syndrome measurement

	defbox	synd,4,0,'\txt{Process\\Syndrome}'
	defbox	rop,7,4,'{\cal R}'

	qubit	q0	# code data qubits
	qubit	q1
	qubit	q2
	qubit	s0,0	# syndrome measurement qubits
	qubit	s1,0
	cbit	c0,0	# classical bits to store syndromes
	cbit	c1,0

	h	s0	# create EPR pair for FT meas
	cnot	s0,s1
	cnot	q0,s0	# measure parity of q0,q1
	nop	s1	# prevent cnot's from colliding
	cnot	q1,s1
	cnot	s0,s1	# uncreate EPR
	h	s0
	measure	s0	# measure syndrome qubits
	nop	s1
	measure s1
	cnot	s0,c0	# copy to classical bits
	nop	s1
	cnot	s1,c1
	space	s0

	zero	s0
	zero	s1
	h	s0	# create EPR pair for FT meas
	cnot	s0,s1
	cnot	q1,s0	# measure parity of q1,q2
	nop	s1	# prevent cnot's from colliding
	cnot	q2,s1
	cnot	s0,s1	# uncreate EPR
	h	s0
	measure	s0	# measure syndrome qubits
	nop	s1
	measure s1

	synd	s0,s1,c0,c1
	rop	s0,s1,c0,c1,q0,q1,q2
