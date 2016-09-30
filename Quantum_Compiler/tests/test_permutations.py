import scipy

# The combinatorics function n choose k
def n_choose_k(n, k):
	n_fact = scipy.factorial(n)
	k_fact = scipy.factorial(k)
	n_minus_k_fact = scipy.factorial(n-k)
	return n_fact / (k_fact * n_minus_k_fact)

def swap(array, i, j):
	temp = array[i]
	array[i] = array[j]
	array[j] = temp
	
# Return a list of tuples of all distinct pairs in the set {1,2,...,n}
def generate_all_pairs(n):
	pairs = []
	for i in range(1,n+1):
		for j in range(i+1,n+1):
			pairs.append((i,j))
	# As a sanity check, make sure we have all the pairs we were expecting
	pair_count = n_choose_k(n,2)
	assert(len(pairs) == pair_count)
	return pairs

def generate_permutations(i):
	original = range(1,i+1)

print "pairs(3)= " + str(generate_all_pairs(3))
print "pairs(4)= " + str(generate_all_pairs(4))
print "pairs(16)= " + str(generate_all_pairs(16))

