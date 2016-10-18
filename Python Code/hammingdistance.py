from numpy import binary_repr

# INPUT must obey the normalization condition:
# dec1 + dec2 = 1 (since they constitute probabilities)
dec1 = 0.50;
dec2 = 0.50;

print "Input vector: ", [dec1, dec2]

# |0> vector binary representation
training1 = "11001000000000";
# |1> vector binary representation
training2 = "00000001100100";

# Hamming distance function from Wikipedia
def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))

# Convert decimal to binary
br1 = binary_repr(int(100*dec1));
br2 = binary_repr(int(100*dec2));
print "Binary string 1: ", br1
print "Binary string 2: ", br2

# HD function takes strings as input > convert to string
s1 = str(br1);
s2 = str(br2);

# make all binary strings equal to the same length by adding leading zeros
if len(s1) != len(s2):
    maxbinarylength = max([len(s1),len(s2)]);
    for i in range((maxbinarylength-len(s1))):
        br1 = "0" + br1;
    for i in range(maxbinarylength-len(s2)):
        br2 = "0" + br2;
    if 2*maxbinarylength > len(training1):
        for i in range(2*maxbinarylength-len(s1)):
            training1 = "0" + training1;
            training2 = "0" + training2;

if  len(s1) < len(training1) or len(s2) < len(training1):
    

inputvector = br1 + br2;
print "New binary string 1: ", br1
print "New binary string 2: ", br2
print "Training vector 1: ", training1
print "Training vector 2: ", training2
print "Input vector:      ", inputvector

#s3old = "10010110011001";
#s3 = "00110011001011";
#s3 = "01010000111100"

# Compute the HD between s1 and s2
hdT1T2 = hammingDistance(training1,training2);
hdT1IV = hammingDistance(training1,inputvector);
hdT2IV = hammingDistance(training2,inputvector);
print "Hamming Distance training-training: ", hdT1T2
print "Hamming Distance training1-input:   ", hdT1IV
print "Hamming Distance training2-input:   ", hdT2IV

if dec1 > dec2:
    print "Should be closer to T1"
    if hdT1IV < hdT2IV:
        print "TRUE"
    else:
        print "FALSE"
else:
    print "Should be closer to T2"
    if hdT2IV < hdT1IV:
        print "TRUE"
    else:
        print "FALSE"
