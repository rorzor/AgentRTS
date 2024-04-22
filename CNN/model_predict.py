from keras.saving import load_model
from keras.applications.imagenet_utils import decode_predictions
import numpy as np
import pandas as pd

def string_to_matrix(matrix_string):
    # Remove square brackets if present
    clean_string = matrix_string.strip("[]")
    try:
        # Convert string to float list
        matrix = np.array(clean_string.split(), dtype=float).reshape(9, 9)
        return matrix
    except ValueError:
        # This will catch strings that don't split into 81 items
        return None
    
# Load a saved model
model = load_model('test_model.keras')

# Load and prepare new data
df_new = pd.read_csv('training_dataTEST.csv')
df_new['matrix'] = df_new['matrix'].apply(string_to_matrix)
df_new = df_new.dropna(subset=['matrix'])
X_new = np.stack(df_new['matrix'].values)
X_new = X_new / 2.0  # Normalize
X_new = X_new.reshape(X_new.shape[0], 9, 9, 1)

# Define a list of labels
labels = ['up', 'down', 'left', 'right']

# Create a dictionary that maps each label to a unique index
label_dict = {label: index for index, label in enumerate(labels)}

for i in range(X_new.shape[0]):
    # Select the instance and reshape it to (1, 9, 9, 1) to match the input shape the model expects
    instance = X_new[i].reshape(1, 9, 9, 1)
    print(X_new[i])

    # Make a prediction
    prediction = model.predict(instance)
    
    # Get the class index with the highest probability
    predicted_class_index = np.argmax(prediction)
    
    # Optionally, convert the index to a label
    predicted_label = list(label_dict.keys())[predicted_class_index]
    
    # Print or process the result as needed
    print(f"Data Point {i + 1}: Predicted Label = {predicted_label}")
    input()