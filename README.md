# Run Tests
Run tests by
```
python -m unittest discover
```
RPi module cannot run on non-RPi hardware, so this entire class is faked on non-RPi systems. This dummy fake RPi module that is used as a mock must be installed by:
    `cd packages/BotFakeRPi`
    `python setup.py install`
If RPi not found errors arise, run in debug mode by appending DEV=1 when running from CLI.

# Dependencies
Enable camera in raspberry pi settings:
  - `raspbian-config`
  - Install `RPi.GPIO`
  - Install `python3-picamera`, which gives access to picamera and picamera.array
- `opencv-python`
- `numpy`
- `BotFakeRPi` (for testing; adapted from https://github.com/sn4k3/FakeRPi)
- Pillow and its dependencies, which require the following on RPi
  - `sudo apt-get install libopenjp2-7`
  - `sudo apt install libtiff5`
- `Flask` for webserver


# References
- **Ultrasonic Sensor**: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
- **L298**: https://www.explainingcomputers.com/rasp_pi_robotics.html
- **Websockets**: https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
- **mjpeg**: https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited

# Notes to Self
- if you get `picamera.exc.PiCameraMMALError: Failed to enable connection: Out of resources` when instantiating the engine, existing python processes (`ps -a`) must be killed
- for ErrNo 48 port in use, use `ps -fA | grep python` and kill the offending process
- Image default size 320x240 is good


# To Do / Future
**HARDWARE**
- Replace motor driver
- Look into DC adapter
- Attach camera properly
- Tie down battery pack / ultrasonic sensor
- Make 'roads' - need hard paper

**WEB SERVER**
- Add catch-all route for main page
- Add **tables** for users and training data (use models?)
- Add **authentication** to main page
- Collect training data when driving (database, downloading files, etc.)
- Prettify front end **VueJS** front end

**ENGINE CLASS**
- Figure out wheel radius and speed of motor (this will be voltage dependent)
- Use PWM (default 100%) to control speed. Self Driving car can use this to control speed

**LOGGING**
- Add logging class that logs when DEV=1

**CAR CLASS**
- Make a ControllableCar class, and call that instead of Car from webserver entrypoint
- Self Driving car
    - self.brain should be defined - this makes decisions on what to do
    - check for forwrd object
    - check for stopsign (if so, wait 3 sec)
    - check for traffic light
    - get model to predict based on inputs 
    - add to engine class a drive_continuously with a speed attirnute that uses PWM

**CAMERA**
- Write more tests for Camera class

**LEARNING**
- Forward collision detection
- Learning Strategy
    - fake input data by flipping image / adding noise / brightness / contrast
    - Haar feature-based cascade classifiers for objects (stop signs and traffic lights)
    - OpenCV
- Navigation?


**LOW PRIORITY**
--------------------
**IMAGE CLASS** (LOW PRIORITY)
- Image class - should return ImageData instance when converting images to b&w etc.
