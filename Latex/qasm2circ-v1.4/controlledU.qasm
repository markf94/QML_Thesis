#
# File:   controlledU.qasm
# Date:   22-Mar-04
# Author: Mark Fingerhuth

# Two-qubit controlled-U gate

	def	c-U,1,'U'

	qubit	q0
  qubit q1

  q0.labels = none

	c-U	q0,q1
