from copy import deepcopy
from random import shuffle

EMPTY = '.'
SOLID = '@'
NAV   = '*'

class Point:
	def __init__(self, z, y, x):
		self.z = z
		self.y = y
		self.x = x

class Block:
	def __init__(self, z0, y0, x0, z1, y1, x1):
		self.z0 = z0
		self.y0 = y0
		self.x0 = x0
		self.z1 = z1
		self.y1 = y1
		self.x1 = x1

class Matrix:
	def __init__(self, zsize, ysize, xsize):
		self.size = Point(zsize,ysize,xsize)
		self.length = zsize*ysize*xsize
		self.m = self.length * [EMPTY]

	def __iter__(self):
		for i in self.m:
			yield i

	def __str__(self):
		s = [ val + (' ' if ((i+1) % self.size.x) else '\n') for (i,val) in enumerate(self.m) ]
		return "".join(s)

	def __getitem__(self, key):
		return self.m[ self.offset(key) ]

	def __setitem__(self, key, value):
		self.m[ self.offset(key) ] = value

	def offset(self, key):
		if key[0] < 0 or key[0] >= self.size.z or key[1] < 0 or key[1] >= self.size.y or key[2] < 0 or key[2] >= self.size.x:
			raise IndexError()
		return key[0]*self.size.x*self.size.y + key[1]*self.size.x + key[2]

	# can every navpoint in the matrix be reached from every other?
	def navigable(self, navs):
		# make a copy to trample
		m = deepcopy(self.m)

		found = 0
		todo = [navs[0]]

		while len(todo):
			p = todo.pop()
			z,y,x = p.z,p.y,p.x
			if m[ self.offset((z,y,x)) ] == SOLID:
				continue
			if m[ self.offset((z,y,x)) ] == NAV:
				found += 1
				if found == len(navs):
					return True
			m[ self.offset((z,y,x)) ] = SOLID # do not traverse here again

			if z > 0            : todo.append(Point(z-1,y  ,x  ))
			if z < self.size.z-1: todo.append(Point(z+1,y  ,x  ))
			if y > 0            : todo.append(Point(z  ,y-1,x  ))
			if y < self.size.y-1: todo.append(Point(z  ,y+1,x  ))
			if x > 0            : todo.append(Point(z  ,y  ,x-1))
			if x < self.size.x-1: todo.append(Point(z  ,y  ,x+1))
		return False

	def fill(self, navs):
		# get shuffled list of fillable positions
		fillable = [ Point(k,j,i) for k in range(self.size.z) for j in range(self.size.y) for i in range(self.size.x) ]
		shuffle(fillable)

		# fill as much as possible with solids
		for p in fillable:
			z,y,x = p.z,p.y,p.x
			if not self[z,y,x] == EMPTY: continue
			self[z,y,x] = SOLID
			if not self.navigable(navs): self[z,y,x] = EMPTY

	# anywhere that other is empty, make ourself empty as well
	# this effectively merges open paths
	def merge(self, other):
		self.m[:] = [ EMPTY if other.m[i] == EMPTY else self.m[i] for i in range(self.length) ]


# vim: ts=8 sw=8 noet
