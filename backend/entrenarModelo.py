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

# Path donde se encuentra el dataset y sus segmentaciones (train, valid, test)
general_path = r'C:\Users\isaac\Desktop\Datasets\skin-lesions3'

train_path = os.path.join(general_path,'train\\')
valid_path = os.path.join(general_path,'valid\\')
test_path =  os.path.join(general_path,'test\\')

test_number = '102'

# ImageDataGenerator generates batches of tensor image data with real-time data augmentation.
# The data will be looped over (in batches).
# in this example, we won't be doing any image augmentation
train_batches = ImageDataGenerator().flow_from_directory(train_path,target_size=(224,224),batch_size=10)

valid_batches = ImageDataGenerator().flow_from_directory(valid_path,target_size=(224,224),batch_size=30)

test_batches = ImageDataGenerator().flow_from_directory(test_path,target_size=(224,224),batch_size=50,shuffle=False)

base_model = vgg16.VGG16(weights = "imagenet", include_top=False, input_shape = (224,224, 3),pooling='avg')

# base_model.summary()

# iterate through its layers and lock them except for the last 5 layers
for layer in base_model.layers[:-4]:
    layer.trainable = False

# base_model.summary()


# save the output of the base_model to be the input of the next layer
last_output = base_model.output

# add our new softmax layer with 10 hidden units
x = Dense(3, activation='softmax', name='softmax')(last_output)
# instantiate a new_model using keras’s Model class
new_model = Model(inputs=base_model.input, outputs=x)
# print the new_model summary
# new_model.summary()


new_model.compile(Adam(lr=0.0001), loss='categorical_crossentropy', 
                  metrics=['accuracy'])
 

# No necesario correr si ya se tiene un archivo de pesos

# checkpointer = ModelCheckpoint(filepath=f'melanoma.model{test_number}.hdf5', 
#                                save_best_only=True)
 
# history = new_model.fit_generator(train_batches, steps_per_epoch=18,
#                    validation_data=valid_batches, validation_steps=3, 
#                    epochs=20, verbose=1, callbacks=[checkpointer])

def load_dataset(path):
    data = load_files(path)
    paths = np.array(data['filenames'])
    targets = to_categorical(np.array(data['target']))
    return paths, targets

# print(test_path)

test_files, test_targets = load_dataset(test_path)

# print(test_files)
# print(test_targets)

def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)

def paths_to_tensor(img_paths):
    list_of_tensors = [path_to_tensor(img_path) for img_path in tqdm(img_paths)]
    return np.vstack(list_of_tensors)

test_tensors = preprocess_input(paths_to_tensor(test_files))


new_model.load_weights(f'melanoma.model{test_number}.hdf5')

# print('\nTesting loss: {:.4f}\nTesting accuracy:{:.4f}'.format(*new_model.evaluate(test_tensors,test_targets)))

# 0 es melanoma 1 nevus 2 seborrheic_keratosis
# cm_labels = ['melanoma','nevus','seborrheic_keratosis']
# cm = confusion_matrix(np.argmax(test_targets, axis=1),
# np.argmax(new_model.predict(test_tensors), axis=1))
# plt.imshow(cm, cmap=plt.cm.Blues)
# plt.colorbar()
# indexes = np.arange(len(cm_labels))
# for i in indexes:
#     for j in indexes:
#         plt.text(j, i, cm[i, j])


# plt.xticks(indexes, cm_labels)
# plt.xlabel('Predicted label')
# plt.yticks(indexes, cm_labels)
# plt.ylabel('True label')
# plt.title('Confusion matrix')
# plt.show()


live_test_path = r'C:\Users\isaac\Desktop\Melanoma'
def give_results(path):
    paths = [abspath(arch.path) for arch in scandir(path) if arch.is_file()]
    for image_test_path in paths:
        # load an image from file
        image = load_img(image_test_path, target_size=(224, 224))
        # convert the image pixels to a numpy array
        image = img_to_array(image)
        # reshape data for the model
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        # prepare the image for the model
        image = preprocess_input(image)

        # predict the probability across all output classes
        yhat = new_model.predict(image)

        prediction = np.argmax(yhat[0])
        
        print(yhat)
        # print(prediction)
        
        if prediction == 0 and yhat[0][prediction]>.5:
            print(f"La imagen {ntpath.basename(image_test_path)}, muestra una lesión en la piel con un %{yhat[0][prediction]*100:.2f} de ser melanoma")
        else:
            print(f"La imagen {ntpath.basename(image_test_path)}, muestra una lesión en la piel que no es melanoma") 


give_results(live_test_path)