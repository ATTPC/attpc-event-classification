# attpc-event-classification


## Evaluating Machine Learning Methods for Event Classification in the Active-Target Time Projection Chamber
This work is a survey of methods to use for track classification in the AT-TPC. The work was done with the goal of classifying proton tracks from the 46Ar(p,p) experiment that ran in August of 2015.

This repository contains code produced for Jack Taylor's 2017-18 academic year independent research project. All results found in this work are presented in my physics honors thesis, and are also available on the arXiv: https://arxiv.org/abs/1810.10350.

Algorithms tested include those available in the [scikit-learn](http://scikit-learn.org/stable/) package and neural
networks written using [Keras](https://keras.io/) with a [Tensorflow](https://www.tensorflow.org/) backend.


## Dependencies / Packages used
* [pytpc](https://github.com/ATTPC/pytpc)
* numpy
* matplotlib
* scipy
* pandas
* scikit-learn
* keras
* tensorflow

See requirements.txt for more exhaustive list with release information.

## Models/Algorithms Explored
* Logistic Regression
* Single-Layer Densely-Connected Neural Network
* Two Layer Densely-Connected Neural Network
* Pre-Trained Convolutional Neural Network (VGG16 Architecture - Image Recognition Problem)
* Support Vector Machines (One Class Classification)
