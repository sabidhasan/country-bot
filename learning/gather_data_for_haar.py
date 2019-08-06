# From https://github.com/quiltdata/open-images/blob/master/src/openimager/openimager.py

from tqdm import tqdm
import pandas as pd
import requests
import sys
import os

def exit_with_err(err):
  """ Fatal error occurred; exit the script """
  print("[ERR] %s" % err)
  exit()

# Download files
def download_file(url, file_name):
  """ Download the given URL to file_name. Returns True if successful, False is failed """
  try:
    req = requests.get(url)
    # This will raise exception if it fails
    req.raise_for_status()
    with open(file_name, "wb") as f:
        f.write(req.content)
    return True
  except:
    return False


try:
  # Holds keyword for which data will be downloaded
  requested_keyword = sys.argv[1]
except:
  exit_with_err("No keyword specified!")

# Read CSV for LabelName (requested_keyword) to get keyword ID
try:
  print("[INFO] Attempting to read CSV files...")
  # Given a keyword, gives LabelName
  label_names = pd.read_csv('class-descriptions-boxable.csv', header=None, names=['LabelName', 'keyword'])
  # Given a LabelName, gives ImageIDs and X/Y coordinates of the box
  image_boxes = pd.read_csv('train-annotations-bbox.csv').set_index('ImageID')
  # Given an image ID, gives image URL
  image_urls = pd.read_csv('train-images-boxable-with-rotation.csv').set_index('ImageID')
except:
  exit_with_err("""
    [ERR] Error reading CSV files.
    Download from https://storage.googleapis.com/openimages/2018_04/class-descriptions-boxable.csv 
    Download from https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv
    Download from https://storage.googleapis.com/openimages/2018_04/train/train-images-boxable-with-rotation.csv
    Exiting!
  """)

try:
  # Get the label name from the CSV file for the requested keyword
  print("[INFO] Attemping to find label name based on keyword...")
  label_name = label_names[label_names['keyword'] == requested_keyword].LabelName.iloc[0]
except IndexError:
  exit("Key not found!")

# From image_boxes table, select those with LabelName being chosen label_name
print("[INFO] Finding boxes for picked images...")
wanted_columns = ['XMin', 'XMax', 'YMin', 'YMax']
desired_images = image_boxes[image_boxes.LabelName == label_name].loc[:, wanted_columns]

# Join these desired images on the image_urls table's ImageID column, keeping OriginalURL column
# Contains these columns: ['XMin', 'XMax', 'YMin', 'YMax', 'OriginalURL']
print("[INFO] Found %s images. Joining these images on URLs table." % desired_images.shape[0])
desired_images = desired_images.join(image_urls.loc[:, ['OriginalURL']])

# This dict store 
# Keys are ImageIDs, value is { 'XMin' 'XMax' 'YMin' 'YMax' 'URL' Downloaded' }
# Make file for box data
with open('%s_data.txt' % requested_keyword, 'w') as f:
  f.write('ImageID,XMin,XMax,YMin,YMax,URL,Downloaded\n')

# Make the base directory for saving images
BASE_DIRECTORY = 'temp'
if not os.path.exists(BASE_DIRECTORY):
  print("[INFO] Directory %s does not exist; making it" % BASE_DIRECTORY)
  os.mkdir(BASE_DIRECTORY)
else:
  print("[INFO] Directory %s exist; using it" % BASE_DIRECTORY)

print("[INFO] Building dictionary")
with tqdm(total=desired_images.shape[0]) as pbar:
  for (image_id, row) in tqdm(desired_images.iterrows()):
    file_name = BASE_DIRECTORY + "/" + str(image_id) + '.jpg'
    downloaded = download_file(row['OriginalURL'], file_name)

    if downloaded == False:
      pbar.update()
      continue
    # Write to file
    xMin, xMax, yMin, yMax = row['XMin'], row['XMax'], row['YMin'], row['YMax']
    with open('%s_data.txt' % requested_keyword, 'a') as f:
      f.write('%s,%s,%s,%s,%s,%s,%s\n' % (image_id, xMin, xMax, yMin, yMax, row['OriginalURL'], downloaded))
    pbar.update()