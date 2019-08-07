
import sqlite3
import pickle
import io

# This module gathers training data from the car's database and:
# 1. writes it to disk
# 2. flips it, and writes it to disk
# 3. adds noise, and writes it to disk
# 4. changes brightness (up or down depending on existing brightness), and writes it to disk
# 5. writes all of the above's trained outcome (Forward, Right, Left)

# This data is used for training the neural network and the Haar classifier

# Allow importing image data class
import sys
sys.path.append('../..')

def die(err_msg=""):
  """ Exit script after printing error message """
  print("[ERR] %s" % err_msg)
  exit()

try:
  path = sys.argv[1]
except:
  path = "../../webserver/trainingdata.db"
finally:
  print("Using path '%s' for database" % path)

try:
  print("[INFO] Attempting to read the database")
  conn = sqlite3.connect(path)
  c = conn.cursor()
  c.execute("SELECT * FROM 'training'")
  raw_data = c.fetchall()
  print("[INFO] Loaded %s records" % len(raw_data))
except:
  die("Could not open the database at path %s" % path)


# Data is an array of training data points - tuple (histogram, label)
data = []

# Loop through data, and add label and histogram
for idx, row in enumerate(raw_data):
  # Determine label
  if row[4] == 1:
    label = 'F'
  elif row[5] == 1:
    label = 'R'
  elif row[6] == 1:
    label = 'L'
  else:
    raise ValueError("Row %s has no command" % idx) 

  # Load raw image data from DB
  try:
    raw_image_data = io.BytesIO(row[2])
    image_data = pickle.load(raw_image_data)
    histogram = image_data.histogram().flatten()
  except:
    die("Error occurred in reading histogram from row %s" % idx)

  data.append((histogram, label))

print(data)

exit()
  # # Grab image as ImageData class, which is pickled in DB (depickling needs file-like obj)
  # raw_image_data = io.BytesIO(row[2])
  # image_data = pickle.load(raw_image_data)
  # # Each pixel is represented as 0/1 based on luminosity; threshold suggested by ImageData class
  # histogram = image_data.histogram()
  # if idx == 4:
  #   print(histogram)
  # # data.append(histogram)

# labels = np.array(labels)
# data = np.array(data)