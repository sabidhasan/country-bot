import os
import unittest
import time
import sys
import math
from unittest.mock import Mock, MagicMock, call, patch
from helpers.image_data import ImageData

# Set environment variable to import correct files
os.environ["country_bot_env"] = "TESTING"
import hardware.engine as Engine


def mock_gpio_input(RPi_pin_number):
  """ The mock input function uses time to mock a pulse from ultrasonic sensor """
  return int(round(time.time() * 100) % 100 == 33)

def mock_gpio_infinite(RPi_pin_number):
  """ This RPi will never report the echo coming back, so should time out """
  return 0

class EngineTests(unittest.TestCase):
    def setUp(self):
      self.engine = Engine.Engine(ultra_sonic_sensor_timeout=7E4)

    # Defines a revolutions per move constant
    def test_revs_per_move(self):
      self.assertIsInstance(self.engine.revolutions_per_move, float,
                        'tire revolutions per move is not a number')

    # Defines a move_duration
    def test_move_duration(self):
      self.assertIsInstance(self.engine.move_duration, float,
                        'duration for a move event is not a number')
      self.assertGreater(self.engine.move_duration, 0,
                        'duration for a move event not greater than 0')

    # Ultrasonic distance reading returns a distance
    @patch('hardware.engine.GPIO.input', side_effect=mock_gpio_input)
    def test_get_us_distance(self, mock_gpio):
      reported_distance = self.engine.get_us_distance()
      self.assertIsInstance(reported_distance, float)
      self.assertLess(reported_distance, math.inf,
                        'reported distance is not non-infinite or non-float, when object present')

    # An infinite distance measurement times out and returns infinity
    @patch('hardware.engine.GPIO.input', side_effect=mock_gpio_infinite)
    def test_long_us_distance(self, mock_gpio):
      reported_distance = self.engine.get_us_distance()
      self.assertTrue(reported_distance == math.inf,
                        'distance is not infinite when no object in front of sensor')

    # # get_image returns an image of type ImageData (raw image)
    def test_get_image(self):
      raw_image = self.engine.get_image()
      self.assertIsInstance(raw_image, ImageData,
                        'raw image returned is not of type ImageData')
    
    # When issued a go_straight command the time taken has <1% error
    def test_go_straight_time(self):
      measured_time = measure_time_for_fn(self.engine.go_straight)
      expected_time = self.engine.move_duration
      error = percent_error(measured_time, expected_time) 
      self.assertLessEqual(error, .1,
                        'time taken to move straight is not as expected; percent error too high')

    # When issued a go_left command the time taken has <1% error
    def test_go_left_time(self):
      measured_time = measure_time_for_fn(self.engine.go_left)
      expected_time = self.engine.move_duration
      error = percent_error(measured_time, expected_time) 
      self.assertLessEqual(error, .1,
                        'time taken to move left is not as expected; percent error too high')

    # When issued a go_right command the time taken has <1% error
    def test_go_right_time(self):
      measured_time = measure_time_for_fn(self.engine.go_right)
      expected_time = self.engine.move_duration
      error = percent_error(measured_time, expected_time) 
      self.assertLessEqual(error, .1,
                        'time taken to move right is not as expected')

    # When issued a go_straight command, RPi straight called
    @patch('hardware.engine.GPIO.output')
    def test_go_straight_command(self, mock_gpio):
      print(mock_gpio)
      self.engine.go_straight()
      mock_gpio.assert_called_with(131, 0,
                        'forward command did not touch expected RPi pin')
      
    # # When issued a go_right command, RPi right + straight called
    # def test_go_right_command(self):
    #   self.engine.go_right()
    #   self.assertTrue(RPi.GPIO.call_count == 2,
    #                     'expected two pins to be activated, but only one was')
    #   expected_calls = [call(13, 0), call(7, 0)]
    #   self.assertTrue(RPi.GPIO.mock_calls == expected,
    #                     'right command did not touch expected RPi pins')

    # # When issued a go_left command, RPi left + straight called
    # def test_go_left_command(self):
    #   self.engine.go_left()
    #   self.assertTrue(RPi.GPIO.call_count == 2,
    #                     'expected two pins to be activated, but only one was')
    #   expected_calls = [call(13, 0), call(11, 0)]
    #   self.assertTrue(RPi.GPIO.mock_calls == expected,
    #                     'left command did not touch expected RPi pins')

def measure_time_for_fn(function):
  start_time = time.time()
  function()
  end_time = time.time()
  return end_time - start_time

def percent_error(a, b):
  return abs(a - b) / b