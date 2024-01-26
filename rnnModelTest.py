import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense
import pandas as pd
import numpy as np

#data handler code
airThresh = 140
tricks = []
inAir = False

#read data file 
df = pd.read_csv('data/testdata1.csv')

df['result'] = 0

#find tricks
for i in range(df['FR'].size-2):
    #find start of trick with outlier filter
    if ((inAir == False) & (df['FR'].iloc[i] < airThresh) & (df['FR'].iloc[i + 1] < airThresh) & (df['FR'].iloc[i + 2] < airThresh)):
        trickStart = i
        #note: this may be an issue if trick detected is before two seconds, size would be less then 12
        tricks.append(df.iloc[max(0, i-8) : min(i+4, df['FR'].size-2)]) #create trick df with -2000 and +1000 millis
        inAir = True

    #find end of trick with outlier filter
    if ((inAir == True) & (df['FR'].iloc[i] > airThresh) & (df['FR'].iloc[i + 1] > airThresh) & (df['FR'].iloc[i + 2] > airThresh)):
        inAir = False

#create array with tricks
data = np.array([np.array(trick.drop('result', axis = 1)) for trick in tricks])
result = np.array([np.array(trick['result']) for trick in tricks])

data = data.reshape((data.shape[0], data.shape[1], data.shape[2]))

#model
model = Sequential()
model.add(keras.Input(shape=(data.shape[1], data.shape[2])))
#potentially use simpleRNN?
model.add(keras.layers.LSTM(50, activation='tanh'))
model.add(Dense(1))
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss=keras.losses.MeanSquaredError(), metrics='accuracy')

#training
model.fit(data, result, batch_size=20, epochs=300, verbose=1)
#is training result saved and used later on?