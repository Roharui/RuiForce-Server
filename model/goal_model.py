from model.base_model import BaseModel

from tensorflow.keras.layers import (
    BatchNormalization,
    Dense,
    Dropout,
    Flatten,
    GlobalAveragePooling1D,
    AveragePooling2D,
    Conv2D,
    Reshape,
)
from tensorflow.keras.activations import tanh
from tensorflow.keras.optimizer import Adam

from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import BinaryAccuracy


class GoalModel(BaseModel):
    def __init__(self):
        super().__init__()

        self.reshape_1 = Reshape((4, 800 * 450))
        self.glavgPool_1 = GlobalAveragePooling1D()
        self.reshape_2 = Reshape((450, 800, 1))
        self.conv_1 = Conv2D(3, (3, 3), strides=(2, 2), padding="valid")
        self.avgPool_1 = AveragePooling2D((5, 5), padding="same")
        self.conv_2 = Conv2D(5, (2, 2), strides=(2, 2), padding="valid")
        self.avgPool_2 = AveragePooling2D((5, 5), padding="same")
        self.flatten = Flatten()
        self.dense_1 = Dense(100, activation=tanh)
        self.dense_2 = Dense(36, activation=tanh)
        self.dense_3 = Dense(6, activation=tanh)

        self.dropout = Dropout(0.5)

    def buildModel(self):
        self.build((None, 450, 800, 4))

    def call(self, inputs, train=False):
        x = self.reshape_1(inputs)
        x = self.glavgPool_1(x)
        x = self.reshape_2(x)
        x = self.conv_1(x)
        x = self.avgPool_1(x)
        x = self.conv_2(x)
        x = self.avgPool_2(x)
        x = self.flatten(x)
        x = self.dense_1(x)
        x = self.dense_2(x)
        x = self.dense_3(x)
        if train:
            x = self.dropout(x)
        return x

    def compileModel(self):
        self.compile(
            optimizer=Adam(learning_rate=1e-3),
            loss=MeanSquaredError(),
            metrics=[
                BinaryAccuracy(),
            ],
        )


if __name__ == "__main__":
    x = GoalModel()

    x.summary()
