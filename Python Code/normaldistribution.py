import math
from scipy.integrate import quad
import numpy as np

# This code needs to be modified such that it generates the theta_i values
# for either gaussian or poissonian distributions as well as differentiation between
# different means!

# Define the function for a gaussian distribution
def normaldistribution(x, sigma, mu):
    # sigma is standard deviation
    # mu is mean
    return 1/(sigma*math.sqrt(2*math.pi))*math.exp(-(x-mu)**2/(2*sigma**2));

# As defined in Grover & Rudolph (2002)
# "Creating superpositions that correspond to efficiently integrable probability distributions"
def GroverTheta(f):
    return math.acos( math.sqrt(f) )

### DEFINING THE RECURSIVE FUNCTION ###

# the index variable being the i in theta_i as described in Grover & Rudolph (2002)  =[0]*numberofpartitions
def theta_i_recursive(min,index,stepsizeintern,meanintern,numberofpartitions,theta, distribution="unknown"):
    #function needs to be called initially with index=0

    # define the first pair of limits
    lowerlimit = float(min)
    upperlimit = lowerlimit + stepsizeintern

    if upperlimit == meanintern:
        #lowerlimit = float(min)
        #upperlimit = float(max)
        # print "basecase"
        # print "lowerlimit", lowerlimit
        # print "upperlimit", upperlimit
        I = quad(normaldistribution, lowerlimit, upperlimit, args=(std,mean))
        # Compute the arccos(sqrt(f(i)))
        theta[index] = GroverTheta(I[0])

        # fill the theta's based on symmetry if gaussian
        if distribution=="gaussian":
            for i in reversed(range(index+1)):
                theta[index+i+1] = theta[index-i]
        #print "thetabase: ", theta
        return theta;
        #and don't call your own function again!

    # calculate the width of each partition
    #stepsize = 2.0*float(max)/numberofpartitions
    #halfpoint = findmiddle(minbound,0) #2.5std to the left



    # print "lowerlimit", lowerlimit
    # print "upperlimit", upperlimit
    # perform the integration over the partition
    I = quad(normaldistribution, lowerlimit, upperlimit, args=(std,mean))

    # Compute the arccos(sqrt(f(i)))
    theta[index] = GroverTheta(I[0])
    index += 1

    return theta_i_recursive(upperlimit,index,stepsizeintern,meanintern,numberofpartitions,theta,distribution)


# Print intro
print "######################################################################"
print "This code generates the theta_i values for the Grover & Rudolph (2002)"
print "quantum state preparation for a gaussian probability distribution. \n"
print ""
mean = float(raw_input("Mean: "))
std = float(raw_input("Standard Deviation: "))
maxstdboundary = float(raw_input("How many stds out do you wanna set the boundary?: "))
numberofpartitions = int(raw_input("Maximum number of partitions (input must satisfy input=2^N): "))
minbound = mean-maxstdboundary*std
#print "minbound", minbound
maxbound = mean+maxstdboundary*std
#print "maxbound", maxbound

if maxbound>0 and minbound>0:
    rangeofinterest = float(maxbound-minbound)
if maxbound>0 and minbound<0:
    rangeofinterest = float(abs(maxbound)+abs(minbound))
if maxbound<0 and minbound<0:
    rangeofinterest = float(abs(minbound)-abs(maxbound))
if maxbound == 0:
    rangeofinterest = float(abs(minbound))
if minbound == 0:
    rangeofinterest = float(maxbound)

#print "range: ", rangeofinterest

print "======================================================================"
print "Theta_i results: "
print ""

# CALL RECURSIVE
needed_iterations = int(math.log(numberofpartitions,2))
for i in range(needed_iterations):
    currentpartitions = 2**(i+1)
    print "%i partitions: " %(currentpartitions)
    stepsize = rangeofinterest/float(currentpartitions)
    print "stepsize: ", stepsize
    theta = [0]*currentpartitions
    current_thetas = theta_i_recursive(minbound,0,stepsize,mean,currentpartitions,theta,distribution="gaussian")
    print current_thetas
    print "_______________________________"

####### OFFICIAL END OF CODE #######


# Previous integration code snippet

'''
# Print intro
print "######################################################################"
print "This code generates the theta_i values for the Grover & Rudolph (2002)"
print "quantum state preparation for a gaussian probability distribution. \n"

# Read user input
mean = float(raw_input("Mean: "))
std = float(raw_input("Standard Deviation: "))
lowerlimit = raw_input("Lower  integration limit (-inf to +inf): ")
upperlimit = raw_input("Upper integration limit (-inf to +inf): ")

if upperlimit == "+inf":
    upperlimit = np.inf;
else:
    upperlimit = float(upperlimit);
if lowerlimit == "-inf":
    lowerlimit = -np.inf;
else:
    lowerlimit = float(lowerlimit);

# Perform integration
I = quad(normaldistribution, lowerlimit, upperlimit, args=(std,mean))

#halfpoint = (lowerlimit-upperlimit)/2;
#print "halfpoint: ", halfpoint
#I2 = quad(normaldistribution, lowerlimit,halfpoint, args=(std,mean))

print "\n------------ RESULTS ------------"
print "Raw integration result: ", I
print " "
print "Probability for random variable to be found in this interval: ", I[0]*100
print " "
print "Probability as fraction: ", I[0].as_integer_ratio()
print " "
'''

# PREVIOUS NON-RECURSIVE CODE BELOW
'''
# Compute the halfpoint
def findmiddle(min,max):
    if min>max:
        return (max-min)/2
    else:
        return (min-max)/2

# i being the counter for theta_i
def theta_i(i,min,max):

    if max == mean:
        lowerlimit = float(min)
        upperlimit = float(max)
        print "lowerlimit", lowerlimit
        print "upperlimit", upperlimit
        I = quad(normaldistribution, lowerlimit, upperlimit, args=(std,mean))
        # Compute the arccos(sqrt(f(i)))
        return math.acos(math.sqrt(I[0]))
        #and don't call your own function again!

    #halfpoint = findmiddle(minbound,0) #2.5std to the left
    lowerlimit = float(min)
    upperlimit = float(max)
    print "lowerlimit", lowerlimit
    print "upperlimit", upperlimit
    I = quad(normaldistribution, lowerlimit, upperlimit, args=(std,mean))
    # Compute the arccos(sqrt(f(i)))
    return math.acos(math.sqrt(I[0]));

# 2 partitions
print "2 Partitions: "
numberofpartitions = 2.0
stepsize = 2.0*float(maxbound)/numberofpartitions
print "stepsize: ", stepsize
lowerlimit = minbound
upperlimit = minbound+stepsize
theta_0 = theta_i(0,lowerlimit,upperlimit)
theta_1 = theta_0
print "theta0: ", theta_0
print "theta1: ", theta_1
print ""

# 4 partitions
print "4 Partitions: "
stepsize = 2.0*float(maxbound)/numberofpartitions
print "stepsize", stepsize
lowerlimit = minbound
upperlimit = minbound+stepsize
theta_0 = theta_i(0,lowerlimit,upperlimit)
print "theta0: ", theta_0
lowerlimit = upperlimit
upperlimit = lowerlimit + stepsize
theta_1 = theta_i(1,lowerlimit,upperlimit)
print "theta1: ", theta_1
'''
