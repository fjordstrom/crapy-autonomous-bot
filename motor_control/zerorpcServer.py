#!/bin/env python

import zerorpc
from pololu_drv8835_rpi import motors, MAX_SPEED

class MotorControl(object):
    def setMove(self, L, R):
    	motors.setSpeeds(MAX_SPEED*L/100, MAX_SPEED*R/100)
        print "Setting motors to {} {}".format(L,R)

s = zerorpc.Server(MotorControl())
s.bind("tcp://0.0.0.0:4242")
s.run()
