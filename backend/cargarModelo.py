from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.layers import Dense 
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16  import VGG16

import os

def cargar_modelo():
    base_model = VGG16(weights = "imagenet", include_top=False, input_shape = (224,224, 3),pooling='avg')

    base_model.trainable = False

    # save the output of the base_model to be the input of the next layer
    last_output = base_model.output

    # add our new softmax layer with 10 hidden units
    x = Dense(3, activation='softmax', name='softmax')(last_output)
    # instantiate a new_model using keras’s Model class
    new_model = Model(inputs=base_model.input, outputs=x)

    new_model.compile(Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    new_model.load_weights(os.path.join(os.path.dirname(__file__), f'melanoma.model102.hdf5'))
