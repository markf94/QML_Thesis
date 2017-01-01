import qutip as qp
import cmath
import numpy as np
import math

b = qp.Bloch()

#Add basis vectors
#b.vector_color = ['k']
#x_basis = (qp.basis(2,0)+(1+0j)*qp.basis(2,1)).unit()
#y_basis = (qp.basis(2,0)+(0+1j)*qp.basis(2,1)).unit()
#z_basis = (qp.basis(2,0)+(0+0j)*qp.basis(2,1)).unit()
#b.add_states([x_basis,y_basis,z_basis])
#b.add_states([x_basis]);

# color vector for 3/4 state visualization
#b.vector_color = ['k','k','y','m','r']
#b.vector_color = ['k','m']
b.vector_color = ['m','g','b','y','r']
b.vector_width = 3
#onestate = [[0.,0.,-1.]]
#b.add_vectors(onestate)
#Qubit amplitudes

#xp = [np.cos(th) for th in np.linspace(0, -23*math.pi/16, 30)]

#yp = [np.sin(th) for th in np.linspace(0, -23*math.pi/16, 30)]

#zp = np.zeros(30)
#zp = [np.sin(th) for th in np.linspace(0, math.pi/4, 20)]
#zp = np.append(zp1,zp2)
#pnts = [xp, yp, zp]
#b.add_points(pnts)

#zp = [np.cos(th) for th in np.linspace(0.25*math.pi, -0.25*math.pi, 20)]

#yp = [np.sin(th) for th in np.linspace(0.25*math.pi, -0.25*math.pi, 20)]

#zp = np.zeros(10)
#xp = np.zeros(20)
#zp = np.append(zp1,zp2)
#pnts = [xp, yp, zp]

#b.add_points(pnts)
'''
alpha = -0.70711
beta = 0.70711
'''

#original -23/16pi z-rotation
x = -0.195075369355
y = 0.980788254554
z = 9.09619999983e-06
new_vec = [x.real,y.real,z.real] #works only for the right half sphere....
b.add_vectors(new_vec)
'''
# 0.22739
x = -0.475682821273
y =  0.851984391192
z = -0.218742887344
new_vec = [x.real,y.real,z.real] #works only for the right half sphere....
b.add_vectors(new_vec)
'''
#gen5 n=1 0.15165
alpha = 0.750003414067-0.103553861978j
beta = -0.250001138022+0.603556138022j
x = -0.499999218983
y = 0.853552057314
z = 0.146457046886
new_vec = [x.real,y.real,z.real] #works only for the right half sphere....
b.add_vectors(new_vec)

#n=2 0.10722
alpha = 0.625002845056-0.125000569011j
beta = -0.1767775+0.750003414067j
x = -0.4084714563
y = 0.893307110308
z = -0.187492602838
new_vec = [x.real,y.real,z.real] #works only for the right half sphere....
b.add_vectors(new_vec)

#n=3 0.020864
alpha = 0.715878092735-0.0451934273334j
beta = -0.0629761224178+0.693915861379j
x = -0.15288589139
y = 0.987816850855
z = 0.0290477790642
new_vec = [x.real,y.real,z.real] #works only for the right half sphere....
b.add_vectors(new_vec)

#gen6 n=7 0.00156
x = -0.195068414425
y = 0.980789637338
z = 3.26698397897e-05
new_vec = [x.real,y.real,z.real] #works only for the right half sphere....
b.add_vectors(new_vec)
b.show()

'''
# #1 in Liquid (3/4 state)
#alpha = 0.85355 - 0.35355j
#beta = 0.35355 - 0.14645j
#alpha = 1/math.sqrt(2)
#beta = 1/math.sqrt(2)*cmath.exp(1j*math.pi/4)

# #2 in Liquid (7/8 state)
#alpha = 0.96194 - 0.19134j
#beta = 0.19134 - 0.03806j

# #3 in Liquid (x-y-plane)
#alpha = 0.70711
#beta = 0.70711*cmath.exp(1j*cmath.pi/4)


#Find and eliminate global phase
angle_alpha = cmath.phase(alpha)
print "angle_alpha:", angle_alpha
angle_beta = cmath.phase(beta)
print "angle_beta:", angle_beta

if angle_beta < 0:
	if angle_alpha < angle_beta:
		alpha_new = alpha/cmath.exp(1j*angle_beta)
		beta_new = beta/cmath.exp(1j*angle_beta)
	else:
		alpha_new = alpha/cmath.exp(1j*angle_alpha)
        	beta_new = beta/cmath.exp(1j*angle_alpha)
else:
	if angle_alpha > angle_beta:
                alpha_new = alpha/cmath.exp(1j*angle_beta)
                beta_new = beta/cmath.exp(1j*angle_beta)
        else:
                alpha_new = alpha/cmath.exp(1j*angle_alpha)
                beta_new = beta/cmath.exp(1j*angle_alpha)
print "alpha_new:", alpha_new
print "beta_new:", beta_new

if abs(alpha) == 0 or abs(beta) == 0:
	if alpha == 0:
		b.clear()
		down = [0,0,-1]
		b.add_vectors(down)
	else:
		b.clear()
		up = [0,0,1]
		b.add_vectors(up)
else:
	#Compute theta and phi from alpha and beta
	theta = 2*cmath.acos(alpha_new)
	phi = -1j*cmath.log(beta_new/cmath.sin(theta/2))
	print "theta:", theta
	print "phi:", phi

	#Compute the cartesian coordinates
	x = cmath.sin(theta)*cmath.cos(phi)
	y = cmath.sin(theta)*cmath.sin(phi)
	z = cmath.cos(theta)
	print "x:", x
	print "y:", y
	print "z:", z

	#Create the new state vector and plot it onto the Bloch sphere
	new_vec = [x.real,y.real,z.real] #works only for the right half sphere....
	b.add_vectors(new_vec)


b.show()
'''
