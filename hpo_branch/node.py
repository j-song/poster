import random
import numpy as np
import numpy.random

class Node:
	def __init__(self):
		self.parents = []
		self.children = []
		self.proper_children = []
		self.patients = set([])

	def get_ancestors(self):
		if  hasattr(self, 'ancestors'):
			return self.ancestors
		else:
			ancestors = set([self])
			for p in self.parents:
				ancestors = ancestors.union(p.get_ancestors())
			self.ancestors = ancestors
			return self.ancestors
		
	def get_descendants(self):
		if hasattr(self, 'descendants'):
			return self.descendants
		else:
			descendants = set([self])
			for c in self.children:
				descendants = descendants.union(c.get_descendants())
			self.descendants = descendants
			return self.descendants
	
	def clean(self):
		self.parents = list(set(self.parents))
		self.children = list(set(self.children))
		self.proper_children = list(set(self.proper_children))

	def map(self, f):
		f(self)
		for child in self.children:
			child.map(f)
	
	def set_proper_children(self):
		if len(self.parents) > 0 and self not in self.parents[0].proper_children:
			self.parents[0].proper_children.append(self)
	
	def add_child(self, child):
		self.children.append(child)
		if child is not None:
			child.parents.append(self)
	
	def __iter__(self):
		return next(self)

	def next(self):
		yield self
		for child in self.proper_children:
			for node in child:
				yield node
class Term(Node):
	def __init__(self):
		Node.__init__(self)
		self.dir_freq = 0
		self.raw_freq = 0
		self.freq = 0

	def show(self, n=0):
		print "  "*n + self.name
		for child in self.children:
			child.show(n+1)		
