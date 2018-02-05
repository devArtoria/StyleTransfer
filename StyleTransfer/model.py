import tensorflow as tf
import numpy as np
import scipy.io

MODEL_FILE = 'imagenet-vgg-verydeep-19.mat'

def conv2d(inputs, weights, bias):

    conv = tf.nn.conv2d(input=inputs,
                        filter=tf.constant(weights),
                        strides=1,
                        padding='SAME')

    return tf.nn.bias_add(conv, bias)

def pooling(inputs):
    return tf.layers.max_pooling2d(inputs=inputs,
                                   pool_size=2,
                                   strides=2,
                                   padding='SAME')

def pre_process(image, mean_pixel):
    return image - mean_pixel

def undo_pre_process(image, mean_pixel):
    return image + mean_pixel


class VGG19:
    layers = (
        'conv1_1', 'relu1_1', 'conv1_2', 'relu1_2', 'pool1',

        'conv2_1', 'relu2_1', 'conv2_2', 'relu2_2', 'pool2',

        'conv3_1', 'relu3_1', 'conv3_2', 'relu3_2', 'conv3_3',
        'relu3_3', 'conv3_4', 'relu3_4', 'pool3',

        'conv4_1', 'relu4_1', 'conv4_2', 'relu4_2', 'conv4_3',
        'relu4_3', 'conv4_4', 'relu4_4', 'pool4',

        'conv5_1', 'relu5_1', 'conv5_2', 'relu5_2', 'conv5_3',
        'relu5_3', 'conv5_4', 'relu5_4'
    )

    def __init__(self, data_path):
        data = scipy.io.loadmat(data_path)
        self.mean_pixel = np.array([123.68, 116.779, 103.939])
        self.weights = data['layers'][0]

    def pre_process(self, image):
        return image - self.mean_pixel

    def feed_foward(self, input_image, scope=None):
        net = {}
        current = input_image

        with tf.variable_scope(scope):
            for i, name in enumerate(self.layers):
                kind = name[:4]
                if kind == 'conv':
                    kernels = self.weights[i][0][0][2][0][0]
                    bias = self.weights[i][0][0][2][0][1]

                    # matconvnet: weights are [width, height, in_channels, out_channels]
                    # tensorflow: weights are [height, width, in_channels, out_channels]
                    kernels = np.transpose(kernels, (1, 0, 2, 3))
                    bias = bias.reshape(-1)

                    current = conv2d(current, kernels, bias)
                elif kind == 'relu':
                    current = tf.nn.relu(current)
                elif kind == 'pool':
                    current = pooling(current)
                net[name] = current

            assert len(net) == len(self.layers)
            return net