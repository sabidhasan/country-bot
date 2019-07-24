import numpy as np
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

class ImageData(object):
  """
    Used for storing image data from car camera.
  """
  def __init__(self, raw_image):
    """ Raw image is numpy array from PiCamera stream capture in RGB format """
    self.image = raw_image

  @property
  def height(self):
    return np.shape(self.image)[0]

  @property
  def width(self):
    return np.shape(self.image)[1]

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

  def suggested_histogram_luminosity(self):
    """ Retuns suggested luminosity for generating a histogram effective for finding roads """
    # Calc. sum of all pixels; since histograms are only bottom 1/2, discard top half
    pixel_sum = np.sum(self.image[ self.height // 2 : ])
    # The sum is fitted to an empirical formula, which was calculated for 320 width x 240 height
    # Scale sum if current img dimensions are different
    pixel_sum *= (320 / self.width) * (240 / self.height)
    # Determine suggested luminosity
    return 0.9795224 - (0.8033605 / (1+((pixel_sum/17160920)**2.708226)))

  def histogram(self, output='numpy', luminescence_threshold=None):
    """
      Generates a histogram representation of the image in specified format,
      with binary pixels that are filtered based on specified luminescence threshold.
      Throws out the top half of image, as that is not useful in making predictions.

      output: [ "numpy", "base64", "ImageData" ]
      luminescence_threshold: <int, optional> 0 to 1, automatically selected if omitted
    """

    if output not in ['numpy', 'base64', 'ImageData']:
      raise TypeError('unexpected output format %s' % str(output))

    if luminescence_threshold is None:
      luminescence_threshold = self.suggested_histogram_luminosity()
      print('no lumin thresh. using %s' % str(luminescence_threshold))

    if not(0 < luminescence_threshold <= 1):
      raise ValueError('luminescence_threshold not in range 0 to 1.')
  
    # Remove top half of image
    image = self.image[ self.height // 2 : ]
    # Multiply by luminescence coefficients
    image = image * np.array([0.299, 0.587, 0.114])
    # Sum RGBs to get total luminesence value, and normalize to 0 to 1 scale
    image = np.sum(image, axis=2)
    image = np.multiply(image, 1 / 256)
    # Create array of True/False based on threshold
    booleanized = image > luminescence_threshold
    
    # Make array of 0s, and fill with 1s based on booleanized above
    zeros = np.zeros_like(image)
    zeros[booleanized] = 1

    if output == 'numpy':
      return zeros
    elif output == 'ImageData':
      return ImageData(zeros)
    else:
      buffered = BytesIO()
      plt.imshow(zeros)
      plt.savefig(buffered, format='jpg')
      return base64.b64encode(buffered.getvalue())
