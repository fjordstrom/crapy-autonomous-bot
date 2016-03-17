import numpy as np
import cv2
import math
import time

import MockCameraHandler as ch

print "Init cameras"
ch.initFrames()


#Init useful variables
boardSize = (9,6)#(9,6)
requiredSuccessfulDetections = 10
cornerFindCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
squareSize = 0.16; #this one is really important. Size in meters for one square 0.025 means 25 mm

#my sizes:
#A4 paper: 0.025 (25 mm)
#half: 0.0155 (15.5 mm)
#small: 0.006 (6 mm)
#smaller: 0.004 (4 mm)

totalCorners = boardSize[0] * boardSize[1]

leftImagePoints = []
rightImagePoints = []

imageSize = (0,0)


#preTest to assert if it will fail
ch.grabFrames()
#get image size #@TODO make sure left and right are the same
imageSize = ch.imageLeft.shape[::-1][1:3]
print "Imagesize at {} for each camera".format(imageSize)
#-------------------------------------------------#
#       Calibration data acquisition loop         #
#-------------------------------------------------#
#while successful < numberOfRequiredBoards

successfulDetections = 0

latch = False
while(successfulDetections < requiredSuccessfulDetections):

	#Grab frames
	ch.grabFrames()
	frameLeft = ch.imageLeft
	frameRight = ch.imageRight



	#make gray copies
	gray_frameLeft = cv2.cvtColor(frameLeft, cv2.COLOR_BGR2GRAY)
	gray_frameRight = cv2.cvtColor(frameRight, cv2.COLOR_BGR2GRAY)



	#Find corners
	resultLeft, cornersLeft = cv2.findChessboardCorners(frameLeft, boardSize, flags=cv2.CALIB_CB_ADAPTIVE_THRESH|cv2.CALIB_CB_FILTER_QUADS)
	resultRight, cornersRight = cv2.findChessboardCorners(frameRight, boardSize, flags=cv2.CALIB_CB_ADAPTIVE_THRESH|cv2.CALIB_CB_FILTER_QUADS)


	#have you found anything matching?
	if (resultLeft):
		#draw found corners and show them
		cv2.drawChessboardCorners(frameLeft, boardSize, cornersLeft,resultLeft)

	if (resultRight):
		#draw found corners and show them
		cv2.drawChessboardCorners(frameRight, boardSize, cornersRight,resultRight)


	if cv2.waitKey(1) & 0xFF == ord('c'):
		latch = True
	if (latch & resultLeft & resultRight):
		latch = False

		successfulDetections += 1
		#refine
		cv2.cornerSubPix(gray_frameLeft,cornersLeft,(11,11),(-1,-1),cornerFindCriteria)
		cv2.cornerSubPix(gray_frameRight,cornersRight,(11,11),(-1,-1),cornerFindCriteria)

		#store in stack
		leftImagePoints.append(cornersLeft.reshape(-1, 2))   
		rightImagePoints.append(cornersRight.reshape(-1, 2))

		print "Callibration {}% finished".format(successfulDetections*100/requiredSuccessfulDetections)

	#show camera view
	# cv2.imshow('Camera Left',frameLeft)
	# cv2.imshow('Camera Right',frameRight)

	cv2.imshow('Cameras', np.concatenate((frameLeft, frameRight), axis=1))


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#endwhile

#kill all windows, release cams
# cv2.destroyAllWindows() #@TODO
# ch.releaseCameras()


#-------------------------------------------------#
#Compute the acquired data for use in calibration #
#-------------------------------------------------#
print "Computing instrinsinc calibration parameters"

#mtx -> identity
cameraMatrixLeft = np.identity(3)
cameraMatrixRight = np.identity(3)
#dst -> zero
distortionCoeffsLeft = np.zeros((1,5))
distortionCoeffsRight = np.zeros((1,5))



pattern_points = np.zeros((np.prod(boardSize), 3), np.float32)
pattern_points[:, :2] = np.indices(boardSize).T.reshape(-1, 2)
pattern_points *= squareSize

objPoints = []
for i in range (0,requiredSuccessfulDetections):
	objPoints.append(pattern_points)


returnCalibrate, cameraMatrixLeft, distortionCoeffsLeft, cameraMatrixRight, distortionCoeffsRight, calib_R, calib_T, calib_E, calib_F \
	= cv2.stereoCalibrate(objPoints, leftImagePoints, rightImagePoints, imageSize, cameraMatrixLeft, distortionCoeffsLeft, cameraMatrixRight, distortionCoeffsRight, \
	criteria=(cv2.TERM_CRITERIA_MAX_ITER|cv2.TERM_CRITERIA_EPS, 100, 1e-5), \
	flags=(cv2.CALIB_FIX_ASPECT_RATIO|cv2.CALIB_ZERO_TANGENT_DIST|cv2.CALIB_SAME_FOCAL_LENGTH) \
	)

print "Found intrinsinc calibration parameters, rmi {}".format(returnCalibrate)


