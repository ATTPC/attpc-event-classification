"""
finetuneCNN_sim2sim_pC.py
=========================

Testing pretrained/finetunable convolutional neural network solution to event classification
problem. Model uses a VGG16 architecture pretrained on the ImageNet database to
learn basic and universal image rcognition features such as edge detection and
etc. A small top model is then trained on top of the VGG16 network to classify
our data.

Inputs are 128x128 pixel plots of events.
Baseline real proton vs. real Carbon vs. real junk
"""
import matplotlib.pyplot as plt
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
metrics = metrics.MulticlassMetrics()

seed = 7
np.random.seed(seed)
img_width, img_height = 128, 128
input_shape = (img_width, img_height, 3)

batch_size = 16
epochs = 100
validation_split = 0.25

#paths
hdf5_path = '../cnn-plots/hdf5s/'
bottleneck_features_train_path = '../models/CNN-real2real/bottleneck_features_real2real_multic_train.npy'
bottleneck_features_test_path = '../models/CNN-real2real/bottleneck_features_real2real_multic_test.npy'
top_model_weights_path = '../models/CNN-real2real/top_model_trained_real2real_multic.h5'

#load images from hdf5 files
real_p_file = h5py.File(hdf5_path + 'real_p.h5', 'r')
real_C_file = h5py.File(hdf5_path + 'real_C.h5', 'r')
real_junk_file = h5py.File(hdf5_path + 'real_junk.h5', 'r')

real_p = real_p_file['img']
real_C = real_C_file['img']
real_junk = real_junk_file['img']

#labels
real_p_labels = np.zeros((real_p.shape[0],))
real_C_labels = np.ones((real_C.shape[0],))
real_junk_labels = np.full((real_junk.shape[0],), 2)

real_X = np.vstack((np.array(real_p), np.array(real_C), np.array(real_junk)))
real_labels_categorical = np.hstack((real_p_labels, real_C_labels, real_junk_labels))
#one-hot encode for use with categorical_crossentropy
real_labels = np_utils.to_categorical(real_labels_categorical)

X_train, X_test, labels_train, labels_test = train_test_split(real_X, real_labels, test_size=validation_split, random_state=42)

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
    model.add(Dense(real_labels.shape[1], activation='softmax'))

    model.compile(loss='categorical_crossentropy',
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
    # summarize history for accuracy
    plt.figure(1)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('CNN Accuracy Real Data - Multiclass')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train data', 'test data'], loc='upper left')
    #plt.savefig('../plots/results/CNN/CNN_real2real_multic_acc_binarycross.pdf')

    textfile = open('../keras-results/CNN/real2real/multic.txt', 'w')
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
