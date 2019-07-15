# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
# from sklearn.preprocessing import LabelBinarizer
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from keras.models import Sequential
# from keras.layers.core import Dense
# from keras.optimizers import SGD
# import matplotlib.pyplot as plt
# import numpy as np
import sqlite3
# import random
import pickle
# import cv2
# import os
import io

print("READING DATABASE...")
# Data holds images, labels holds corresponding label
data = []
labels = []

# Attempt to open images
conn = sqlite3.connect('../webserver/trainingdata.db')
c = conn.cursor()
c.execute("SELECT * FROM 'training'")
raw_data = c.fetchall()

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
  
  # Grab image
  image_object = io.BytesIO(row[2])
  image_object = pickle.load(image_object)
  print(type(image_object))