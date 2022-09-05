import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"  
import tensorflow as tf

import numpy as np

class Bot:
    def __init__(self, player_color=1) -> None:
        self.player = player_color
        with tf.device('/cpu:0'):
            self.model = tf.keras.models.load_model('chessEngine/model_0.dense_elu')

    def evaluate(self, position):
        input = np.append(position.reshape(-1, 12, 8, 8), [1, 1, 1, 1, self.player]).reshape(-1, 12*8*8+5)
        v = self.model.predict(input)
        return v[0]
    