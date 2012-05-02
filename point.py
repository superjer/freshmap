import math

class Point:
	def __init__(self, z, y, x):
		self.z = z
		self.y = y
		self.x = x

def magnitude(p):
	return math.sqrt( p.x*p.x + p.y*p.y + p.z*p.z )

def normalize(p,mag=None):
	if not mag: mag = magnitude(p)
	p.x /= mag
	p.y /= mag
	p.z /= mag

def dotproduct(a,b):
	return a.x*b.x + a.y*b.y + a.z*b.z

# vim: ts=8 sw=8 noet
