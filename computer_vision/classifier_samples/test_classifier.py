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
import os


classifier_dirs = os.listdir("./classifiers")

colorPixHSV = np.array([[[0,255,255]]], dtype=np.uint8)
colorIncrement = 180 / len(classifier_dirs) if len(classifier_dirs) else 1

classifiers = []
for dirc in classifier_dirs:
	name = dirc
	clasf = cv2.CascadeClassifier('./classifiers/'+dirc+'/cascade.xml')

	temp = cv2.cvtColor(colorPixHSV, cv2.COLOR_HSV2BGR)
	color = tuple(map(int,temp[0][0]))
	colorPixHSV[0][0][0] += colorIncrement

	classifiers.append((name, color, clasf))


while True:
	
	
	input_port.read(yarp_image)


	test = cv2.cvtColor(np.delete(imageLeft,3,2), cv2.COLOR_RGB2BGR)

	gray = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)


	for (name, color, cascade) in classifiers:
		stuff = cascade.detectMultiScale(gray, scaleFactor=1.1, \
			  minNeighbors=500 \
			)

		for (x,y,w,h) in stuff:
			cv2.rectangle(test, (x,y), (x+w, y+h), color, 2)
			cv2.putText(test, name, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


	cv2.imshow("dd", test)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

input_port.close()