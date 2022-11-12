import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from keras import models
from keras.preprocessing.image import image_utils
import tensorflow.python.platform.tf_logging


def do_predict(model_path, imagePath_list):
    list_output = []
    model = models.load_model(model_path)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    for i in range(0, len(imagePath_list[0])):
        if os.path.isfile(imagePath_list[0][i]):
            img_data = image_utils.load_img(imagePath_list[1][i], target_size=(224, 224))
            img_array = image_utils.img_to_array(img_data)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.
            if np.argmax(model.predict(img_array)) == 0:
                list_output.append(imagePath_list[0][i])
    return list_output      # 리스트 뱉기 전에 중복 제거하는 부분 추가하기


