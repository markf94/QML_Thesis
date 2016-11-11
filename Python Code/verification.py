import math
import numpy
# Verification of DiffusionKNN results

# The following probabilities have been retrieved from Liqui|> simulations with
# 4 diffusion qubits and 10000 runs

# order
# [|0000>,|1000>,|0100>,|0010>,|0001>,|1100>,|1010>,|1001>,|0110>,|0101>,|0011>,|1011>,|1110>,|1101>,|0111>,|1111>]

# The following probs are extracted from ParsingWindowDiffusion with delta = 0.6
print "======================"
print "----delta = 0.6 ------"
# Gaussian around |0000>:
inputamplitudes = [0.130900,0.085610,0.085650,0.085460,0.086460,0.058570,0.056800,0.058640,0.057890,0.057210,0.058190,0.039250,0.037940,0.038270,0.037730,0.025430]
# Gaussian around |0100>:
training1amplitudes = [0.086590,0.056460,0.128060,0.058430,0.057830,0.087820,0.038270,0.038180,0.086570,0.085880,0.038360,0.025700,0.057730,0.057270,0.058160,0.038690]
# Gaussian around |1011>:
training2amplitudes = [0.039450,0.055970,0.025590,0.056510,0.058190,0.038810,0.084940,0.084910,0.039040,0.039190,0.086720,0.130250,0.058510,0.057930,0.057240,0.086750]

i = numpy.array(inputamplitudes)
t1 = numpy.array(training1amplitudes)
t2 = numpy.array(training2amplitudes)
dist1 = numpy.linalg.norm(i-t1)
hdist1 = 0.70711*dist1
print "Hellinger distance I-T1", hdist1
dist2 = numpy.linalg.norm(i-t2)
hdist2 = 0.70711*dist2
print "Hellinger distance I-T2", hdist2
print "HD difference", abs(hdist1-hdist2)

# reconstruct the amplitudes
inputamplitudes[:] = [math.sqrt(x) for x in inputamplitudes]
training1amplitudes[:] = [math.sqrt(x) for x in training1amplitudes]
training2amplitudes[:] = [math.sqrt(x) for x in training2amplitudes]

#initialize lists
ancilla0m0 = [0]*16
ancilla0m1 = [0]*16
ancilla1m0 = [0]*16
ancilla1m1 = [0]*16

for i in range(16):
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


print "PREDICTION1 for ancilla in |0> state: ", prediction1
#print "PREDICTION2 for ancilla in |0> state: ", prediction2
print ""
print "PREDICTION for class in |0> state: ", classprediction0state
print "PREDICTION for class in |1> state: ", classprediction1state
print "SUM: ", (classprediction0state+classprediction1state)
print ""
#print "ancilla0m0 prob: ", sum(ancilla0m0)
#print "ancilla0m1 prob: ", sum(ancilla0m1)

#print "ancilla1m0 prob: ", sum(ancilla1m0)
#print "ancilla1m1 prob: ", sum(ancilla1m1)
print "==================================="
print ""


# The following probs are extracted from ParsingWindowDiffusion with delta = 0.8
print "======================"
print "----delta = 0.8 ------"
# Gaussian around |0000>:
inputamplitudes = [0.412160,0.102370,0.101410,0.101660,0.102800,0.026320,0.025790,0.024910,0.025560,0.025800,0.024260,0.006360,0.006150,0.006520,0.006510,0.001420]
# Gaussian around |0100>:
training1amplitudes = [0.102380,0.026480,0.408300,0.025320,0.025900,0.101470,0.006460,0.006290,0.103360,0.103480,0.006000,0.001660,0.026980,0.025020,0.024900,0.006000]
# Gaussian around |1011>:
training2amplitudes = [0.006150,0.025640,0.001680,0.025410,0.025970,0.006510,0.101900,0.101640,0.006180,0.006150,0.101480,0.411870,0.024740,0.025240,0.024960,0.104480]

i = numpy.array(inputamplitudes)
t1 = numpy.array(training1amplitudes)
t2 = numpy.array(training2amplitudes)
dist1 = numpy.linalg.norm(i-t1)
hdist1 = 0.70711*dist1
print "Hellinger distance I-T1", hdist1
dist2 = numpy.linalg.norm(i-t2)
hdist2 = 0.70711*dist2
print "Hellinger distance I-T2", hdist2
print "HD difference", abs(hdist1-hdist2)

# reconstruct the amplitudes
inputamplitudes[:] = [math.sqrt(x) for x in inputamplitudes]
training1amplitudes[:] = [math.sqrt(x) for x in training1amplitudes]
training2amplitudes[:] = [math.sqrt(x) for x in training2amplitudes]

#initialize lists
ancilla0m0 = [0]*16
ancilla0m1 = [0]*16
ancilla1m0 = [0]*16
ancilla1m1 = [0]*16

for i in range(16):
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


