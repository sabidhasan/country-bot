# Run Tests
Run tests by
```
python -m unittest discover
```
RPi module cannot run on non-RPi devices. To get around this, a dummy fake RPi module is used as a mock.


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


# Notes to Self
- if you get `picamera.exc.PiCameraMMALError: Failed to enable connection: Out of resources` when instantiating the engine, existing python processes (`ps -a`) must be killed
- for ErrNo 48 port in use, use `ps -fA | grep python` and kill the offending process


# To Do / Future
**HARDWARE**
- Hardware: battery pack / camera / ultrasonic sensor / car is unscrewed
- Make 'roads'

**WEB SERVER**
- Add catch-all route for main page
- Add authentication to main page
- Training
    - Use a model (?) to add a Training_DB
    - Collect data when driving (database, downloading files, etc)
- fix image data from `/data` endpoint 
    - fix binary JSON (it sends as "b'<data>'", so chop it before sending).
    - endpoint should accept parameters for type of image
- Probe a websockets approach for continuous stream

**IMAGE CLASS**
- Image class - should return ImageData instance when converting images to b&w etc.

**ENGINE CLASS**
- Figure out wheel radius and speed of motor (this will be voltage dependent)
- reduce sleep time for camera capturing time.sleep 
- Image default size 320x240 is good
- Write non-blocking versions of get_us_distance and get_camera (threadpool executor) - is it needed?

**CAR CLASS**
- Make a ControllableCar class, and call that instead of Car from webserver entrypoint
- Self Driving car
    - self.brain should be defined
    - check for forwrd object
    - check for stopsign (if so, wait 3 sec)
    - check for traffic light
    - get model to predict based on inputs 

**LEARNING**
- Forward collision detection
- Learning Strategy
    - fake input data by flipping image / adding noise / brightness / contrast
    - Haar feature-based cascade classifiers for objects (stop signs and traffic lights)
    - OpenCV
- Navigation?
