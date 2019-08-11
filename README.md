# Dependencies
- Install `Raspbian GNU/Linux 9 (stretch)` (Linux raspberrypi 4.14.98-v7+)
- Install python3 for RPi 
  - `sudo apt-get install python3-pip python3-dev`
- Enable camera in raspberry pi settings:
  - `raspbian-config`
  - Install `RPi.GPIO`
  - Install `python3-picamera`, which gives access to picamera and picamera.array
- Python package `opencv-python`
- Python package `numpy` (1.17.0)
- Python package `BotFakeRPi` (for testing or running on desktop; adapted from https://github.com/sn4k3/FakeRPi)
- PIL and its dependencies, which require the following on RPi
  - `sudo apt-get install libopenjp2-7`
  - `sudo apt install libtiff5`
- Python package `matplotlib` for generating histogram images
- Python package `Flask` for webserver
- Python package `SQLAlchemy` for database management
- NPM package manager and packages
  - `sudo apt-get install nodejs npm node-semver`
  - `npm install --global vue
- NPM package `VueCLI` for front end. Build front end:
  - `cd /webserver/frontend`
  - `npm run build` - the resulting dist folder contains built files; `app.py` serves these
- Build database (SQLite 3) for training data
  - `python migrate.py` in the webserver directory.
- Python package `keras` for training/loading the car driver
  - Install tensorflow `wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.8.0/tensorflow-1.8.0-cp35-none-linux_armv7l.whl` 
  - install it via `sudo pip3 install ./tensorflow-1.8.0-cp35-none-linux_armv7l.whl`
  - `pip install h5py`
  - `sudo apt install libhdf5-100`

  - Running the command `import keras` should work in a Py3 shell


# Tests
Run Python tests:
```
python -m unittest discover
```
RPi module cannot run on non-RPi hardware, so this entire class is faked on non-RPi systems. This dummy fake RPi module that is used as a mock must be installed by:
    `cd packages/BotFakeRPi`
    `python setup.py install`


# Development | Notes
- Run car-facing Python modules in debug mode by appending `DEV=1` when running from CLI.
- To only run front end code locally, run `npm run serve` in the /webserver/frontend directory
- if you get `picamera.exc.PiCameraMMALError: Failed to enable connection: Out of resources` when instantiating the engine, existing python processes (`ps -a`) must be killed
- for ErrNo 48 port in use, use `ps -fA | grep python` and kill the offending process
- Image default size 320x240 is good


# Machine Learning
- ML steps are optional, as the repo comes with a trained model
- There are two ML models: (1) Haar classifier for stop signs, and (2) CNN for self driving
- For training either model, training data must be gathered:
  - Run the car (see **Running the Car** section)
  - Enable recording of training data
  - Go into **Training Mode** from the web interface 
  - Drive the car around on white roads (learning uses camera image as input and direction taken as label)

**Training CNN**
- Train CNN by `cd learning/Neural Network` 
- Run `python app.py [optional path to training-db]`
  (if path not supplied, the default path is used from `webserver/trainingdata.db`)
- This script loops thru each training point, doing the following:
  - Applys each transformation filter
  - Saving the transformed image as JPG
  - Saving histogram (used by car's CNN to predict) of transformed image as JPG
  - Recording an array-representation of histogram with human-trained direction and saving to disk
  - Returning array
- Custom Transformation Filters can be created for any image transformation!


# Running the Car
To run the car, transfer entire repo to RPi, and install dependencies.
`cd` into the `webserver/frontend` directory and run `python3 app.py`
The app is network-served using the Flask dev server on RPi and can be accessed at RPi's network IP


# References
- **Ultrasonic Sensor**: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
- **L298**: https://www.explainingcomputers.com/rasp_pi_robotics.html
- **Websockets**: https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
- **mjpeg**: https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
- **Training CNN on Public Images**: https://github.com/quiltdata/open-images and https://blog.quiltdata.com/how-to-classify-photos-in-600-classes-using-nine-million-open-images-3cdb989ad1c2

# Notes to Self


# To Do / Future
**HARDWARE**
- Replace motor driver / DC adapter

**WEB SERVER**
- Add 404 page for front end as routing is handled there now
- Collect training data
- Add front end for training data - show image slideshow, histogram, distance, command, etc.
- Write tests for project

**ENGINE CLASS**
- Figure out wheel radius and speed of motor (this will be voltage dependent)
- Use PWM (default 100%) to control speed. Self Driving car can use this to control speed
- Create a thread that continuously updates the US distance in main class, and the get_distance
  method just grabs the latest data.

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
- To train the neural network, first acquire some training data (or have a training database):
  To acquire data, go to 

- Forward collision detection
- Train Car to Drive
  1. Gather training data accurately (this serves as BG for below) - need ~800 points
     Curvy runs             0001-0274
     Straight runs          0565
     L turns
     Intersections          0457-0564
     Circles                0275-0456
  2. Flip images from above to get more data
  3. Augment the images (add blur, noise, contrast, etc.)
  4. Build the model using DB - try 1 hidden layer with 32 or 64 nodes
  5. Verify that it works
- Train Car to Recognize Stop Sign
  - Remove DL'd pos imgs that are obviously irrelevant
  - Remove DL's pos imgs with messed up aspect ratios
  - Crop DL'd pos imgs to 320x320
  - Grayscale DL'd pos imgs
  - Make a list of positives.txt (list of file paths)
  - Make a list of negatives.txt (pos will be 2x neg)
  - Use bin/createsamples.pl (calls opencv_createsamples to put each img onto background) and
    tools/mergevec.py (merges resultant vectors from perl script into one) from
    https://github.com/spmallick/opencv-haar-classifier-training to make positive sample on BG
    Also see https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/
  - Use above to train classifier using opencv_traincascade
- Navigation? Speed detection?

**LOW PRIORITY**
--------------------
**IMAGE CLASS** (LOW PRIORITY)
- Image class - should return ImageData instance when converting images to b&w etc.
**LOGGING** (LOW PRIORITY)
- Add logging class that logs when DEV=1

