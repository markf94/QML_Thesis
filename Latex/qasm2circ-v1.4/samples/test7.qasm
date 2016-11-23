# 
# File:	  test7.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - measurement
# of operator with correction

	def	c-U,1,'U'
	def	c-V,1,'V'

	qubit	q0
	qubit	q1

	H	q0
	c-U	q0,q1
	H	q0
	measure	q0
	c-V	q0,q1
	nop	q0
	nop	q1
