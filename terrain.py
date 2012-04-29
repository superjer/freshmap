from random import randint

from navigable import *

def maketerrain(ydivs, xdivs, size):
	ymax = ydivs*size+1
	xmax = xdivs*size+1
	matrix = Matrix(1, ymax, xmax)
	var = 512

	for j in range(ydivs+1):
		for i in range(xdivs+1):
			matrix[0,j*size,i*size] = randint(0,var)

	step = size
	while step > 1:
		offs = step/2
		#edges
		var /= 2
		for j in range(offs,ymax,step):
			for i in range(0,xmax,step):
				avg = (matrix[0,j-offs,i] + matrix[0,j+offs,i]) / 2
				matrix[0,j,i] = randint(-var,var) + avg
		for j in range(0,ymax,step):
			for i in range(offs,xmax,step):
				avg = (matrix[0,j,i-offs] + matrix[0,j,i+offs]) / 2
				matrix[0,j,i] = randint(-var,var) + avg
		#middles
		for j in range(offs,ymax,step):
			for i in range(offs,xmax,step):
				avg = (matrix[0,j-offs,i] + matrix[0,j,i-offs] +
				       matrix[0,j+offs,i] + matrix[0,j,i+offs]) / 4
				matrix[0,j,i] = randint(-var,var) + avg
		step /= 2

	# tweak the random nonsense into something believable
	for j in range(0,ymax):
		for i in range(0,xmax):
			val = matrix[0,j,i] - 100
			if val < 24:               val = 24 - (24-val)/10
			if val < 0:                val = 0
			if val > 16 and val <= 20: val = 16
			if val > 20 and val <= 24: val = 24
			matrix[0,j,i] = val

	return matrix

# vim: ts=8 sw=8 noet
