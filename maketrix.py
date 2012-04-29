from random import randint

from navigable import *

def maketrix( size, extranavs=0, blockchance=0, min_multipaths=0, max_multipaths=0 ):
	# make a matrix
	# positions are either EMPTY empty, NAV navpoint, or SOLID solid
	# every nav position must be reachable from every other without having to cross any solids
	empty = Matrix(size.z,size.y,size.x)
	matrix = deepcopy(empty)

	# list of navpoints
	navs = []

	# pick random positions in the matrix to make navpoint
	for i in range(randint(2,2+extranavs)):
		z = randint(0,matrix.size.z-1)
		y = randint(0,matrix.size.y-1)
		x = randint(0,matrix.size.x-1)

		#first 2 points should cross the square
		if i==0: y = 0
		if i==1: y = matrix.size.y-1

		if matrix[z,y,x].c == EMPTY:
			matrix[z,y,x].c = NAV
			navs.append( Point(z,y,x) )

	# make a block of navpoints somewhere
	if randint(0,100)<blockchance and matrix.size.y>5 and matrix.size.x>5:
		y = randint(0,matrix.size.y-5)
		x = randint(0,matrix.size.x-5)
		w = randint(2,5)
		h = randint(2,5)
		for j in range(x,x+w):
			for i in range(y,y+h):
				if matrix[0,j,i].c == EMPTY:
					matrix[0,j,i].c = NAV
					navs.append( Point(0,j,i) )

	matrix.fill(navs)
	print 'Original matrix:'
	print matrix

	for i in range(randint(min_multipaths,max_multipaths)):
		addtl = deepcopy(empty)
		addtl[navs[0].z,navs[0].y,navs[0].x] = NAV
		addtl[navs[1].z,navs[1].y,navs[1].x] = NAV
		addtl.fill(navs[:2])
		print 'Addtl matrix:'
		print addtl
		matrix.merge(addtl)

	# view it after merge
	print 'Final matrix:'
	print matrix

	matrix.navs = navs
	return matrix

# vim: ts=8 sw=8 noet
