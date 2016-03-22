import math

def rotatePoints(points, angle):
	return ( points[0]*math.cos(angle)-points[1]*math.sin(angle), points[0]*math.sin(angle)+points[1]*math.cos(angle) ) 

def toRectCenter(point, center):
	return ( point[0]-center[0], point[1]-center[1] )

def toOrigin(point, center):
	return ( point[0]+center[0], point[1]+center[1] )

def getPoints(xy, size):
	return ( (xy[0], xy[1]), (xy[0]+size[0], xy[1]), (xy[0]+size[0], xy[1]+size[1]), (xy[0], xy[1]+size[1]) )

def boxPoints(rect):
	xy = rect[0]
	size = rect[1]
	angle = rect[2]

	center = ( xy[0]+size[0]/2, xy[1]+size[1]/2 )

	points = getPoints(xy, size)

	v1 = toOrigin( rotatePoints( toRectCenter(points[0], center), angle ), center )
	v2 = toOrigin( rotatePoints( toRectCenter(points[1], center), angle ), center )
	v3 = toOrigin( rotatePoints( toRectCenter(points[2], center), angle ), center )
	v4 = toOrigin( rotatePoints( toRectCenter(points[3], center), angle ), center )

	return (v1, v2, v3, v4)