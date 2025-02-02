# This module generates data for training the neural network and for generating
# background images for training the Haar classifier for stop sign detection.

# It gathers training data from a database generated by the car server and:
# - Performs transformations on each data point
# - Writes resulting histogram and image to disk
# - Saves the data in text format, that can be used to train the neural network

# Included transfomation classes are:
# - Original (do nothing)
# - Flip horizontal
# - Blur
# - Sharpen,
# - Brighten

import time
import os

from helpers import read_sqlite_db, get_saved_data_from_row, transform_and_save_img, save_augmented_data
from transformers import TransformOriginal, TransformFlip, TransformBlur, TransformSharpen, \
  TransformBrighten, TransformBlurFlip, TransformSharpenFlip, TransformBrightenFlip

# Allow importing image data class from parent directory
import sys
sys.path.append('../..')
from hardware import image_data


class Augmenter():
  """
    Main class for dealing  training
    Augments raw training data from car into data that can be used for training
    both Haar (Stopsign detection) and CNN (Self driving) algorithms
  """
  
  IMAGE_DIR = "Augmented Images"

  def __init__(self, path, transformation_classes=[]):
    self.db_path = path

    print("[TRAINING_DATA] Attempting to read the database from %s" % self.db_path)
    self.raw_data = read_sqlite_db(self.db_path)
    print("[TRAINING_DATA] Loaded %s records" % len(self.raw_data))

    # Create Augmented Images directory if needed
    if not os.path.exists(self.IMAGE_DIR):
      os.mkdir(self.IMAGE_DIR)

    # transfomation_classes are applied to augment each image
    if len(transformation_classes) == 0:
      raise TypeError("No transformation classes given")

    self.transformation_classes = transformation_classes


  def augment_data(self, save_text_output, save_histogram):
    """
      Parses data from self.raw_data into usable data, while augmenting
      Writes text output to disk if <save_text_output> Bool is True.
      Writes graphical histogram to JPG if save_histogram is False
    """
    
    if len(self.raw_data) == 0:
      print("[TRAINING_DATA] No training data exists. The database may be empty.")

    image_data = []
    # Loop through data, and add label and histogram
    for idx, row in enumerate(self.raw_data):
      row_idx = row[0]
      print("[TRAINING_DATA] Processing image %s of %s" % (idx + 1, len(self.raw_data)))

      # Original image - get saved image in PIL, ImageData format and label
      (db_pil_image, training_label) = get_saved_data_from_row(row)

      # Apply each transformation
      for transform_class in self.transformation_classes:
        data = transform_and_save_img(db_pil_image, transform_class, \
          self.IMAGE_DIR, row_idx, training_label, save_histogram)
        image_data.append(data)

    if save_text_output == True:
      try:
        data_file_path = os.path.join(self.IMAGE_DIR, "_data%s.pkl" % round(time.time()))
        save_augmented_data(image_data, data_file_path)
        print("[TRAINING_DATA] Wrote training data results to %s" % data_file_path)
      except:
        print("[TRAINING_DATA] Could not write training data to disk")
    
    print("[TRAINING_DATA] Done. Transformed %s images into %s" % (len(self.raw_data), len(image_data)))
    return image_data

# labels = np.array(labels)
# data = np.array(data)

if __name__ == '__main__':
  transformation_classes = [
    TransformOriginal, TransformFlip, TransformBlur, TransformSharpen, TransformBrighten
  ]

  try:
    path = sys.argv[1]
  except:
    path = "../../webserver/trainingdata.db"

  augmenter = Augmenter(path=path, transformation_classes=transformation_classes)

  # Augment all images. Saving histogram is slow, and they are only for the
  # end user, so generating them is omitted here.
  data = augmenter.augment_data(save_text_output=True, save_histogram=True)