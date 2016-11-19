import PIL
import Image
import numpy
import math
from matplotlib import pyplot as plt
from scipy import stats
import scipy

# READING THE PICTURE
FILENAME = 'grant.jpg' #image can be in gif jpeg or png format
# Extract RGB values
im = Image.open(FILENAME).convert('RGB')
pix = numpy.array(im) #convert to numpy array
array = pix.ravel() # splits the triples and yields a 1D data array
length = array.size
print "length: ", length

#create histogram
plt.hist(array,256,[0,256])
plt.title('Pixel colour histogram for picture')
plt.show()

# Find all the zeros and save their positions in index
counter = 0
index = []
for i in range(length):
    if array[i] <= 0: #or array[i] > 80:
        index.append(i)
        counter = counter + 1
        #array[i] = array[i] + 1
# delete all zeros
new_array = numpy.delete(array, index)

# Plot histogram without zeros
plt.hist(new_array,256,[0,256])
plt.title('Reduced pixel colour histogram')
plt.show()

# Create Q-Q plots
fig = plt.figure()
ax1 = fig.add_subplot(211)
x = new_array
stats.probplot(x, dist=stats.norm, plot=ax1)
ax1.set_xlabel('')
ax1.set_title('Probplot against normal distribution')

ax2 = fig.add_subplot(212)
# Perform Box Cox transformation
xt = stats.boxcox(x,0.7) #0.6 for apple #0.9903 with 0.7 for grant
stats.probplot(xt, dist=stats.norm, plot=ax2)
ax2.set_title('Probplot after Box-Cox transformation')
plt.show()

# Plot transformed data in histogram
plt.hist(xt,100,[0,80])
plt.title('Box Cox transformed pixel colour histogram')
plt.show()

#### END OF BOX COX ####

# Define function for inverse hyperbolic sine transformation
def IHS(y, theta):
    return (numpy.log(theta*y+(theta**2*y**2+1)**0.5)/theta)

# define function for log-likelihood
def loglikelihood(theta,y):
    n = y.size;
    # vectorize the IHS function
    IHS_vectorized = numpy.vectorize(IHS,otypes=[numpy.float]);
    # compute the IHS transformed data
    xt = IHS_vectorized(y, theta);
    result = (-0.5*n*numpy.log(sum((xt - numpy.mean(xt))**2))-0.5*sum(numpy.log(1+theta**2*y**2)))*(-1);
    return result

# try this on our data
# theta must be greater than 0!
bnds = ((0.00001, None),);
# Maximize the log likelihood (we minimize the log-likelihood multiplied by -1)
theta_optim = scipy.optimize.minimize(loglikelihood, x0=1, args=(new_array), bounds=bnds,tol=1e-10) # 2.0407
print "theta optimized: ", theta_optim.x

# vectorize IHS outside of loglikelihood
f = numpy.vectorize(IHS);
# transform data with optimized theta value
transformed = f(new_array, theta_optim.x)

# Create Q-Q plots for IHS
fig = plt.figure()
ax1 = fig.add_subplot(211)
x = new_array
stats.probplot(x, dist=stats.norm, plot=ax1)
ax1.set_xlabel('')
ax1.set_title('Probplot against normal distribution')
ax2 = fig.add_subplot(212)
stats.probplot(transformed, dist=stats.norm, plot=ax2)
ax2.set_title('Probplot after IHS transformation')
plt.show()

# Plot the transformed data in histogram
plt.hist(transformed,256,[0,256])
plt.title('IHS transformed pixel colour histogram')
plt.show()

# Trying to fit a curve onto the histogram
# >> postponed to a later moment in time

'''
def f (x, a, b, c):
    return a * x ** 2 + b * x + c

#x should be bins
x = numpy.linspace(0, 256, new_array.size)
#y should be n >> what is n?
y = new_array

#It is not quite as simple though, since bins is 1 element bigger than n. So you have to extract the relevant data, which may be the left side of the bin (bins[:-1]), the right side (bins[1:]), the center ((bins[:-1]+bins[1:])/2) or something else. Depends how you want to model it.

# Fitting the curve
popt, pcov = scipy.optimize.curve_fit(f, x, y, [1.0, 1.0, 1.0])

# Plot data
plt.plot(x, y, 'o')

# Plot fit curve
fit_x = numpy.linspace(0, 256, new_array.size)
plt.plot(fit_x, f(fit_x, *popt))
plt.show()


'''
