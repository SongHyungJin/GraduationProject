import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import keras
from ResNet_base import ResNet
import logging
import absl.logging

size_of_batch = 3


def train_module(train_path, test_level, model_path):
    train_gen = ImageDataGenerator(rescale=1. / 255)
    train_generator = train_gen.flow_from_directory(
        train_path,
        target_size=(224, 224),
        batch_size=size_of_batch,
        shuffle=True,
        class_mode='categorical'
    )

    if test_level == 1:
        layer_num = 18
        epoch_num = 2
    elif test_level == 2:
        layer_num = 18
        epoch_num = 400
    elif test_level == 3:
        layer_num = 34
        epoch_num = 200
    elif test_level == 4:
        layer_num = 34
        epoch_num = 400
    elif test_level == 5:
        layer_num = 50
        epoch_num = 400
    elif test_level == 6:
        layer_num = 50
        epoch_num = 700
    elif test_level == 7:
        layer_num = 101
        epoch_num = 400
    elif test_level == 8:
        layer_num = 101
        epoch_num = 700
    elif test_level == 9:
        layer_num = 152
        epoch_num = 400
    elif test_level == 10:
        layer_num = 152
        epoch_num = 700
    else:
        print('test level setting error')
        return

    absl.logging.set_verbosity(absl.logging.ERROR)
    tf.get_logger().setLevel('ERROR')
    model = ResNet(2, layer_num)
    callback1 = keras.callbacks.ModelCheckpoint(model_path, monitor='accuracy', save_best_only=True)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_generator,
              steps_per_epoch=len(train_generator),
              epochs=epoch_num,
              verbose=3,
              callbacks=callback1)

    ans = []
    ques = np.empty((train_generator.n, 224, 224, 3), dtype=float)
    k = 0
    for i in range(0, len(train_generator)):
        x_test, y_test = train_generator.next()
        for j in range(0, len(x_test)):
            ques[k] = x_test[j]
            ans.append(np.argmax(y_test[j]))
            k += 1

    output = []
    predict = model.predict(ques)
    for i in range(0, len(predict)):
        output.append(np.argmax(predict[i]))

    correct_count = 0
    for i in range(0, len(ans)):
        if ans[i] == output[i]:
            correct_count += 1
    accuracy = (correct_count / train_generator.n) * 100
    return accuracy

