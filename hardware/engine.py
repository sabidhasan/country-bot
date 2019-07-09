import time
import math
import io
import os

if os.environ.get('country_bot_env') == "TESTING":
  import BotFakeRPi.GPIO as GPIO
else:
  try:
    import RPi.GPIO as GPIO
  except ImportError:
    import BotFakeRPi.GPIO as GPIO

class Engine(object):
  TRIG_PIN = 16
  ECHO_PIN = 18
  MOTOR_PINS = [7, 11, 13, 15]
  ULTRASONIC_SENSOR_SETTLE_TIME = 0.2
  SPEED_OF_SOUND = 34300
  MOVE_DURATION = 0.3
  BRAKE_AND_TURN_PAUSE_TIME = 0.1

  def __init__(self, ultra_sonic_sensor_timeout=500000):
    self.revolutions_per_move = 2.0
    # Length in time of each move command in seconds
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

  def apply_brakes(self):
    """ Momentarily applies brakes to prevent car from rolling """
    GPIO.output(13, True)
    time.sleep(self.BRAKE_AND_TURN_PAUSE_TIME)
    GPIO.output(13, False)

  def complex_motion(self, turn_pin, straight_pin):
    """ Turn car in direction of pin specified """
    if not turn_pin in self.MOTOR_PINS or not straight_pin in self.MOTOR_PINS:
      raise ValueError
    # Turn the steering
    GPIO.output(turn_pin, True)
    time.sleep(self.BRAKE_AND_TURN_PAUSE_TIME)
    # Move forward
    GPIO.output(straight_pin, True)
    time.sleep(self.MOVE_DURATION)
    # Stop forward motion and wait for car to stop
    GPIO.output(straight_pin, False)
    self.apply_brakes()
    # time.sleep(2 * self.MOVE_DURATION)
    GPIO.output(turn_pin, False)
    return True
  
  def simple_motion(self, pin):
    """ Moves the car forward for MOVE_DURATION, applying motion to given pin """
    if not pin in self.MOTOR_PINS: raise ValueError
    GPIO.output(pin, True)
    time.sleep(self.MOVE_DURATION)
    GPIO.output(pin, False)
    self.apply_brakes()
    return True

  def go_straight(self):
    """ Make the car go straight for the duration specified by class """
    return self.simple_motion(15)

  def go_left(self):
    """ Make the car go straight for the duration specified by class """
    return self.complex_motion(11, 15)
    
  def go_right(self):
    """ Make the car go straight for the duration specified by class """
    return self.complex_motion(7, 15)
