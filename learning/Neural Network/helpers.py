from PIL import Image

import numpy as np
import base64
import pickle
import sqlite3
import os
import io

import sys
sys.path.append('../..')
from hardware import image_data


def read_sqlite_db(db_path, table_name="training"):
  """
    Reads data from <db_path> sqlite3 database's table called <table_name>, and returns as list
  """
  try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM '%s'" % table_name)
    return c.fetchall()
  except:
    raise TypeError("Could not load data from db %s" % db_path)


def save_imagedata_histogram(image_data_image, histogram_filename_to_save):
  # get base64
  original_histogram_2d_b64 = image_data_image.histogram(output="base64")

  # Save to provided filename
  with open(histogram_filename_to_save, "wb") as f:
    f.write(base64.decodebytes(original_histogram_2d_b64))


def get_saved_data_from_row(row):
    """
      Receives a row from training database, and returns corresponding label
      and corresponding PIL image object.
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
    saved_pil_image = Image.fromarray(saved_image_data.image)

    return (saved_pil_image, label)


def transform_and_save_img(pil_image, transform_class, directory, idx, label, save_histogram=True):
  """
    Applies transformation to PIL image, and saves transformed image and histogram to disk
  """
  transformer = transform_class()

  # Flip label if necessary
  actual_label = transformer.get_transformed_label(label)

  histogram_path_to_save = os.path.join(directory, transformer.get_histogram_filename(idx, label))
  image_path_to_save = os.path.join(directory, transformer.get_image_filename(idx, label))

  # Transform pil_image into transformed image
  transformed_pil = transformer.transform(pil_image)
  transformed_image_data = image_data.ImageData(np.array(pil_image))

  # Save transformed image and histogram to disk
  transformed_pil.save(image_path_to_save)
  
  if save_histogram == True:
    save_imagedata_histogram(transformed_image_data, histogram_path_to_save)
  

  # Get flattened histogram
  original_histogram = transformed_image_data.histogram().flatten()

  # Build return object
  ret = {
    "index": idx, "label": actual_label, "histogram": original_histogram, 
    "img_file": image_path_to_save, "hist_file": histogram_path_to_save,
    "filter": transformer.FILE_INFIX
  }
  return ret


def save_augmented_data(data_to_save, path):
  """ Saves (pickles) data_to_save to the specified path """
  to_save = []
  
  for data_pt in data_to_save:
    # Keep only essential data points
    curr_data = {
      "flt": data_pt["filter"],
      "idx": data_pt["index"],
      "lbl": data_pt["label"],
      "his": data_pt["histogram"].tolist()
    }

    to_save.append(curr_data)

  with open(path, 'wb') as f:
    pickle.dump(to_save, f)
