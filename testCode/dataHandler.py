import pandas as pd
import numpy as np

airThresh = 140
inAir = False
tricks = []

dataFile = pd.read_csv('data/testdata1.csv')
df = pd.DataFrame(dataFile)

#insert result col
df['target'] = 0

#detect tricks
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

#concat data
trickData = np.array([np.array(trick.drop('target', axis=1)) for trick in tricks])
target = np.array([np.array(trick['target']) for trick in tricks])

#shape for model: 3 tricks, 12 steps, 7 sensors
trickData = trickData.reshape((trickData.shape[0], trickData.shape[1], trickData.shape[2]))