#!/usr/bin/python

import math
from sys import argv

from point import *

def aligntex( x0, y0, z0,  x1, y1, z1,  x2, y2, z2,  texw=512, texh=512 ):
	a = Point( z0, y0, x0 )
	b = Point( z1, y1, x1 )
	c = Point( z2, y2, x2 )

	u = Point( z0-z1, y0-y1, x0-x1 )
	v = Point( z1-z2, y1-y2, x1-x2 )

	mu = magnitude(u)
	mv = magnitude(v)

	usc = mu/(texw)
	vsc = mv/(texh)

	normalize(u,mu)
	normalize(v,mv)

	ush = -math.fmod( dotproduct(u,a)/usc, texw )
	vsh = -math.fmod( dotproduct(v,a)/vsc, texh )

	data = '\t\t\t"uaxis" "[%f %f %f %f] %f"\n\t\t\t"vaxis" "[%f %f %f %f] %f"'

	return data % (u.x,u.y,u.z,ush,usc,
	               v.x,v.y,v.z,vsh,vsc)

ls = argv[1].translate(None,'()').strip().split() 
ls = [ float(i) for i in ls ]
print aligntex( *ls, texw=1024, texh=1024 )


# vim: ts=8 sw=8 noet

