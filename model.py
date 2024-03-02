from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import numpy as np
import os

# Define paths
directory = "C:\\snowboard_model_weights"
data_path = 'C:\\Users\\zane5\\OneDrive\\Desktop\\snowBoardRCNN\\testdata1.csv'

# Create the model directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Define the full model path
model_path = os.path.join(directory, "my_model.h5")

# Load the dataset
df = pd.read_csv(data_path)

# Initialize a column 'Results' with binary classification targets
df['Results'] = 0  # Ensure this column reflects your actual binary targets

# Detection thresholds and initializations
airThresh = 140
inAir = False
tricks = []

# Trick detection logic
for i in range(df['FR'].size - 2):
    if (not inAir) and (df['FR'].iloc[i] < airThresh) and (df['FR'].iloc[i + 1] < airThresh) and (df['FR'].iloc[i + 2] < airThresh):
        trickStart = i
        inAir = True
    if (inAir) and (df['FR'].iloc[i] > airThresh) and (df['FR'].iloc[i + 1] > airThresh) and (df['FR'].iloc[i + 2] > airThresh):
        trickEnd = i
        trick_df = df.iloc[max(0, trickStart - 4):min(trickEnd + 4, df['FR'].size - 2)]
        if len(trick_df) > 19:
            trick_df = trick_df.iloc[-19:]
        tricks.append(trick_df)
        inAir = False

# Assume last detected trick's shape for model input
num_timesteps = len(trick_df)
num_features = 7  # Adjust based on your actual features

# Model definition
model = Sequential([
    LSTM(50, activation='relu', input_shape=(num_timesteps, num_features)),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Convert tricks data into a suitable format
data = np.array([trick.drop('Results', axis=1).to_numpy() for trick in tricks])
labels = np.array([trick['Results'].iloc[0] for trick in tricks])  # Assuming a single label per trick

# Reshape data to match the expected model input
data = data.reshape((data.shape[0], data.shape[1], num_features))

# Train the model
history = model.fit(data, labels, epochs=200, verbose=1)

# Save the model
model.save(model_path)

# Print training history
for key in history.history:
    for epoch, value in enumerate(history.history[key]):
        print(f"Epoch {epoch + 1}: {key} = {value}")
