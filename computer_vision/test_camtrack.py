import sys
sys.path.append("/opt/openrobots/lib/python2.7/site-packages")

import cv2
import numpy as np

import MockCameraHandler as ch



trackWindow = None
windowHistogram = None

pointA = None
pointB = None
clickDown = False
camTrack = False
startCamTrack = False
def eventCallback(event, x, y, flags, param):
	global clickDown
	global camTrack
	global pointA
	global pointB
	global startCamTrack
	if event == cv2.EVENT_LBUTTONDOWN:
		clickDown = True
		camTrack = False
		pointA = (x,y)
		pointB = pointA
	elif event == cv2.EVENT_LBUTTONUP:
		clickDown = False
		startCamTrack = True
	elif event == cv2.EVENT_MOUSEMOVE:
		if(clickDown):
			pointB = (x,y)




import SurrogateBoxPoints as sbp
import VisionTools as vt


termination_criteria = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

ch.initFrames()

viewportName = "Viewport - click and drag to make a track bracket"
cv2.namedWindow(viewportName)
cv2.setMouseCallback(viewportName, eventCallback)

isCaptureOn = False
captureDir = "./classifier_samples/actual_samples/screenshot"

while True:
	ch.grabFrames()
	test = ch.imageLeft
	clean = np.copy(ch.imageLeft)


	if pointA != None and pointB != None and not camTrack:
			cv2.rectangle(test, pointA, pointB, (255, 0, 0), 2)

	if startCamTrack:
		trackWindow = vt.getRect(pointA, pointB)
		if trackWindow[2]>0 and trackWindow[3]>0:
			windowHistogram = vt.getHistByWindow(test, trackWindow)

			
			camTrack = True
		startCamTrack = False

	if camTrack:
		#gogo HSV
		hsv = cv2.cvtColor(test, cv2.COLOR_BGR2HSV)
		dst = cv2.calcBackProject([hsv], [0], windowHistogram, [0,180], 1)

		#apply meanshift
		ret, trackWindow = cv2.CamShift(dst, trackWindow, termination_criteria)

		if trackWindow[0]+trackWindow[2]==0 or trackWindow[1]+trackWindow[3]==0:
			print("Lost camtrack!")
			camTrack = False
			pointA = None
			pointB = None
		else:
			#draw it
			pts = sbp.boxPoints(ret)
			pts = np.int0(pts)
			cv2.polylines(test, [pts], isClosed=True, color=(255,0,0), thickness=2)

			cent = ret[0]
			sze = ret[1]
			pA = map(int, (cent[0]-sze[0]/2, cent[1]-sze[1]/2))
			pB = map(int, (cent[0]+sze[0]/2, cent[1]+sze[1]/2))
			cv2.rectangle(test, (pA[0], pA[1]), (pB[0], pB[1]), (0, 0, 255), 2)


			if isCaptureOn:
				vt.captureScreenshot(clean, captureDir, vt.scaleROI( vt.getRect(pA, pB), 1.2, 1.2 ) )

	cv2.imshow(viewportName, test)

	if cv2.waitKey(1) & 0xFF == ord('c'):
		isCaptureOn = not isCaptureOn
		print("Capture is {}".format(isCaptureOn) )

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

ch.releaseCameras()


#['EVENT_FLAG_ALTKEY', 'EVENT_FLAG_CTRLKEY', 'EVENT_FLAG_LBUTTON', 'EVENT_FLAG_MBUTTON', 'EVENT_FLAG_RBUTTON', 'EVENT_FLAG_SHIFTKEY', 'EVENT_LBUTTONDBLCLK', 'EVENT_LBUTTONDOWN', 'EVENT_LBUTTONUP', 'EVENT_MBUTTONDBLCLK', 'EVENT_MBUTTONDOWN', 'EVENT_MBUTTONUP', 'EVENT_MOUSEMOVE', 'EVENT_RBUTTONDBLCLK', 'EVENT_RBUTTONDOWN', 'EVENT_RBUTTONUP']
