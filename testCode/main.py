import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
from dataHandler import tricks

trickNum = 1
for trick in tricks:
    results = trick.pop('results')
    tf.convert_to_tensor(trick)
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(trick)
    normalizer(trick.iloc[:3])