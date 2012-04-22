#!/usr/bin/python
from random import randint
from random import shuffle

from navigable import *
from vmf import *

# matrix size
size = Point(7,14,14)

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

# make a block of navpoints somewhere
if size.y>5 and size.x>5:
	y = randint(0,size.y-5)
	x = randint(0,size.x-5)
	w = randint(2,5)
	h = randint(2,5)
	for j in range(x,x+w):
		for i in range(y,y+h):
			if matrix[0][j][i] == EMPTY:
				matrix[0][j][i] = NAV
				navs.append( Point(0,j,i) )

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

# write vmf file
vmf = Vmf("nasty.vmf")
vmf.worldspawn()

X = 64
Y = 64
Z = 64

for k in range(size.z):
	for j in range(size.y):
		for i in range(size.x):
			if matrix[k][j][i] == '@': continue
			vmf.block(Block(k*Z,j*Y,i*X,(k+1)*Z,(j+1)*Y,(i+1)*X))

vmf.end_ent()
vmf.close()

# vim: ts=8 sw=8 noet
