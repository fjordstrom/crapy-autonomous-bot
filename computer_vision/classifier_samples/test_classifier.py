import numpy as np

import sys
sys.path.append("/opt/openrobots/lib/python2.7/site-packages")

import yarp

import matplotlib.pylab as mpl

yarp.Network.init()

input_port = yarp.Port() #BufferedPortImageRgba()
input_port.open("/image-port")

yarp.Network.connect("/morse/atrv/videocameraL/out", "/image-port")




imageLeft = np.zeros((512,768,4), dtype=np.uint8)

yarp_image = yarp.ImageRgba()
yarp_image.resize(512, 768)

yarp_image.setExternal(imageLeft, imageLeft.shape[1], imageLeft.shape[0])


import cv2

cascade = cv2.CascadeClassifier('./classifier/cascade.xml')



while True:
	
	
	input_port.read(yarp_image)


	test = cv2.cvtColor(np.delete(imageLeft,3,2), cv2.COLOR_RGB2BGR)

	gray = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

	stuff = cascade.detectMultiScale(gray, scaleFactor=1.3, \
		minNeighbors=100 \
		)
	for (x,y,w,h) in stuff:
		cv2.rectangle(test, (x,y), (x+w, y+h), (255,0,0), 2)


	cv2.imshow("dd", test)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

input_port.close()