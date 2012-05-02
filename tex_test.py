#!/usr/bin/python

import math
from sys import argv

from point import *
from tex import *


ls = argv[1].translate(None,'()').strip().split() 
x0, y0, z0,  x1, y1, z1,  x2, y2, z2 = [ float(i) for i in ls ]

a = Point( z0, y0, x0 )
b = Point( z1, y1, x1 )
c = Point( z2, y2, x2 )

data = '\t\t\t"uaxis" "[%f %f %f %f] %f"\n\t\t\t"vaxis" "[%f %f %f %f] %f"'

print data % texfit(a,b,c,texw=1024,texh=1024)


# vim: ts=8 sw=8 noet
