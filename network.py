# -*- coding: UTF-8 -*-
from aip import AipOcr
import json
import tensorflow as tf
import config as cfg
from tensorflow.contrib import layers
from tensorflow.python.layers.core import Dense
import numpy as np
slim=tf.contrib.slim

def network(_image, scope,is_training,reuse=None):
    with tf.variable_scope(scope, reuse=reuse):
        net = tf.layers.batch_normalization(_image, training=is_training)
        net = slim.conv2d(net, 64, [3, 3], scope='conv1')
        net = slim.max_pool2d(net, [2, 2], scope='pool1')
        net = slim.conv2d(net, 128, [3, 3], scope='conv2')
        net = slim.max_pool2d(net, [2, 2], scope='pool2')
        net = slim.conv2d(net, 256, [3, 3], activation_fn=None, scope='conv3')
        net = tf.layers.batch_normalization(net, training=is_training)
        net = tf.nn.relu(net)
        net = slim.conv2d(net, 256, [3, 3], scope='conv4')
        net = slim.max_pool2d(net, [2, 2], [1, 2], scope='pool3')
        net = slim.conv2d(net, 512, [3, 3], activation_fn=None, scope='conv5')
        net = tf.layers.batch_normalization(net, training=is_training)
        net = tf.nn.relu(net)
        net = slim.conv2d(net, 512, [3, 3], scope='conv6')
        net = slim.max_pool2d(net, [2, 2], [1, 2], scope='pool4')
        net = slim.conv2d(net, 512, [2, 2], padding='VALID', activation_fn=None, scope='conv7')
        net = tf.layers.batch_normalization(net, training=is_training)
        net = tf.nn.relu(net)#CRNN
        cnn_out = tf.squeeze(net,axis=2)

        cell = tf.contrib.rnn.GRUCell(num_units=cfg.RNN_UNITS)
        enc_outputs, enc_state = tf.nn.bidirectional_dynamic_rnn(cell_fw=cell,cell_bw=cell,inputs=cnn_out,dtype=tf.float32)#双向LSTM
        encoder_outputs = tf.concat(enc_outputs, -1)
        return encoder_outputs,enc_state

