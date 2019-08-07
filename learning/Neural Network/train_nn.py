# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# Allow importing image data class
import sys
sys.path.append('..')

# import the necessary packages
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from hardware.image_data import ImageData
import numpy as np
import sqlite3
# import random
import pickle
# import cv2
# import os
import io

print("Reading database")
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
  labels.append(label)

  # Grab image as ImageData class, which is pickled in DB (depickling needs file-like obj)
  raw_image_data = io.BytesIO(row[2])
  image_data = pickle.load(raw_image_data)
  # Each pixel is represented as 0/1 based on luminosity; threshold suggested by ImageData class
  histogram = image_data.histogram().flatten()
  data.append(histogram)

labels = np.array(labels)
data = np.array(data)

# partition the data into training and testing sets
trainX, testX, trainY, testY = train_test_split(data,	labels, test_size=0.25, random_state=1)

# convert labels from int to vectors, using one hot encoding
binarizer = LabelBinarizer()
trainY = binarizer.fit_transform(trainY)
testY = binarizer.transform(testY)

size = trainX.shape[1]

# Build the model
model = Sequential()
model.add(Dense(2048, input_dim=size, activation="sigmoid"))
model.add(Dense(2048, activation="relu"))
model.add(Dense(len(binarizer.classes_), activation="softmax"))

# Learning rate and epochs
INIT_LEARNING_RATE = 0.01
EPOCHS = 50

# Compile the model
print("Training network")
opt = SGD(lr=INIT_LEARNING_RATE)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])


# train neural network
trained_model = model.fit(trainX, trainY, validation_data=(testX, testY),	epochs=EPOCHS, batch_size=32)

# evaluate the network
print("Evaluating network")
print(testX)
predictions = model.predict(testX, batch_size=32)
print(classification_report(testY.argmax(axis=1),
	predictions.argmax(axis=1), target_names=binarizer.classes_))
 

