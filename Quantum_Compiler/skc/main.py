from skc.basic_approx import *
from skc.operator import *

import cPickle
import time

f = open('basic_approxes.pickle', 'rb')

begin_time = time.time()

iset = cPickle.load(f)

iset_time = time.time() - begin_time
print "Loaded instruction set in: " + str(iset_time)
print "Iset = " + str(iset)

begin_time = time.time()

basic_approxes = cPickle.load(f)
#basic_approxes = [I2]

approx_time = time.time() - begin_time

print "Loaded basic approximations in: " + str(approx_time)
print "Number of BA: " + str(len(basic_approxes))

def solovay_kitaev(U, n):
	if (n == 0):
		basic_approx, min_dist = find_basic_approx(basic_approxes, U)
		# discard min_dist for now. but just you wait...
		print "Returning basic approx: " + str(basic_approx)
		return basic_approx
	else:
		print "Beginning level " + str(n)
		U_n1 = solovay_kitaev(U, n-1) # U_{n-1}
		print "U_"+str(n-1)+": " + str(U_n1)
		U_n1_dagger = U_n1.dagger()
		V,W = bgc_decompose(U.multiply(U_n1_dagger))
		print "V: " + str(V)
		print "W: " + str(W)
		V_n1 = solovay_kitaev(V, n-1) # V_{n-1}
		print "V_"+str(n-1)+": " + str(V_n1)
		V_n1_dagger = V_n1.dagger()
		W_n1 = solovay_kitaev(W, n-1) # W_{n-1}
		print "W_"+str(n-1)+": " + str(W_n1)
		W_n1_dagger = W_n1.dagger()
		V_n1_dagger_W_n1_dagger = V_n1_dagger.multiply(W_n1_dagger)
		V_n1_W_n1 = V_n1.multiply(W_n1)
		delta = V_n1_W_n1.multiply(V_n1_dagger_W_n1_dagger)
		U_n = delta.multiply(U_n1)
		print "delta_"+str(n)+": " + str(U_n)
		print "Ending level " + str(n)
		return U_n
