import math

# Verification of DiffusionKNN results

# The following probabilities have been retrieved from Liqui|> simulations with
# 4 diffusion qubits and 10000 runs
# The probabilities are extracted after interferring training with input vectors

# order
# [|0000>,|1000>,|0100>,|0010>,|0001>,|1100>,|1010>,|1001>,|0110>,|0101>,|0011>,|1011>,|1110>,|1101>,|0111>,|1111>]

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

totalsum = sum(results1)+sum(results2)+sum(results3)+sum(results4);

print "sum1: ", sum(results1)
print "sum2: ", sum(results2)
print "sum3: ", sum(results3)
print "sum4: ", sum(results4)
print "totalsum: ", totalsum
