import math

class Point:
	def __init__(self, z, y, x):
		self.z = z
		self.y = y
		self.x = x

	def __str__(self):
		return "Point( %f, %f, %f )" % (self.z,self.y,self.x)

	def __add__(self, other):
		return Point(self.z+other.z, self.y+other.y, self.x+other.x)

	def __sub__(self, other):
		return Point(self.z-other.z, self.y-other.y, self.x-other.x)
	
	def __mul__(self, scalar):
		scalar = float(scalar)
		return Point(self.z*scalar, self.y*scalar, self.x*scalar)

	def __rmul__(self, scalar):
		scalar = float(scalar)
		return Point(self.z*scalar, self.y*scalar, self.x*scalar)

def magnitude(p):
	return math.sqrt( p.x*p.x + p.y*p.y + p.z*p.z )

def normalize(p,mag=None):
	if not mag: mag = magnitude(p)
	p.x /= mag
	p.y /= mag
	p.z /= mag

def dotproduct(a,b):
	return a.x*b.x + a.y*b.y + a.z*b.z

def crossproduct(a,b):
	return Point( a.x*b.y - a.y*b.x, a.z*b.x - a.x*b.z, a.y*b.z - a.z*b.y )

# vim: ts=8 sw=8 noet
