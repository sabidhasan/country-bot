from PIL import Image, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import random
import pickle
import base64
import io
import os

# This module gathers training data from the car's database and:
# 1. writes it to disk
# 2. flips it, and writes it to disk
# 3. adds noise, and writes it to disk
# 4. changes brightness (up or down depending on existing brightness), and writes it to disk
# 5. writes all of the above's trained outcome (Forward, Right, Left)

# This data is used for training the neural network and
# generating backgrounds images for the Haar classifier

# Allow importing image data class
import sys
sys.path.append('../..')
from hardware import image_data

def get_saved_image_and_label_from_row(row):
  """
    Receives a row from training database, and returns corresponding label
    and corresponding ImageData object.
  """
  if row[4] == 1:
    label = 'F'
  elif row[5] == 1:
    label = 'R'
  elif row[6] == 1:
    label = 'L'
  else:
    raise ValueError("Row has malformed command")

  raw_image_data = io.BytesIO(row[2])
  saved_image_data = pickle.load(raw_image_data)

  return (saved_image_data, label)


def transform_original_img_and_save(pil_image, idx, label):
  """
    Recieves a PIL image (eg. from DB), an index and a label, and:
    1. Saves the original image to disk
    2. Saves original image's histogram (from matplotlib.pyplot) to disk
    3. Returns label and histogram
  """
  # Will save original to /<index>_<original>_<image/histogram>_<label>.jpg
  image_data_img = image_data.ImageData(np.array(pil_image))

  # Save original in jpeg format
  original_image_filename = "Augmented Images/%s_O_I_%s.jpg" % (str(idx), label)
  pil_image.save(original_image_filename)
  
  # Save original histogram, b64 image representation (using matplotlib.pyplot)
  original_histogram_2d_b64 = image_data_img.histogram(output="base64")
  original_histogram_filename = "Augmented Images/%s_O_H_%s.jpg" % (str(idx), label)
  with open(original_histogram_filename, "wb") as f:
    f.write(base64.decodebytes(original_histogram_2d_b64))

  # Get flattened original histogram
  original_histogram = image_data_img.histogram().flatten()

  # Return dictionary with index and label
  ret = {
    "index": idx, "label": label, "histogram": original_histogram, 
    "img_file": original_image_filename, "hist_file": original_histogram_filename
  }
  return ret


def transform_flipped_img_and_save(pil_image, idx, label):
  """
    Recieves a PIL image (eg. from DB), an index and a label, and:
    0. Flips the image
    1. Saves the flipped image to disk
    2. Saves flipped image's histogram (from matplotlib.pyplot) to disk
    3. Returns flipped label and histogram
  """
  # Flip the image
  pil_flipped = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
  image_data_flipped = image_data.ImageData(np.array(pil_flipped))

  # Get flipped image direction
  flipped_dirs = { 'R': 'L', 'L': 'R', 'F': 'F' }
  flipped_label = flipped_dirs[label]
  
  # Save flipped to /<index>_<flipped>_<image/histogram>_<label>.jpg
  flipped_image_filename = "Augmented Images/%s_F_I_%s.jpg" % (str(idx), flipped_label)
  pil_flipped.save(flipped_image_filename)

  # Save flipped histogram, b64 image representation (using matplotlib.pyplot)
  flipped_histogram_2d_b64 = image_data_flipped.histogram(output="base64")
  flipped_histogram_filename = "Augmented Images/%s_F_H_%s.jpg" % (str(idx), flipped_label)
  with open(flipped_histogram_filename, "wb") as f:
    f.write(base64.decodebytes(flipped_histogram_2d_b64))

  # Get  flipped histogram
  flipped_histogram = image_data_flipped.histogram().flatten()

  # Return dictionary with index and label
  ret = {
    "index": idx, "label": flipped_label, "histogram": flipped_histogram, 
    "img_file": flipped_image_filename, "hist_file": flipped_histogram_filename
  }
  return ret


def transform_blurred_img_and_save(pil_image, idx, label):
  """
    Recieves a PIL image (eg. from DB), an index and a label, and:
    0. Blurs the image
    1. Saves the blurred image to disk
    2. Saves blurred image's histogram (from matplotlib.pyplot) to disk
    3. Returns blurred image's label and histogram
  """
  # Blur the image, based on empirically determined constant
  BLUR_CONSTANT = 51200
  blur_radius = pil_image.size[0] * pil_image.size[1] / BLUR_CONSTANT

  pil_blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
  image_data_blurred = image_data.ImageData(np.array(pil_blurred))

  # Save blurred to /<index>_<blurred>_<image/histogram>_<label>.jpg
  blurred_image_filename = "Augmented Images/%s_B_I_%s.jpg" % (str(idx), label)
  pil_blurred.save(blurred_image_filename)

  # Save blurred histogram, b64 image representation (using matplotlib.pyplot)
  blurred_histogram_2d_b64 = image_data_blurred.histogram(output="base64")
  blurred_histogram_filename = "Augmented Images/%s_B_H_%s.jpg" % (str(idx), label)
  with open(blurred_histogram_filename, "wb") as f:
    f.write(base64.decodebytes(blurred_histogram_2d_b64))

  # Get blurred histogram
  blurred_histogram = image_data_blurred.histogram().flatten()

  # Return dictionary with index and label
  ret = {
    "index": idx, "label": label, "histogram": blurred_histogram, 
    "img_file": blurred_image_filename, "hist_file": blurred_histogram_filename
  }
  return ret


