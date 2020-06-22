import json

import numpy as np
from tensorboard.compat.tensorflow_stub.io.gfile import exists
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.python.keras.models import load_model
from tensorflow.keras.preprocessing import image as imgprocess


class Classifier:
    def __init__(self, model_path, class_labels_json):
        self.class_labels = class_labels_json
        self.height = 150
        self.width = 150
        self.model_path = model_path
        self.model = Sequential()
        self.class_labels = self.read_class_labels_if_exists()

    def read_class_labels_if_exists(self):
        if exists(self.class_labels):
            with open(self.class_labels, 'r') as file:
                return json.load(file)
        else:
            return None

    def create(self):
        model = self.model
        model.add(Conv2D(32, (3, 3), input_shape=(
            self.width, self.height, 3)))  # this means - 150 x 150 with 3 channels (RGB image)
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        self.model = self.compile(model)

    def compile(self, model):
        model.compile(loss='binary_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])
        return model

    def fit(self, train, test, model_path):
        self.model.fit_generator(train,
                                 steps_per_epoch=3000 / 16,
                                 # step size equal to the image count in train dir / batch size
                                 epochs=50,
                                 validation_data=test,
                                 validation_steps=1000 / 16)  # step size equal to the image count in test dir  / batch size

        self.model.save(model_path)

    def predict(self, path):
        if exists(self.model_path):
            model = load_model(self.model_path)
            X = imgprocess.load_img(path, target_size=(self.width, self.height))
            X = imgprocess.img_to_array(X)
            X = np.expand_dims(X, axis=0)
            return self.interpret_class(X, model)

    def interpret_class(self, x, model):
        classes = model.predict_classes(x)

        if self.class_labels is None:
            return classes
        else:
            return [k for k in self.class_labels if (self.class_labels[k] == classes[0][0])][0]
