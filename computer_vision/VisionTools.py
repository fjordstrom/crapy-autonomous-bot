import cv2
import time
import numpy as np

def getRect(A,B):
	#Return a rect from two points
	if(A[0] > B[0]):
		c = B[0]
		w = A[0] - B[0]
	else:
		c = A[0]
		w = B[0] - A[0]

	if(A[1] > B[1]):
		r = B[1]
		h = A[1] - B[1]
	else:
		r = A[1]
		h = B[1] - A[1]

	return (c,r,w,h)

def scaleROI(roi, hs, ws):
	#scale a ROI by height and width
	(c,r,w,h) = roi

	c = c - ( (ws - 1) / 2 ) * w
	w = w * ws

	r = r - ( (hs - 1) / 2 ) * h
	h = h * hs

	return (c,r,w,h)

def getHistByWindow(image, window):
	#get histogram of a window
	(c,r,w,h) = window
	roi = image[r:r+h, c:c+w]
	hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.))) #check this step
	roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
	cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

	return roi_hist


def captureScreenshot(image, where, roi=None):
	import time
	if roi != None:
		(c,r,w,h) = roi
		height, width, channels = image.shape
		if c<0:
			c = 0
		elif c>width:
			return False

		if r<0:
			r = 0
		elif r>height:
			return False

		if (c+w)>width:
			w = width - c
		if (r+h)>height:
			h = height - r


		image = image[r:r+h, c:c+w]
	if where[len(where)-1] != "/":
		where = where+"/"

	params = list()
	params.append(cv2.IMWRITE_PNG_COMPRESSION)
	params.append(8)

	cv2.imwrite(where+str(int(time.time()))+".png", image, params)
	return True