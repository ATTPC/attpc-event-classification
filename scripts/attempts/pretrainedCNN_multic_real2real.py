"""
pretrainedCNN_pvsall_real2real.py
=================================

Testing pretrained convolutional neural network solution to event classification
problem. Model uses a VGG16 architecture pretrained on the ImageNet database to
learn basic and universal image rcognition features such as edge detection and
etc. A small top model is then trained on top of the VGG16 network to classify
our data.

Inputs are 128x128 pixel plots of events.

Testing proton vs.carbon vs. junk approach - multiclass (only real data)
Trains the last layer of VGG16 - Long training periods
"""
import matplotlib.pyplot as plt
import numpy as np
import h5py

from keras import applications
from keras.models import Model, Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.utils import np_utils

seed = 7
np.random.seed(seed)
img_width, img_height = 128, 128
input_shape = (img_width, img_height, 3)

batch_size = 16
epochs = 25
validation_split = 0.15

#paths
hdf5_path = '../cnn-plots/hdf5s/'

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

#real data labels
real_X = np.vstack((np.array(real_p), np.array(real_C), np.array(real_junk)))
real_labels = np.hstack((real_p_labels, real_C_labels, real_junk_labels))
real_labels_1hot = np_utils.to_categorical(real_labels)

#build VGG16 network
print("Loading VGG16 base model pretrained on imagenet db.")
base_model = applications.VGG16(include_top=False, weights='imagenet', input_shape=input_shape)

#build a classifier to put on top of the VGG16
top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(real_labels_1hot.shape[1], activation='sigmoid'))

model = Model(inputs=base_model.input, outputs=top_model(base_model.output))

def train_final_model():
    #freeze all layers of the VGG16 except the last layer
    for layer in model.layers[:15]:
        layer.trainable = False

    #compile the model
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    history = model.fit(real_X, real_labels_1hot,
                        validation_split=validation_split,
                        shuffle='batch',
                        batch_size=batch_size,
                        epochs=epochs)

    print(history.history.keys())
    # summarize history for accuracy
    plt.figure(1)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('CNN Accuracy - p vs. C vs. junk')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['simulated data (train)', 'real data (test)'], loc='upper left')
    plt.savefig('../plots/results/CNN/CNN_sim2real_multic_acc.pdf')

train_final_model()
