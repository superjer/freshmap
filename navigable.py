from copy import deepcopy

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

EMPTY = '.'
SOLID = '@'
NAV   = '*'

# can every navpoint in the matrix be reached from every other?
def navigable(matrix,navs):
	# make a copy to trample
	m = deepcopy(matrix)

	found = 0
	todo = [navs[0]]

	while len(todo):
		p = todo.pop()
		z,y,x = p.z,p.y,p.x
		if m[z][y][x] == SOLID:
			continue
		if m[z][y][x] == NAV:
			found += 1
			if found == len(navs):
				return True
		m[z][y][x] = SOLID # do not traverse here again

		if z > 0             : todo.append(Point(z-1,y  ,x  ))
		if z < len(m)      -1: todo.append(Point(z+1,y  ,x  ))
		if y > 0             : todo.append(Point(z  ,y-1,x  ))
		if y < len(m[0])   -1: todo.append(Point(z  ,y+1,x  ))
		if x > 0             : todo.append(Point(z  ,y  ,x-1))
		if x < len(m[0][0])-1: todo.append(Point(z  ,y  ,x+1))
	return False

