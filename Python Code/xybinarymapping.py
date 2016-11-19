import math
import cmath
import qutip as qp

# Mapping of a real valued 2D vector x onto the x-y plane
# of the complex valued Bloch sphere

#3/4 mapping
#x0 = 0.75
#x1 = 0.25

#7/8 mapping
x0 = 0.875
x1 = 0.125

theta = math.radians(90) #guarantees point to lie in the x-y plane
phi = math.radians(90-180*x1)
print "theta", theta
print "phi", phi
print "Required z-rotation to prepare this state from |+>: ", phi/math.pi, "*pi"

Px = math.sin(theta)*math.cos(phi)
Py = math.sin(theta)*math.sin(phi)
Pz = math.cos(theta)
print "Px", Px
print "Py", Py
print "Pz", Pz

b = qp.Bloch()
new_vec = [Px,Py,Pz]
b.add_vectors(new_vec)
b.show()
