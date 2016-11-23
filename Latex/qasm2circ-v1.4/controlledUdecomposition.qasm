#
# File:   controlledUdecomposition.qasm
# Date:   22-Mar-04
# Author: Mark Fingerhuth

# Two-qubit controlled-U gate decomposition

  def C,0,'C'
  def B,0,'B'
  def A,0,'A'
  def Ryt,0,'\m{1&0\cr0&e^{i\alpha}}'

	qubit	q0
  qubit q1

  C q1
  cnot q0,q1
  B q1
  cnot q0,q1
  A q1
  Ryt q0
