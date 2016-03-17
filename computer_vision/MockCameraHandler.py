#Mock camera handler class
import numpy as np

import sys
sys.path.append("/opt/openrobots/lib/python2.7/site-packages")

import yarp
import cv2

#external
imageLeft = None
imageRight = None


#consts
cameraLeftName = "videocameraL"
cameraRightName = "videocameraR"

imageWidth = 768
imageHeight = 512

#internal
_imageLeftProto = None
_imageRightProto = None

_yarpImageLeft = None
_yarpImageRight = None

_yarpPortLeft = None
_yarpPortRight = None

def initFrames():
	global _yarpPortLeft
	global _yarpPortRight
	global _yarpImageLeft
	global _yarpImageRight
	global _imageLeftProto
	global _imageRightProto
	global imageWidth
	global imageHeight
	global cameraLeftName
	global cameraRightName
	#ran once at start
	yarp.Network.init()

	_yarpPortLeft = yarp.Port()
	_yarpPortRight = yarp.Port()

	_yarpPortLeft.open("/opencv/video/left")
	_yarpPortRight.open("/opencv/video/right")

	yarp.Network.connect("/morse/atrv/"+cameraLeftName+"/out", "/opencv/video/left")
	yarp.Network.connect("/morse/atrv/"+cameraRightName+"/out", "/opencv/video/right")

	_imageLeftProto = np.zeros((imageHeight,imageWidth,4), dtype=np.uint8)
	_imageRightProto = np.zeros((imageHeight,imageWidth,4), dtype=np.uint8)

	_yarpImageLeft = yarp.ImageRgba()
	_yarpImageRight = yarp.ImageRgba()

	_yarpImageLeft.resize(imageWidth, imageHeight)
	_yarpImageRight.resize(imageWidth, imageHeight)

	_yarpImageLeft.setExternal(_imageLeftProto, imageWidth, imageHeight)
	_yarpImageRight.setExternal(_imageRightProto, imageWidth, imageHeight)


	
def grabFrames():
	global _yarpPortLeft
	global _yarpPortRight
	global _yarpImageLeft
	global _yarpImageRight
	global _imageLeftProto
	global _imageRightProto
	global imageLeft
	global imageRight
	#run everytime you want image update
	_yarpPortLeft.read(_yarpImageLeft)
	_yarpPortRight.read(_yarpImageRight)

	imageLeft = cv2.cvtColor(np.delete(_imageLeftProto,3,2), cv2.COLOR_RGB2BGR)
	imageRight = cv2.cvtColor(np.delete(_imageRightProto,3,2), cv2.COLOR_RGB2BGR)
def releaseCameras():
	global _yarpPortLeft
	global _yarpPortRight
	#run before end
	_yarpPortLeft.close()
	_yarpPortRight.close()