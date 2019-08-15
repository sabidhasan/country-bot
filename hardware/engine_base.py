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


# Engine initialization can be done only once due to hardware limitations
# This global variable keeps track of whether init code has been run in Engine class
_engine_initialized = False

class BaseEngine():
  """
    Base class for Self Driving and Controllable car engines.
    Metaclass singleton.Singleton ensures that this class can only be instantiated once.
    This is needed to prevent engine initialization errors from RPi
  """
  TRIG_PIN = 16
  ECHO_PIN = 18

  MOTOR_RIGHT_PIN = 7
  MOTOR_LEFT_PIN = 11
  MOTOR_REVERSE_PIN = 13
  MOTOR_STRAIGHT_PIN = 15
  MOTOR_PINS = [MOTOR_RIGHT_PIN, MOTOR_LEFT_PIN, MOTOR_REVERSE_PIN, MOTOR_STRAIGHT_PIN]
  
  ULTRASONIC_SENSOR_SETTLE_TIME = 0.2
  SPEED_OF_SOUND = 34300

  PWM_FREQUENCY = 200

  def __init__(self, ultra_sonic_sensor_timeout):
    if type(self) == BaseEngine:
      # Prevent direct instatiation of this class
      raise NotImplementedError
      
    # Length in time of each move command in seconds
    self.ultra_sonic_sensor_timeout = ultra_sonic_sensor_timeout

    if os.environ.get('country_bot_env') != "TESTING":
      GPIO.setwarnings(False)

    global _engine_initialized
    if _engine_initialized == False:
      self.initialize_engine()


  def initialize_engine(self):
    """
      These RPi initialization tasks only occur once
    """
    # Set up the Raspberry Pi Board configuration
    GPIO.setmode(GPIO.BOARD)

    # Set up ultrasonic sensor pins
    GPIO.setup(self.TRIG_PIN, GPIO.OUT)
    GPIO.setup(self.ECHO_PIN, GPIO.IN)

    # Set up and reset motor pins
    for pin in self.MOTOR_PINS:
      GPIO.setup(pin, GPIO.OUT)

    global _engine_initialized
    _engine_initialized = True


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
        if cycles > self.ultra_sonic_sensor_timeout:
          return math.inf

      cycles = 0
      while GPIO.input(self.ECHO_PIN) == 1:
        pusle_end_time = time.time()
        cycles += 1
        if cycles > self.ultra_sonic_sensor_timeout:
          return math.inf

      duration = pusle_end_time - pulse_start_time
      return duration * self.SPEED_OF_SOUND / 2
    except:
      # Error occured, return infinity for distance
      return math.inf