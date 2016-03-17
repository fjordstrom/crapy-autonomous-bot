import cv2
import numpy as np

import MockCameraHandler as ch

#from SimpleCV import *

# cameraMatrixLeft = np.load("calibrations/cameraMatrixLeft.npy")
# distortionCoeffsLeft = np.load("calibrations/distortionCoeffsLeft.npy")
# cameraMatrixRight = np.load("calibrations/cameraMatrixRight.npy")
# distortionCoeffsRight = np.load("calibrations/distortionCoeffsRight.npy")
# calib_R = np.load("calibrations/calib_R.npy")
# calib_T = np.load("calibrations/calib_T.npy")
# calib_E = np.load("calibrations/calib_E.npy")
# calib_F = np.load("calibrations/calib_F.npy")

# calib_R_left = np.load("calibrations/calib_R_left.npy")
# calib_R_right = np.load("calibrations/calib_R_right.npy")
#calib_P_left = np.load("calibrations/calib_P_left.npy")
#calib_P_right = np.load("calibrations/calib_P_right.npy")
calib_Q = np.load("calibrations/calib_Q.npy")

rectifyMapLeft1 = np.load("calibrations/rectifyMapLeft1.npy")
rectifyMapLeft2 = np.load("calibrations/rectifyMapLeft2.npy")
rectifyMapRight1 = np.load("calibrations/rectifyMapRight1.npy")
rectifyMapRight2 = np.load("calibrations/rectifyMapRight2.npy")



validROI_left = np.load("calibrations/validROI_left.npy")
validROI_right = np.load("calibrations/validROI_right.npy")









ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
	verts = verts.reshape(-1, 3)
	colors = colors.reshape(-1, 3)
	verts = np.hstack([verts, colors])
	with open(fn, 'wb') as f:
		f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
		np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


def selectRectFrom(image, rect):
	[x,y,w,h] = rect
	return image[y:(y+h), x:(x+w)]


#stereo = cv2.StereoBM(preset=cv2.STEREO_BM_NARROW_PRESET, ndisparities=32, SADWindowSize=33)




stereo = cv2.StereoSGBM( \
	minDisparity = 16, \
    numDisparities = 112-16, \
    SADWindowSize = 5, \
    P1 = 8*(5**2), \
    P2 = 32*(5**2), \
    disp12MaxDiff = 1, \
    uniquenessRatio = 10, \
    speckleWindowSize = 150, \
    speckleRange = 2, \
    preFilterCap=5
    )



ch.initFrames()


imageSize = (0,0)


#preTest to assert if it will fail
ch.grabFrames()
#get image size #@TODO make sure left and right are the same
imageSize = ch.imageLeft.shape[::-1][1:3]

area = imageSize[0]*imageSize[1]




