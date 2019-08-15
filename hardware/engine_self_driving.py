from hardware.engine_base import BaseEngine
import os

if os.environ.get('country_bot_env') == "TESTING":
  import BotFakeRPi.GPIO as GPIO
else:
  try:
    import RPi.GPIO as GPIO
  except ImportError:
    import BotFakeRPi.GPIO as GPIO


class SelfDrivingEngine(BaseEngine):
  PWM_DUTY_CYCLE = 30

  def __init__(self, ultra_sonic_sensor_timeout=500000):
    super().__init__(ultra_sonic_sensor_timeout=ultra_sonic_sensor_timeout)

    #  Set up PWM pin for slower forward motion
    self.pwm = GPIO.PWM(self.MOTOR_STRAIGHT_PIN, self.PWM_FREQUENCY)


  def turn_wheels_left(self):
    """ Turn wheels to the left, removing pin output to 'right' wheels """
    GPIO.output(self.MOTOR_RIGHT_PIN, False)
    GPIO.output(self.MOTOR_LEFT_PIN, True)


  def turn_wheels_right(self):
    """ Turn wheels to the right, removing pin output to 'left' wheels """
    GPIO.output(self.MOTOR_LEFT_PIN, False)
    GPIO.output(self.MOTOR_RIGHT_PIN, True)


  def start_continuous_move(self):
    """ Start slow continuous motion """
    self.pwm.start(self.PWM_DUTY_CYCLE)


  def turn_wheels_forward(self):
    """ Straighten the wheels """
    GPIO.output(self.MOTOR_LEFT_PIN, False)
    GPIO.output(self.MOTOR_RIGHT_PIN, False)


  def stop_all_motion(self):
    """ Stop the car from forward motion and straighten the wheels """
    self.pwm.stop()
    self.turn_wheels_forward()
