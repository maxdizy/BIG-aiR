import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from dataHandler import trickData, target, trickData_test

# define model
input_size = trickData.shape[2]
seq_length = trickData.shape[1]
model = keras.models.Sequential()
model.add(keras.Input(shape=(seq_length, input_size)))
# test SimpleRNN, LSTM, and GRU
model.add(layers.LSTM(50, activation="relu", return_sequences=True))
model.add(layers.Dropout(0.2))
model.add(layers.LSTM(25, activation="relu"))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation="sigmoid"))
# print(model.summary())

#  loss and optimizer
loss = keras.losses.BinaryCrossentropy()
optim = keras.optimizers.RMSprop(learning_rate=0.001)
metrics = ["accuracy"]
model.compile(loss=loss, optimizer=optim, metrics=metrics)

# Train model
# epochs=10 specifies the number of times the training process will work through the entire dataset. One epoch means that each sample in the training dataset has had an opportunity to update the internal model parameters. A higher number of epochs can lead to better training but also risks overfitting if too large.
# batch_size=32 defines the number of samples that will be propagated through the network before the model's internal parameters are updated. In this case, 32 samples from trickData are processed, and then the model is updated. The choice of batch size can affect the speed and stability of the training process.
# verbose = 1 means that you will see a progress bar in the output showing the training progress. If set to 0, you would see no output during training, and if set to 2, you would see one line per epoch.
model.fit(trickData, target, epochs=200, batch_size=16, verbose=1)

print("\n\nThe model predicts...\n\n")
print(model.predict(trickData_test))

# # Evaluate model
# loss, accuracy = model.evaluate(trickData_test, target_test)
# print(f'Test accuracy: {accuracy}')