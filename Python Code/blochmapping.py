import qutip as qp
import cmath

b = qp.Bloch()

#Add basis vectors
#x_basis = (qp.basis(2,0)+(1+0j)*qp.basis(2,1)).unit()
#y_basis = (qp.basis(2,0)+(0+1j)*qp.basis(2,1)).unit()
#z_basis = (qp.basis(2,0)+(0+0j)*qp.basis(2,1)).unit()
#b.add_states([x_basis,y_basis,z_basis])
vec = [[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]
b.add_vectors(vec)

#Qubit amplitudes
alpha = 0.5-0.5j
beta = -0.5+0.5j

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
