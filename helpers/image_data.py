class ImageData(object):
  """
    Used for storing image data from car camera.
  """

  def __init__(self, raw_image):
    """ Raw image is numpy array from PiCamera stream capture in RGB format """
    self.raw_image = raw_image
    self.working_image = raw_image
    
    self.colored = True


# method  desaturate
# method  histogram
# method  to base64
# method  save_to_disk
# attrib  width
# attrib  height
