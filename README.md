# Run Tests
Run tests by
```
python -m unittest discover
```
RPi module cannot run on non-RPi devices. To get around this, a dummy fake RPi module is used as a mock.


# Dependencies
Enable camera in raspberry pi settings: `raspbian-config`
- `python3-picamera`
- `opencv-python`
- `BotFakeRPi` (adapted from https://github.com/sn4k3/FakeRPi)


# References
**Ultrasonic Sensor**: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
**L298**: https://www.explainingcomputers.com/rasp_pi_robotics.html


# Notes to Self
- if you get `picamera.exc.PiCameraMMALError: Failed to enable connection: Out of resources` when instantiating the engine, existing python processes (`ps -a`) must be killed
- Figure out wheel radius and speed of motor (this will be voltage dependent)
- self.brain for SelfDrivingCar(Car)
- Car - acceleration calc'd by distan
      has a moved_timestamps array [] for when move issued
      this allows calculating acceleration and "current speed"
      has a self.car_hardware object that actually talks to hardware
- **Websockets**: https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent


# To Do / Future
- Hardware: battery pack / camera / ultrasonic sensor / car is unscrewed
- Write tests for ImageData class (processes a raw image into numpy array)
- Write ImageData class 240 x 320 is sufficient
- Write web server for controllable car (basic auth, db, shows curr img, controls for moving, us_distance) - simple version
- Write non-blocking versions of get_us_distance and get_camera (threadpool executor)
- Sockets for continuous stream of inputs
- Make 'roads'
- Add functionality for gathering data (database, sessions, downloading files, button for 'make my brake count' (as normally the training will only record upon a forward/right/left from user))
- Object detection for stopsigns and traffic lights
- Forward collision detection
- ML training
    - fake more data by flipping image / adding noise / brightness / contrast
    - Haar feature-based cascade classifiers for objects
    - OpenCV
- Self Driving car
    - check for forwrd object
    - check for stopsign (if so, wait 3 sec)
    - check for traffic light
    - get model to predict based on inputs 
- Navigation?