print "PREDICTION1 for ancilla in |0> state: ", prediction1
#print "PREDICTION2 for ancilla in |0> state: ", prediction2
print ""
print "PREDICTION for class in |0> state: ", classprediction0state
print "PREDICTION for class in |1> state: ", classprediction1state
print "SUM: ", (classprediction0state+classprediction1state)
print ""
# print "ancilla0m0 prob: ", sum(ancilla0m0)
# print "ancilla0m1 prob: ", sum(ancilla0m1)
#
# print "ancilla1m0 prob: ", sum(ancilla1m0)
# print "ancilla1m1 prob: ", sum(ancilla1m1)
print "==================================="
print ""

# The following probs are extracted from ParsingWindowDiffusion with delta = 0.8
print "======================"
print "----delta = 0.9 ------"
# Gaussian around |0000>:
inputamplitudes = [0.658530,0.072440,0.071590,0.071950,0.073030,0.007590,0.007990,0.008720,0.007970,0.008380,0.007950,0.000870,0.000990,0.001070,0.000900,0.000030]
# Gaussian around |0100>:
training1amplitudes = [0.072630,0.007940,0.656030,0.007850,0.008090,0.072850,0.000880,0.000940,0.073220,0.073780,0.000940,0.000040,0.007960,0.008170,0.007920,0.000760]
# Gaussian around |1011>:
training2amplitudes = [0.000930,0.007530,0.000120,0.008130,0.007950,0.001000,0.073260,0.073440,0.000800,0.000830,0.072670,0.657180,0.007710,0.007760,0.007800,0.072890]

i = numpy.array(inputamplitudes)
t1 = numpy.array(training1amplitudes)
t2 = numpy.array(training2amplitudes)
dist1 = numpy.linalg.norm(i-t1)
hdist1 = 0.70711*dist1
print "Hellinger distance I-T1", hdist1
dist2 = numpy.linalg.norm(i-t2)
hdist2 = 0.70711*dist2
print "Hellinger distance I-T2", hdist2
print "HD difference", abs(hdist1-hdist2)

# reconstruct the amplitudes
inputamplitudes[:] = [math.sqrt(x) for x in inputamplitudes]
training1amplitudes[:] = [math.sqrt(x) for x in training1amplitudes]
training2amplitudes[:] = [math.sqrt(x) for x in training2amplitudes]

#initialize lists
ancilla0m0 = [0]*16
ancilla0m1 = [0]*16
ancilla1m0 = [0]*16
ancilla1m1 = [0]*16

for i in range(16):
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


print "PREDICTION1 for ancilla in |0> state: ", prediction1
#print "PREDICTION2 for ancilla in |0> state: ", prediction2
print ""
print "PREDICTION for class in |0> state: ", classprediction0state
print "PREDICTION for class in |1> state: ", classprediction1state
print "SUM: ", (classprediction0state+classprediction1state)
print ""
# print "ancilla0m0 prob: ", sum(ancilla0m0)
# print "ancilla0m1 prob: ", sum(ancilla0m1)
#
# print "ancilla1m0 prob: ", sum(ancilla1m0)
# print "ancilla1m1 prob: ", sum(ancilla1m1)
print "==================================="
print ""
'''
# The following probabilities are extracted after interferring training with input vectors with delta = 0.6:

# ancilla = 0 // m =0
results1 = [0.221016,0.151997,0.001939,0.132997,0.142303,0.001939,0.092284,0.090733,0.001163,0.000388,0.090345,0.068244,0.001163,0.001163,0.001163,0.001163]
# ancilla = 1 // m = 0
results2 = [0.003617,0.000804,0.215836,0.000804,0.002412,0.139469,0.000804,0.000804,0.145096,0.144293,0.000402,0.000804,0.087621,0.094453,0.094453,0.068328]
# ancilla = 0 // m = 1
results3 = [0.124659,0.118869,0.007153,0.116485,0.121253,0.003065,0.121594,0.119210,0.000681,0.000341,0.128406,0.129768,0.000341,0.001022,0.000341,0.006812]
# ancilla = 1 // m = 1
results4 = [0.018072,0.001506,0.139056,0.002510,0.003012,0.114458,0.002510,0.001506,0.120984,0.109940,0.001506,0.012048,0.104920,0.121486,0.117470,0.129016]

# reconstruct the amplitudes
for i in range(8):
    results1[i] = math.sqrt(results1[i])
    results2[i] = math.sqrt(results2[i])
    results3[i] = math.sqrt(results3[i])
    results4[i] = math.sqrt(results4[i])

print "SUMMING THE AMPLITUDES: "
print ""
totalsum = sum(results1)+sum(results2)+sum(results3)+sum(results4);

print "sum1: ", sum(results1)
print "sum2: ", sum(results2)
print "sum3: ", sum(results3)
print "sum4: ", sum(results4)
print "totalsum: ", totalsum
'''
