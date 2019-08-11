from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import random

import sys
sys.path.append('../..')
from hardware import image_data


class Transform():
  """
    Abstract Base class for transform classes, that perform image transformation (such as
    flipping, blurring, sharpening, and brightening)
  """
  @property
  def FILE_INFIX(self):
    raise NotImplementedError("Child classes should define file infixes")
  
  def get_transformed_label(self, original_label):
    return original_label

  def get_histogram_filename(self, idx, original_label):
    """ Returns string of filename to use for histogram for transformed file """
    file_label = self.get_transformed_label(original_label)
    return "%s_%s_H_%s.jpg" % (str(idx), self.FILE_INFIX, file_label)

  def get_image_filename(self, idx, original_label):
    """ Returns string of filename to use for histogram for transformed file """
    file_label = self.get_transformed_label(original_label)
    return "%s_%s_I_%s.jpg" % (str(idx), self.FILE_INFIX, file_label)


class TransformOriginal(Transform):
  """ Does no transformation but returns pil_image and a copy as ImageData object """
  
  @property
  def FILE_INFIX(self):
    return "O"

  def transform(self, pil_image):
    """ Does actual transformation of image (which is nothing) """
    return pil_image


class TransformFlip(Transform):
  """ Flips image horizontally """
  
  @property
  def FILE_INFIX(self):
    return "F"

  FLIPPED_DIRS = { 'R': 'L', 'L': 'R', 'F': 'F' }

  def transform(self, pil_image):
    """ Does actual transformation of image (which is flip horizontally) """
    flipped_pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    return flipped_pil_image

  def get_transformed_label(self, original_label):
    return self.FLIPPED_DIRS[original_label]

    
class TransformBlur(Transform):
  """ Blurs an image """

  @property
  def FILE_INFIX(self):
    return "B"

  BLUR_RADIUS = 1.5

  def transform(self, pil_image):
    """ Does actual transformation of image (add blur) """
    blurred_pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=self.BLUR_RADIUS))
    return blurred_pil_image


class TransformBlurFlip(Transform):
  """ Flips image horizontally and blurs """
  
  @property
  def FILE_INFIX(self):
    return "L"

  FLIPPED_DIRS = { 'R': 'L', 'L': 'R', 'F': 'F' }
  BLUR_RADIUS = 1.5

  def transform(self, pil_image):
    """ Does actual transformation of image (which is flip horizontally) """
    flipped_pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    blurred_pil_image = flipped_pil_image.filter(ImageFilter.GaussianBlur(radius=self.BLUR_RADIUS))
    return blurred_pil_image

  def get_transformed_label(self, original_label):
    return self.FLIPPED_DIRS[original_label]


class TransformSharpen(Transform):
  """ Sharpens an image """

  @property
  def FILE_INFIX(self):
    return "S"

  def transform(self, pil_image):
    """ Does actual transformation of image (apply unsharpmask) """
    sharpened_pil_image = pil_image.filter(ImageFilter.UnsharpMask)
    return sharpened_pil_image


class TransformSharpenFlip(Transform):
  """ Flips image horizontally and sharpens """
  
  @property
  def FILE_INFIX(self):
    return "H"

  FLIPPED_DIRS = { 'R': 'L', 'L': 'R', 'F': 'F' }

  def transform(self, pil_image):
    """ Does actual transformation of image (which is flip horizontally) """
    flipped_pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_pil_image = flipped_pil_image.filter(ImageFilter.UnsharpMask)
    return flipped_pil_image

  def get_transformed_label(self, original_label):
    return self.FLIPPED_DIRS[original_label]


class TransformBrighten(Transform):
  """ Brightens an image """
  @property
  def FILE_INFIX(self):
    # Infix is used for determining file path. 'R', as 
    return "R"

  def transform(self, pil_image):
    """ Does actual transformation of image (blur image) """
    brightness_factor = random.choice([0.5, 1.5])

    brightened_pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness_factor)
    return brightened_pil_image


class TransformBrightenFlip(Transform):
  """ Flips image horizontally and sharpens """
  
  @property
  def FILE_INFIX(self):
    return "G"

  FLIPPED_DIRS = { 'R': 'L', 'L': 'R', 'F': 'F' }

  def transform(self, pil_image):
    """ Does actual transformation of image (which is flip horizontally) """
    brightness_factor = random.choice([0.5, 1.5])
    blurred_pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness_factor)
    flipped_pil_image = blurred_pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    return flipped_pil_image

  def get_transformed_label(self, original_label):
    return self.FLIPPED_DIRS[original_label]
