from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

################## 1ST PLOT #######################
# INITIAL STATE

# Initialize the 3D figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# Draw cube
r = [-1, 1]
for s, e in combinations(np.array(list(product(r,r,r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s,e), color="b")

# Label the edges
ax.text(1,1,1,  '%s' % ("|000>\np=0.0"), size=20, zorder=1,color='k')
ax.text(1,-1,1,  '%s' % ("|001>\np=0.0"), size=20, zorder=1,color='k')
ax.text(1,-1,-1,  '%s' % ("|011>\np=0.0"), size=20, zorder=1,color='k')
ax.text(1,1,-1,  '%s' % ("|010>\np=1.0"), size=20, zorder=1,color='k')
ax.text(-1,-1,1,  '%s' % ("|101>\np=0.0"), size=20, zorder=1,color='k')
ax.text(-1,1,1,  '%s' % ("|100>\np=0.0"), size=20, zorder=1,color='k')
ax.text(-1,1,-1,  '%s' % ("|110>\np=0.0"), size=20, zorder=1,color='k')
ax.text(-1,-1,-1,  '%s' % ("|111>\np=0.0"), size=20, zorder=1,color='k')

# Hide the axes
ax = plt.gca(projection='3d')
ax._axis3don = False

# Show the figure
plt.show()

################## 2ND PLOT #######################
# After Diffusion (stats obtained from 100 000 runs in Liqui|>)

# Initialize the 3D figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# Draw cube
r = [-1, 1]
for s, e in combinations(np.array(list(product(r,r,r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s,e), color="b")

# Label the edges
ax.text(1,1,1,  '%s' % ("|000>\np=0.081570"), size=20, zorder=1,color='k')
ax.text(1,-1,1,  '%s' % ("|001>\np=0.008790"), size=20, zorder=1,color='k')
ax.text(1,-1,-1,  '%s' % ("|011>\np=0.078770"), size=20, zorder=1,color='k')
ax.text(1,1,-1,  '%s' % ("|010>\np=0.730840"), size=20, zorder=1,color='k')
ax.text(-1,-1,1,  '%s' % ("|101>\np=0.001100"), size=20, zorder=1,color='k')
ax.text(-1,1,1,  '%s' % ("|100>\np=0.009110"), size=20, zorder=1,color='k')
ax.text(-1,1,-1,  '%s' % ("|110>\np=0.081000"), size=20, zorder=1,color='k')
ax.text(-1,-1,-1,  '%s' % ("|111>\np=0.008820"), size=20, zorder=1,color='k')

# Hide the axes
ax = plt.gca(projection='3d')
ax._axis3don = False

# Show the figure
plt.show()

####################### 3RD PLOT ###########################
# Show that it distributes in a Gaussian fashion

x = [-3,-2,-1,0,1,2,3]
#order:
# |101>,|001>,|011>,|010>,|000>,|100>,|101>
y = [0.001100,0.008790,0.078770,0.730840,0.081570,0.009110,0.001100]
plt.plot(x,y)
plt.ylabel('Probability')
plt.xlabel('abs(x) = Hamming distance')
plt.show()
