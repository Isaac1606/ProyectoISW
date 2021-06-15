from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications import vgg16
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.layers import Dense, Flatten, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image  
from tensorflow.keras.applications.vgg16 import preprocess_input
from tqdm import tqdm

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16  import decode_predictions
from tensorflow.keras.applications.vgg16  import VGG16
from tensorflow.keras.callbacks import ModelCheckpoint

from sklearn.metrics  import confusion_matrix
from sklearn.datasets import load_files
from sklearn.metrics  import confusion_matrix

import itertools
import numpy as np
import matplotlib.pyplot as plt
import os

from os import scandir, getcwd
from os.path import abspath

import ntpath

from tensorflow.keras import Input

from tensorflow.keras.layers import GlobalAveragePooling2D

from tensorflow.keras.losses import CategoricalCrossentropy

def cargar_modelo():
    base_model = vgg16.VGG16(weights = "imagenet", include_top=False, input_shape = (224,224, 3),pooling='avg')

    base_model.trainable = False

    # save the output of the base_model to be the input of the next layer
    last_output = base_model.output

    # add our new softmax layer with 10 hidden units
    x = Dense(3, activation='softmax', name='softmax')(last_output)
    # instantiate a new_model using keras’s Model class
    new_model = Model(inputs=base_model.input, outputs=x)

    new_model.compile(Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    new_model.load_weights(os.path.join(os.path.dirname(__file__), f'melanoma.model102.hdf5'))
