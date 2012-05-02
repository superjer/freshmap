import math

from point import *

texsizes = {
	"NATURE/SWAMP_TREES_CARD01": (1024,1024),
	"TOOLS/TOOLSNODRAW"        : (  64,  64),
}

# figure out the texture axes, shifts, and scales to "fit" on the polygon
# same as the Fit button in Hammer
def texfit( a, b, c, tex=None, texw=512, texh=512 ):
	if tex in texsizes: texw,texh = texsizes[tex]

	u = a - b
	v = b - c

	mu = magnitude(u)
	mv = magnitude(v)

	uscale = mu/(texw)
	vscale = mv/(texh)

	normalize(u,mu)
	normalize(v,mv)

	ushift = -math.fmod( dotproduct(u,a)/uscale, texw )
	vshift = -math.fmod( dotproduct(v,a)/vscale, texh )

	return (u.x,u.y,u.z,ushift,uscale, v.x,v.y,v.z,vshift,vscale)

# vim: sw=8 ts=8 noet
