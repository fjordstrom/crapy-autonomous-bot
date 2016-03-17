#!/bin/env python
import pygame
from pygame.locals import *



import zerorpc

pygame.init()
width, height = 300, 300
screen=pygame.display.set_mode((width, height))

keys = [False, False, False, False]


client = zerorpc.Client()
client.connect("tcp://192.168.90.128:4242")
def sendSig(L, R):
	client.setMove(L,R)

fullSpeed = 100
cruiseSpeed = fullSpeed/5
fraction = 2

currentSpeed = cruiseSpeed

runGame = True
eventStat = False
while runGame:

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == K_UP:
				keys[0] = True
			elif event.key == K_DOWN:
				keys[1] = True
			elif event.key == K_LEFT:
				keys[2] = True
			elif event.key == K_RIGHT:
				keys[3] = True
			elif event.key == K_LSHIFT or event.key == K_RSHIFT:
				currentSpeed = fullSpeed
			elif event.key == K_q:
				runGame = False
		elif event.type == pygame.KEYUP:
			if event.key == K_UP:
				keys[0] = False
			elif event.key == K_DOWN:
				keys[1] = False
			elif event.key == K_LEFT:
				keys[2] = False
			elif event.key == K_RIGHT:
				keys[3] = False
			elif event.key == K_LSHIFT or event.key == K_RSHIFT:
				currentSpeed = cruiseSpeed
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			if keys[2] and keys[0]: # <^
				sendSig(currentSpeed/fraction, currentSpeed)
			elif keys[3] and keys[0]: # ^>
				sendSig(currentSpeed, currentSpeed/fraction)
			elif keys[2] and keys[1]: # <v
				sendSig(-currentSpeed/fraction, -currentSpeed)
			elif keys[3] and keys[1]: # v>
				sendSig(-currentSpeed, -currentSpeed/fraction)
			elif keys[0]: # ^
				sendSig(currentSpeed, currentSpeed)
			elif keys[1]: # v
				sendSig(-currentSpeed, -currentSpeed)
			elif keys[2]: # <
				sendSig(-currentSpeed, currentSpeed)
			elif keys[3]: # >
				sendSig(currentSpeed, -currentSpeed)
			else:
				sendSig(0,0)

