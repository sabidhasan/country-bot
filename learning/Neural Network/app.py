from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.models import load_model
from keras.layers.core import Dense
from keras.optimizers import SGD
import numpy as np
import time

from augment import Augmenter
from transformers import TransformOriginal, TransformFlip, TransformBlur, \
  TransformSharpen, TransformBrighten, TransformBlurFlip, TransformSharpenFlip, TransformBrightenFlip


def train_model(training_data):
  """
    Trains NN model for self driving car.
    Outputs h5 file of trained models contianing weights/parameters 
  """

  # Data holds images, labels holds corresponding label at same index
  data_processed = []
  labels_processed = []

  for idx, row in enumerate(training_data):
    labels_processed.append(row["label"])
    data_processed.append(row["histogram"])

  labels_processed = np.array(labels_processed)
  data_processed = np.array(data_processed)

  # partition the data into training and testing sets
  trainX, testX, trainY, testY = train_test_split(data_processed,	labels_processed,
    test_size=0.2, random_state=1)

  # convert labels from strings into vectors, using one hot encoding
  binarizer = LabelBinarizer()
  trainY = binarizer.fit_transform(trainY)
  testY = binarizer.transform(testY)

  size = trainX.shape[1]

  # Build the model
  model = Sequential()
  model.add(Dense(64, input_dim=size, activation="sigmoid"))
  model.add(Dense(64, activation="relu"))
  model.add(Dense(len(binarizer.classes_), activation="softmax"))

  INIT_LEARNING_RATE = 0.01
  EPOCHS = 75

  # Compile model
  opt = SGD(lr=INIT_LEARNING_RATE)
  model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

  # train neural network
  history = model.fit(trainX, trainY, validation_data=(testX, testY),	epochs=EPOCHS, batch_size=32)

  # evaluate built network
  predictions = model.predict(testX, batch_size=32)
  print(classification_report(testY.argmax(axis=1),
	  predictions.argmax(axis=1), target_names=binarizer.classes_))

  model_file_name = "model_%s.h5" % round(time.time())
  model.save(model_file_name)
  print("Saved model to disk as %s" % model_file_name)

if __name__ == "__main__":
  # Train the model using 5 default image augmentation algorthims
  transformation_classes = [
    TransformOriginal, TransformFlip, TransformBlur, TransformSharpen, TransformBrighten,
    TransformBlurFlip, TransformSharpenFlip, TransformBrightenFlip
  ]

  db_path = "../../webserver/trainingdata.db"
  augmenter = Augmenter(path=db_path, transformation_classes=transformation_classes)
  data = augmenter.augment_data(save_text_output=False, save_histogram=False)

  try:
    train_model(data)
  except:
    print("Training model failed.")