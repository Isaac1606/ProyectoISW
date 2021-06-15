from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.layers import Dense 
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16  import VGG16
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input

from os.path import abspath
import numpy as np
import ntpath
import os

base_model = VGG16(weights = "imagenet", include_top=False, input_shape = (224,224, 3),pooling='avg')

base_model.trainable = False

# save the output of the base_model to be the input of the next layer
last_output = base_model.output

# add our new softmax layer with 10 hidden units
x = Dense(3, activation='softmax', name='softmax')(last_output)
# instantiate a new_model using keras’s Model class
new_model = Model(inputs=base_model.input, outputs=x)

new_model.compile(Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])



def cargar_modelo():
    new_model.load_weights(os.path.join(os.path.dirname(__file__), f'melanoma.model102.hdf5'))


def give_results(image_test_path):
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