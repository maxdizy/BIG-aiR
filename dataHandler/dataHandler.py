import pandas as pd
import numpy as np

airThresh = 140
inAir = False
tricks = []

dataFile = pd.read_csv('data/testdata1.csv')
df = pd.DataFrame(dataFile)

print(df['FR'].size)

#detect tricks
for i in range(df['FR'].size-2):
    #find start of trick with outlier filter
    if ((inAir == False) & (df['FR'].iloc[i] < airThresh) & (df['FR'].iloc[i + 1] < airThresh) & (df['FR'].iloc[i + 2] < airThresh)):
        trickStart = i
        inAir = True

    #find end of trick with outlier filter
    if ((inAir == True) & (df['FR'].iloc[i] > airThresh) & (df['FR'].iloc[i + 1] > airThresh) & (df['FR'].iloc[i + 2] > airThresh)):
        trickEnd = i
        tricks.append(df.iloc[max(0, trickStart-4) : min(trickEnd+4, df['FR'].size-2)]) #create trick df with +- 1000 millis
        inAir = False

trickNum = 1
for trickData in tricks:
    print('Trick ' + str(trickNum) + ':\n')
    print(trickData)
    print('\n')
    trickNum += 1