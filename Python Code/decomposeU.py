#from scipy.optimize import root
from mpmath import findroot
import cmath
import math
import numpy as np
from itertools import product

#Hadamard matrix elements
u00 = 0.70711;
u01 = 0.70711; #top right
u10 = 0.70711; #top left
u11 = -0.70711;

## STILL DOESN'T COPE WITH ZERO ENTRIES IN THE U MATRIX!
# S phase shift matrix elements
#u00 = 1.0;
#u01 = 0.0; #top right
#u10 = 0.0; #top left
#u11 = -1.0;

#INITIALIZE SOME VARIABLES
some_list = [math.pi/4, math.pi/2, 3/4*math.pi, math.pi, 0, -math.pi*1.5, -math.pi, -3/4*math.pi, -math.pi/2, -math.pi/4, 1.5*math.pi];
alpha = 10;
beta = 10;
delta = 10;
gamma = 10;

if u10 != 0.0 and u01 != 0.0:

	#First find beta & delta
	def z1(beta,delta):
		temp=cmath.exp(1j*(beta+delta))-u11/u00;
		return temp

	def z2(beta,delta):
		temp=cmath.exp(1j*(beta-delta))+u10/u01;
		return temp

	#for strtp1 in reversed(some_list):
		#for strtp2 in reversed(some_list):

	for strtp1, strtp2 in product(reversed(some_list), reversed(some_list)):
			try:
				ans =  findroot([z1,z2],(strtp1,strtp2));
				beta_save = ans[0].real;
				delta_save = ans[1].real;
				if abs(beta_save) < abs(beta) and abs(delta_save) < abs(delta):
					beta = beta_save;
					delta = delta_save;
					print "beta:", beta
					print "delta:", delta
					break
			except ZeroDivisionError:
				print "divide by zero"

	#Move on to finding gamma
	def z3(alpha,gamma):
		temp=u11*cmath.exp(-1j*alpha)*cmath.exp(1j*(-beta/2-delta/2))-cmath.cos(gamma/2);
    		return temp
	def z4(alpha,gamma):
		temp=u10*cmath.exp(-1j*alpha)*cmath.exp(1j*(-beta/2+delta/2))-cmath.sin(gamma/2);
    		return temp

	for strtp1, strtp2 in product(reversed(some_list), reversed(some_list)):
			try:
				ans =  findroot([z3,z4],(strtp1,strtp2));
				alpha_save = ans[0].real;
				gamma_save = ans[1].real;
				if abs(alpha_save) < abs(alpha) and abs(gamma_save) < abs(gamma):
					alpha = alpha_save;
					gamma = gamma_save;
					break
			except ZeroDivisionError:
				print "divide by zero"
			except OverflowError:
				print "overflow"
	'''
	def z3(gamma):
		temp=u11*cmath.exp(-1j*delta)*cmath.tan(gamma/2)-u10;                #-U[1,1]/U[0,0];
    		return temp

	for strtp1 in reversed(some_list):
			try:
				ans =  findroot(z3,strtp1);
				gamma_save = ans.real;
				if abs(gamma_save) < abs(gamma):
					gamma = gamma_save;
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
				alpha_save = ans
				print "alpha_save:", alpha_save
				if abs(alpha_save) < abs(alpha):
					alpha = alpha_save;
					print "alpha:", alpha
			except ZeroDivisionError:
				print "divide by zero"
			except ValueError:
				print "try another starting point"
	'''
	print "alpha, beta, gamma, delta:", alpha, beta, gamma, delta
	nu00 = cmath.exp(1j*(alpha-beta/2-delta/2))*cmath.cos(gamma/2)
	print "nu00", nu00
	nu01 = -cmath.exp(1j*(alpha-beta/2+delta/2))*cmath.sin(gamma/2)
	print "nu01", nu01
	nu10 = cmath.exp(1j*(alpha+beta/2-delta/2))*cmath.sin(gamma/2)
	print "nu10", nu10
	nu11 = cmath.exp(1j*(alpha+beta/2+delta/2))*cmath.cos(gamma/2)
	print "nu11", nu11
else:
	print "Calculate it by hand!"
	'''
	#set gamma=0
	gamma = 0;

	#First find beta & delta
	def z1(beta,delta):
		temp=cmath.exp(1j*(beta+delta))-u11/u00;
		return temp

	def z2(beta,delta):
		temp=cmath.exp(1j*(beta-delta)); #+u10/u01; (zero anyway)
		return temp

	#for strtp1 in reversed(some_list):
		#for strtp2 in reversed(some_list):

	for strtp1, strtp2 in product(reversed(some_list), reversed(some_list)):
			try:
				print "strtp1", strtp1
				print "strtp2", strtp2
				ans =  findroot([z1,z2],(strtp1,strtp2));
				beta_save = ans[0].real;
				delta_save = ans[1].real;
				if abs(beta_save) < abs(beta) and abs(delta_save) < abs(delta):
					beta = beta_save;
					delta = delta_save;
					print "beta:", beta
					print "delta:", delta
					break
			except ZeroDivisionError:
				print "divide by zero"
			except ValueError:
				print "value error"

	#Move on to finding gamma
	def z3(alpha):
		temp=u11*cmath.exp(-1j*alpha)*cmath.exp(1j*(-beta/2-delta/2))-cmath.cos(gamma/2);
    		return temp
	def z4(alpha):
		temp=u10*cmath.exp(-1j*alpha)*cmath.exp(1j*(-beta/2+delta/2))-cmath.sin(gamma/2);
    		return temp

	for strtp1 in reversed(some_list):
			try:
				ans =  findroot([z3,z4],strtp1);
				alpha_save = ans.real;
				if abs(alpha_save) < abs(alpha):
					alpha = alpha_save;
					break
			except ZeroDivisionError:
				print "divide by zero"
			except OverflowError:
				print "overflow"
	'''
