import numpy as np
import base64
from io import BytesIO
from PIL import Image

class ImageData(object):
  """
    Used for storing image data from car camera.
  """
  def __init__(self, raw_image):
    """ Raw image is numpy array from PiCamera stream capture in RGB format """
    self.image = raw_image

  @property
  def height(self):
    return np.shape(self.image)[1]

  @property
  def width(self):
    return np.shape(self.image)[0]

  def save_to_disk(self, file_name):
    """ Saves the image to disk at the specified path in JPEG format """

    if not file_name.endswith('.jpg'):
      raise TypeError('Non JPG formats not supported.')

    image = Image.fromarray(self.image)
    image.save(file_name, format='JPEG')

  def save_desaturated(self, file_name):
    """ Saves a desaturated copy of the image """

    if not file_name.endswith('.jpg'):
      raise TypeError('Non JPG formats not supported.')
    image = Image.fromarray(self.image).convert('L')
    image.save(file_name, format='JPEG')

  def tobase64(self):
    """ Gets base64 representation of the image """

    # Create a PIL image and save into IO buffer
    buffered = BytesIO()
    image = Image.fromarray(self.image)
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())

  def column_histogram(self):
    """
      Generates a columnar histogram; returns an array, which lists the total number of pixels
      in each column that are considered 'bright'.
      Brightness is measured with formula:  b = sqrt((0.241R)**2+ (0.691G)**2 + (0.0678B)**2)
    """
    col_brightnesses = []
    # Loop thru each column
    for i in range(self.width):
      # Get current column's pixels as an array (array contains arrays of [R,G,B] values)
      current_column = self.image[:,i,:]
      # determine how many pixel arrays in this column are 'bright'
      bright_pixels_in_curr_column = 0
      for p in current_column:
        if self.pixel_brightness(p) > 128: bright_pixels_in_curr_column += 1
      
      col_brightnesses.append(bright_pixels_in_curr_column)

    return np.array(col_brightnesses)

  @staticmethod
  def pixel_brightness(pixel):
    return ((.241*pixel[0]**2) + (.691*pixel[1]**2) + (.068*pixel[2]**2))**.5
