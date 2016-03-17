import numpy as np
import cv2

#class CameraHandler(object):
"""Class to handle the two cameras.

Should do:
	select devices
	open devices
	calibrate devices
	grab images
"""

deviceNumberLeft = 0 #TODO move these to a config + defaults
deviceNumberRight = 1

#captureLeft = None
#captureRight = None

imageLeft = None
imageRight = None


def resizeFilter(image):
	#cheap resize filter
	resizeFactor = 0.5

	return cv2.resize(cv2.resize(image, None, fx=resizeFactor, fy=resizeFactor), None, fx=1/resizeFactor, fy=1/resizeFactor)

def bilateralFilter(image):
	#BILATERAL FILTER
	d = 1
	sigmaColor = 500000
	sigmaSpace = sigmaColor

	return cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

# filterStackLeft = None
# filterStackRight = None

#def __init__(self):

#@staticmethod
def initFrames():
	"""Initialize devices
	"""
	global captureLeft
	global captureRight

	captureLeft = cv2.VideoCapture(deviceNumberLeft)
	captureRight = cv2.VideoCapture(deviceNumberRight)


	# returnLeft, tempLeft = captureLeft.read()
	# il = cv2.cvtColor(cv2.flip(cv2.transpose(tempLeft), 0), cv2.COLOR_RGBA2GRAY)

	# returnLeft, tempRight = captureRight.read()
	# ir = cv2.cvtColor(cv2.flip(cv2.transpose(tempRight), 0), cv2.COLOR_RGBA2GRAY)

	# global filterStackLeft
	# global filterStackRight
	# filterStackLeft = np.array([il, il, il])
	# filterStackRight = np.array([ir, ir, ir])

	#and here should be the settings

#@staticmethod
def grabFrames():
	global imageLeft
	global imageRight

	# global filterStackLeft
	# global filterStackRight

	returnLeft, tempLeft = captureLeft.read()
	returnLeft, tempRight = captureRight.read()


	imageLeft = cv2.flip(cv2.transpose(tempLeft), 0) #imageLeft = cv2.flip(tempLeft, -1)
	imageRight = cv2.flip(cv2.transpose(tempRight), 0) #imageRight = tempRight#

	# grayL = cv2.cvtColor(imageLeft, cv2.COLOR_RGBA2GRAY)
	# grayR = cv2.cvtColor(imageRight, cv2.COLOR_RGBA2GRAY)


	# filterStackLeft = np.roll(filterStackLeft, 1, axis=0)
	# filterStackLeft[0] = grayL

	# filterStackRight = np.roll(filterStackRight, 1, axis=0)
	# filterStackRight[0] = grayR

	imageLeft = bilateralFilter(imageLeft)
	imageRight = bilateralFilter(imageRight)


	# hsvLeft = cv2.cvtColor(imageLeft, cv2.COLOR_BGR2HSV)
	# cutHSVLeft = cv2.split(hsvLeft)
	# cv2.imshow("DEBUG HSV", hsvLeft)

	# cv2.imshow("DEBUG HSV -- H", cutHSVLeft[0])
	# cv2.imshow("DEBUG HSV -- S", cutHSVLeft[1])
	# cv2.imshow("DEBUG HSV -- V", cutHSVLeft[2])


#@staticmethod
def releaseCameras():
	captureLeft.release()
	captureRight.release()