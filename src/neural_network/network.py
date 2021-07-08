import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Input, ReLU, BatchNormalization, Conv2D, Add, Flatten, Dense, Softmax, Multiply
from tensorflow.keras import metrics, Model
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.python.keras.metrics import MeanSquaredError
from ..game.action import action_space

def softmax(x):
    y = np.exp(x - np.max(x))
    f_x = y / np.sum(np.exp(x))
    return f_x

def magnify_available(probs):
    s = sum(probs)
    probs /= s
    return probs

def relu_bn(inputs):
    relu = ReLU()(inputs)
    bn = BatchNormalization()(relu)
    return bn

def residual_block(input, filters, kernel_size, strides):
    f1, f2 = filters
    y = Conv2D(kernel_size=kernel_size,
               strides=strides,
               filters=f1,
               padding="same")(input)
    y = relu_bn(y)
    y = Conv2D(kernel_size=kernel_size,
               strides=strides,
               filters=f2,
               padding="same")(y)
    out = Add()([input, y])
    out = relu_bn(out)
    return out

def game_board_net(height, width, depth):

    num_res_blocks=10

    inputs = Input((depth, height, width))

    x = Conv2D(kernel_size=(3, 5), strides=(1, 1), filters=256, padding="same")(inputs)
    x = relu_bn(x)
    for i in range(num_res_blocks):
        x = residual_block(x, filters=(256, 256), kernel_size=(3, 5), strides=(1, 1))

    outputs = Flatten()(x)

    # this output is ~2^17 (actually 179712, or 2^17.45)

    model = Model(inputs, outputs)

    return model

class TerraMysticaAINetwork():

    def __init__(self):

        height = 9
        width = 26
        depth = 78

        # cult_board_input = None
        # player_input = None

        game_board_cnn = game_board_net(height, width, depth)
        action_mask = Input(action_space)

        x = Dense(4096)(game_board_cnn.output)
        x = Dense(2048)(x)
        x = Dense(action_space, activation='softmax', name='action_output')(x)

        y = Dense(4096)(game_board_cnn.output)
        y = Dense(2048)(y)
        y = Dense(1, activation='tanh', name='value_output')(y)

        self._model = Model(inputs=game_board_cnn.input, outputs=[x, y], name="tm_nn")

        losses = {
            'action_output': CategoricalCrossentropy(),
            'value_output': MeanSquaredError()
        }

        mets = {
            'action_output': metrics.CategoricalCrossentropy(),
            'value_output': metrics.MeanSquaredError(),
        }

        self._model.compile(loss=losses, optimizer='sgd', metrics=mets)

    def predict_actions(self, input, action_mask):
        input_tensor = input.get_game_board_state()
        actions, _ = self._model.predict(input_tensor)
        action_probs = np.asarray(actions[0])
        probs = action_probs * action_mask
        probs = magnify_available(probs)
        return probs

    def predict_value(self, input):
        input = input.get_game_board_state()
        _, values = self._model.predict(input)
        return values[0][0]