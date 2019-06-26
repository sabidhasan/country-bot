import unittest
import random
import math
from unittest.mock import Mock, MagicMock, call, patch
from helpers.image_data import ImageData
from helpers.os import set_environ
from helpers.testing_tools import measure_time_for_fn, percent_error, \
  get_activated_pin_ids_from_calls

# Set testing environment so Engine imports fake RPi modules
set_environ("TESTING")
import hardware.engine as Engine


def mock_gpio_input(RPi_pin_number):
  """ The mock input function randomly decides when it has it an object a pulse from ultrasonic sensor """
  return random.random() > 0.9

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
    
    # When issued a go_straight command the time taken has <20s% error
    def test_go_straight_time(self):
      measured_time = measure_time_for_fn(self.engine.go_straight)
      expected_time = self.engine.move_duration
      error = percent_error(measured_time, expected_time) 
      self.assertLessEqual(error, .2,
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

    # When issued a go_straight command, RPi straight pin is activated
    @patch('hardware.engine.GPIO.output')
    def test_go_straight_command(self, mock_gpio):
      expected_pins = [13]
      self.engine.go_straight()
      # Get what pins were activated from calls to GPIO.output function
      actual_activated_pins = get_activated_pin_ids_from_calls(mock_gpio.call_args_list)
      self.assertEqual(sorted(actual_activated_pins), sorted(expected_pins))

    # When issued a go_left command, RPi left + straight pins are activated
    @patch('hardware.engine.GPIO.output')
    def test_go_left_command(self, mock_gpio):
      expected_pins = [11, 13]
      self.engine.go_left()
      # Get what pins were activated from calls to GPIO.output function
      actual_activated_pins = get_activated_pin_ids_from_calls(mock_gpio.call_args_list)
      self.assertEqual(sorted(actual_activated_pins), sorted(expected_pins))

    # When issued a go_right command, RPi right + straight called
    @patch('hardware.engine.GPIO.output')
    def test_go_right_command(self, mock_gpio):
      expected_pins = [7, 13]
      self.engine.go_right()
      # Get what pins were activated from calls to GPIO.output function
      actual_activated_pins = get_activated_pin_ids_from_calls(mock_gpio.call_args_list)
      self.assertEqual(sorted(actual_activated_pins), sorted(expected_pins))
