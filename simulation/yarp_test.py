import numpy as np

import sys
sys.path.append("/opt/openrobots/lib/python2.7/site-packages")

import yarp

import matplotlib.pylab as mpl

yarp.Network.init()

input_port = yarp.Port() #BufferedPortImageRgba()
input_port.open("/image-port")

yarp.Network.connect("/morse/atrv/videocameraL/out", "/image-port")




imageLeft = np.zeros((512,512,4), dtype=np.uint8)

yarp_image = yarp.ImageRgba()
yarp_image.resize(512, 512)
#yarp_image.setQuantum(1)

yarp_image.setExternal(imageLeft, imageLeft.shape[1], imageLeft.shape[0])



import cv2

while True:
	
	
	input_port.read(yarp_image)
	#print(yarp_image.getRawImageSize ())

	test = cv2.cvtColor(np.delete(imageLeft,3,2), cv2.COLOR_RGB2BGR)
	print(test.shape)
	cv2.imshow("dd", test)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

input_port.close()