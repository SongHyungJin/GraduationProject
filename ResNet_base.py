import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import tensorflow as tf
import keras
from keras import datasets, layers, models


class IdentityBlock(keras.models.Model):
    def __init__(self, filters, kernel_size):
        super(IdentityBlock, self).__init__(name='IdentifyBlock')
        self.conv1 = keras.layers.Conv2D(filters, kernel_size, padding='same', kernel_initializer='he_normal')
        self.bn1 = keras.layers.BatchNormalization()

        self.conv2 = keras.layers.Conv2D(filters, kernel_size, padding='same', kernel_initializer='he_normal')
        self.bn2 = keras.layers.BatchNormalization()

        self.act = keras.layers.Activation('relu')
        self.add = keras.layers.Add()

    def call(self, input_tensor):
        x = self.conv1(input_tensor)
        x = self.bn1(x)
        x = self.act(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.act(x)

        x = self.add([x, input_tensor])
        x = self.act(x)
        return x


class ConvIdentityBlock(keras.models.Model):
    def __init__(self, filters, kernel_size):
        super(ConvIdentityBlock, self).__init__(name='ConvBlock')

        self.conv1 = keras.layers.Conv2D(filters, kernel_size, strides=(2, 2), padding='same', kernel_initializer='he_normal')
        self.bn1 = keras.layers.BatchNormalization()

        self.conv2 = keras.layers.Conv2D(filters, kernel_size, padding='same', kernel_initializer='he_normal')
        self.bn2 = keras.layers.BatchNormalization()

        self.conv1x1 = keras.layers.Conv2D(filters, 1, strides=(2, 2), padding='same', kernel_initializer='he_normal')
        self.bn3 = keras.layers.BatchNormalization()
        self.act = keras.layers.Activation('relu')
        self.add = keras.layers.Add()

    def call(self, input_tensor):
        x = self.conv1(input_tensor)
        x = self.bn1(x)
        x = self.act(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.act(x)

        y = self.conv1x1(input_tensor)
        y = self.bn3(y)
        x = self.add([x, y])
        x = self.act(x)
        return x


class BottleIdentityBlock(keras.models.Model):
    def __init__(self, filters, kernel_size):
        super(BottleIdentityBlock, self).__init__(name='IdentifyBlock')
        self.conv1 = keras.layers.Conv2D(filters, 1, padding='same', kernel_initializer='he_normal')
        self.bn1 = keras.layers.BatchNormalization()

        self.conv2 = keras.layers.Conv2D(filters, kernel_size, padding='same', kernel_initializer='he_normal')
        self.bn2 = keras.layers.BatchNormalization()

        self.conv3 = keras.layers.Conv2D(4 * filters, 1, padding='same', kernel_initializer='he_normal')
        self.bn3 = keras.layers.BatchNormalization()

        self.act = keras.layers.Activation('relu')
        self.add = keras.layers.Add()

    def call(self, input_tensor):
        x = self.conv1(input_tensor)
        x = self.bn1(x)
        x = self.act(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.act(x)

        x = self.conv3(x)
        x = self.bn3(x)

        x = self.add([x, input_tensor])
        x = self.act(x)
        return x


class BottleConvIdentityBlock(keras.models.Model):
    def __init__(self, filters, kernel_size, stride=(2, 2)):
        super(BottleConvIdentityBlock, self).__init__(name='ConvBlock')

        self.conv1 = keras.layers.Conv2D(filters, 1, strides=stride, padding='same', kernel_initializer='he_normal')
        self.bn1 = keras.layers.BatchNormalization()

        self.conv2 = keras.layers.Conv2D(filters, kernel_size, padding='same', kernel_initializer='he_normal')
        self.bn2 = keras.layers.BatchNormalization()

        self.conv3 = keras.layers.Conv2D(4 * filters, 1, padding='same', kernel_initializer='he_normal')
        self.bn3 = keras.layers.BatchNormalization()

        self.conv1x1 = keras.layers.Conv2D(4 * filters, 1, strides=stride, padding='same')
        self.bn4 = keras.layers.BatchNormalization()
        self.act = keras.layers.Activation('relu')
        self.add = keras.layers.Add()

    def call(self, input_tensor):
        x = self.conv1(input_tensor)
        x = self.bn1(x)
        x = self.act(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.act(x)

        x = self.conv3(x)
        x = self.bn3(x)
        x = self.act(x)

        y = self.conv1x1(input_tensor)
        y = self.bn4(y)
        x = self.add([x, y])
        x = self.act(x)
        return x


class ResNet(keras.models.Model):   # 배열로 갯수만큼 담기
    def __init__(self, num_classes, num_of_layers):
        super(ResNet, self).__init__()
        self.conv = keras.layers.Conv2D(64, 7, strides=(2, 2), padding='same')
        self.bn = keras.layers.BatchNormalization()
        self.act = keras.layers.Activation('relu')
        self.max_pool = keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding='same')

        self.first_block = []
        self.second_block = []
        self.third_block = []
        self.fourth_block = []

        if num_of_layers == 18:
            self.make_block(2, 2, 2, 2, 0)
        elif num_of_layers == 34:
            self.make_block(3, 4, 6, 3, 0)
        elif num_of_layers == 50:
            self.make_block(3, 4, 6, 3, 1)
        elif num_of_layers == 101:
            self.make_block(3, 4, 23, 3, 1)
        elif num_of_layers == 152:
            self.make_block(3, 8, 36, 3, 1)

        self.global_pool = keras.layers.GlobalAveragePooling2D()
        self.classifier = keras.layers.Dense(num_classes, activation='softmax')

    def make_block(self, first, second, third, fourth, scale):
        if scale == 0:
            for q in range(0, first):
                self.first_block.append(IdentityBlock(64, 3))
            self.second_block.append(ConvIdentityBlock(128, 3))
            for q in range(0, second - 1):
                self.second_block.append(IdentityBlock(128, 3))
            self.third_block.append(ConvIdentityBlock(256, 3))
            for q in range(0, third - 1):
                self.third_block.append(IdentityBlock(256, 3))
            self.fourth_block.append(ConvIdentityBlock(512, 3))
            for q in range(0, fourth - 1):
                self.fourth_block.append(IdentityBlock(512, 3))
        elif scale == 1:
            self.first_block.append(BottleConvIdentityBlock(64, 3, (1, 1)))
            for q in range(0, first - 1):
                self.first_block.append(BottleIdentityBlock(64, 3))
            self.second_block.append(BottleConvIdentityBlock(128, 3))
            for q in range(0, second - 1):
                self.second_block.append(BottleIdentityBlock(128, 3))
            self.third_block.append(BottleConvIdentityBlock(256, 3))
            for q in range(0, third - 1):
                self.third_block.append(BottleIdentityBlock(256, 3))
            self.fourth_block.append(BottleConvIdentityBlock(512, 3))
            for q in range(0, fourth - 1):
                self.fourth_block.append(BottleIdentityBlock(512, 3))

    def call(self, inputs):
        x = self.conv(inputs)
        x = self.bn(x)
        x = self.act(x)
        x = self.max_pool(x)

        for p in range(0, len(self.first_block)):
            x = self.first_block[p].call(x)
        for p in range(0, len(self.second_block)):
            x = self.second_block[p].call(x)
        for p in range(0, len(self.third_block)):
            x = self.third_block[p].call(x)
        for p in range(0, len(self.fourth_block)):
            x = self.fourth_block[p].call(x)

        x = self.global_pool(x)
        return self.classifier(x)


