import time
import math
import io
import os

from hardware.image_data import ImageData

if os.environ.get('country_bot_env') == "TESTING":
  import BotFakeRPi.GPIO as GPIO
  import BotFakeRPi.picamera as picamera
else:
  import RPi.GPIO as GPIO
  import picamera
  import picamera.array

class Engine(object):
  TRIG_PIN = 16
  ECHO_PIN = 18
  MOTOR_PINS = [7, 11, 13, 15]
  ULTRASONIC_SENSOR_SETTLE_TIME = 0.2
  SPEED_OF_SOUND = 34300

  def __init__(self, ultra_sonic_sensor_timeout=500000):
    self.revolutions_per_move = 2.0
    # Length in time of each move command in seconds
    self.move_duration = 0.5
    self.ultra_sonic_sensor_timeout = ultra_sonic_sensor_timeout

    # Set up the Raspberry Pi
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()

    # Set up ultrasonic sensor pins
    GPIO.setup(self.TRIG_PIN, GPIO.OUT)
    GPIO.setup(self.ECHO_PIN, GPIO.IN)

    # Set up and reset motor pins
    for pin in self.MOTOR_PINS:
      GPIO.setup(pin, GPIO.OUT)
    
    # Set up camera
    self.camera = picamera.PiCamera()

  def get_us_distance(self):
    """
      Measures the distance using the ultrasonic sensor. Returns a distance
      in cm. Returns `math.inf` if distance cannot be measured
    """
    try:
      # Send off trigger, and wait for sensor to settle
      GPIO.output(self.TRIG_PIN, False)
      time.sleep(self.ULTRASONIC_SENSOR_SETTLE_TIME)

      # Create the pulse for a short amount of time
      GPIO.output(self.TRIG_PIN, True)
      time.sleep(0.00001)
      GPIO.output(self.TRIG_PIN, False)

      pulse_start_time, pusle_end_time = time.time(), time.time()
      
      # grab start time
      cycles = 0
      while GPIO.input(self.ECHO_PIN) == 0:
        pulse_start_time = time.time()
        cycles += 1
        if cycles > self.ultra_sonic_sensor_timeout: raise ValueError

      cycles = 0
      while GPIO.input(self.ECHO_PIN) == 1:
        pusle_end_time = time.time()
        cycles += 1
        if cycles > self.ultra_sonic_sensor_timeout: raise ValueError

      duration = pusle_end_time - pulse_start_time
      return duration * self.SPEED_OF_SOUND / 2
    except:
      # Error occured, return infinity for distance
      return math.inf

  def get_image(self, width=672, height=496):
    """
      Acquires an image and returns it as ImageData
    """
    if height < 64 or width < 64:
      # Resolution is too low for camera
      raise ValueError
      
    self.camera.resolution = (width, height)
    self.camera.start_preview()
    # Await camera preview to settle
    time.sleep(1.5)
    stream = picamera.array.PiRGBArray(self.camera)
    self.camera.capture(stream, format='bgr')
    raw_data = stream.array
    return ImageData(raw_data, flip_vertical=True)

  def move_car_with_pins(self, pins):
    """
      Moves the car, given an array of pins. Expected length 1 or 2 (move straight or a turn)
      pins = [7, 11] -> turn wheels, then move car (duration for *each* step is self.move_duration / 2)
      pins = [11] -> move car (duration is self.move_duration)
    """
    if not 0 < len(pins) < 3:
      raise TypeError

    if len(pins) == 2:
      # First turn wheel
      GPIO.output(pins[0], True)
      time.sleep(self.move_duration / 2)
      # Then move forward
      GPIO.output(pins[1], True)
      time.sleep(self.move_duration / 2)
    else:
      # Move forward, as there is only one pin specified
      GPIO.output(pins[0], True)
      time.sleep(self.move_duration)
    
    # Reset all pins
    for pin in pins:
      GPIO.output(pin, False)

  def go_straight(self):
    """ Make the car go straight for the duration specified by class """
    self.move_car_with_pins([15])
    return True

  def go_left(self):
    """ Make the car go straight for the duration specified by class """
    self.move_car_with_pins([11, 15])
    return True
    
  def go_right(self):
    """ Make the car go straight for the duration specified by class """
    self.move_car_with_pins([7, 15])
    return True
