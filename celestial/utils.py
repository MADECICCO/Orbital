
import numpy as np
from visual import *

def deg2rad(deg):
	return deg * math.pi/180

def rad2deg(rad):
	return rad * 180/math.pi

def getAngleBetweenVectors(v1, v2):
	MAG = (v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])/(mag(v1)*mag(v2))
	print "v1=", v1, ", v2=", v2
	#print "getAngleBetweenVectors, cos(theta)=", dotProduct/(mag(v1)*mag(v2))
	if abs(MAG) > 1:
		print "getAngleBetweenVectors: Invalid arccos Value. V1=", v1, ", V2=", v2
		return 0
	else:
		#theta = np.arccos(dotProduct/(mag(v1)*mag(v2)))
		return rad2deg(np.arccos(MAG))

# projection of vector v1 onto v2
def getVectorProjectionToVector(v1, v2):
	return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]/mag(v2)

def getXYprojection(vec):
	return getVectorProjection(vec, vector(1,0,0), vector(0,1,0))

def getXZprojection(vec):
	return getVectorProjection(vec, vector(1,0,0), vector(0,0,1))

def getYZprojection(vec):
	return getVectorProjection(vec, vector(0,1,0), vector(0,0,1))

def getVectorProjection(vec, pv1, pv2):
	# get vector orthogonal to a plane defined by 2 vectors pv1 and pv2
	# Recall that the vector projection of a vector u onto another vector v is given by 
	# 
	# projv(u) = (u.v/||v||^2) x v
	# 
	# The projection of u onto a plane can be calculated by subtracting the component of  
	# u that is orthogonal to the plane from  u.  If you think of the plane as being horizontal, 
	# this means computing  u minus the vertical component of u, leaving the horizontal component. 
	# This "vertical" component is calculated as the projection of  u onto the plane normal vector n.
	#
	# projPlane(u) = u - projn(u) = u - (u.n/||n||^2) x n
	# where n is a vector normal to plane
	#
	n = getVectorOrthogonalToPlane(pv1, pv2)
	vec = (1/mag(vec)) * vec
	projn_vec = (vec[0]*n[0] + vec[1]*n[1] + vec[2]*n[2]) * n
	return vec - projn_vec
	return vector(vec[0]-n[0], vec[1]-n[1], vec[2]-n[2])


def getOrthogonalVector(vec, direction = "x"):
	# The set of all possible orthogonal vectors to a given vector is a Plane. Among 
	# all possible orthogonal vectors we choose the one that also lay on the (x,y) 
	# plane (with z=0) and whose x coordinate is arbitrary 1. Using these presets, we 
	# can deduct the y coordinate by applying a dot product between our vec and its 
	# orthogonal vector. The result of the dot product must be zero since the vectors 
	# are othogonal: 
	# For direction = 'x' (we choose x=1)
	# (x.x1 + y.y1 + z.z1 = 0)  => y = -(z.z1 + x.x1)/y1 
	#
	# For direction = 'y' (we choose y=1)
	# (x.x1 + y.y1 + z.z1 = 0)  => x = -(z.z1 + y.y1)/x1 
	z = 0
	x, y = 0, 0
	if direction == 'x':
		if vec[1] != 0:
			x = 1
			#x = mag(vec)/np.sqrt(1+(vec[0]/vec[1])**2)
			y = -vec[0]*x/vec[1]
		else:
			y = 1
			x = 0
	else:
		if vec[0] != 0:
			y = 1
			x = -vec[1]*y/vec[0]
		else:
			x = 1
			y = 0


	# return a unit vector
	return norm(vector(x,y,z))

def getOrthogonalVector_SAVE(vec):
	# The set of all possible orthogonal vectors to a given vector is a Plane. Among 
	# all possible orthogonal vectors we choose the one that also lay on the (x,y) 
	# plane (with z=0) and whose x coordinate is arbitrary 1. Using these presets, we 
	# can deduct the y coordinate by applying a dot product between our vec and its 
	# orthogonal vector. The result of the dot product must be zero since the vectors 
	# are othogonal: 
	# 
	# (x.x1 + y.y1 + z.z1 = 0)  => y = -(z.z1 + x.x1)/y1 
	#
	z = 0
	x, y = 0, 0
	if vec[1] != 0:
		x = 1
		#x = mag(vec)/np.sqrt(1+(vec[0]/vec[1])**2)
		y = -vec[0]*x/vec[1]
	else:
		y = 1
		x = 0

	# return a unit vector
	return norm(vector(x,y,z))

def getVectorOrthogonalToPlane(A, B):
	# Vectors A and B defined a plane. To determine the unit vector that is
	# orthogonal to this plane, we need to calculate the cross product:
	# A X B = (a1b2 - b1a2, b0a2 - a0b2, a0b1 - b0a1) which comes from calculating 
	# the determinant:
	# 			    | i		j		k  |   
	#	P = A X B = | a0	a1		a2 | = i(a1b2 - b1a2) - j(a0b2 - b0a2) + k(a0b1 - b0a1)
	#			    | b0	b1		b2 |
	#

	x = A[1]*B[2] - A[2]*B[1]
	y = A[2]*B[0] - A[0]*B[2]
	z = A[0]*B[1] - B[0]*A[1]

	# return a unit vector
	norm = mag((x, y, z))
	if norm != 0:
		return (1/norm) * vector(x, y, z)
	else:
		return None

	#return vector(x/norm, y/norm, z/norm)

def getPlaneOrthogonalToVector(v): # not finished
	# given a vector v we want to determine the plane equation of the plane
	# orthogonal to this vector, we need to calculate the scalar product:
	# if the vector v has its origin in L (x0, y0, z0) and L is a point of the plane.
	# Then any point P (x,y,z) in the plane will verify:
	# (x-x0).vx + (y-y0).vy + (z-z0).vz = 0, as the vector LP must be orthogonal
	# to v.
	# A X B = (a1b2 - b1a2, b0a2 - a0b2, a0b1 - b0a1) which comes from calculating 
	# the determinant:
	# 			    | i		j		k  |   
	#	P = A X B = | a0	a1		a2 | = i(a1b2 - b1a2) - j(a0b2 - b0a2) + k(a0b1 - b0a1)
	#			    | b0	b1		b2 |
	#

	x = A[1]*B[2] - A[2]*B[1]
	y = A[2]*B[0] - A[0]*B[2]
	z = A[0]*B[1] - B[0]*A[1]

	# return a unit vector
	norm = mag((x, y, z))
	return (1/norm) * vector(x, y, z)
	#return vector(x/norm, y/norm, z/norm)

def sleepThis(delay): # delay in seconds
	if delay > 1:
		return rate(1)
	return rate(1/delay)
