import time
import unittest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from helpers.os import set_environ

# Set testing environment so Engine imports fake RPi modules
set_environ("TESTING")
from hardware.camera import Camera

se = Mock()

class CameraTests(unittest.TestCase):
  # Since the Camera class sets camera as a class level property, setUp doesn't seem
  # to work here - instantiating a new class doesn't clear its class attributes

  def tearDown(self):
    Camera.camera = None

  def test_frame(self):
    camera = Camera()
    self.assertEqual(camera.frame, None, 'frame is defined before data acquired')

  # Invalid resolution raises error
  def test_invalid_resolution(self):
    self.assertRaises(ValueError, Camera, width = 22, height = 22)

  # Test resolution
  def test_resolution(self):
    camera = Camera(width=999, height=999)
    self.assertEqual(camera.width, 999)

