import math

def rotatePoints(points, angle):
	return ( points[0]*math.cos(angle)-points[1]*math.sin(angle), points[0]*math.sin(angle)+points[1]*math.cos(angle) ) 

# def toRectCenter(point, center):
# 	return ( point[0]-center[0], point[1]-center[1] )

def toOrigin(point, center):
	return ( point[0]+center[0], point[1]+center[1] )

def getPoints(center, size):
	return ( (-size[0]/2, -size[1]/2), (+size[0]/2,-size[1]/2), (+size[0]/2, +size[1]/2), (-size[0]/2, +size[1]/2) )

def boxPoints(rect):
	center = rect[0]
	size = rect[1]
	angle = rect[2]

	points = getPoints(center, size)

	v1 = toOrigin( rotatePoints( points[0], angle ), center )
	v2 = toOrigin( rotatePoints( points[1], angle ), center )
	v3 = toOrigin( rotatePoints( points[2], angle ), center )
	v4 = toOrigin( rotatePoints( points[3], angle ), center )

	return (v1, v2, v3, v4)