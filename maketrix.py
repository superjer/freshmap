from random import randint

from navigable import *

def maketrix( size, extranavs=0, blockchance=0, min_multipaths=0, max_multipaths=0, parent=None, pspot=Point(0,0,0) ):
	# make a matrix
	# positions are either EMPTY empty, NAV navpoint, or SOLID solid
	# every nav position must be reachable from every other without having to cross any solids
	empty = Matrix(size.z,size.y,size.x)
	matrix = deepcopy(empty)

	base = 2 if parent is None else 0

	# list of navpoints
	navs = []
	reqd = []

	Z = matrix.size.z-1
	Y = matrix.size.y-1
	X = matrix.size.x-1

	def link(mat,p):
		q = deepcopy(p)
		# flip the specifics
		if q.z is not None: q.z = Z if q.z==0 else 0
		if q.y is not None: q.y = Y if q.y==0 else 0
		if q.x is not None: q.x = X if q.x==0 else 0
		for nav in mat.navs:
			if q.z is not None and nav.z!=q.z: continue
			if q.y is not None and nav.y!=q.y: continue
			if q.x is not None and nav.x!=q.x: continue
			print "Nav to link:", nav.z, nav.y, nav.x
			yield Point( nav.z if p.z is None else p.z,
			             nav.y if p.y is None else p.y,
				     nav.x if p.x is None else p.x )

	def connect(reqd,cell,p):
		if cell.c == SOLID:  return
		if cell.sub is None: reqd.append(p)
		else:                reqd.extend( link(cell.sub,p) )

	# connect to neighboring matrices
	if parent is None:
		# with no parent, connect north to south
		p = Point(None,0,None)
		setattr( p, 'end', 'start' )
		reqd.append(p)
		p = Point(None,Y,None)
		setattr( p, 'end', 'end' )
		reqd.append(p)
	else:
		z,y,x = pspot.z,pspot.y,pspot.x
		# FIXME: what about z?!?
		if y>0              : connect(reqd, parent[z,y-1,x], Point(None,0,None))
		if y<parent.size.y-1: connect(reqd, parent[z,y+1,x], Point(None,Y,None))
		if x>0              : connect(reqd, parent[z,y,x-1], Point(None,None,0))
		if x<parent.size.x-1: connect(reqd, parent[z,y,x+1], Point(None,None,X))
	
		magicpoint = False
		p = Point(Z/2,Y/2,X/2)
		if parent.start == (z,y,x):
			print "Setting start at",p.z,p.y,p.x,"in",z,y,x
			setattr( p, 'end', 'start' )
			magicpoint = True
		if parent.end   == (z,y,x):
			print "Setting end at",p.z,p.y,p.x,"in",z,y,x
			setattr( p, 'end', 'end'   )
			magicpoint = True
		if magicpoint or len(reqd) < 2:
			reqd.append(p)

	print "Reqd:",[ (r.z,r.y,r.x) for r in reqd ]

	# pick random positions in the matrix to make navpoint
	for i in range( randint(len(reqd),len(reqd)+extranavs) ):
		z = randint(0,Z)
		y = randint(0,Y)
		x = randint(0,X)

		# create required connections
		if i < len(reqd):
			if reqd[i].z is not None: z = reqd[i].z
			if reqd[i].y is not None: y = reqd[i].y
			if reqd[i].x is not None: x = reqd[i].x

			if hasattr(reqd[i],'end'):
				if reqd[i].end=='start': matrix.start = (z,y,x)
				if reqd[i].end=='end'  : matrix.end   = (z,y,x)

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
	#print 'Original matrix:'
	#print matrix

	if len(navs) > 1:
		for i in range(randint(min_multipaths,max_multipaths)):
			addtl = deepcopy(empty)
			addtl[navs[0].z,navs[0].y,navs[0].x].c = NAV
			addtl[navs[1].z,navs[1].y,navs[1].x].c = NAV
			addtl.fill(navs[:2])
			#print 'Addtl matrix:'
			#print addtl
			matrix.merge(addtl)

	# view it after merge
	print 'Final matrix:'
	print matrix

	matrix.navs = navs
	return matrix

# vim: ts=8 sw=8 noet
