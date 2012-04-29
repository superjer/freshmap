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

	return matrix

# vim: ts=8 sw=8 noet