while True:
	#Grab frames
	ch.grabFrames()
	frameLeft = ch.imageLeft
	frameRight = ch.imageRight

	# cv2.imshow('Camera Left',frameLeft)
	# cv2.imshow('Camera Right',frameRight)

	cv2.imshow('Cameras', np.concatenate((frameLeft, frameRight), axis=1))

	# frameLeftUndistorted = cv2.undistort(frameLeft, cameraMatrixLeft, distortionCoeffsLeft, newCameraMatrix=newCameraLeft)
	# frameRightUndistorted = cv2.undistort(frameRight, cameraMatrixRight, distortionCoeffsRight, newCameraMatrix=newCameraRight)

	frameLeftRemaped = cv2.remap(frameLeft, rectifyMapLeft1, rectifyMapLeft2, interpolation=cv2.INTER_LINEAR)
	frameRightRemaped = cv2.remap(frameRight, rectifyMapRight1, rectifyMapRight2, interpolation=cv2.INTER_LINEAR)


	# cv2.imshow('Camera Left Undistorted',frameLeftRemaped)
	# cv2.imshow('Camera Right Undistorted',frameRightRemaped)

	

	#print "Shapely norm {} and undistort {}".format(frameLeft.shape, frameLeftRemaped.shape)

	grayL = cv2.cvtColor(frameLeftRemaped, cv2.COLOR_RGBA2GRAY)
	grayR = cv2.cvtColor(frameRightRemaped, cv2.COLOR_RGBA2GRAY)

	
	# roiWidth = max(validROI_left[2], validROI_right[2])
	# roiHeight = max(validROI_left[3], validROI_right[3])
	

	# frameLeftROIClipped = frameLeftRemaped[validROI_left[1]:(validROI_left[1]+roiHeight), validROI_left[0]:(validROI_left[0]+roiWidth)]
	# frameRightROIClipped = frameRightRemaped[validROI_right[1]:(validROI_right[1]+roiHeight), validROI_right[0]:(validROI_right[0]+roiWidth)]

	# cv2.imshow("!!!", frameLeftROIClipped)
	# cv2.imshow("!!!@@@", frameRightROIClipped)

	#disparity = stereo.compute(frameLeftRemaped, frameRightRemaped) #(grayL, grayR)
	

	# hsvLeft = cv2.cvtColor(frameLeftRemaped, cv2.COLOR_BGR2HSV)
	# hsvRight = cv2.cvtColor(frameRightRemaped, cv2.COLOR_BGR2HSV)
	# cutHSVLeft = cv2.split(hsvLeft)
	# cutHSVRight = cv2.split(hsvRight)
	# disparity = stereo.compute(cutHSVLeft[2], cutHSVRight[2])


	kernel = np.ones((9,9),np.uint8)


	#grayL = cv2.morphologyEx(cv2.morphologyEx(grayL, cv2.MORPH_OPEN, kernel), cv2.MORPH_CLOSE, kernel)
	#grayR = cv2.morphologyEx(cv2.morphologyEx(grayR, cv2.MORPH_OPEN, kernel), cv2.MORPH_CLOSE, kernel)


	disparity = stereo.compute(grayL, grayR)


	fin = cv2.normalize(disparity, alpha=0, beta=255, norm_type=cv2.cv.CV_MINMAX, dtype=cv2.cv.CV_8U)
	


	
	#imageee = cv2.morphologyEx(frameRightRemaped, cv2.MORPH_TOPHAT, kernel)
	#erode = cv2.erode(fin,kernel,iterations = 1)
	#cv2.imshow("morphological transform er", erode)
	#imageee = cv2.morphologyEx(frameRightRemaped, cv2.MORPH_GRADIENT, kernel)
	dilate = cv2.dilate(fin,kernel,iterations = 1)
	cv2.imshow("morphological transform dil", dilate)

	#fin = cv2.compare(fin, 80, cv2.CMP_GT)

	# disparityImage = Image(fin)
	# someImage = Image(frameLeftRemaped)

	

	# blobs = disparityImage.findBlobs(minsize=area*0.035, maxsize=area*0.8 )
	# if blobs:
	# 	for b in blobs:
	# 		newlayer = DrawingLayer(someImage.size())
	# 		b.drawOutline(color=(255,0,0), width=5, layer = newlayer)
	# 		someImage.addDrawingLayer(newlayer)
	# 	textLayer = DrawingLayer(someImage.size())
	# 	textLayer.text(str(len(blobs)), (50,50), color=Color.WHITE)
	# 	someImage.addDrawingLayer(textLayer)

	

	# someImage = someImage.applyLayers()
	# test = someImage.getNumpy()

	offset = validROI_left[0:2]
	#@TODO find better way to cut ROI from image
	leftROICut = selectRectFrom(frameLeftRemaped, validROI_left)
	
	#cv2.imshow("h", leftROICut)
	gray = cv2.cvtColor(leftROICut,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)

	cv2.imshow("dtz", thresh)

	#################      Now finding Contours         ###################

	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE, offset=(offset[0], offset[1]) )



	# print hierarchy
	for i in range(0,len(contours)):
		cnt = contours[i]
		currentHierarchy = hierarchy[0][i]

		[x,y,w,h] = cv2.boundingRect(cnt)
		if(w > 10 and h > 10):
			if(currentHierarchy[3] == -1):
				cv2.rectangle(frameLeftRemaped,(x,y),(x+w,y+h),(0,0,255),2)

				if(currentHierarchy[2] != -1):

					childCnt = contours[currentHierarchy[2]]
					[cdx,cdy,cdw,cdh] = cv2.boundingRect(childCnt)
					cv2.rectangle(frameLeftRemaped,(cdx,cdy),(cdx+cdw,cdy+cdh),(255,0,0),2)

	# for cnt in contours:
	# 	if cv2.contourArea(cnt)>100:
	# 		[x,y,w,h] = cv2.boundingRect(cnt)

	# 		if  (h>25) & (w>25):
	# 			cv2.rectangle(frameLeftRemaped,(x,y),(x+w,y+h),(0,0,255),2)






	cv2.rectangle(frameLeftRemaped, (validROI_left[0], validROI_left[1]), (validROI_left[0]+validROI_left[2], validROI_left[1]+validROI_left[3]), (0,255,0), 2)
	cv2.rectangle(frameRightRemaped, (validROI_right[0], validROI_right[1]), (validROI_right[0]+validROI_right[2], validROI_right[1]+validROI_right[3]), (0,255,0), 2)


	cv2.imshow('Cameras Undistorted', np.concatenate((frameLeftRemaped, frameRightRemaped), axis=1))

	cv2.imshow("disp", fin)

	# cv2.imshow("huh", frameLeftRemaped[validROI_left])
	




	if cv2.waitKey(1) & 0xFF == ord('q'):

		points = cv2.reprojectImageTo3D(disparity, calib_Q)
		colors = cv2.cvtColor(frameLeftRemaped, cv2.COLOR_BGR2RGB)
		mask = disparity > disparity.min()
		out_points = points[mask]
		out_colors = colors[mask]
		out_fn = 'out.ply'
		write_ply('out.ply', out_points, out_colors)
		print('%s saved' % 'out.ply')

		break
#---------------------------------#


cv2.destroyAllWindows() #@TODO
ch.releaseCameras()