import time
import numpy as np

def measure_time_for_fn(function):
  start_time = time.time()
  function()
  end_time = time.time()
  return end_time - start_time

def percent_error(a, b):
  return abs(a - b) / b

def get_activated_pin_ids_from_calls(call_args_list):
  """
    Gets a list calls from the Patch object, and converts them to a list of IDs generated
  """
  # Map extracts tuples of arguments for each call, from 'calls' object
  call_arguments = map(lambda x: x[0], call_args_list)
  # Filter for pins that were actually called with True (ie. activated)
  activated_pins = filter(lambda x: x[1] == True, call_arguments)
  # Map only first argument - this is the pin that was activated
  return list(map(lambda x: x[0], activated_pins))


def get_all_pin_ids_from_calls(call_args_list):
  """
    Gets a list all calls from the Patch object, and converts them to a list of IDs generated
  """
  # Map extracts tuples of arguments for each call, from 'calls' object
  return list(set(map(lambda x: x[0][0], call_args_list)))


def get_mocked_camera_input():
  """ Loads raw camera numpy array for testing purposes """
  # The np.save function doens't play nicely with 3D arrays, so we stored it 
  # flat, and reshape it upon load
  flat_array = np.load('test/test_images/image_banana_color_raw.npy')
  return flat_array.reshape(256, 256, 3)