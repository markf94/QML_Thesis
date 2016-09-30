from skc_utils import *
from skc_basic_approx import *

# The leaves of recursive subtiling have at most 3 points in them
TILE_COUNT = 150
MAX_INSERT_DEPTH = 475

class Tile_SU2:

	# pivot is a tuple of psi, theta, and phi
	def __init__(self, psi, theta, phi, width):
		self.psi = psi
		self.theta = theta
		self.phi = phi
		self.width = width
		self.points = []
		self.count = 0
		
	# Returns True if this tile has split, False otherwise
	def is_split(self):
		# Boolean which is True if subtiles exist and False otherwise
		subtiles_exist = ('subtiles' in dir(self))
		# Boolean which is True if points is <= TILE_COUNT and False otherwise
		points_less = (len(self.points) <= TILE_COUNT)
		return (subtiles_exist)
		
	# Set a function to be called from this tile when it splits into subtiles
	def set_split_hook(self, split_hook):
		self.split_hook = split_hook
		
	# Don't call this indiscriminately, or we'll have infinite recursion
	def subtile(self):
		if ('split_hook' in dir(self)):
			self.split_hook()
			
		psi1_subpivot = self.psi - (self.width/4)
		psi2_subpivot = self.psi + (self.width/4)
		theta1_subpivot = self.theta - (self.width/4)
		theta2_subpivot = self.theta + (self.width/4)
		# Tiles are wider in the phi direction b/c of asymmetry in hyperspherical coords
		phi1_subpivot = self.phi - (self.width/2)
		phi2_subpivot = self.phi + (self.width/2)
		subwidth = self.width/2.0
		self.subtiles = {};
		subtile111 = Tile_SU2(psi1_subpivot, theta1_subpivot, phi1_subpivot, subwidth)
		self.subtiles[(1,1,1)] = subtile111
		subtile112 = Tile_SU2(psi1_subpivot, theta1_subpivot, phi2_subpivot, subwidth)
		self.subtiles[(1,1,2)] = subtile112
		subtile121 = Tile_SU2(psi1_subpivot, theta2_subpivot, phi1_subpivot, subwidth)
		self.subtiles[(1,2,1)] = subtile121
		subtile122 = Tile_SU2(psi1_subpivot, theta2_subpivot, phi2_subpivot, subwidth)
		self.subtiles[(1,2,2)] = subtile122
		subtile211 = Tile_SU2(psi2_subpivot, theta1_subpivot, phi1_subpivot, subwidth)
		self.subtiles[(2,1,1)] = subtile211
		subtile212 = Tile_SU2(psi2_subpivot, theta1_subpivot, phi2_subpivot, subwidth)
		self.subtiles[(2,1,2)] = subtile212
		subtile221 = Tile_SU2(psi2_subpivot, theta2_subpivot, phi1_subpivot, subwidth)
		self.subtiles[(2,2,1)] = subtile221
		subtile222 = Tile_SU2(psi2_subpivot, theta2_subpivot, phi2_subpivot, subwidth)
		self.subtiles[(2,2,2)] = subtile222

	def find_closest_point(self, operator, distance):
		if (not self.is_split()):
			# Not split yet, just do a linear search from skc_basic_approx
			return find_basic_approx(self.points, operator, distance)
		else:
			indices = self.get_hspherical_indices(operator)
			subtile = self.subtiles[indices]
			assert(subtile != None)
			return subtile.find_closest_point(operator, distance)

	def get_hspherical_indices(self, operator):
		matrix = operator.matrix
		unitary = matrix_to_unitary4d(matrix)
		[psi, theta, phi] = unitary_to_hspherical(unitary)

		# Decide on psi pivot
		if (psi <= self.psi):
			psi_index = 1
		else:
			psi_index = 2
		
		# Decide on theta pivot
		if (theta <= self.theta):
			theta_index = 1
		else:
			theta_index = 2
			
		# Decide on phi pivot
		if (phi <= self.phi):
			phi_index = 1
		else:
			phi_index = 2
		return (psi_index, theta_index, phi_index)

	def insert_into_subtiles(self, operator, depth):
		(psi_index, theta_index, phi_index) = self.get_hspherical_indices(operator)
			
		subtile = self.subtiles[(psi_index, theta_index, phi_index)]
		assert(subtile != None)
		subtile.insert_helper(operator, depth)
		
	def insert(self, operator):
		self.insert_helper(operator, MAX_INSERT_DEPTH)
	
	def insert_helper(self, operator, depth):
	
		if (depth <= 0):
			print "********************************************"
			self.print_string(0)
			raise RuntimeError("Exceeded maximum insert depth here")
			
		# We always keep a cumulative count of this tile and all subtiles recursively here
		self.count += 1
		
		if (self.count < TILE_COUNT):
			# We are still a tile of constant size, even with one more addition
			#assert(len(self.points) < TILE_COUNT)
			self.points.append(operator)
			return
		elif (not self.is_split()):
			# Else if have not split yet, we need to subtile!
			# But don't forget to insert this new operator
			self.points.append(operator)
			self.subtile()
			#self.print_string(0)
			assert(self.is_split())
		
			#print str(self.points)
			for point in self.points:
				self.insert_into_subtiles(point, depth-1)
		
			# Clear self.points, since these have now been distributed among our subtiles
			self.points = []
		else:
			# Otherwise, delegate this new
			self.insert_into_subtiles(operator, depth-1)

	def print_string(self, depth):
		parent = "Tile (psi,theta,phi) = ("+str(self.psi)+","+str(self.theta)+","+ \
		                                 str(self.phi)+"), has " + \
		                                 str(self.count) + " points"
		print_indented(parent, depth)
		
		if (self.is_split()):
			self.print_subtiles(depth+1)
		else:
			points_string = "  Unsplit. Points are = "
			for point in self.points:
				points_string += str(point)
			print_indented(points_string, depth)
	
	def print_subtiles(self, depth):
		for index, subtile in self.subtiles.items():
			subtile.print_string(depth)