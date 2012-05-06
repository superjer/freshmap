from random import randint
from itertools import product

from navigable import *

def maketerrain(ydivs, xdivs, size):
	ymax = ydivs*size+1
	xmax = xdivs*size+1
	matrix = Matrix(1, ymax, xmax)
	var = 512
	chaos = randint(-200,130)
	bias = randint(-150,0)

	print "y,x max:",ymax,xmax,"chaos:",chaos,"bias:",bias

	for j in range(ydivs+1):
		for i in range(xdivs+1):
			matrix[0,j*size,i*size] = randint(0,var) + bias

	var += chaos

	step = size
	while step > 1:
		offs = step/2
		#edges
		var /= 2
		for j in range(offs,ymax,step):
			for i in range(0,xmax,step):
				avg = matrix[0,j-offs,i] + matrix[0,j+offs,i]
				matrix[0,j,i] = randint(-var,var) + avg / 2
				if step>32 and randint(0,1024)<step: matrix[0,j,i] = randint(0,var) + bias
		for j in range(0,ymax,step):
			for i in range(offs,xmax,step):
				avg = matrix[0,j,i-offs] + matrix[0,j,i+offs]
				matrix[0,j,i] = randint(-var,var) + avg / 2
				if step>32 and randint(0,1024)<step: matrix[0,j,i] = randint(0,var) + bias
		#middles
		for j in range(offs,ymax,step):
			for i in range(offs,xmax,step):
				avg = matrix[0,j-offs,i] + matrix[0,j,i-offs] + matrix[0,j+offs,i] + matrix[0,j,i+offs]
				matrix[0,j,i] = randint(-var,var) + avg / 4
				if step>32 and randint(0,1024)<step: matrix[0,j,i] = randint(0,var) + bias
		step /= 2

	# smoothing passes
	class SmoothingSpot:
		def __init__(self,x,y,radius,passes):
			self.x,self.y,self.radius,self.passes = x,y,radius,passes

	smoothing_spots = []
	for i in range(randint(1,4)):
		temp = SmoothingSpot( randint(-100,ymax+100),
		                      randint(-100,xmax+100),
		                      randint(5,20)         ,
		                      randint(1,5)          , )
		print "Smoothing spot:",temp.x,temp.y,temp.radius,temp.passes
		#smoothing_spots.append(temp)

	for k in range(0,5):
		smoother = deepcopy(matrix)
		for j,i in product(range(1,ymax-1),range(1,xmax-1)):
			allowed_passes = []
			for s in smoothing_spots:
				if (j-s.y)**2 + (i-s.x)**2 < s.radius**2: allowed_passes.append(s.passes)
			allowed_passes = 0 if len(allowed_passes)==0 else sum(allowed_passes)/len(allowed_passes)
			if allowed_passes < k: continue
			avg = matrix[0,j-1,i] + matrix[0,j+1,i] + matrix[0,j,i-1] + matrix[0,j,i+1]
			smoother[0,j,i] = avg / 4
		matrix = smoother

	# flatten the lower bits and stretch away from water
	for j,i in product(range(0,ymax),range(0,xmax)):
		val = matrix[0,j,i] - 100
		if val < 24:               val = 24 - (24-val)/10
		if val < 0:                val = 0
		if val > 18 and val <= 20: val = 18
		if val > 20 and val <= 22: val = 22
		matrix[0,j,i] = val

	return matrix

# vim: ts=8 sw=8 noet
