Computer Vision
---------------

This directory contains scripts pertaining to computer vision.

Calibrations aren't uploaded since they are both camera specific and binaries that take up space.

`CameraHandler` is for the actual cameras, `MockCameraHandler` is for MORSE Simulator yarp stream.

`runStereoWithCalibrations` should be the main program. It requires that calibrations are done.

`calibrate` does exactly what it says. Use a checkerboard pattern. Configure it manually for the size of each square (edit script, for now). Press `c` in viewer to take a snapshot. Currently, 10 are needed, but can be configured for more or less.
