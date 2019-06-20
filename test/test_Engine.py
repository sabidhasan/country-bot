import unittest
import time
from hardware.engine import Engine
from helpers.image_data import ImageData

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = Engine()

    # Defines a revolutions per move constant
    def test_revs_per_move(self):
      self.assertIsInstance(self.engine.revolutions_per_move, float,
                        'tire revolutions per move is not a number')

    # Defines a move_duration
    def test_move_duration(self):
      self.assertIsInstance(self.engine.move_duration, float,
                        'duration for a move event is not a number')

    # Ultrasonic distance reading returns a distance
    def test_get_us_distance(self):
      reported_distance = self.engine.get_us_distance()
      self.assertIsInstance(reported_distance, float,
                        'reported distance is not a float')

    # get_image returns an image of type ImageData (raw image)
    def test_get_image(self):
      raw_image = self.engine.get_image()
      self.assertIsInstance(reported_distance, ImageData,
                        'reported distance is not a float')
    
    # When issued a go_straight command the time taken has <1% error
    def test_go_straight(self):
      measured_time = measure_time_for_fn(self.engine.go_straight)
      expected_time = self.engine.move_duration
      error = percent_error(measured_time, expected_time) 
      self.assertTrue(error < .01,
                        'time taken to move is not as expected')



    
    # When isseud a go_left command, it lasts ~move_duration length
    # When isseud a go_right command, it lasts ~move_duration length
    # When issued a go_straight command, RPi straight called
    # When issued a go_right command, RPi right + straight called
    # When issued a go_left command, RPi left + straight called


    # def test_distance_travelled(self):
    #     self.assertEqual(self.car.get_distance_travelled(), 0,
    #                     'initial distance is not reported as 0')


def measure_time_for_fn(function):
  start_time = time.time()
  function()
  end_time = time.time()
  return end_time - start_time

def percent_error(a, b):
  return abs(a - b) / b