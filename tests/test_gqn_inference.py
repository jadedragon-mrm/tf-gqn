"""
Quick test script to shape-check graph definition of GQN latent space
inference with random toy data.
"""

import os
import sys
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TF_GQN_HOME = os.path.abspath(os.path.join(SCRIPT_PATH, '..'))
sys.path.append(TF_GQN_HOME)

import tensorflow as tf
import numpy as np

from gqn.gqn_params import PARAMS
from gqn.gqn_draw import inference_rnn

# constants
_BATCH_SIZE = 1
_DIM_POSE = PARAMS.POSE_CHANNELS
_DIM_H_IMG = PARAMS.IMG_HEIGHT
_DIM_W_IMG = PARAMS.IMG_WIDTH
_DIM_C_IMG = PARAMS.IMG_CHANNELS
_DIM_R_H = PARAMS.ENC_HEIGHT
_DIM_R_W = PARAMS.ENC_WIDTH
_DIM_R_C = PARAMS.ENC_CHANNELS
_SEQ_LENGTH = PARAMS.SEQ_LENGTH

# input placeholders
query_pose = tf.placeholder(
    shape=[_BATCH_SIZE, _DIM_POSE], dtype=tf.float32)
target_frame = tf.placeholder(
    shape=(_BATCH_SIZE, _DIM_H_IMG, _DIM_W_IMG, _DIM_C_IMG),
    dtype=tf.float32)
scene_representation = tf.placeholder(
    shape=[_BATCH_SIZE, _DIM_R_H, _DIM_R_W, _DIM_R_C], dtype=tf.float32)

# set up the generator LSTM cell
mu_target, ep_inference = inference_rnn(
    representations=scene_representation,
    query_poses=query_pose,
    target_frames=target_frame,
    sequence_size=_SEQ_LENGTH)

# feed random input through the graph
with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  feed_dict = {
      query_pose : np.random.rand(_BATCH_SIZE, _DIM_POSE),
      target_frame : np.random.rand(_BATCH_SIZE, _DIM_H_IMG, _DIM_W_IMG, _DIM_C_IMG),
      scene_representation : np.random.rand(_BATCH_SIZE, _DIM_R_H, _DIM_R_W, _DIM_R_C),
  }
  mu = sess.run(mu_target, feed_dict=feed_dict)
  print(mu)
  print(mu.shape)
  for ep, t in ep_inference.items():
    print(ep, t)

print("TEST PASSED!")
