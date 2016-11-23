# 
# File:	  test15.qasm
# Date:	  24-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - "D-type" measurement
# requested by Nielsen

	def	MeasZ,0,'\dmeterwide{HZ_\theta}{18pt}'

	qubit	q0,\psi
	qubit	q1,+

	nop	q0
	ZZ	q0,q1
	nop	q0
	MeasZ	q0
