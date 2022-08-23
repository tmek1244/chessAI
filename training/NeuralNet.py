# https://github.com/suragnair/alpha-zero-general/blob/master/NeuralNet.py


import numpy as np
import tensorflow as tf

import chess
import os


class NeuralNet():
    """
    This class specifies the base NeuralNet class. To define your own neural
    network, subclass this class and implement the functions below. The neural
    network does not consider the current player, and instead only deals with
    the canonical form of the board.

    See othello/NNet.py for an example implementation.
    """

    def __init__(self, game):
        dropout = 0.3
        num_channels = 512

        input_layer= tf.keras.Input(shape=(12, 8, 8))       
        x_image = tf.keras.layers.Reshape((12, 8, 8, 1))(input_layer)                # batch_size  x board_x x board_y x 1
        h_conv1 = tf.keras.layers.Activation('relu')(tf.keras.layers.BatchNormalization(axis=3)(tf.keras.layers.Conv2D(num_channels, 3, padding='same', use_bias=False)(x_image)))         # batch_size  x board_x x board_y x num_channels
        h_conv2 = tf.keras.layers.Activation('relu')(tf.keras.layers.BatchNormalization(axis=3)(tf.keras.layers.Conv2D(num_channels, 3, padding='same', use_bias=False)(h_conv1)))         # batch_size  x board_x x board_y x num_channels
        h_conv3 = tf.keras.layers.Activation('relu')(tf.keras.layers.BatchNormalization(axis=3)(tf.keras.layers.Conv2D(num_channels, 3, padding='valid', use_bias=False)(h_conv2)))        # batch_size  x (board_x-2) x (board_y-2) x num_channels
        h_conv4 = tf.keras.layers.Activation('relu')(tf.keras.layers.BatchNormalization(axis=3)(tf.keras.layers.Conv2D(num_channels, 3, padding='valid', use_bias=False)(h_conv3)))        # batch_size  x (board_x-4) x (board_y-4) x num_channels
        h_conv4_flat = tf.keras.layers.Flatten()(h_conv4)       
        s_fc1 = tf.keras.layers.Dropout(dropout)(tf.keras.layers.Activation('relu')(tf.keras.layers.BatchNormalization(axis=1)(tf.keras.layers.Dense(1024, use_bias=False)(h_conv4_flat))))  # batch_size x 1024
        s_fc2 = tf.keras.layers.Dropout(dropout)(tf.keras.layers.Activation('relu')(tf.keras.layers.BatchNormalization(axis=1)(tf.keras.layers.Dense(512, use_bias=False)(s_fc1))))          # batch_size x 1024
        self.pi = tf.keras.layers.Dense(64*64, activation='softmax', name='pi')(s_fc2)   # batch_size x self.action_size
        self.v = tf.keras.layers.Dense(1, activation='tanh', name='v')(s_fc2)                    # batch_size x 1

        self.model = tf.keras.Model(inputs=input_layer, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=tf.keras.optimizers.Adam())

    def train(self, examples):
        """
        This function trains the neural network with examples obtained from
        self-play.

        Input:
            examples: a list of training examples, where each example is of form
                      (board, pi, v). pi is the MCTS informed policy vector for
                      the given board, and v is its value. The examples has
                      board in its canonical form.
        """        
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        input_boards = np.asarray([self._from_fen_to_array(board) for board in input_boards]).reshape(-1, 12, 8, 8)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        self.model.fit(x = input_boards, y = [target_pis, target_vs], batch_size = 64, epochs = 10)

    def predict(self, board):
        """
        Input:
            board: current board in its canonical form.

        Returns:
            pi: a policy vector for the current board- a numpy array of length
                game.getActionSize
            v: a float in [-1,1] that gives the value of the current board
        """
        pi, v = self.model.predict(self._from_fen_to_array(board).reshape(-1, 12, 8, 8), verbose=False)

        return pi[0], v[0]
    
    def _from_fen_to_array(self, board):
        chess_board = chess.Board(fen=board)
        result = np.zeros((2, 6, 8, 8))

        for row in range(1, 9):
            for i, col in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
                piece = chess_board.piece_at(chess.parse_square(col+str(row)))
                if not piece:
                    continue
                
                color = 0 if piece.color == chess.WHITE else 1
                piece_id = None
                if piece.piece_type == chess.KING:
                    piece_id = 0
                elif piece.piece_type == chess.QUEEN:
                    piece_id = 1
                elif piece.piece_type == chess.ROOK:
                    piece_id = 2
                elif piece.piece_type == chess.BISHOP:
                    piece_id = 3
                elif piece.piece_type == chess.KNIGHT:
                    piece_id = 4
                elif piece.piece_type == chess.PAWN:
                    piece_id = 5
                result[color, piece_id, row-1, i] = 1
        return result

    def save_checkpoint(self, folder, filename):
        """
        Saves the current neural network (with its parameters) in
        folder/filename
        """
        filepath = os.path.join(folder, filename + ".h5")
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.model.save_weights(filepath)

    def load_checkpoint(self, folder, filename):
        """
        Loads parameters of the neural network from folder/filename
        """
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename + ".h5")
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))

        self.model.load_weights(filepath)
