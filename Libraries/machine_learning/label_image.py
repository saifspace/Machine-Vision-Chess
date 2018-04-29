# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time
import os

import numpy as np
import tensorflow as tf

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


ml_model = None
ml_labels = None
tf_session = None
input_operation = None
output_operation = None
sess = None


def load_model():
	global ml_model
	global ml_labels
	global tf_session
	global input_operation
	global output_operation
	global sess

	input_layer = "input"
	output_layer = "final_result"

	model_file = os.getcwd() + "\Libraries/machine_learning\\retrained_graph.pb"
	label_file = os.getcwd() + "\Libraries\machine_learning\\retrained_labels.txt"

	input_name = "import/" + input_layer
	output_name = "import/" + output_layer

	ml_model = load_graph(model_file)
	ml_labels = load_labels(label_file)


	input_operation = ml_model.get_operation_by_name(input_name);
	output_operation = ml_model.get_operation_by_name(output_name);

	sess = tf.Session(graph=ml_model)


def predict_label(file_name):
  global ml_model
  global ml_labels
  global tf_session
  global input_operation
  global output_operation

  input_height = 224
  input_width = 224
  input_mean = 128
  input_std = 128

  graph = ml_model
  t = read_tensor_from_image_file(file_name,
                                  input_height=input_height,
                                  input_width=input_width,
                                  input_mean=input_mean,
                                  input_std=input_std)
  
  # with tf.Session(graph=graph) as sess:
  start = time.time()
  results = sess.run(output_operation.outputs[0],{input_operation.outputs[0]: t})
  end=time.time()
  results = np.squeeze(results)

  top_k = results.argsort()[-5:][::-1]
  labels = ml_labels
  print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

  return ( (labels[top_k[0]], labels[top_k[1]]) )
  # for i in top_k:
	#   print(i)
	#   print(labels[i], results[i])