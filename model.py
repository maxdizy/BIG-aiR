from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import numpy as np

airThresh = 140
inAir = False
tricks = []

data_path = 'C:\\Users\\zane5\\OneDrive\\Desktop\\snowBoardRCNN\\testdata1.csv'

df = pd.read_csv(data_path)

# Add a new column Results with all zeros
df['Results'] = 0

print(df['FR'].size)

#detect tricks
for i in range(df['FR'].size-2):
    #find start of trick with outlier filter
    if (not inAir) and (df['FR'].iloc[i] < airThresh) and (df['FR'].iloc[i + 1] < airThresh) and (df['FR'].iloc[i + 2] < airThresh):
        trickStart = i
        inAir = True

    #find end of trick with outlier filter
    if (inAir) and (df['FR'].iloc[i] > airThresh) and (df['FR'].iloc[i + 1] > airThresh) and (df['FR'].iloc[i + 2] > airThresh):
        trickEnd = i
        trick_df = df.iloc[max(0, trickStart-4) : min(trickEnd+4, df['FR'].size-2)]

        # If the number of timestamps is greater than 19, trim the trick data
        if len(trick_df) > 19:
            trick_df = trick_df.iloc[-19:]  # Keep the last 19 rows
            
        tricks.append(trick_df)
        inAir = False

num_timesteps = len(trick_df)
num_features = 7    # number of sensor inputs

model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(num_timesteps, num_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Convert list of DataFrames into a NumPy array
data = np.array([np.array(trick.drop('Results', axis=1)) for trick in tricks])

# Extract labels from the 'Results' column
labels = np.array([np.array(trick['Results']) for trick in tricks])

# Reshape data to be a 3D array: [samples, timesteps, features]
data = data.reshape((data.shape[0], data.shape[1], data.shape[2]))

# Train the model
# Train the model and save the history
history = model.fit(data, labels, epochs=200, verbose=1)

# history.history['loss'] will contain the loss at each epoch
loss_per_epoch = history.history['loss']
for epoch, loss in enumerate(loss_per_epoch):
    print(f"Epoch {epoch+1}/{len(loss_per_epoch)} - loss: {loss}")
