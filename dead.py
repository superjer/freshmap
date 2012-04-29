#!/usr/bin/python
from random import randint
from copy import deepcopy
from itertools import product

from maketrix  import *
from terrain   import *
from navigable import *
from vmf       import *

XMAIN = randint(4,8)
YMAIN = 12-XMAIN
DIVPOWER = 4
DIVSIZE = pow(2,DIVPOWER)

matrix = maketrix(
	size = Point(1,XMAIN,YMAIN),
	extranavs = 0,
	blockchance = 0,
	min_multipaths = 0,
	max_multipaths = 0 )

# find neighbors, create connections
for k,j,i in product(range(matrix.size.z),range(matrix.size.y),range(matrix.size.x)):
	1

hmap = maketerrain(XMAIN,YMAIN,DIVSIZE)

# write vmf file
vmf = Vmf("mapsrc/nasty.vmf")
vmf.worldspawn()

disp = Displacement(DIVPOWER)
disp.dists = [ randint(0,64) for i in range(disp.nverts*disp.nverts) ]

X = 2048
Y = 2048
Z = 128

def alphaval(n):
	return str(randint(128,255)) if n<24 else "0"

for k,j,i in product(range(matrix.size.z),range(matrix.size.y),range(matrix.size.x)):
	if matrix[k,j,i].c == '@': continue
	yx_range = [ (y,x) for y,x in product(range(j*DIVSIZE,(j+1)*DIVSIZE+1), range(i*DIVSIZE,(i+1)*DIVSIZE+1)) ]
	disp.dists = [ hmap[0,y,x] for y,x in yx_range ]
	disp.alphas = [ alphaval(hmap[0,y,x]) for y,x in yx_range ]
	b = Block(k*Z,j*Y,i*X,(k+1)*Z,(j+1)*Y,(i+1)*X)
	vmf.block( b, "NATURE/BLEND_GRASS_MUD_01", disp )
	vmf.block( b, "TOOLS/TOOLSNODRAW" )
	b.z0 = (k+10)*Z
	b.z1 = (k+11)*Z
	vmf.block( b, "TOOLS/TOOLSSKYBOX" )
	if min(disp.dists) < 24:
		b.z0 = 128
		b.z1 = 148
		vmf.block( b, "LIQUIDS/WATER_SWAMP_M1" )

vmf.end_ent()

start = matrix.navs[0]
z,y,x = (start.z+9)*Z, start.y*Y+64, start.x*X+64

vmf.fog_controller        (z   ,y    ,x    )
vmf.light_environment     (z-16,y    ,x    )
vmf.info_survivor_position(z-64,y    ,x    )
vmf.info_survivor_position(z-64,y+128,x    )
vmf.info_survivor_position(z-64,y    ,x+128)
vmf.info_survivor_position(z-64,y+128,x+128)
vmf.info_player_start     (z-64,y+64 ,x+64 )

vmf.close()

# vim: ts=8 sw=8 noet
