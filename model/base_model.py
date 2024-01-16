from tensorflow.python.keras import Model
from tensorflow.python.keras.optimizer_v2.adam import Adam

from tensorflow.python.keras.losses import BinaryCrossentropy
from tensorflow.python.keras.metrics import BinaryAccuracy, FalseNegatives


class BaseModel(Model):
    def __init__(self):
        super().__init__(self)

        self.train_x = None
        self.train_y = None

        self.test_x = None
        self.test_y = None

    def setTrainData(self, x, y):
        self.train_x = x
        self.train_y = y

    def setTestData(self, x, y):
        self.test_x = x
        self.test_y = y

    def compileModel(self):
        self.compile(
            optimizer=Adam(learning_rate=1e-3),
            loss=BinaryCrossentropy(),
            metrics=[
                BinaryAccuracy(),
                FalseNegatives(),
            ],
        )

    def trainModel(
        self,
        epochs,
        batch_size,
    ):
        self.fit(
            self.train_x,
            self.train_y,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(self.test_x, self.test_y),
        )

    def evaluateModel(self):
        self.evaluate(self.test_x, self.test_y, batch_size=32)

    def predictModel(self, x):
        return self.predict(x)

    def saveModel(self, filename):
        self.save_weights(filename)

    def loadModel(self, filename):
        self.load_weights(filename)


if __name__ == "__main__":
    pass
