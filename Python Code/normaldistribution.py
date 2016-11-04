import math
from scipy.integrate import quad
import numpy as np

# This code needs to be modified such that it generates the theta_i values
# for a given number of discrete partitions of a given log-concave probability
# distribution!

# Define the function for a gaussian distribution
def normaldistribution(x, sigma, mu):
    # sigma is standard deviation
    # mu is mean
    return 1/(sigma*math.sqrt(2*math.pi))*math.exp(-(x-mu)**2/(2*sigma**2));

# As defined in Grover & Rudolph (2002)
# "Creating superpositions that correspond to efficiently integrable probability distributions"
def GroverTheta(f):
    return math.acos( math.sqrt(f) )

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

theta0 = math.acos(math.sqrt(0.3));
print "theta0: ", theta0
print "cos(theta0): ", math.cos(theta0)
print "sin(theta0): ", math.sin(theta0)
