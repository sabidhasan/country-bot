import unittest
from unittest.mock import Mock, MagicMock, call, patch
from helpers.os import set_environ
from helpers.testing_tools import measure_time_for_fn, percent_error, \
  get_activated_pin_ids_from_calls, get_all_pin_ids_from_calls

# Set testing environment so Engine imports fake RPi modules
set_environ("TESTING")
import hardware.engine_self_driving


class SelfDrivingEngineTests(unittest.TestCase):
    @patch('hardware.engine_self_driving.GPIO.PWM')
    def setUp(self, mock_gpio):
      self.engine = hardware.engine_self_driving.SelfDrivingEngine()


    @patch('hardware.engine_self_driving.GPIO.output')
    def test_turn_wheels_left(self, mock_gpio):
      self.engine.turn_wheels_left()
      actual_activated_pins = get_activated_pin_ids_from_calls(mock_gpio.call_args_list)
      self.assertTrue(11 in actual_activated_pins, 'Pin 11 was not activated, as expected')


    @patch('hardware.engine_self_driving.GPIO.output')
    def test_turn_wheels_right(self, mock_gpio):
      self.engine.turn_wheels_right()
      actual_activated_pins = get_activated_pin_ids_from_calls(mock_gpio.call_args_list)
      self.assertTrue(7 in actual_activated_pins, 'Pin 7 was not activated')


    @patch('hardware.engine_self_driving.GPIO.output')
    def test_turn_wheels_forward(self, mock_gpio):
      expected_calls = [call(11, False), call(7, False)]
      self.engine.turn_wheels_forward()

      all_called = [call in mock_gpio.call_args_list for call in expected_calls]
      self.assertTrue(all_called, 'All expected calls were not called')


    def test_start_continuous_move(self):
      expected_duty_cycle = 30
      self.engine.start_continuous_move()
      first_call = self.engine.pwm.start.call_args_list[0][0][0]
      self.assertEqual(first_call, expected_duty_cycle, 'Expected duty cycle not used for PWM')


    def test_stop_all_motion(self):
      self.engine.stop_all_motion()
      call_count = len(self.engine.pwm.stop.call_args_list)
      self.assertEqual(call_count, 1)
