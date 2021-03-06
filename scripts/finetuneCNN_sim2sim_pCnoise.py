"""
finetuneCNN_sim2sim_pCnoise.py
==============================

Testing pretrained/finetunable convolutional neural network solution to event classification
problem. Model uses a VGG16 architecture pretrained on the ImageNet database to
learn basic and universal image rcognition features such as edge detection and
etc. A small top model is then trained on top of the VGG16 network to classify
our data.

Inputs are 128x128 pixel plots of events.
Binary classification
Baseline sim proton vs. sim Carbon + sim junk
"""
import os
import numpy as np
import h5py

from keras import applications
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

import sys
sys.path.insert(0, '../modules/')
import metrics
metrics = metrics.BinaryMetrics()

seed = 7
np.random.seed(seed)
img_width, img_height = 128, 128
input_shape = (img_width, img_height, 3)

batch_size = 16
epochs = 100
validation_split = 0.25

#paths
hdf5_path = '../cnn-plots/hdf5s/'
bottleneck_features_train_path = '../models/CNN-sim2sim/bottleneck_features_sim2sim_pCnoise_train.npy'
bottleneck_features_test_path = '../models/CNN-sim2sim/bottleneck_features_sim2sim_pCnoise_test.npy'
top_model_weights_path = '../models/CNN-sim2sim/top_model_trained_sim2sim_pCnoise.h5'

#load images from hdf5 files
sim_p_file = h5py.File(hdf5_path + 'sim_p_largeEvts.h5', 'r')
sim_C_file = h5py.File(hdf5_path + 'sim_C_largeEvts.h5', 'r')
sim_junk_file = h5py.File(hdf5_path + 'sim_junk.h5', 'r')

sim_p = sim_p_file['img']
sim_C = sim_C_file['img']
sim_junk = sim_junk_file['img']

#labels
sim_p_labels = np.zeros((sim_p.shape[0],))
sim_C_labels = np.ones((sim_C.shape[0],))
sim_junk_labels = np.ones((sim_junk.shape[0],))

sim_X = np.vstack((np.array(sim_p), np.array(sim_C), np.array(sim_junk)))
sim_labels = np.hstack((sim_p_labels, sim_C_labels, sim_junk_labels))

X_train, X_test, labels_train, labels_test = train_test_split(sim_X, sim_labels, test_size=0.25, random_state=42)

def save_bottleneck_features():

    #build VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    print("Calculating pre-trained weights for train set...")
    bottleneck_features_train  = model.predict(X_train)
    np.save(open(bottleneck_features_train_path, 'wb'), bottleneck_features_train)

    print("Calculating pre-trained weights for test set...")
    bottleneck_features_test = model.predict(X_test)
    np.save(open(bottleneck_features_test_path, 'wb'), bottleneck_features_test)


def train_top_model():
    train_data = np.load(open(bottleneck_features_train_path, 'rb'))
    test_data = np.load(open(bottleneck_features_test_path, 'rb'))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    print("Training top model on training data")
    history = model.fit(train_data, labels_train,
                        validation_data = (test_data, labels_test),
                        shuffle='batch',
                        batch_size=batch_size,
                        epochs=epochs,
                        callbacks=[metrics])

    print(history.history.keys())

    textfile = open('../keras-results/CNN/sim2sim/pCnoise.txt', 'w')
    textfile.write('acc \n')
    textfile.write(str(history.history['acc']))
    textfile.write('\n')
    textfile.write('\nval_acc \n')
    textfile.write(str(history.history['val_acc']))
    textfile.write('\n')
    textfile.write('\nloss \n')
    textfile.write(str(history.history['loss']))
    textfile.write('\n')
    textfile.write('\nval_loss \n')
    textfile.write(str(history.history['val_loss']))
    textfile.write('\n')
    textfile.write('\nconfusion matrices \n')
    for cm in metrics.val_cms:
        textfile.write(str(cm))
        textfile.write('\n')

if not (os.path.isfile(bottleneck_features_train_path) and os.path.isfile(bottleneck_features_test_path)):
    save_bottleneck_features()
else:
    print("Pre-trained weights already calculated and stored")

train_top_model()
