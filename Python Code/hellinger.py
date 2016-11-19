import math
import numpy as np

# Determine Big O complexity of Hellinger distance

data1 = [0.000100, 0.000880, 0.008090, 0.073020,  0.653810 , 0.072500 , 0.007950, 0.000870 , 0.000100]
data2 = [0.001600, 0.006500, 0.025810, 0.103850,  0.407530 , 0.101520 , 0.025120, 0.006420 , 0.001600]
#data1 = list(range(0,10))
#data2 = list(range(10,20))
#print data1
#print data2
datasize = len(data1)
print "data vector entries: ", datasize

#O(1)
hellingersum = 0

# Compute Hellinger sum
# O(n)
for i in range(datasize-1):
    hellingersum = hellingersum + math.sqrt( ( math.sqrt(data1[i]) - math.sqrt(data2[i]) )**2 )

# O(1)
total_hellinger = 1/(math.sqrt(2))*hellingersum

print "Hellinger distance", total_hellinger

# CONCLUSION:
# Computing hellinger distance takes O(n) steps when computed classically!

# Additional computations
print ""
maxentries = float(2**23)
print "Total number of entries possible with 23 qubits in Liqui|>: \n", maxentries
print ""
nanoflops = float((354*10**9)/1000000000)
print "Operations per nanosecond on a Intel Core i7 [5960X (Haswell E), 8 core @ 3.0GHz AVX2] processor: \n", nanoflops
print ""
#source:https://www.pugetsystems.com/labs/hpc/Linpack-performance-Haswell-E-Core-i7-5960X-and-5930K-594/
comptime = maxentries/nanoflops
print "Classical time needed to compute Hellinger distance for %d entries: \n%d nanoseconds" %(maxentries, comptime)
print ""
# Quantum alg complexity is O(1/p_acc)
print "Quantum algorithm complexity with p_acc=0.00001: ", 1/0.00001
print "Quantum algorithm complexity with p_acc=0.1: ", 1/0.1
print "Quantum algorithm complexity with p_acc=0.6: ", 1/0.6
print "Quantum algorithm complexity with p_acc=0.9: ", 1/0.9
