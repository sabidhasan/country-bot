import math
import time
from helpers.os import set_environ

# Set testing environment so Camera imports fake RPi camera
set_environ("TESTING")
from hardware.camera import Camera

class Car(object):
  WHEEL_RADIUS_CM = 1

  def __init__(self, engine):
    """
      engine is an instance of the Engine object that controls
      the hardware of the raspberry pi.
    """
    self.created = time.time()
    self.engine = engine
    # Number of times a move command has been issued
    self.moves = 0
    # What times move commands were issued at
    self.moves_times = []
    # Camera control 
    self.camera = Camera(flip_vertical=True)
  
  def get_distance_travelled(self):
    """ Returns how much distance has been travelled in total """

    circumference = 2 * math.pi * self.WHEEL_RADIUS_CM 
    return circumference * self.engine.revolutions_per_move * self.moves
  
  def currently_moving(self):
    """ Returns whether car moved in the last two seconds """

    try:
      return abs((self.moves_times[-1] + self.engine.move_duration) - time.time()) <= 2
    except IndexError:
      return False

  def move_car(self, direction):
    """
      Moves the car in the direction specified by one unit, which is
      defined as the duration in the engine. Direction is a string
      ['straight', 'left' or 'right'].
    """
    directions = {
      'straight': self.engine.go_straight,
      'left': self.engine.go_left,
      'right': self.engine.go_right
    }
    try:
      move_success = directions[direction]()
      self.moves_times.append(time.time())
      self.moves += 1
    except KeyError:
      # Illegal command was issued
      move_success = False
    return move_success

  def go_straight(self):
    """
      Moves the car forward; returns False is failure or tuple of current car 
      sensors if successful (inputs are Ultrasonic and camera)
    """

    return self.move_car('straight')

  def go_left(self):
    """
      Moves the car forward; returns False is failure or tuple of current car 
      sensors if successful (inputs are Ultrasonic and camera)
    """
    return self.move_car('left')

  def go_right(self):
    """
      Moves the car right; returns False is failure or tuple of current car 
      sensors if successful (inputs are Ultrasonic and camera)
    """

    return self.move_car('right')

  def get_image(self):
    """ Returns a processed image from the car - a base64 representation of a JPEG """
    latest_image_data = self.camera.get_latest_image()
    return str(latest_image_data.tobase64())

  def get_distance(self):
    """ Returns current forward distance """
    return self.engine.get_us_distance()

  def get_moves(self):
    return self.moves