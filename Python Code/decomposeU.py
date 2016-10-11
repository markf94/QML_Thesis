#from scipy.optimize import root
from mpmath import findroot
import cmath
import math
import numpy as np

#Hadamard matrix elements
#u00 = 0.70711;
#u01 = 0.70711; #top right
#u10 = 0.70711; #top left
#u11 = -0.70711;

# S phase shift matrix elements
u00 = 1.0;
u01 = 0.0; #top right
u10 = 0.0; #top left
u11 = -1.0;

some_list = [-math.pi*1.5, -math.pi, -3/4*math.pi, -math.pi/2, -math.pi/4, 1.5*math.pi, math.pi/4, math.pi/2, 3/4*math.pi, math.pi,0];

if u10 != 0.0 and u01 != 0.0:
	#First find beta & delta
	def z1(beta,delta):
		temp=cmath.exp(1j*(beta+delta))-u11/u00;		#-U[1,1]/U[0,0];
		return temp

	def z2(beta,delta):
		temp=cmath.exp(1j*(beta-delta))+u10/u01;			#+U[1,0]/U[0,1];
		return temp

	for strtp1 in reversed(some_list):
		for strtp2 in reversed(some_list):
			try:
				ans =  findroot([z1,z2],(strtp1,strtp2))
				beta = ans[0].real;
				delta = ans[1].real;
				print "beta:", beta
				print "delta:", delta
			except ZeroDivisionError:
				print "divide by zero"

	#Move on to finding gamma
	def z3(gamma):
		temp=u11*cmath.exp(-1j*delta)*cmath.tan(gamma/2)-u10;                #-U[1,1]/U[0,0];
    		return temp
	for strtp1 in reversed(some_list):
			try:
				ans =  findroot(z3,strtp1)
				gamma = ans.real
				print "gamma:", gamma
			except ZeroDivisionError:
				print "divide by zero"

	#Now compute alpha
	def z4(alpha):
		temp=u11*cmath.exp(-1j*(beta/2+delta/2))*1/(cmath.cos(gamma/2)-cmath.exp(1j*alpha));
		return temp

	for strtp1 in reversed(some_list):
			try:
				ans =  findroot(z4,strtp1)
				alpha = ans
				print "alpha:", alpha
			except ZeroDivisionError:
				print "divide by zero"
			except ValueError:
				print "try another starting point"

	print "alpha, beta, gamma, delta:", [alpha, beta, gamma, delta]
else:
	gamma = 0; #makes the off-diagonal entries equal to 0
	#guess alpha
	for alpha in reversed(some_list):
		print "alpha", alpha

		def z1(beta,delta):
			temp=cmath.exp(1j*(alpha-beta/2-delta/2))-u00;		#-U[1,1]/U[0,0];
			return temp

		def z2(beta,delta):
			temp=cmath.exp(1j*(alpha+beta/2+delta/2))-u11;			#+U[1,0]/U[0,1];
			return temp

		for strtp1 in reversed(some_list):
				for strtp2 in reversed(some_list):
					try:
						ans =  findroot([z1,z2],(strtp1,strtp2))
						beta = ans[0];
						delta = ans[1];
						print "beta:", beta
						print "delta:", delta
						nu00 = cmath.exp(1j*(alpha-beta/2-delta/2))*cmath.cos(gamma/2);
						print "nu00", nu00
					except ZeroDivisionError:
						print "divide by zero"
