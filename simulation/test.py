from morse.builder import *

atrv = ATRV()

motion = MotionVW()
motion.translate(z=0.3)
atrv.append(motion)

cameraH = 512
cameraW = 768

videocameraL = VideoCamera()
videocameraL.properties(cam_width=cameraW, cam_height=cameraH)
videocameraL.translate(z=0.7, y=0.1, x=0.5)
atrv.append(videocameraL)
videocameraL.add_stream('yarp')

videocameraR = VideoCamera()
videocameraR.properties(cam_width=cameraW, cam_height=cameraH)
videocameraR.translate(z=0.7, y=-0.1, x=0.5)
atrv.append(videocameraR)
videocameraR.add_stream('yarp')


keyboard = Keyboard()
keyboard.properties(Speed=3.0)
atrv.append(keyboard)






# camera = VideoCamera()
# camera.properties(cam_width=512, cam_height=512)
# camera.translate(z=0.7, y=0.1, x=0.5)
# atrv.append(camera)


# camera.add_stream('yarp')

env = Environment('./indoor_scene.blend')
env.set_camera_location([5, -5, 6])
env.set_camera_rotation([1.0470, 0, 0.7854])

