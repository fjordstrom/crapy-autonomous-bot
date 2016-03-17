Ground Drone with Command Autonomy
==================================

Hello and welcome to my end-of-year project! A drone that should be able to find it's own way to any objective and survey the area. At least, that's the MVP: simple inertial navigation, object identification, idendification of "interesting" objects.

I'm writing it in mostly Python, because this allows me to make quick adjustments. That, and the added support for Python libraries and easy debugging.

I'll put the project paper here as well, probably, after I'm done writting it. (unfortunately, in Romanian). You probably don't need that document if you're interested in just my workflow and/or the finite product

Done so far:
------------
 * Link to web cameras
 * Basic image processing and streaming
 * Basic motor control
 * Hardware platform


Problems so far:
----------------

Cameras tend to suck. They are cheap webcams, afterall.
 * Lighting conditions are the worst. Natural light would be nice, IF it were constant. It's not. You need a STRONG and CONSTANT artificial light source. How strong? Well, how good are your cameras in low light?
 * They aren't syncronized. They both have a quartz crystal. Solution would be to either buy synced or sync them. I didn't dare, since I didn't want to ruin what I bought (PCB boards with very very small contacts)
 * The noise coming from them is horrible. It's not salt-and-papper. It's unicorn excrement. The noise is so big that no filter, not means, not bilateral, not even errosion and dilation work. Not even a custom temporal median filter works. Probable causes: exposed CMOS (these don't have a lens), arbitrary light sensitivity, power source noise (I'm not expecting expert filtering on them).

My solution: use Blender to simulate robot, plug in same code to think it's using the actual bot.

How did that fare? Well, Blender currently doesn't support multi-threading. Why? When Blender runs a Python script, it waits for it to finish before going back to rendering and executing other scripts. Fine to avoid race conditions, not so fine if you want to run async stuff. So, why not make a thread, let that run and close the script? Well, you'd have to have a way to keep thread handler somewhere to join it back. Blender does have a way of sharing variables, but, apparently, it acts real funny with threads. I'm not risking this one, since many have done before and failed. I'm not really up to fixing Blender right now.

Meanwhile, there is another something called MORSE Simulator, made for these kind of hassles. Supports exacty what I was looking for: a transport protocol. First off, I try sockets, over telnet. And boy, did it work. And my joy was short, since I couldn't send images bigger than 64x64 pixels without frame rate dropping faster than hippies were dropping acid in the 70s. Second try: YARP. What could go wrong? Other than, there were no official packages for Debian.

Usually, compiling packages with the Make system is straightforward on a largely supported system such as Debian. Unless your dependencies include Python. My problem? OpenCV supports Python 2.7. MORSE Simulator supports Python 3. Downgrade, you say? Well I kind of need some very specific features that are supported only on newer versions. After toying with that for about a day, I decided to use robotpkg, a set of packages for robotics that had, among others, MORSE and, best of all, YARP Python bindings, for both 2.7 and 3.4. Rejoyce. After a few more tweaks (setting up PYTHONPATH variables in scripts), I could actually hook up the simulator to my OpenCV Python scripts. Hurray.

About the chasis and motors. I'm using a Tamiya robotics set (cheap-o, if you find cheap-o deals). It's plastic. It's cheap plastic. It's a fun thing to use, if you want to make a quick demo for a prototype, or if you want to make toys, but it's got anything but precision:
 * Plastic (plastic-rubber? They aren't quite rubber, but not quite plastic, either) threads tend to break where they are most thin (how surprising)
 * Cheap motors are brushed DC. Too much power into them, and they start smelling real bad. Like, caution fire hazard bad.
 * Gear box is neat, though still plastic. Lubricant that comes boxed seems to wear out and/or dry after some time. Had to add extra vaseline.
 * The whole ansamble of gearbox, wheels and threads aren't quite balanced. That, and add the uncertainty of the thread making proper ground contact and your bot is sure to stray from a straight line

If you'd want to use that as your robot chassis, you'd need a lot of ancillary devices to make sure you're on track, like:
 * inertial navigation system: accelerometer, gyroscope and magnetometer
 * maybe a GPS would be easier for navigation?
 * an optic counter for the motor wheel would be a nice touch to count how much a thread has travelled
 * something to figure out how you're moving relative to the ground. Infrared? Ladar? Radar?

Of course, you can compensate a lot through computer vision, but that takes processing power. Something like, well, a fancy thing calle SLAM/Bundle Adjustment
