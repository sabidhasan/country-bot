import numpy as np
import pkgutil

def get_flat_array():
	""" Returns fake image data, a flattened numpy array """
	raw_data = pkgutil.get_data('BotFakeRPi', 'fake_image.npy')
	# First 128 are useless - numpy.load discards them automatically, but frombuffer reads 
	# the data in its entirety, so we ignore the first 128 manually here.
	return np.frombuffer(raw_data, dtype=np.uint8)[128:]

class PiCamera(object):
	""" Fake class for mocking PiCamera """
	def __init__(self, resolution=(256,256, 3)):
		self.resolution = resolution
		self.rotation = 0
		flat_array = get_flat_array()
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