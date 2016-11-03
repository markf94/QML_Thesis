import PIL
import Image
import numpy
import math
from matplotlib import pyplot as plt
from scipy import stats
import scipy

FILENAME = 'grant.jpg' #image can be in gif jpeg or png format
im = Image.open(FILENAME).convert('RGB')
pix = numpy.array(im)#im.load()
w = im.size[0]
h = im.size[1]
array = pix.ravel()
length = array.size
print "length: ", length
plt.hist(array,256,[0,256])
plt.title('Pixel colour histogram for picture')
plt.show()

counter = 0
index = []
for i in range(length):
    if array[i] <= 0: #or array[i] > 80:
        index.append(i)
        counter = counter + 1
        #array[i] = array[i] + 1
new_array = numpy.delete(array, index)

'''
plt.hist(new_array,256,[0,256])
plt.title('Reduced pixel colour histogram')
plt.show()

fig = plt.figure()
ax1 = fig.add_subplot(211)
x = new_array #stats.loggamma.rvs(5, size=500) + 5
stats.probplot(x, dist=stats.norm, plot=ax1)
ax1.set_xlabel('')
ax1.set_title('Probplot against normal distribution')
ax2 = fig.add_subplot(212)
xt = stats.boxcox(x,0.7) #0.6 for apple #0.9903 with 0.7 for grant
stats.probplot(xt, dist=stats.norm, plot=ax2)
ax2.set_title('Probplot after Box-Cox transformation')
plt.show()


plt.hist(xt,100,[0,80])
plt.title('Box Cox transformed pixel colour histogram')
plt.show()
'''
'''
# Inverse hyperbolic sine transformation

def IHS(y, theta):
    return (numpy.log(theta*y+(theta**2*y**2+1)**0.5)/theta)

def loglikelihood(theta,y):
    n = y.size;
    IHS_vectorized = numpy.vectorize(IHS,otypes=[numpy.float]);
    xt = IHS_vectorized(y, theta);
    #print xt
    #loglike = f(xt,n)
    #print loglike
    #return loglike
    result = (-0.5*n*numpy.log(sum((xt - numpy.mean(xt))**2))-0.5*sum(numpy.log(1+theta**2*y**2)))*(-1)
    return result

# try this on our data
bnds = ((0.00001, None),)
theta_optim = scipy.optimize.minimize(loglikelihood, x0=1, args=(new_array), bounds=bnds,tol=1e-10) # 2.0407
print "theta optimized: ", theta_optim.x

f = numpy.vectorize(IHS);
transformed = f(new_array, theta_optim.x)

fig = plt.figure()
ax1 = fig.add_subplot(211)
x = new_array #stats.loggamma.rvs(5, size=500) + 5
stats.probplot(x, dist=stats.norm, plot=ax1)
ax1.set_xlabel('')
ax1.set_title('Probplot against normal distribution')
ax2 = fig.add_subplot(212)
stats.probplot(transformed, dist=stats.norm, plot=ax2)
ax2.set_title('Probplot after IHS transformation')
plt.show()

plt.hist(new_array,256,[0,256])
plt.title('IHS transformed pixel colour histogram')
plt.show()
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
random = numpy.random.normal(10,8,20)
for i in range(random.size):
    if random[i] < 0:
        random[i] = random[i] - (random[i]-1)
    if random[i] == 0:
        random[i] = random[i] + 1
'''
'''
counter = 0
check = 0
for l in range(256):
    for i in range(length):
    #if array[i] <= 0:
        if array[i] == l:
            check = 1
            break;
        if i == w*h and check == 0:
            numpy.append(array, l)
'''

'''
# EXAMPLE BOX COX PROBABILITY
fig = plt.figure()
ax1 = fig.add_subplot(211)
x = stats.loggamma.rvs(5, size=500) + 5
stats.probplot(x, dist=stats.norm, plot=ax1)
ax1.set_xlabel('')
ax1.set_title('Probplot against normal distribution')
ax2 = fig.add_subplot(212)
xt, _ = stats.boxcox(x)
stats.probplot(xt, dist=stats.norm, plot=ax2)
ax2.set_title('Probplot after Box-Cox transformation')
plt.show()
'''
