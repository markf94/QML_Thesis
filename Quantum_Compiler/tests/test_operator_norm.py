# Test file to print out distances between some standard gates

#from skc_unitary_decompose import *
from skc_operator import *
from skc_utils import *
import scipy.linalg

gates = [I2, SX, SY, SZ, H, T]
gates2 = list(gates)

# These norms should all be 1
print "scipy.linalg.norm is not the operator norm :["
print "|I2| = " + str(scipy.linalg.norm(I2.matrix))
print "|SX| = " + str(scipy.linalg.norm(SX.matrix))
print "|SY| = " + str(scipy.linalg.norm(SY.matrix))
print "|SZ| = " + str(scipy.linalg.norm(SZ.matrix))
print "|H| = " + str(scipy.linalg.norm(H.matrix))
print "|T| = " + str(scipy.linalg.norm(T.matrix))

print "trace norm is better?"
print "|I2| = " + str(trace_norm(I2.matrix))
print "|SX| = " + str(trace_norm(SX.matrix))
print "|SY| = " + str(trace_norm(SY.matrix))
print "|SZ| = " + str(trace_norm(SZ.matrix))
print "|H| = " + str(trace_norm(H.matrix))
print "|T| = " + str(trace_norm(T.matrix))

print "sup norm is better?"
print "|I2| = " + str(operator_norm(I2.matrix))
print "|SX| = " + str(operator_norm(SX.matrix))
print "|SY| = " + str(operator_norm(SY.matrix))
print "|SZ| = " + str(operator_norm(SZ.matrix))
print "|H| = " + str(operator_norm(H.matrix))
print "|T| = " + str(operator_norm(T.matrix))

for gate1 in gates:
	gates2.remove(gate1)
	dist_text = "Dist("+gate1.name+",...)"
	for gate2 in gates2:
		dist_text += "\t" + str(fowler_distance(gate1.matrix, gate2.matrix))
	print dist_text
		
#print "Distance(I2,SX) = " + str(I2.distance(SX))
#print "Distance(I2,SY) = " + str(I2.distance(SY))
#print "Distance(I2,SZ) = " + str(I2.distance(SZ))
#print "Distance(I2,H) = " + str(I2.distance(SX))
#print "Distance(I2,SX) = " + str(I2.distance(SX))