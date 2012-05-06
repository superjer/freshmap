#!/usr/bin/python
from random import *
from copy import deepcopy
from itertools import product

from point     import *
from maketrix  import *
from terrain   import *
from navigable import *
from vmf       import *

seed(6)

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

maxcorn = Point(   0,   0,   0)
squares = []

for k,j,i in product(range(matrix.size.z),range(matrix.size.y),range(matrix.size.x)):
	if matrix[k,j,i].c == '@': continue
	sub = matrix[k,j,i].sub
	for w,v,u in product(range(sub.size.z),range(sub.size.y),range(sub.size.x)):
		if sub[w,v,u].c == '@': continue
		square = Square(k*DIVSIZE+w, j*DIVSIZE+v, i*DIVSIZE+u)
		if (w,v,u) == sub.start: square.is_start = True
		if (w,v,u) == sub.end  : square.is_end   = True
		maxcorn.z = max(maxcorn.z,square.z)
		maxcorn.y = max(maxcorn.y,square.y)
		maxcorn.x = max(maxcorn.x,square.x)
		squares.append(square)

biggrid = [ [ [ None for x in range(0,maxcorn.x+2) ] for y in range(0,maxcorn.y+2) ] for z in range(0,maxcorn.z+2) ]

for square in squares:
	biggrid[square.z][square.y][square.x] = square

class Node:
	def __init__(self,y,x,normal):
		self.y = y
		self.x = x
		self.normal = normal
nodes = {}
edges = []

def add_node(y,x,normal):
	if (y,x) in nodes: nodes[y,x].normal += normal
	else:              nodes[y,x] = Node(y,x,normal)
	return nodes[y,x]

def link(y0,x0,y1,x1,normal):
	edges.append( (add_node(y0,x0,normal), add_node(y1,x1,normal)) )

for klev in biggrid:
	for jlev in klev:
		for square in jlev:
			if square is None: continue
			z,y,x = square.z,square.y,square.x
			if z != 0 or y>maxcorn.y or x>maxcorn.x: continue
			if square: print '%2d%2d%2d' % (z,y,x),
			else:      print '      ',
			if y==0 or biggrid[z][y-1][x  ] is None: link( (y-CEN  )*Y, (x-CEN  )*X, (y-CEN  )*Y, (x-CEN+1)*X, Point(0, 1, 0) )
			if x==0 or biggrid[z][y  ][x-1] is None: link( (y-CEN+1)*Y, (x-CEN  )*X, (y-CEN  )*Y, (x-CEN  )*X, Point(0, 0, 1) )
			if         biggrid[z][y+1][x  ] is None: link( (y-CEN+1)*Y, (x-CEN+1)*X, (y-CEN+1)*Y, (x-CEN  )*X, Point(0,-1, 0) )
			if         biggrid[z][y  ][x+1] is None: link( (y-CEN  )*Y, (x-CEN+1)*X, (y-CEN+1)*Y, (x-CEN+1)*X, Point(0, 0,-1) )
		print '\n'

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
	vmf.block( b, "NATURE/BLENDSWAMPMUDROOTS01", disp )
	vmf.block( b, "TOOLS/TOOLSNODRAW" )
	b.z0 = (k+10)*Z
	b.z1 = (k+11)*Z
	vmf.block( b, "TOOLS/TOOLSSKYBOX" )
	if min(disp.dists) < 24:
		b.z0 = 128
		b.z1 = 148
		vmf.block( b, "LIQUIDS/WATER_SWAMP_M1" )

# push some nodes around
for node in nodes.values():
	normalize(node.normal)
	node.normal += Point(0,random()*0.2,random()*0.2)
	normalize(node.normal)
	dist = -384.0 + random() * 576.0
	node.y += dist*node.normal.y
	node.x += dist*node.normal.x

# output a card
for node0,node1 in edges:
	card_quad = [
		Point( Z    , node0.y, node0.x ),
		Point( Z    , node1.y, node1.x ),
		Point( Z+512, node1.y, node1.x ),
		Point( Z+512, node0.y, node0.x ),
	]
	tex = "NATURE/SWAMP_TREES_CARD02" + ("a" if randint(0,1) else "")
	vmf.pyramid( card_quad, 80, tex, "TOOLS/TOOLSNODRAW" )

z = startblock.z0 + Z*2
y = startblock.y0 + Y/2
x = startblock.x0 + X/2

# end worldspawn
vmf.end_ent()

vmf.fog_controller        (z+100,y   ,x   )
vmf.light_environment     (z+120,y   ,x   )
vmf.info_survivor_position(z-64 ,y-64,x-64)
vmf.info_survivor_position(z-64 ,y+64,x-64)
vmf.info_survivor_position(z-64 ,y-64,x+64)
vmf.info_survivor_position(z-64 ,y+64,x+64)
vmf.info_player_start     (z-64 ,y   ,x   )

vmf.close()

# vim: ts=8 sw=8 noet
