#!/usr/bin/python
import random
from random import randint
from copy import deepcopy
from itertools import product

from point     import *
from maketrix  import *
from terrain   import *
from navigable import *
from vmf       import *

random.seed(6)

XMAIN = randint(4,6)
YMAIN = 10-XMAIN
XMAIN,YMAIN = 3,3
DIVPOWER = 3
DIVSIZE = 2**DIVPOWER

matrix = maketrix(
	size = Point(1,XMAIN,YMAIN),
	extranavs = 0,
	blockchance = 0,
	min_multipaths = 0,
	max_multipaths = 0 )

# find neighbors, create connections
for k,j,i in product(range(matrix.size.z),range(matrix.size.y),range(matrix.size.x)):
	if matrix[k,j,i].c == SOLID: continue
	matrix[k,j,i].sub = maketrix(
		size = Point(1,DIVSIZE,DIVSIZE),
		extranavs = randint(0,3),
		blockchance = 10,
		min_multipaths = 0,
		max_multipaths = 5,
		parent = matrix,
		pspot = Point(k,j,i) )

hmap = maketerrain(XMAIN,YMAIN,DIVSIZE*16)

# write vmf file
vmf = Vmf("mapsrc/nasty.vmf")
vmf.worldspawn()

disp = Displacement(DIVPOWER)
disp.dists = [ randint(0,64) for i in range(disp.nverts*disp.nverts) ]

X = 512
Y = 512
Z = 128
CEN = DIVSIZE*max(XMAIN,YMAIN)/2

# make a list of squares to export
class Square:
	def __init__(self,z,y,x):
		self.z = z
		self.y = y
		self.x = x
		self.is_start = False
		self.is_end = False

squares = []

for k,j,i in product(range(matrix.size.z),range(matrix.size.y),range(matrix.size.x)):
	if matrix[k,j,i].c == '@': continue
	sub = matrix[k,j,i].sub
	for w,v,u in product(range(sub.size.z),range(sub.size.y),range(sub.size.x)):
	        if sub[w,v,u].c == '@': continue
		square = Square(k*DIVSIZE+w, j*DIVSIZE+v, i*DIVSIZE+u)
		if (w,v,u) == sub.start: square.is_start = True
		if (w,v,u) == sub.end  : square.is_end   = True
		squares.append(square)

def alphaval(n):
	return str(randint(128,255)) if n<24 else "0"

startblock = None
endblock = None

for square in squares:
	k,j,i = square.z,square.y,square.x
	yx_range = [ (y,x) for y,x in product(range(j*DIVSIZE,(j+1)*DIVSIZE+1), range(i*DIVSIZE,(i+1)*DIVSIZE+1)) ]
	disp.dists = [ hmap[0,y,x] for y,x in yx_range ]
	disp.alphas = [ alphaval(hmap[0,y,x]) for y,x in yx_range ]
	b = Block( k*Z, (j-CEN)*Y, (i-CEN)*X, (k+1)*Z, (j+1-CEN)*Y, (i+1-CEN)*X )
	if square.is_start:
		startblock = deepcopy(b)
	if square.is_end:
		endblock = deepcopy(b)
	vmf.block( b, "NATURE/BLEND_GRASS_MUD_01", disp )
	vmf.block( b, "TOOLS/TOOLSNODRAW" )
	b.z0 = (k+10)*Z
	b.z1 = (k+11)*Z
	vmf.block( b, "TOOLS/TOOLSSKYBOX" )
	if min(disp.dists) < 24:
		b.z0 = 128
		b.z1 = 148
		vmf.block( b, "LIQUIDS/WATER_SWAMP_M1" )

z = startblock.z0 + Z*2
y = startblock.y0 + 64
x = startblock.x0 + 64

# output a card
card_quad = [
	Point( z     , y+ 64, x+ 64 ),
	Point( z     , y+564, x+200 ),
	Point( z+1000, y+564, x+200 ),
	Point( z+1000, y+ 64, x+ 64 ),
]
vmf.pyramid( card_quad, 20, "NATURE/SWAMP_TREES_CARD01", "TOOLS/TOOLSNODRAW" )

# end worldspawn
vmf.end_ent()

vmf.fog_controller        (z   ,y    ,x    )
vmf.light_environment     (z-16,y    ,x    )
vmf.info_survivor_position(z-64,y    ,x    )
vmf.info_survivor_position(z-64,y+128,x    )
vmf.info_survivor_position(z-64,y    ,x+128)
vmf.info_survivor_position(z-64,y+128,x+128)
vmf.info_player_start     (z-64,y+64 ,x+64 )

vmf.close()

# vim: ts=8 sw=8 noet
