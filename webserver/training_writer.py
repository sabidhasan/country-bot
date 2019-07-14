import time
import datetime
import json
from models import Training
from dbconfig import db

class TrainingWriter(object):
  """ 
    Keeps track of whether training mode is activated or not.
  """

  def __init__(self):
    # activated is time when training was last activated
    self.activated = 0

  def set_active(self):
    """ Sets activated time to now """
    self.activated = time.time()

  @property
  def active(self):
    return self.activated != 0

  def record_training_if_active(self, car, direction):
    if not self.active:
      return False

    image = car.camera.get_latest_image()
    # Record the training
    data = {
      'created': datetime.datetime.now(),
      'image_data': image,
      'ultrasonic': car.get_distance(),
      'cmd_forward': direction.startswith('f'),
      'cmd_right': direction.startswith('r'),
      'cmd_left': direction.startswith('l'),
      'moves': car.get_moves(),
    }
    try:
      new_training = Training(**data)
      db.session.add(new_training)
      db.session.commit()
      return True
    except:
      return False
