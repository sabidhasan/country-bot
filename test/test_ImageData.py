import unittest
import os
from unittest.mock import Mock, MagicMock, seal
import numpy as np
from PIL import Image

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

    # Test width and height attributes
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
    
    def test_suggested_histogram_luminosity(self):
      # Suggests correct histogram luminosity (based on bottom half of the image)
      mocked_camera_input = get_mocked_camera_input()
      bottom_half_sum = np.sum(mocked_camera_input[128 : ])
      # Adjust the sum for image height/width of test image
      height_factor, width_factor = (240 / 256), (320 / 256)
      adjusted_sum = bottom_half_sum * height_factor * width_factor
      expected_luminosity = (0.9795224 - (0.8033605 / (1+((adjusted_sum/17160920)**2.708226))))
      actual_luminosity = self.image.suggested_histogram_luminosity()
      
      self.assertEqual(expected_luminosity, actual_luminosity,
                          'expected luminosity does not equal calculated luminosity')

    def test_histogram_with_format(self):
      # Throws error when unexpected format passed
      self.assertRaises(TypeError, self.image.histogram, format='jpeg')
    
    def test_histogram_with_lumin(self):
      # Throws error when unexpected luminescence_threshold is invalid
      self.assertRaises(ValueError, self.image.histogram, luminescence_threshold=1.1)

    def test_histogram(self):
      # Tests if produced histogram matches expected value
      LUMINESCENCE_THRESHOLD = 0.5
      expected_histogram = []

      # Get bottom half of mock image
      mocked_camera_input = get_mocked_camera_input()[128 : ]
      for row in mocked_camera_input:
        expected_histogram.append([])
        for rgb in row:
          # Use luminescence formula and threshold to set "boolean" value
          (r, g, b) = rgb[0], rgb[1], rgb[2]
          curr_lumin = ((r * 0.299) + (g * 0.587) + (b * 0.114)) / 256
          expected_histogram[-1].append(1.0 if curr_lumin > LUMINESCENCE_THRESHOLD else 0.0)
      expected_histogram = np.array(expected_histogram)
      
      actual_histogram = self.image.histogram(luminescence_threshold=LUMINESCENCE_THRESHOLD)
      
      self.assertTrue(np.array_equal(expected_histogram, actual_histogram), "Not equal")
