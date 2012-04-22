from random import randint
from random import shuffle
from copy import deepcopy

class Point:
	def __init__(self, z, y, x):
		self.z = z
		self.y = y
		self.x = x

EMPTY = '.'
SOLID = '@'
NAV   = '*'

# m       matrix
# z,y,x   position
# found   number of navigable positions found so far
# goal    number of navigable positions we're looking for
def navigable_inner(m,z,y,x,found,goal):
	if m[z][y][x] == SOLID:
		return False
	if m[z][y][x] == NAV:
		found += 1
		if found == goal:
			return True
	m[z][y][x] = SOLID # do not traverse here again

	if z > 0              and navigable_inner(m,z-1,y  ,x  ,found,goal): return True
	if z < len(m)      -1 and navigable_inner(m,z+1,y  ,x  ,found,goal): return True
	if y > 0              and navigable_inner(m,z  ,y-1,x  ,found,goal): return True
	if y < len(m[0])   -1 and navigable_inner(m,z  ,y+1,x  ,found,goal): return True
	if x > 0              and navigable_inner(m,z  ,y  ,x-1,found,goal): return True
	if x < len(m[0][0])-1 and navigable_inner(m,z  ,y  ,x+1,found,goal): return True
	return False


# can every EMPTY in the matrix be reached from every other?
def navigable(matrix,navs):
	# make a copy to trample
	m = deepcopy(matrix)
	ret = navigable_inner( m, navs[0].z, navs[0].y, navs[0].x, 0, len(navs) )
	if False:
		for k in matrix:
			for j in k:
				print " ".join(j)
			print ""
	return ret

# matrix size
size = Point(1,8,8)

# make a matrix
# positions are either EMPTY empty, NAV navpoint, or SOLID solid
# every nav position must be reachable from every other without having to cross any solids
matrix = [[[EMPTY for i in range(size.x)] for j in range(size.y)] for k in range(size.z)]

# list of navpoints
navs = []

# pick random positions in the matrix to make navpoint
for i in range(randint(2,8)):
	z = randint(0,size.z-1)
	y = randint(0,size.y-1)
	x = randint(0,size.x-1)
	if matrix[z][y][x] == EMPTY:
		matrix[z][y][x] = NAV
		navs.append( Point(z,y,x) )

# get shuffled list of fillable positions
fillable = []
for k in range(size.z):
	for j in range(size.y):
		for i in range(size.x):
			fillable.append(Point(k,j,i))
shuffle(fillable)

# fill as much as possible with solids
for p in fillable:
	z,y,x = p.z,p.y,p.x
	if not matrix[z][y][x] == EMPTY: continue
	matrix[z][y][x] = SOLID
	if not navigable(matrix,navs): matrix[z][y][x] = EMPTY

# view it!
for k in matrix:
	for j in k:
		print " ".join(j)
	print ""


# vim: ts=8 sw=8 noet
