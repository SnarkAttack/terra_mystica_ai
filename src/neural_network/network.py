import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Input, ReLU, BatchNormalization, Conv2D, Add, Flatten, Dense
from tensorflow.keras import metrics, Model
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.python.keras.metrics import MeanSquaredError
from ..junk import all_locations

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

    model = Model(inputs, outputs)

    return model

class TerraMysticaAINetwork():

    def __init__(self):

        height = 9
        width = 25
        depth = 78

        # cult_board_input = None
        # player_input = None

        game_board_cnn = game_board_net(height, width, depth)

        x = Dense(128)(game_board_cnn.output)
        x = Dense(64)(x)
        x = Dense(32)(x)
        x = Dense(113, activation='softmax', name='action_output')(x)

        y = Dense(128)(game_board_cnn.output)
        y = Dense(64)(y)
        y = Dense(32)(y)
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

    def predict_actions(self, input):
        input = input.get_game_board_state()
        actions, _ = self._model.predict(input)
        return actions[0]

    def predict_value(self, input):
        input = input.get_game_board_state()
        _, values = self._model.predict(input)
        return values[0][0]