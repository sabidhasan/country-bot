from hardware.engine_base import BaseEngine
import time
import os

if os.environ.get('country_bot_env') == "TESTING":
  import BotFakeRPi.GPIO as GPIO
else:
  try:
    import RPi.GPIO as GPIO
  except ImportError:
    import BotFakeRPi.GPIO as GPIO


class ControllableEngine(BaseEngine):
  MOVE_DURATION = 0.3
  BRAKE_AND_TURN_PAUSE_TIME = 0.1

  def __init__(self, ultra_sonic_sensor_timeout=500000):
    """
      Starts instance of Controllable engine. 
      Ultrasonic sensor timeout is number of cycles waited until US sensor times out
    """
    super().__init__(ultra_sonic_sensor_timeout=ultra_sonic_sensor_timeout)
    self.revolutions_per_move = 2.0


  def _apply_brakes(self):
    """ Momentarily applies brakes to prevent car from rolling """
    GPIO.output(self.MOTOR_STRAIGHT_PIN, False)
    GPIO.output(self.MOTOR_REVERSE_PIN, True)
    time.sleep(self.BRAKE_AND_TURN_PAUSE_TIME)
    GPIO.output(self.MOTOR_REVERSE_PIN, False)


  def _move_straight_and_turn(self, turn_pin):
    """ Turn car in direction of pin specified """
    if not turn_pin in self.MOTOR_PINS:
      raise ValueError

    # Turn the steering
    GPIO.output(turn_pin, True)
    time.sleep(self.BRAKE_AND_TURN_PAUSE_TIME)

    # Move forward
    GPIO.output(self.MOTOR_STRAIGHT_PIN, True)
    time.sleep(self.MOVE_DURATION)

    # Stop car
    self._apply_brakes()
    GPIO.output(turn_pin, False)
  

  # Public methods for moving or turning car
  def go_straight(self):
    """ Moves the car forward for MOVE_DURATION, applying motion to given pin """
    GPIO.output(self.MOTOR_STRAIGHT_PIN, True)
    time.sleep(self.MOVE_DURATION)
    GPIO.output(self.MOTOR_STRAIGHT_PIN, False)
    self._apply_brakes()


  def go_left(self):
    """ Make the car go straight for the duration specified by class """
    self._move_straight_and_turn(self.MOTOR_LEFT_PIN)
    

  def go_right(self):
    """ Make the car go straight for the duration specified by class """
    self._move_straight_and_turn(self.MOTOR_RIGHT_PIN)
