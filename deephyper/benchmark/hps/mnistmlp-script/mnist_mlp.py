'''Trains a simple deep NN on the MNIST dataset.
Gets to 98.40% test accuracy after 20 epochs
(there is *a lot* of margin for parameter tuning).
2 seconds per epoch on a K520 GPU.
'''

from load_data import load_data

import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop

import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)


def run(param_dict):
    print(param_dict)
    num_classes = 10

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = load_data()

    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Dense(
        param_dict['nunits_l1'], activation=param_dict['activation_l1'], input_shape=(784,)))
    model.add(Dropout(param_dict['dropout_l1']))
    model.add(Dense(param_dict['nunits_l2'],
                    activation=param_dict['activation_l2']))
    model.add(Dropout(param_dict['dropout_l2']))
    model.add(Dense(num_classes, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy',
                  optimizer=RMSprop(),
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train,
                        batch_size=param_dict['batch_size'],
                        epochs=param_dict['epochs'],
                        verbose=1,
                        validation_data=(x_test, y_test))
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    return score[1]


if __name__ == "__main__":
    from deephyper.benchmark.hps.mnistmlp.problem import Problem
    param_dict = Problem.starting_point_asdict
    run(param_dict)
