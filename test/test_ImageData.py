import unittest
import os
from unittest.mock import Mock, MagicMock, seal
import numpy as np

from hardware.image_data import ImageData
from helpers.testing_tools import get_mocked_camera_input


class ImageDataTests(unittest.TestCase):
    def setUp(self):
      # Known image (numpy array)
      raw_camera_data = get_mocked_camera_input()
      self.image = ImageData(raw_camera_data)

    def tearDown(self):
      for filename in ['test/test_images/test_color.jpg', 'test/test_images/test_desaturated.jpg']:
        try:
          os.remove(filename)
        except FileNotFoundError:
          # Test must have failed, so no file was created
          continue

    # # Test width and height attributes
    def test_height(self):
      self.assertEqual(self.image.height, 256,
                        'height does not equal expected value')

    def test_width(self):
      self.assertEqual(self.image.width, 256,
                        'width does not equal expected value')

    def test_save_to_disk(self):
      with open('test/test_images/image_banana_color.jpg', 'rb') as f:
        expected_color_image = f.read()
      self.image.save_to_disk('test/test_images/test_color.jpg')
      with open('test/test_images/test_color.jpg', 'rb') as f:
        actual_color_image = f.read()
      self.assertEqual(expected_color_image, actual_color_image,
                        'saved image does not match expected image')

    def test_desaturate(self):
      with open('test/test_images/image_banana_bw.jpg', 'rb') as f:
        expected_bw_image = f.read()
      self.image.save_desaturated('test/test_images/test_desaturated.jpg')
      with open('test/test_images/test_desaturated.jpg', 'rb') as f:
        actual_bw_image = f.read()
      self.assertEqual(expected_bw_image, actual_bw_image,
                        'after desaturation, the image does not match expected value')

    def test_base64(self):
      with open('test/test_images/image_banana_b64.bin', 'rb') as f:
        expected_b64 = f.read()
      actual_b64 = self.image.tobase64()
      self.assertEqual(actual_b64, expected_b64, 
                        'base 64 string does not equal expected string')
    
    def test_column_histogram(self):
      actual_histogram = self.image.column_histogram()
      expected_histogram = np.load('test/test_images/image_banana_color_histogram.npy')
      self.assertEqual(np.array_equal(expected_histogram, actual_histogram), True,
                        'expected histrogram did not match the produced histogram')