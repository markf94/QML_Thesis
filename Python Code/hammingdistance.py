from numpy import binary_repr

# Set to True if you want to find out if the binary encoding works well with respect to HD classification
testmode = False;

# INPUT must obey the normalization condition:
# dec1 + dec2 = 1 (since they constitute probabilities)
inputdec1 = 0.6;
inputdec2 = 0.4;

if testmode == True:
    # Generate a list of numbers to fill the input vector with:
    dummytest = [None]*5;
    for k in range(0,5):
        dummytest[k] = 0.1*k;
    print dummytest
    #dummy_list = [0.1,0.2,0.21,0.22,0.23,0.24,0.3,0.4,0.5,0.53,0.54,0.55,0.6,0.65,0.66,0.67,0.68,0.69,0.7,0.75,0.8,0.85,0.9,0.95,1]
else:
    dummytest = [1];

# Hamming distance function from Wikipedia
def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))

for j in reversed(dummytest):

    if testmode == True:
        inputdec1 = j;
        inputdec2 = 1-j;
    else:
        print "Input vector (dec): ", [inputdec1, inputdec2]

    training1dec1 = 1;
    training1dec2 = 0;
    if testmode == False:
        print "Training vector 1 (dec)", [training1dec1, training1dec2]

    training2dec1 = 0;
    training2dec2 = 1;
    if testmode == False:
        print "Training vector 2 (dec): ", [training2dec1, training2dec2]

    # Convert all vector entries from decimal to binary
    inputbin1 = binary_repr(int(10*inputdec1));
    inputbin2 = binary_repr(int(10*inputdec2));
    print "I Binary string 1: ", inputbin1
    print "I Binary string 2: ", inputbin2
    training1bin1 = binary_repr(int(10*training1dec1));
    training1bin2 = binary_repr(int(10*training1dec2));
    print "T1 Binary string 1: ", training1bin1
    print "T1 Binary string 2: ", training1bin2
    training2bin1 = binary_repr(int(10*training2dec1));
    training2bin2 = binary_repr(int(10*training2dec2));
    print "T2 Binary string 1: ", training2bin1
    print "T2 Binary string 2: ", training2bin2


    # HD function takes strings as input > convert to string
    inputs1 = str(inputbin1);
    inputs2 = str(inputbin2);
    training1s1 = str(training1bin1);
    training1s2 = str(training1bin2);
    training2s1 = str(training2bin1 );
    training2s2 = str(training2bin2 );


    # make all binary strings equal to length 8
    # by adding leading zeros (8 bits = 1 byte)

    for i in range(4):
        if len(inputs1) != 4:
            inputs1 = "0" + inputs1;
        if len(inputs2) != 4:
            inputs2 = "0" + inputs2;
        if len(training1s1) != 4:
            training1s1 = "0" + training1s1;
        if len(training1s2) != 4:
            training1s2 = "0" + training1s2;
        if len(training2s1) != 4:
            training2s1 = "0" + training2s1;
        if len(training2s2) != 4:
            training2s2 = "0" + training2s2;

    # for each vector glue the two 8 bitstrings together
    inputvector = inputs1 + inputs2;
    training1 = training1s1 + training1s2;
    training2 = training2s1 + training2s2;
    if testmode == False:
        print "Training vector 1: ", training1
        print "Training vector 2: ", training2
        print "Input vector:      ", inputvector

    # Compute the HD between s1 and s2
    hdT1T2 = hammingDistance(training1,training2);
    hdT1IV = hammingDistance(training1,inputvector);
    hdT2IV = hammingDistance(training2,inputvector);
    if testmode == False:
        print "Hamming Distance training-training: ", hdT1T2
        print "Hamming Distance training1-input:   ", hdT1IV
        print "Hamming Distance training2-input:   ", hdT2IV

    # Perform a check:
    if inputdec1 > inputdec2:
        print "Should be closer to T1"
        if hdT1IV < hdT2IV:
            print "TRUE"
        else:
            print "FALSE", j
            print "Hamming Distance training1-input:   ", hdT1IV
            print "Hamming Distance training2-input:   ", hdT2IV
    else:
        if inputdec1 == inputdec2:
            print "Should be equally close to both"
            if hdT2IV == hdT1IV:
                print "TRUE"
            else:
                print "FALSE", j
                print "Hamming Distance training1-input:   ", hdT1IV
                print "Hamming Distance training2-input:   ", hdT2IV

        else:
            print "Should be closer to T2"
            if hdT2IV < hdT1IV:
                print "TRUE"
            else:
                print "FALSE", j
                print "Hamming Distance training1-input:   ", hdT1IV
                print "Hamming Distance training2-input:   ", hdT2IV
