import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from dataHandler import tricks

trickNum = 1
for trickData in tricks:
    print('Trick ' + str(trickNum) + ':\n')
    print(trickData)
    print('\n')
    trickNum += 1