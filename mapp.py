import tensorflow as tf
import pandas as pd
import numpy as np



directory = "C:\\snowboard_model_weights\\my_model.h5"
data_path = 'C:\\Users\\zane5\\OneDrive\\Desktop\\snowBoardRCNN\\testdata1.csv'

model = tf.keras.models.load_model(directory)

airThresh = 140
inAir = False
tricks = []

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

# Convert list of DataFrames into a NumPy array
data = np.array([np.array(trick.drop('Results', axis=1)) for trick in tricks])

# Extract labels from the 'Results' column
labels = np.array([np.array(trick['Results']) for trick in tricks])

# Reshape data to be a 3D array: [samples, timesteps, features]
data = data.reshape((data.shape[0], data.shape[1], data.shape[2]))


# Assuming data is input data array shaped as [samples, timesteps, features]

# Select a sample for analysis
sample_index = 0  # For demonstration, select the first sample
input_data = data[sample_index:sample_index+1]  # Keep the batch dimension

# Convert input to a TensorFlow tensor
input_tensor = tf.convert_to_tensor(input_data, dtype=tf.float32)

with tf.GradientTape() as tape:
    tape.watch(input_tensor)
    predictions = model(input_tensor)
    predicted_value = predictions[0, 0]

# Compute gradients of the predicted value with respect to the input
gradients = tape.gradient(predicted_value, input_tensor)

# Process gradients to get importance scores
importance_scores = tf.reduce_mean(tf.abs(gradients), axis=-1).numpy()

# importance_score` now holds the importance of each timestep/feature

# set up thresholds to compare sensor readings to "correct" values
thresholds = {
    'Front %': (40, 60),
    'Back %': (40, 60),
    'FR': (150, 250),
    'FL': (150, 250),
    'BL': (150, 250),
    'BR': (150, 250),
    'Millis': (0, 1000)  # Assuming 'Millis' is a timestamp and does not need a range
}


def generate_feedback(importance_scores, trick_data, top_timesteps=3):
    """
    Generate feedback based on importance scores and trick data.
    importance_scores: Importance of each timestep, as calculated by the model.
    trick_data: Sensor data for the specific trick, shape (timesteps, features).
    top_timesteps: Number of timesteps to consider for generating feedback.
    """
    feedback = []
  
    sensor_names = ['Front %', 'Back %', 'FR', 'FL', 'BL', 'BR', 'Millis']
    
    # Find the top timesteps based on importance scores
    top_indices = importance_scores.argsort()[-top_timesteps:][::-1]
    
    for index in top_indices:
        feedback.append(f"At timestep {index}, consider the following adjustments:")
        # Ensure that sensor_values is a 1D array
        sensor_values = trick_data[index, :]  # This should select a single row and give a 1D array

        # Generate feedback for each sensor at this timestep
        for sensor_index, sensor_value in enumerate(sensor_values):
            sensor_name = sensor_names[sensor_index]
            ideal_range = thresholds[sensor_name]

            # Compare the sensor value to the ideal range and provide feedback
            if sensor_value < ideal_range[0] or sensor_value > ideal_range[1]:
                feedback.append(f"The {sensor_name} sensor reading of {sensor_value} is outside the ideal range of {ideal_range}. Consider adjusting your position.")
            else:
                feedback.append(f"The {sensor_name} sensor reading of {sensor_value} is within the ideal range.")

    return "\n".join(feedback)





# Generate feedback using the function

importance_scores = np.squeeze(importance_scores)
print(f"importance_scores shape after squeeze: {importance_scores.shape}")

# Ensuring that we correctly select the data for one trick
if tricks:  # Check if we have detected any tricks
    for trick_index, trick_df in enumerate(tricks):
        # Convert the trick DataFrame to a numpy array and drop the 'Results' column
        trick_data = trick_df.drop('Results', axis=1).to_numpy()

        # Print the shape of trick_data to make sure it is (timesteps, features)
        print(f"trick_data shape for trick {trick_index}: {trick_data.shape}")

        # Generate feedback for the current trick
        feedback = generate_feedback(importance_scores, trick_data)
        print(f"Feedback for trick {trick_index}:\n{feedback}\n")
else:
    print("No tricks were detected.")


