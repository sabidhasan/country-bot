import os
import io
import time
import threading
import numpy as np
from PIL import Image

if os.environ.get('country_bot_env') == "TESTING":
  import BotFakeRPi.picamera as picamera
else:
  try:
    import picamera
  except ImportError:
    import BotFakeRPi.picamera as picamera
from hardware.image_data import ImageData

class Camera(object):
  """
    Class for interacting with pi camera
    1. allows threading for setting up continuous stream
    2. can get latest image as ImageData object (for storing in training DB)
  """
  # Latest frame
  frame = None
  frame_timestamp = None
  # thread for continuously updating frame, above
  thread = None
  # Camera is reference to instantiated picamera.PiCamera - set at class level
  camera = None

  def __init__(self, width=672, height=496, flip_vertical=False):
    """ Set width and height and instantiate the PiCamera class """
    if height < 64 or width < 64:
      # Resolution is too low for camera
      raise ValueError

    if self.camera is None:
      self.width = width
      self.height = height
      resolution = (self.width, self.height)
      Camera.camera = picamera.PiCamera(resolution = resolution)
      Camera.camera.rotation = 0 if flip_vertical == False else 180

  def start_thread(self):
    """ 
      Threading gets the latest image from the camera. It is started when webserver
      routes request it (it is consumed by the `Flask.Response` method)
    """
    if self.thread is None:
      Camera.thread = threading.Thread(target=self.thread_worker)
      Camera.thread.start()
    # Block until the thread has populated some data into Camera.frame
    while Camera.frame is None:
      pass
    # The start_thread method is called by webserver route (in routes.py),
    # which needs access to cls.get_frame method, so return this instance
    return self

  @classmethod
  def thread_worker(cls):
    """ Update the Camera.frame as data comes in """
    # Let camera settle for a bit
    time.sleep(1.5)
    stream = io.BytesIO()
    for _ in cls.camera.capture_continuous(stream, 'jpeg', use_video_port=True):
      # Seek to beginning, update the frame and reset stream for next frame
      stream.seek(0)
      Camera.frame = stream.read()
      Camera.frame_timestamp = time.time()
      time.sleep(0)
      stream.seek(0)
      stream.truncate()

  def get_frame(self):
    """ Returns latest frame. This getter is for the routes.py webserver route """
    return Camera.frame

  def get_latest_image(self):
    """
      Get latest still image from camera, and returns as ImageData object.
      Returns None when continuous image thread (thread_worker) hasn't been started
    """
    # Get latest JPG image from frame buffer
    latest_image = self.get_frame()

    if latest_image is None:
      # No image exists, so lets capture one and send it back
      binary_data = io.BytesIO()
      time.sleep(1.5)
      self.camera.capture(binary_data, 'jpeg')
      Camera.frame_timestamp = time.time()
    else:
      binary_data = io.BytesIO(latest_image)

    image = Image.open(binary_data)
    np_array = np.array(image)
    return ImageData(np_array)
