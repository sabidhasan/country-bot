import numpy as np

class PiCamera(object):
	""" Fake class for mocking PiCamera """
	def __init__(self, resolution=(256,256, 3)):
		self.resolution = resolution
		flat_array = np.load('../test/test_images/image_banana_color_raw.npy')
		self.array = flat_array.reshape(256, 256, 3)

	def close(self):
		pass

	def start_preview(self):
		pass

	def capture(self, image, format=None, use_video_port=None, *args, **kwargs):
		# Image is an instance of class array below
		image.array = self.array

class array(object):
	""" Fake class for mocking picamera.array """
	
	def __init__(self):
		# The array (which represents cam data), is set later from PiCamera.capture(<this object>)
		self.array = None

	@staticmethod
	def PiRGBArray(camera):
		"""
			This method is called directly from outside the class to instantiate it.
			PiCamera.array is actually another module, but here it is creatively faked.
		"""
		return array()