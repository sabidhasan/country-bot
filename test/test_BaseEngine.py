import unittest
import random
import math
from unittest.mock import Mock, MagicMock, call, patch
from helpers.os import set_environ
from helpers.testing_tools import measure_time_for_fn, percent_error, \
  get_activated_pin_ids_from_calls

# Set testing environment so Engine imports fake RPi modules
set_environ("TESTING")
import hardware.engine_base


def mock_gpio_input(RPi_pin_number):
  """ The mock input function randomly decides when it has it an object in front of it """
  return random.random() > 0.9


def mock_gpio_infinite(RPi_pin_number):
  """ This RPi will never report the echo coming back, so should time out """
  return 0



class MockEngine(hardware.engine_base.BaseEngine):
  """
    BaseEngine class cannot be directly instantiated, so this represents
     a mock engine that is a subclass of BaseEngine.
  """
  def __init__(self, ultrasonic_timeout):
    super().__init__(ultrasonic_timeout)


class BaseEngineTests(unittest.TestCase):
    def setUp(self):
      self.engine = MockEngine(1000)


    # Raises error when directly instantiated 
    def test_raises_not_implemented_error(self):
      self.assertRaises(NotImplementedError, hardware.engine_base.BaseEngine, 0)


    # Defines an ultrasonic sensor timeout
    def test_us_timeout(self):
      # self.engine = MockEngine(1000)
      self.assertEqual(self.engine.ultra_sonic_sensor_timeout, 1000)


    # When _engine_instantated is True, it doesn't reinitialize the engine
    def test_engine_initializes_once(self):
      mock_engine = MagicMock()
      hardware.engine_base._engine_initialized = True
      hardware.engine_base.BaseEngine.initialize_engine = mock_engine
      MockEngine(1000)
      self.assertEqual(len(mock_engine.mock_calls), 0)


    # Ultrasonic distance reading returns a distance
    @patch('hardware.engine_base.GPIO.input', side_effect=mock_gpio_input)
    def test_get_us_distance(self, mock_gpio):
      reported_distance = self.engine.get_us_distance()
      self.assertIsInstance(reported_distance, float)
      self.assertLess(reported_distance, math.inf,
                        'reported distance is not non-infinite or non-float, when object present')


    # An infinite distance measurement times out and returns infinity
    @patch('hardware.engine_base.GPIO.input', side_effect=mock_gpio_infinite)
    def test_long_us_distance(self, mock_gpio):
      reported_distance = self.engine.get_us_distance()
      self.assertEqual(reported_distance, math.inf,
                        'distance is not infinite when no object in front of sensor')
