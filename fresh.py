#!/usr/bin/python
from random import *
from copy import deepcopy
from itertools import product

from point     import *
from maketrix  import *
from terrain   import *
from navigable import *
from vmf       import *

seed(13)

XMAIN = randint(4,6)
YMAIN = 10-XMAIN
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
		max_multipaths = 3,
		parent = matrix,
		pspot = Point(k,j,i) )

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

maxcorn = Point(1,0,0)
squares = []

for k,j,i in product(range(matrix.size.z),range(matrix.size.y),range(matrix.size.x)):
	if matrix[k,j,i].c == '@': continue
	sub = matrix[k,j,i].sub
	for w,v,u in product(range(sub.size.z),range(sub.size.y),range(sub.size.x)):
		if sub[w,v,u].c == '@': continue
		square = Square(k*DIVSIZE+w, j*DIVSIZE+v+3, i*DIVSIZE+u+3) # +3's are for buffering!
		if (w,v,u) == sub.start: square.is_start = True
		if (w,v,u) == sub.end  : square.is_end   = True
		maxcorn.y = max(maxcorn.y,square.y)
		maxcorn.x = max(maxcorn.x,square.x)
		squares.append(square)

# all these +3's are to keep several unused squares around the boundary
maxcorn += Point(0,3,3)
biggrid = [ [ [ None for x in range(0,maxcorn.x) ] for y in range(0,maxcorn.y) ] for z in range(0,maxcorn.z) ]
for square in squares:
	biggrid[square.z][square.y][square.x] = square

hmap = maketerrain( int(maxcorn.x/4+1), int(maxcorn.y/4+1), 64 )

class Node:
	def __init__(self,y,x,normal):
		self.y = y
		self.x = x
		self.newy = 0
		self.newx = 0
		self.normal = normal
		self.edges = []
nodes = {}
edges = []

def add_node(y,x,normal):
	global nodes
	if (y,x) in nodes: nodes[y,x].normal += normal
	else:              nodes[y,x] = Node(y,x,normal)
	return nodes[y,x]

def link(y0,x0,y2,x2,normal):
	global nodes, edges
	y1 = (y0+y2)*0.5
	x1 = (x0+x2)*0.5
	node0 = add_node(y0,x0,normal)
	node1 = add_node(y1,x1,normal)
	node2 = add_node(y2,x2,normal)
	edge0 = (node0,node1)
	edge1 = (node1,node2)
	edges += (edge0,edge1)
	node0.edges += (edge0,)
	node1.edges += (edge0,edge1)
	node2.edges += (edge1,)

print "Making edge graph"
for klev in biggrid:
	for jlev in klev:
		for square in jlev:
			if square is None: continue
			z,y,x = square.z,square.y,square.x
			if z != 0 or y>maxcorn.y or x>maxcorn.x: continue
			if y==0 or biggrid[z][y-1][x  ] is None: link( (y-CEN  )*Y, (x-CEN  )*X, (y-CEN  )*Y, (x-CEN+1)*X, Point(0, 1, 0) )
			if x==0 or biggrid[z][y  ][x-1] is None: link( (y-CEN+1)*Y, (x-CEN  )*X, (y-CEN  )*Y, (x-CEN  )*X, Point(0, 0, 1) )
			if         biggrid[z][y+1][x  ] is None: link( (y-CEN+1)*Y, (x-CEN+1)*X, (y-CEN+1)*Y, (x-CEN  )*X, Point(0,-1, 0) )
			if         biggrid[z][y  ][x+1] is None: link( (y-CEN  )*Y, (x-CEN+1)*X, (y-CEN+1)*Y, (x-CEN+1)*X, Point(0, 0,-1) )

def alphaval(n):
	return str(randint(128,255)) if n<24 else "0"

startblock = None
endblock = None

print "Writing"
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
print "Randomizing nodes a bit"
for node in nodes.values():
	if not node.normal.x and not node.normal.y: continue # can't normalize zero vector
	normalize(node.normal)
	node.normal += Point(0,random()*0.2,random()*0.2)
	normalize(node.normal)
	dist = -384.0 + random() * 576.0
	node.y += dist*node.normal.y
	node.x += dist*node.normal.x

REPEL_MIN = 0.99
REPEL_RAND = (1.0-REPEL_MIN) * 2.0

# smooth the nodes
print "Smoothing nodes"
for i in range(6,2,-1):
	print "Smoothing nodes pass",i
	for node in nodes.values():
		avg_denum = 1
		node.newy = node.y
		node.newx = node.x
		# find neighbor nodes
		for edge in node.edges:
			for neigh in edge:
				if neigh is node: continue
				node.newy += neigh.y
				node.newx += neigh.x
				avg_denum += 1
		# nearby nodes repel
		for other in nodes.values():
			if other is node: continue
			othervec = Point(0,other.y,other.x) - Point(0,node.y,node.x)
			othermag = magnitude(othervec)
			too_close = othermag - 50.0 * i
			if too_close < 0.0:
				normalize(othervec)
				node.newy += othervec.y * too_close * (random()*REPEL_RAND + REPEL_MIN)
				node.newx += othervec.x * too_close * (random()*REPEL_RAND + REPEL_MIN)
		node.newy /= avg_denum
		node.newx /= avg_denum

	for node in nodes.values():
		node.y = node.newy
		node.x = node.newx

# output a card for each graph edge
print "Writing"
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
