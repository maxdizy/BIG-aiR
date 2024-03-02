import pandas as pd
import numpy as np
import math

airThresh = 62
inAir = False
tricks = []

dataFile = pd.read_csv('data/BIG_aiR_data.csv')
df = pd.DataFrame(dataFile)

# clean dataset
for i in range(df['RBV'].size-2):
    RFP = df['RFP'].iloc[i]
    RBP = float(df['RBP'].iloc[i])
    RFV = df['RFV'].iloc[i]
    RBV = df['RBV'].iloc[i]
    LFP = df['LFP'].iloc[i]
    LBP = float(df['LBP'].iloc[i])
    LFV = df['LFV'].iloc[i]
    LBV = df['LBV'].iloc[i]
    # check front percentages
    if math.isnan(RFP):
        if not math.isnan(float(RBP)):
            df.loc[i, 'RFP'] = 100 - RBP
    if math.isnan(LFP):
        if not math.isnan(float(LBP)):
            df.loc[i, 'LFP'] = 100 - LBP
    # check back percentages
    if math.isnan(RBP):
        if not math.isnan(float(RFP)):
            df.loc[i, 'RBP'] = 100 - RFP
    if math.isnan(LBP):
        if not math.isnan(float(LFP)):
            df.loc[i, 'LBP'] = 100 - LFP
# fill in all missing NaN's
df = df.fillna(0)

# insert result col
df['target'] = 0

#detect tricks
for i in range(df['RBV'].size-2):
    comb = df['RFV'].iloc[i] + df['RBV'].iloc[i] + df['LFV'].iloc[i] + df['LBV'].iloc[i]

    #find start of trick with outlier filter
    if ((inAir == False) & (comb < airThresh)):
        trickStart = i
        #note: this may be an issue if trick detected is before two seconds, size would be less then 12
        tricks.append(df.iloc[max(0, i-4) : min(i+4, df['RBV'].size-2)]) #create trick df with -2000 and +1000 millis
        inAir = True

    #find end of trick with outlier filter
    if ((inAir == True) & (comb > airThresh)):
        inAir = False

# label test data
successfulAttempts = [0,1,2,3,4,6,7,12,13]
target = np.array([1,1,1,1,1,0,1,1,0,0,0,0,1,1])
# for i in range(len(tricks)):
#     if i in successfulAttempts:
#         tricks[i].loc[:,'target'] = 1

tricks_test = tricks[-3:]
trickData_test = np.array([np.array(trick_test.drop('target', axis=1)) for trick_test in tricks_test])
#tricks = tricks[:-3]

#concat data
trickData = np.array([np.array(trick.drop('target', axis=1)) for trick in tricks])
# target = np.array([np.array(trick['target']) for trick in tricks])

#shape for model: 3 tricks, 12 steps, 7 sensors
trickData = trickData.reshape((trickData.shape[0], trickData.shape[1], trickData.shape[2]))