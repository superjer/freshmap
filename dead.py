#!/usr/bin/python
from random import randint
from numpy import *

from navigable import *
from vmf import *

# make a matrix
# positions are either EMPTY empty, NAV navpoint, or SOLID solid
# every nav position must be reachable from every other without having to cross any solids
matrix = Matrix(1,20,20)
matrix2 = Matrix(1,20,20)

# list of navpoints
navs = []

# pick random positions in the matrix to make navpoint
for i in range(randint(2,8)):
	z = randint(0,matrix.size.z-1)
	y = randint(0,matrix.size.y-1)
	x = randint(0,matrix.size.x-1)
	if matrix[[z,y,x]] == EMPTY:
		matrix[[z,y,x]] = NAV
		navs.append( Point(z,y,x) )

# make a block of navpoints somewhere
if matrix.size.y>5 and matrix.size.x>5:
	y = randint(0,matrix.size.y-5)
	x = randint(0,matrix.size.x-5)
	w = randint(2,5)
	h = randint(2,5)
	for j in range(x,x+w):
		for i in range(y,y+h):
			if matrix[[0,j,i]] == EMPTY:
				matrix[[0,j,i]] = NAV
				navs.append( Point(0,j,i) )

matrix.fill(navs)

matrix2[[navs[0].z,navs[0].y,navs[0].x]] = NAV
matrix2[[navs[1].z,navs[1].y,navs[1].x]] = NAV
matrix2.fill(navs[:2])

# view pre-merge
print matrix
print matrix2

matrix.merge(matrix2)

# view it after merge
print matrix

# write vmf file
vmf = Vmf("nasty.vmf")
vmf.worldspawn()

X = 64
Y = 64
Z = 64

for k in range(matrix.size.z):
	for j in range(matrix.size.y):
		for i in range(matrix.size.x):
			if matrix[[k,j,i]] == '@': continue
			vmf.block(Block(k*Z,j*Y,i*X,(k+1)*Z,(j+1)*Y,(i+1)*X))

vmf.end_ent()
vmf.close()

# vim: ts=8 sw=8 noet
