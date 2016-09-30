#!/usr/bin/python
# encoding: utf-8

""" KDTree implementation.

Features:

- nearest neighbours search

Matej Drame [matej.drame@gmail.com]
"""

__version__ = "1r11.1.2010"
__all__ = ["KDTree"]

from skc.utils import *

EPS_0 = 1.0 / 32

def eliminate_close_children(op_list, this_matrix):
	while (op_list):
		child = op_list[0]
		dist = fowler_distance(child.matrix, this_matrix)
		if (dist < EPS_0):
			print "eliminated with dist= " + str(dist)
			del op_list[0]
		else:
			break
	return op_list

def square_distance(pointA, pointB):
	# squared euclidean distance
	distance = 0
	dimensions = len(pointA) # assumes both points have the same dimensions
	for dimension in range(dimensions):
		distance += (pointA[dimension] - pointB[dimension])**2
	return distance

class KDTreeNode():
	def __init__(self, op, left, right):
		self.left = left
		self.right = right
		self.op = op
	
	def is_leaf(self):
		return (self.left == None and self.right == None)

class KDTreeNeighbours():
	""" Internal structure used in nearest-neighbours search.
	"""
	def __init__(self, query_op, t):
		self.query_op = query_op
		self.t = t # neighbours wanted
		self.largest_distance = 0 # squared
		self.current_best = []

	def calculate_largest(self):
		if self.t >= len(self.current_best):
			self.largest_distance = self.current_best[-1][1]
		else:
			self.largest_distance = self.current_best[self.t-1][1]

	def add(self, op):
		sd = fowler_distance(op.matrix, self.query_op.matrix)
		# run through current_best, try to find appropriate place
		for i, e in enumerate(self.current_best):
			if i == self.t:
				return # enough neighbours, this one is farther, let's forget it
			if e[1] > sd:
				self.current_best.insert(i, [op, sd])
				self.calculate_largest()
				return
		# append it to the end otherwise
		self.current_best.append([op, sd])
		self.calculate_largest()
	
	def get_best(self):
		return [element[0] for element in self.current_best[:self.t]]
		
class KDTree():
	""" KDTree implementation.
	
		Example usage:
		
			from kdtree import KDTree
			
			data = <load data> # iterable of points (which are also iterable, same length)
			point = <the point of which neighbours we're looking for>
			
			tree = KDTree.construct_from_data(data)
			nearest = tree.query(point, t=4) # find nearest 4 points
	"""
	
	def __init__(self, data):
		def build_kdtree(op_list, depth):
			# code based on wikipedia article: http://en.wikipedia.org/wiki/Kd-tree
			if not op_list:
				return None

			# select axis based on depth so that axis cycles through all valid values
			axis = depth % len(op_list[0].dimensions) # assumes all points have the same dimension
			#print "axis= " + str(axis)

			# sort point list and choose median as pivot point,
			# TODO: better selection method, linear-time selection, distribution
			op_list.sort(key=lambda point: point.dimensions[axis])
			median = len(op_list)/2 # choose median
			op_this = op_list[median]
			# create node and recursively construct subtrees
			#print "median= " + str(median)
			#print "point[median].dims= " + str(op_list[median].dimensions)
			# Eliminate children that are closer than eps_0
			left_children = op_list[0:median] #eliminate_close_children(op_list[0:median], op_this.matrix)
			right_children = op_list[median+1:] #eliminate_close_children(op_list[median+1:], op_this.matrix)
			node = KDTreeNode(op=op_this,
							  left=build_kdtree(left_children, depth+1),
							  right=build_kdtree(right_children, depth+1)
							  )
			node.axis = axis
			node.dim_val = op_this.dimensions[axis]
			return node
		
		self.root_node = build_kdtree(data, depth=0)
		# Garbage collect the dimensions, since we don't need them anymore
		# although we will if we want to combine trees later
		for op in data:
			del op.dimensions
	
	@staticmethod
	def construct_from_data(data):
		tree = KDTree(data)
		return tree

	def query(self, query_op, t=1):
		statistics = {'nodes_visited': 0, 'far_search': 0, 'leafs_reached': 0}
		
		def nn_search(node, query_op, t, depth, best_neighbours):
			if node == None:
				return
			
			#statistics['nodes_visited'] += 1
			
			# if we have reached a leaf, let's add to current best neighbours,
			# (if it's better than the worst one or if there is not enough neighbours)
			if node.is_leaf():
				#statistics['leafs_reached'] += 1
				best_neighbours.add(node.op)
				return
			
			# this node is no leaf
			
			# select dimension for comparison (based on current depth)
			axis = depth % len(query_op.dimensions)
			
			# figure out which subtree to search
			near_subtree = None # near subtree
			far_subtree = None # far subtree (perhaps we'll have to traverse it as well)
			
			# compare query_point and point of current node in selected dimension
			# and figure out which subtree is farther than the other
			if query_op.dimensions[axis] < node.dim_val:
				near_subtree = node.left
				far_subtree = node.right
			else:
				near_subtree = node.right
				far_subtree = node.left

			# recursively search through the tree until a leaf is found
			nn_search(near_subtree, query_op, t, depth+1, best_neighbours)

			# while unwinding the recursion, check if the current node
			# is closer to query point than the current best,
			# also, until t points have been found, search radius is infinity
			best_neighbours.add(node.op)
			
			# check whether there could be any points on the other side of the
			# splitting plane that are closer to the query point than the current best
			if (node.dim_val - query_op.dimensions[axis])**2 < best_neighbours.largest_distance:
				#statistics['far_search'] += 1
				nn_search(far_subtree, query_op, t, depth+1, best_neighbours)
			
			return
		
		# if there's no tree, there's no neighbors
		if self.root_node != None:
			neighbours = KDTreeNeighbours(query_op, t)
			nn_search(self.root_node, query_op, t, depth=0, best_neighbours=neighbours)
			result = neighbours.get_best()
		else:
			result = []
		
		#print statistics
		return result
