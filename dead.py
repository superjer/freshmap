#!/usr/bin/python
from random import randint
from copy import deepcopy

from maketrix  import *
from terrain   import *
from navigable import *
from vmf       import *

XMAIN = 5
YMAIN = 5
DIVPOWER = 4
DIVSIZE = pow(2,DIVPOWER)

matrix = maketrix(
	size = Point(1,XMAIN,YMAIN),
	extranavs = 0,
	blockchance = 0,
	min_multipaths = 0,
	max_multipaths = 0 )

hmap = maketerrain(XMAIN,YMAIN,DIVSIZE)

# write vmf file
vmf = Vmf("mapsrc/nasty.vmf")
vmf.worldspawn()

disp = Displacement(DIVPOWER)
disp.dists = [ randint(0,64) for i in range(disp.nverts*disp.nverts) ]

X = 2048
Y = 2048
Z = 2048

for k in range(matrix.size.z):
	for j in range(matrix.size.y):
		for i in range(matrix.size.x):
			if matrix[k,j,i] == '@': continue
			y_range = range(j*DIVSIZE,(j+1)*DIVSIZE+1)
			x_range = range(i*DIVSIZE,(i+1)*DIVSIZE+1)
			disp.dists = [ hmap[0,y,x] for y in y_range for x in x_range ]
			vmf.block( Block(k*Z,j*Y,i*X,(k+1)*Z,(j+1)*Y,(i+1)*X), "NATURE/BLEND_GRASS_MUD_01", disp )

vmf.end_ent()
vmf.close()

# vim: ts=8 sw=8 noet
