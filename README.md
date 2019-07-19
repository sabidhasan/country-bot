# Run Tests
Run tests by
```
python -m unittest discover
```
RPi module cannot run on non-RPi hardware, so this entire class is faked on non-RPi systems. This dummy fake RPi module that is used as a mock must be installed by:
    `cd packages/BotFakeRPi`
    `python setup.py install`

# Development
- Run Python modules in debug mode by appending DEV=1 when running from CLI.
- To only run front end code, run `npm run serve` in the /webserver/frontend directory

# Dependencies
Install `Raspbian GNU/Linux 9 (stretch)` (Linux raspberrypi 4.14.98-v7+)
Enable camera in raspberry pi settings:
  - `raspbian-config`
  - Install `RPi.GPIO`
  - Install `python3-picamera`, which gives access to picamera and picamera.array
- `opencv-python`
- `numpy`
- `BotFakeRPi` (for testing; adapted from https://github.com/sn4k3/FakeRPi)
- PIL and its dependencies, which require the following on RPi
  - `sudo apt-get install libopenjp2-7`
  - `sudo apt install libtiff5`
- `matplotlib` for generating histogram image
- `Flask` for webserver
  - cd into `/wesberver`, run `python3 app.py`
- `SQLAlchemy` for database management
- `VueCLI` for front end and `npm` package manager and `NodeJS`
  - Build front end by cd into `/webserver/frontend`
  - `npm run build` - the resulting dist folder contains built files; `app.py` serves these
- Build database for training data by using
  - `python migrate.py` in the webserver directory. This creates a database using model in the file


# References
- **Ultrasonic Sensor**: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
- **L298**: https://www.explainingcomputers.com/rasp_pi_robotics.html
- **Websockets**: https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
- **mjpeg**: https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
- **Training CNN on Public Images**: https://github.com/quiltdata/open-images and https://blog.quiltdata.com/how-to-classify-photos-in-600-classes-using-nine-million-open-images-3cdb989ad1c2

# Notes to Self
- if you get `picamera.exc.PiCameraMMALError: Failed to enable connection: Out of resources` when instantiating the engine, existing python processes (`ps -a`) must be killed
- for ErrNo 48 port in use, use `ps -fA | grep python` and kill the offending process
- Image default size 320x240 is good


# To Do / Future
**HARDWARE**
- Replace motor driver / DC adapter

**WEB SERVER**
- Add 404 page for front end as routing is handled there now
- Collect training data
- Add front end for training data - show image slideshow, histogram, distance, command, etc.

**ENGINE CLASS**
- Figure out wheel radius and speed of motor (this will be voltage dependent)
- Use PWM (default 100%) to control speed. Self Driving car can use this to control speed

**CAR CLASS**
- Original self driving car - make random choice for movement, to see if 300 ms predcition time 
  is feasible
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
- Train Car to Drive
  1. Gather training data accurately (this serves as BG for below)
  2. Build the model using DB
  3. Verify that it works
- Train Car to Recognize Stop Sign
  - Crop DL'd pos imgs to 320x320 and similar aspect ratios (ignore those that fail this criteria)
  - Make a list of positives.txt (list of file paths)
  - Get negative background data from above
  - Make a list of negatives.txt (ultimately, pos will be 2x neg)
  - Use bin/createsamples.pl (calls opencv_createsamples to put each img onto background) and
    tools/mergevec.py (merges resultant vectors from perl script into one) from
    https://github.com/spmallick/opencv-haar-classifier-training to make positive sample on BG
  - Use above to train classifier using opencv_traincascade
- Navigation?

**LOW PRIORITY**
--------------------
**IMAGE CLASS** (LOW PRIORITY)
- Image class - should return ImageData instance when converting images to b&w etc.
**LOGGING** (LOW PRIORITY)
- Add logging class that logs when DEV=1

