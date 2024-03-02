import tensorflow as tf
import numpy as np
import pandas as pd
from datahandler import trickData, target, trickData_test
# Assuming 'trickData_test' is already in your workspace, otherwise, load or preprocess it as necessary.

# Load the model
model_path = "C:\\snowboard_model_weights\\my_model.h5"
model = tf.keras.models.load_model(model_path)

sample_num = 0
index_change = {
    0 : 1,
    1 : 4, 
    2 : 5
}

while(sample_num < 3 ):


    # Prepare the input tensor
    # If trickData_test needs loading or preprocessing, make sure to do so before this step
    input_tensor = tf.convert_to_tensor(trickData_test[sample_num:sample_num + 1], dtype=tf.float32)
    # print(trickData_test)

    # Calculate gradients to get importance scores
    with tf.GradientTape() as tape:
        tape.watch(input_tensor)
        predictions = model(input_tensor)
        
        

    # Get the gradients of the predicted value with respect to the input
    gradients = tape.gradient(predictions, input_tensor)
    # Aggregate importance scores across all outputs (if your model has multiple outputs)
    importance_scores = np.mean(np.abs(gradients), axis=0)

    # Assuming the first dimension is the batch dimension and you're interested in the first sample
    # Direct extraction of importance scores for the single sample and single output
    importance_scores_single_sample = np.abs(gradients.numpy().squeeze())

    # Calculate the mean importance score for each feature across all sets of scores
    consolidated_importance_scores = np.mean(importance_scores_single_sample, axis=0)
    # print(consolidated_importance_scores)



    # Define the thresholds for feedback
    # Define the thresholds for feedback
    # The values here are placeholders. Replace them with your actual thresholds based on domain knowledge.
    thresholds = {
        'RFP': (30, 60), # Assuming a range around the average to allow for normal fluctuations
        'RBP': (100, 130), # Same as above
        'RFV': (50, 70), # This seems to be a percentage or a value that should be close to the average
        'RBV': (250, 500), # Allowing a broad range due to high max value
        'RZA': (-9, 12), # A range around the average allowing for some negative values
        'RXA': (-3, 0), # Assuming that positive values are not expected
        'RZG': (-1, 3), # A small range around the average
        'LFP': (30, 70), # A range around the average
        'LBP': (130, 160), # Same as above
        'LFV': (200, 500), # A broad range considering the high maximum
        'LBV': (400, 600), # A range that captures most of the data
        'LZA': (8, 30), # A range around the average, assuming positive values are expected
        'LXA': (0, 30), # A range around the average, allowing for slight negative values
        'LZG': (0, 10), # A range around the average
        'M': (3500, 4500), # A broad range considering the high maximum
        'target':(1,1)
    }


    indicies = {
        'RFP': 0,  
        'RBP': 1, 
        'RFV': 2, 
        'RBV': 3,  
        'RZA': 4, 
        'RXA': 5,  
        'RZG': 6,  
        'LFP': 7,  
        'LBP': 8,  
        'LFV': 9, 
        'LBV': 10,  
        'LZA': 11,  
        'LXA': 12,  
        'LZG': 13,  
        'M': 14,  
        'target':15
    }

    # If trickData_test is a DataFrame, extract the values
    if isinstance(trickData_test, pd.DataFrame):
        sensor_data = trickData_test.to_numpy()
    else:
        sensor_data = trickData_test

    sensor_names = ['RFP', 'RBP', 'RFV', 'RBV', 'RZA', 'RXA', 'RZG', 'LFP', 'LBP', 'LFV', 'LBV', 'LZA', 'LXA', 'LZG', 'M', 'target']



    def generate_feedback(consolidated_importance_scores, sample, thresholds, sensor_names, top_features=3):
        feedback = []
        # Get indices of top features based on importance scores
        top_indices = np.argsort(consolidated_importance_scores)[-top_features:]

        feedback.append("Feedback for selected sample:")
        for index in reversed(top_indices):  # Iterate in descending order of importance
            # print(top_indices)
            sensor_name = sensor_names[index]
            # print(sensor_name)
            # print(indicies[sensor_name])
            # print(index)
            sensor_value = sample[index-index_change[sample_num]][indicies[sensor_name]]  # Assuming 'sample' is a 1D array of feature values
            # print(sample)
            # print(index)
            # print(indicies[sensor_name])
            # print(sensor_value)
            
            
            ideal_range = thresholds[sensor_name]

            # Generate feedback based on how sensor value compares to the ideal range
            if sensor_value < ideal_range[0]:
                feedback_msg = f"{sensor_name}: Value {sensor_value} is below the ideal range ({ideal_range[0]}, {ideal_range[1]}). Consider adjusting."
            elif sensor_value > ideal_range[1]:
                feedback_msg = f"{sensor_name}: Value {sensor_value} is above the ideal range ({ideal_range[0]}, {ideal_range[1]}). Consider adjusting."
            else:
                feedback_msg = f"{sensor_name}: Value {sensor_value} is within the ideal range."

            feedback.append(feedback_msg)

        return feedback

    # Assuming trickData_test[0] is correctly formatted as a 1D array of feature values for the sample of interest
    sample_feature_values = trickData_test[0] if isinstance(trickData_test, np.ndarray) else trickData_test.iloc[0].to_numpy()
    feedback = generate_feedback(consolidated_importance_scores, sample_feature_values, thresholds, sensor_names)
    print("\n".join(feedback))
    sample_num = sample_num + 1