print "Press 'q' to continue. Showing undistorted using instrinsinc params"
print cameraMatrixLeft
print distortionCoeffsLeft
print cameraMatrixRight
print distortionCoeffsRight
while True:
	#Grab frames
	ch.grabFrames()
	frameLeft = ch.imageLeft
	frameRight = ch.imageRight

	undistortedLeft = cv2.undistort(frameLeft, cameraMatrixLeft, distortionCoeffsLeft)
	undistortedRight = cv2.undistort(frameRight, cameraMatrixRight, distortionCoeffsRight)

	cv2.line(undistortedLeft, (20, 20), (100, 20), (255,0,0),5)

	cv2.imshow('Cameras undistorted (intrinsinc)', np.concatenate((undistortedLeft, undistortedRight), axis=1))

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break



print "Now testing calibration quality"
totalPoints = 0
totalError = 0

for i in range (0,len(leftImagePoints)):
	sampleLeftImagePoints = leftImagePoints[i]
	sampleRightImagePoints = rightImagePoints[i]

	pointsShape = sampleLeftImagePoints.shape

	sampleLeftImagePoints = sampleLeftImagePoints.reshape( (1,)+pointsShape )
	sampleRightImagePoints = sampleRightImagePoints.reshape( (1,)+pointsShape )



	pointsLeftUndistorted = cv2.undistortPoints(sampleLeftImagePoints, cameraMatrixLeft, distortionCoeffsLeft , P=cameraMatrixLeft)
	pointsRightUndistorted = cv2.undistortPoints(sampleRightImagePoints, cameraMatrixRight, distortionCoeffsRight , P=cameraMatrixRight)

	epiLinesLeft = cv2.computeCorrespondEpilines(pointsLeftUndistorted, 1, calib_F)
	epiLinesRight = cv2.computeCorrespondEpilines(pointsRightUndistorted, 2, calib_F)

	for j in range (0,epiLinesLeft.shape[0]):
		totalPoints += 1
		totalError += math.fabs( \
			sampleLeftImagePoints[0][j][0]*epiLinesRight[j][0][0] + \
			sampleLeftImagePoints[0][j][1]*epiLinesRight[j][0][1] + \
			epiLinesRight[j][0][2] \
			) + math.fabs( \
			sampleRightImagePoints[0][j][0]*epiLinesLeft[j][0][0] + \
			sampleRightImagePoints[0][j][1]*epiLinesLeft[j][0][1] + \
			epiLinesLeft[j][0][2] \
			)

averageEpipolarError = totalError / totalPoints
print "Average epipolar error is {}".format(averageEpipolarError)



#--------------------------------------------------#
# Calculate extrinsinc pramaters, R1, R2, P1, P2, Q#
#--------------------------------------------------#
print "Calculating extrinsinc parameters"

calib_R_left, calib_R_right, calib_P_left, calib_P_right, calib_Q, validROI_left, validROI_right = \
	cv2.stereoRectify(cameraMatrixLeft, distortionCoeffsLeft, cameraMatrixRight, distortionCoeffsRight, \
	imageSize=imageSize, \
	R=calib_R, \
	T=calib_T, \
	flags=cv2.CALIB_ZERO_DISPARITY, \
	alpha=1, \
	newImageSize=imageSize \
	)

print "IMPORTANT (isVerticalStereo): {}".format(calib_P_right[1][3] > calib_P_right[0][3])
print "Done calculating extrinsinc parameters"



#----------------------------------------#
print "Saving calibrations"

#instrinsinc
np.save("calibrations/cameraMatrixLeft", cameraMatrixLeft)
np.save("calibrations/distortionCoeffsLeft", distortionCoeffsLeft)
np.save("calibrations/cameraMatrixRight", cameraMatrixRight)
np.save("calibrations/distortionCoeffsRight", distortionCoeffsRight)
np.save("calibrations/calib_R", calib_R)
np.save("calibrations/calib_T", calib_T)
np.save("calibrations/calib_E", calib_E)
np.save("calibrations/calib_F", calib_F)

#extrinsinc
np.save("calibrations/calib_R_left", calib_R_left)
np.save("calibrations/calib_R_right", calib_R_right)
np.save("calibrations/calib_P_left", calib_P_left)
np.save("calibrations/calib_P_right", calib_P_right)
np.save("calibrations/calib_Q", calib_Q)
np.save("calibrations/validROI_left", validROI_left)
np.save("calibrations/validROI_right", validROI_right)

print "Save done"
#----------------------------------------#
print "Calculating rectification maps"

rectifyMapLeft1, rectifyMapLeft2 = cv2.initUndistortRectifyMap( \
	cameraMatrixLeft, distortionCoeffsLeft, calib_R_left, calib_P_left, imageSize, \
	m1type=cv2.CV_16SC2 \
	)
rectifyMapRight1, rectifyMapRight2 = cv2.initUndistortRectifyMap( \
	cameraMatrixRight, distortionCoeffsRight, calib_R_right, calib_P_right, imageSize, \
	m1type=cv2.CV_16SC2 \
	)
print "Done calculating rectification maps"

print "Also saving rect. maps"

np.save("calibrations/rectifyMapLeft1", rectifyMapLeft1)
np.save("calibrations/rectifyMapLeft2", rectifyMapLeft2)
np.save("calibrations/rectifyMapRight1", rectifyMapRight1)
np.save("calibrations/rectifyMapRight2", rectifyMapRight2)

print "Done saving rect. maps"
#---------------------------------#


cv2.destroyAllWindows() #@TODO
ch.releaseCameras()