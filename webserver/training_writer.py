import time
import datetime
from flask import Flask
from functools import wraps
from models import db, Training

app = Flask(__name__)
db.init_app(app)

class TrainingWriter(object):
  """ 
    Keeps track of whether training mode is activated or not.
  """
  TIMEOUT = 1800

  def __init__(self, db):
    # activated is time when training was last activated
    self.activated = 0
    self.db = db

  def set_active(self):
    """ Sets activated time to now """
    self.activated = time.time()

  @property
  def active(self):
    return time.time() - self.activated < self.TIMEOUT

  def record_training_if_active(self, car, direction):
    if not self.active:
      return

    # Record the training
    data = {
      'created': datetime.datetime.now(),
      'image_jpeg': car.camera.get_latest_image().tobase64(),
      'image_np': car.camera.get_latest_image(),
      'ultrasonic': car.get_distance(),
      'cmd_forward': direction.startswith('f'),
      'cmd_right': direction.startswith('r'),
      'cmd_left': direction.startswith('l'),
      'moves': car.get_moves(),
    }
    try:
      new_training = Training(**data)
      self.db.session.add(new_training)
      self.db.session.commit()
    finally:
      # Update the activated time
      self.activated = time.time()
    
