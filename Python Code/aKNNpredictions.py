import math
import numpy
import cmath

#inputamplitudes = [0.92388, 0.38268]
inputamplitudes = [0.98079, 0.19509]
training1amplitudes = [1,0]
training2amplitudes = [0,1]

#initialize lists
ancilla0m0 = [0]*2
ancilla0m1 = [0]*2
ancilla1m0 = [0]*2
ancilla1m1 = [0]*2

for i in range(2):
    # ADD INPUT TO TRAINING vectors
    ancilla0m0[i] = inputamplitudes[i] + training1amplitudes[i]
    ancilla0m1[i] = inputamplitudes[i] + training2amplitudes[i]

    # SUBTRACT TRAINING VECTORS FROM INPUT
    ancilla1m0[i] = inputamplitudes[i] - training1amplitudes[i]
    ancilla1m1[i] = inputamplitudes[i] - training2amplitudes[i]

# calculate probabilities
ancilla0m0[:] = [x**2*0.125 for x in ancilla0m0]
ancilla0m1[:] = [x**2*0.125 for x in ancilla0m1]
ancilla1m0[:] = [x**2*0.125 for x in ancilla1m0]
ancilla1m1[:] = [x**2*0.125 for x in ancilla1m1]

prediction1 = (sum(ancilla0m0)+sum(ancilla0m1))
prediction2 = 1-(sum(ancilla1m0)+sum(ancilla1m1))
classprediction0state = 1/(prediction1)*sum(ancilla0m0)
classprediction1state = 1/(prediction1)*sum(ancilla0m1)

print "PREDICTION for ancilla in |0> state: ", prediction1
print "PREDICTION for ancilla in |1> state: ", (sum(ancilla1m0)+sum(ancilla1m1))

#print "PREDICTION2 for ancilla in |0> state: ", prediction2
print ""
print "PREDICTION for class in |0> state: ", classprediction0state
print "PREDICTION for class in |1> state: ", classprediction1state
print "SUM: ", (classprediction0state+classprediction1state)
print ""
