Motor Control
=============

I've made a convenience script so I can control the motors even manually while the robot is in operation (easier if I want to play with it when I turn autonomy off).

`zerorpcServer` should be put on the robot. Notice the pololu drv library.

`manualOverride` basically connects to that server and tells it to set motor speeds. Simple as that.
