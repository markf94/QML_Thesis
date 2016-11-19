import cmath
import math

# PROBABILITY OF MEASURING THE ANCILLA IN THE |0> STATE
# AND PROBABILITIES FOR THE CLASS QUBIT MEASUREMENT OUTCOMES
# EQUATION FROM SCHULD ET AL. >> Quantum computing for pattern classification

# VARIABLES
n = 4; # number of bits in training/input vectors
N = 4; # number of training samples
HD1 = 1; # hamming distance between input and training vector #1 (class 0)
HD2 = 1; # hamming distance between input and training vector #2 (class 0)
HD3 = 2; # hamming distance between input and training vector #3 (class 1)
HD4 = 3; # hamming distance between input and training vector #4 (class 1)

# Calculate the probability
probanc = 0.25*(math.cos(math.pi/(2*n)*HD1)**2+math.cos(math.pi/(2*n)*HD2)**2+math.cos(math.pi/(2*n)*HD3)**2+math.cos(math.pi/(2*n)*HD4)**2);
probclass0 = (1/(N*probanc))*(math.cos(math.pi/(2*n)*HD1)**2+math.cos(math.pi/(2*n)*HD2)**2)
probclass1 = (1/(N*probanc))*(math.cos(math.pi/(2*n)*HD3)**2+math.cos(math.pi/(2*n)*HD4)**2)

print "Probability of measuring ancilla in |0> state: ", probanc
print "Probability of measuring class in |0> state: ", probclass0
print "Probability of measuring class in |1> state: ", probclass1
