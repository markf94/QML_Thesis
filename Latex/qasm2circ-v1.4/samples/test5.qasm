# 
# File:	  test5.qasm
# Date:	  22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - demonstrate arbitray qubit matrix ops

	def	c-P,1,'\m{e^{i\alpha} & 0 \cr 0 & e^{-i\alpha}}'
	def	Ryt,0,'\m{\cos{\theta}&-\sin{\theta}\cr\sin{\theta}&\cos{\theta}}'

	qubit	j0
	qubit	j1

	c-P	j0,j1
	Ryt	j0