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
    # img_data_image = image_data.ImageData(np.array(pil_image))
    # return (img_data_image, pil_image)
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
    # flipped_img_data_image = image_data.ImageData(np.array(flipped_pil_image))
    # return (flipped_img_data_image, flipped_pil_image)
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
    # blurred_img_data_image = image_data.ImageData(np.array(blurred_pil_image))
    # return (blurred_img_data_image, blurred_pil_image)
    return blurred_pil_image


class TransformSharpen(Transform):
  """ Sharpens an image """

  @property
  def FILE_INFIX(self):
    return "S"

  def transform(self, pil_image):
    """ Does actual transformation of image (apply unsharpmask) """
    sharpened_pil_image = pil_image.filter(ImageFilter.UnsharpMask)
    # sharpened_img_data_image = image_data.ImageData(np.array(sharpened_pil_image))
    # return (sharpened_img_data_image, sharpened_pil_image)
    return sharpened_pil_image


class TransformBrighten(Transform):
  """ Brightens an image """
  @property
  def FILE_INFIX(self):
    # Infix is used for determining file path. 'R', as 
    return "R"

  def transform(self, pil_image):
    """ Does actual transformation of image (blur image) """
    brightness_factor = random.choice([0.5, 1.5])

    blurred_pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness_factor)
    # blurred_img_data_image = image_data.ImageData(np.array(blurred_pil_image))
    # return (blurred_img_data_image, blurred_pil_image)
    return blurred_pil_image
