from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


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
ax.text(1,1,1,  '%s' % ("|000>\np=0.0"), size=14, zorder=1,color='k')
ax.text(1,-1,1,  '%s' % ("|001>\np=0.0"), size=14, zorder=1,color='k')
ax.text(1,-1,-1,  '%s' % ("|011>\np=0.0"), size=14, zorder=1,color='k')
ax.text(1,1,-1,  '%s' % ("|010>\np=1.0"), size=14, zorder=1,color='k')
ax.text(-1,-1,1,  '%s' % ("|101>\np=0.0"), size=14, zorder=1,color='k')
ax.text(-1,1,1,  '%s' % ("|100>\np=0.0"), size=14, zorder=1,color='k')
ax.text(-1,1,-1,  '%s' % ("|110>\np=0.0"), size=14, zorder=1,color='k')
ax.text(-1,-1,-1,  '%s' % ("|111>\np=0.0"), size=14, zorder=1,color='k')

# Hide the axes
ax = plt.gca(projection='3d')
ax._axis3don = False

# Show the figure
plt.show()

################## 2ND PLOT #######################
# After inverse diffusion (stats obtained from 100 000 runs in Liqui|>)

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
ax.text(1,1,1,  '%s' % ("|000>\np=0.009210"), size=14, zorder=1,color='k')
ax.text(1,-1,1,  '%s' % ("|001>\np=0.080990"), size=14, zorder=1,color='k')
ax.text(1,-1,-1,  '%s' % ("|011>\np=0.008800"), size=14, zorder=1,color='k')
ax.text(1,1,-1,  '%s' % ("|010>\np=0.001000"), size=14, zorder=1,color='k')
ax.text(-1,-1,1,  '%s' % ("|101>\np=0.728780"), size=14, zorder=1,color='k')
ax.text(-1,1,1,  '%s' % ("|100>\np=0.081040"), size=14, zorder=1,color='k')
ax.text(-1,1,-1,  '%s' % ("|110>\np=0.009150"), size=14, zorder=1,color='k')
ax.text(-1,-1,-1,  '%s' % ("|111>\np=0.081030"), size=14, zorder=1,color='k')

# Hide the axes
ax = plt.gca(projection='3d')
ax._axis3don = False


# Show the figure
plt.show()

################## 3RD PLOT #######################
# After diffusion (stats obtained from 100 000 runs in Liqui|>)

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
ax.text(1,1,1,  '%s' % ("|000>\np=0.081570"), size=14, zorder=1,color='k')
ax.text(1,-1,1,  '%s' % ("|001>\np=0.008790"), size=14, zorder=1,color='k')
ax.text(1,-1,-1,  '%s' % ("|011>\np=0.078770"), size=14, zorder=1,color='k')
ax.text(1,1,-1,  '%s' % ("|010>\np=0.730840"), size=14, zorder=1,color='k')
ax.text(-1,-1,1,  '%s' % ("|101>\np=0.001100"), size=14, zorder=1,color='k')
ax.text(-1,1,1,  '%s' % ("|100>\np=0.009110"), size=14, zorder=1,color='k')
ax.text(-1,1,-1,  '%s' % ("|110>\np=0.081000"), size=14, zorder=1,color='k')
ax.text(-1,-1,-1,  '%s' % ("|111>\np=0.008820"), size=14, zorder=1,color='k')

# Hide the axes
ax = plt.gca(projection='3d')
ax._axis3don = False

# Show the figure
plt.show()

################## 4TH PLOT #######################
# Tesseract (hypercube) for 4 qubit system

# Initialize the 3D figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# Draw first (smaller) cube
r = [-1, 1]
for s, e in combinations(np.array(list(product(r,r,r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s,e), color="b")

# Label the edges

#inner cube
ax.text(1,1,1,  '%s' % ("|0000>"), size=14, zorder=1,color='k')
ax.text(1,-1,1,  '%s' % ("|0001>"), size=14, zorder=1,color='k')
ax.text(1,-1,-1,  '%s' % ("|1001>"), size=14, zorder=1,color='k')
ax.text(1,1,-1,  '%s' % ("|1000>"), size=14, zorder=1,color='k')
ax.text(-1,-1,1,  '%s' % ("|0011>"), size=14, zorder=1,color='k')
ax.text(-1,1,1,  '%s' % ("|0010>"), size=14, zorder=1,color='k')
ax.text(-1,1,-1,  '%s' % ("|1010>"), size=14, zorder=1,color='k')
ax.text(-1,-1,-1,  '%s' % ("|1011>"), size=14, zorder=1,color='k')
#outer cube
ax.text(-2,-2,-2,  '%s' % ("|1111>"), size=14, zorder=1,color='k')
ax.text(2,-2,-2,  '%s' % ("|1101>"), size=14, zorder=1,color='k')
ax.text(-2,2,2,  '%s' % ("|0110>"), size=14, zorder=1,color='k')
ax.text(-2,2,-2,  '%s' % ("|1110>"), size=14, zorder=1,color='k')
ax.text(-2,-2,2,  '%s' % ("|0111>"), size=14, zorder=1,color='k')
ax.text(2,2,2,  '%s' % ("|0100>"), size=14, zorder=1,color='k')
ax.text(2,2,-2,  '%s' % ("|1100>"), size=14, zorder=1,color='k')
ax.text(2,-2,2,  '%s' % ("|0101>"), size=14, zorder=1,color='k')

# Hide the axes
ax = plt.gca(projection='3d')
ax._axis3don = False

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

# Define the vectors for the lines
a = Arrow3D([-1,-2],[-1,-2],[-1,-2], mutation_scale=20, lw=1, arrowstyle="-", color="b")
b = Arrow3D([1,2],[-1,-2],[-1,-2], mutation_scale=20, lw=1, arrowstyle="-", color="b")
c = Arrow3D([-1,-2],[1,2],[-1,-2], mutation_scale=20, lw=1, arrowstyle="-", color="b")
d = Arrow3D([-1,-2],[-1,-2],[1,2], mutation_scale=20, lw=1, arrowstyle="-", color="b")
e = Arrow3D([1,2],[1,2],[-1,-2], mutation_scale=20, lw=1, arrowstyle="-", color="b")
f = Arrow3D([-1,-2],[1,2],[1,2], mutation_scale=20, lw=1, arrowstyle="-", color="b")
g = Arrow3D([1,2],[-1,-2],[1,2], mutation_scale=20, lw=1, arrowstyle="-", color="b")
h = Arrow3D([1,2],[1,2],[1,2], mutation_scale=20, lw=1, arrowstyle="-", color="b")

ax.add_artist(a)
ax.add_artist(b)
ax.add_artist(c)
ax.add_artist(d)
ax.add_artist(e)
ax.add_artist(f)
ax.add_artist(g)
ax.add_artist(h)

# Draw second cube (bigger one)
r = [-2, 2]
for s, e in combinations(np.array(list(product(r,r,r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s,e), color="b")

# Show the figure
plt.show()
