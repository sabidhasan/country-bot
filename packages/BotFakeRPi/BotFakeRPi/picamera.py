import numpy as np

class PiCamera(object):
	"""Fake class"""
	def __init__(self, resolution=(256,256)):
		self.array = np.random.rand(*resolution)

	def close(self):
		pass

	def start_preview(self):
		pass

	def capture(self, image, format=None, use_video_port=None, *args, **kwargs):
		return str(self.array)