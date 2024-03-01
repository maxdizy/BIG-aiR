import tensorflow as tf

# Assuming data is input data array shaped as [samples, timesteps, features]

# Select a sample for analysis
sample_index = 0  # For demonstration, select the first sample
input_data = data[sample_index:sample_index+1]  # Keep the batch dimension

# Convert input to a TensorFlow tensor
input_tensor = tf.convert_to_tensor(input_data, dtype=tf.float32)

with tf.GradientTape() as tape:
    tape.watch(input_tensor)
    predictions = model(input_tensor)
    # Assuming your model predicts a continuous value, select the output
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
        sensor_values = trick_data[index]

        # Generate feedback for each sensor at this timestep
        for sensor_index, value in enumerate(sensor_values):
            sensor_name = sensor_names[sensor_index]
            ideal_range = thresholds[sensor_name]

            # Compare the sensor value to the ideal range and provide feedback
            if not ideal_range[0] <= value <= ideal_range[1]:
                feedback.append(f"The {sensor_name} sensor reading of {value} is outside the ideal range of {ideal_range}. Consider adjusting your position.")
            else:
                feedback.append(f"The {sensor_name} sensor reading of {value} is within the ideal range.")

    return "\n".join(feedback)


# Generate feedback using the function
feedback = generate_feedback(importance_scores, trick_data)
print(feedback)