def transform_sharpened_img_and_save(pil_image, idx, label):
  """
    Recieves a PIL image (eg. from DB), an index and a label, and:
    0. Sharpens the image
    1. Saves the sharpened image to disk
    2. Saves sharpened image's histogram (from matplotlib.pyplot) to disk
    3. Returns sharpened image's label and histogram
  """
  # Sharpen the image
  pil_sharpened = pil_image.filter(ImageFilter.UnsharpMask)
  image_data_sharpened = image_data.ImageData(np.array(pil_sharpened))

  # Save sharpened to /<index>_<sharpened>_<image/histogram>_<label>.jpg
  sharpened_image_filename = "Augmented Images/%s_S_I_%s.jpg" % (str(idx), label)
  pil_sharpened.save(sharpened_image_filename)

  # Save sharpened histogram, b64 image representation (using matplotlib.pyplot)
  sharpened_histogram_2d_b64 = image_data_sharpened.histogram(output="base64")
  sharpened_histogram_filename = "Augmented Images/%s_S_H_%s.jpg" % (str(idx), label)
  with open(sharpened_histogram_filename, "wb") as f:
    f.write(base64.decodebytes(sharpened_histogram_2d_b64))

  # Get flattened sharpened histogram
  sharpened_histogram = image_data_sharpened.histogram().flatten()

  # Return dictionary with index and label
  ret = {
    "index": idx, "label": label, "histogram": sharpened_histogram, 
    "img_file": sharpened_image_filename, "hist_file": sharpened_histogram_filename
  }
  return ret


def transform_brightened_img_and_save(pil_image, idx, label):
  """
    Recieves a PIL image (eg. from DB), an index and a label, and:
    0. Brightens the image
    1. Saves the brightened image to disk
    2. Saves brightened image's histogram (from matplotlib.pyplot) to disk
    3. Returns brightened image's label and histogram
  """
  # Pick random brightness, and brighten image
  brightness_factor = random.choice([0.5, 1.5])
  pil_brightened = ImageEnhance.Brightness(pil_image).enhance(brightness_factor)
  image_data_brightened = image_data.ImageData(np.array(pil_brightened))

  # Save brightened to /<index>_<brightened>_<image/histogram>_<label>.jpg
  brightened_image_filename = "Augmented Images/%s_R_I_%s.jpg" % (str(idx), label)
  pil_brightened.save(brightened_image_filename)

  # Save brightened histogram, b64 image representation (using matplotlib.pyplot)
  brightened_histogram_2d_b64 = image_data_brightened.histogram(output="base64")
  brightened_histogram_filename = "Augmented Images/%s_R_H_%s.jpg" % (str(idx), label)
  with open(brightened_histogram_filename, "wb") as f:
    f.write(base64.decodebytes(brightened_histogram_2d_b64))
  
  # Get flattened brightened histogram
  brightened_histogram = image_data_brightened.histogram().flatten()

  # Return dictionary with index and label
  ret = {
    "index": idx, "label": label, "histogram": brightened_histogram, 
    "img_file": brightened_image_filename, "hist_file": brightened_histogram_filename
  }
  return ret


class TrainingData():
  """ Augments raw training data from car into data that can be used for training """
  IMAGE_DIR = "Augmented Images"

  def __init__(self, path=None):
    self.db_path = path if path else "../../webserver/trainingdata.db"

    print("[TRAINING_DATA] Using path '%s' for database" % self.db_path)
    self.raw_data = self.read_db()

    # Create Augmented Images directory if needed
    if not os.path.exists(self.IMAGE_DIR):
      os.mkdir(self.IMAGE_DIR)

  def read_db(self):
    try:
      print("[TRAINING_DATA] Attempting to read the database")
      conn = sqlite3.connect(self.db_path)
      c = conn.cursor()
      c.execute("SELECT * FROM 'training'")
      raw_data = c.fetchall()
      print("[TRAINING_DATA] Loaded %s records" % len(raw_data))
      return raw_data
    except:
      raise TypeError("[TRAINING_DATA] Could not load data from db %s" % self.db_path)

  def parse_and_augment_data(self):
    """ Parses data from self.raw_data into usable data, while augmenting """

    ret = []

    # Loop through data, and add label and histogram
    for idx, row in enumerate(self.raw_data):
      row_idx = row[0]
      print("[TRAINING_DATA] Processing image %s of %s" % (idx + 1, len(self.raw_data)))

      # Original image - get label and DB saved image (as ImageData object)
      original_image_data, label = get_saved_image_and_label_from_row(row)
      # Transform ImageData image into PIL image (used for augmentation)
      original_pil_image = Image.fromarray(original_image_data.image)

      # Original Image - save histogram, save original image
      original_img_data = transform_original_img_and_save(original_pil_image, row_idx, label)
      ret.append(original_img_data)

      # Flip Image - save histogram and flipped image
      # flipped_img_data = transform_flipped_img_and_save(original_pil_image, row_idx, label)
      # ret.append(flipped_img_data)

      # Blur Image - save histogram and blurred image
      # blurred_img_data = transform_blurred_img_and_save(original_pil_image, row_idx, label)
      # ret.append(blurred_img_data)

      # Sharpen Image - save histogram and sharpened image
      # sharpened_img_data = transform_sharpened_img_and_save(original_pil_image, row_idx, label)
      # ret.append(sharpened_img_data)

      # Brighten the image
      # brightened_img_data = transform_brightened_img_and_save(original_pil_image, row_idx, label)
      # ret.append(brightened_img_data)



      # TEMP ##
      input('enter to continue')
      # TEMP ##

  # return image_data


# labels = np.array(labels)
# data = np.array(data)

if __name__ == '__main__':
  x = TrainingData()
  x.parse_and_augment_data()