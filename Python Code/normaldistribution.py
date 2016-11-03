import math
from scipy.integrate import quad
import numpy as np

# Define the function for a gaussian distribution
def normaldistribution(x, sigma, mu):
    # sigma is standard deviation
    # mu is mean
    return 1/(sigma*math.sqrt(2*math.pi))*math.exp(-(x-mu)**2/(2*sigma**2));

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

print "Integration result:", I
print "Result as fraction: ", I[0].as_integer_ratio()
theta0 = math.acos(math.sqrt(0.3));
print "theta0: ", theta0
print "cos(theta0): ", math.cos(theta0)
print "sin(theta0): ", math.sin(theta0)
#theta1 = math.acos(math.sqrt(0.5))

#print "f(i): ", I2[0]/I[0]
