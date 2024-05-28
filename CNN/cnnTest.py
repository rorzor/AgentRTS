import pandas as pd
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

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
    
# Load the dataset
df = pd.read_csv('training_data.csv')
df_test = pd.read_csv('training_dataTEST.csv')

# Convert the 'matrix' column to 9x9 numpy arrays
df['matrix'] = df['matrix'].apply(string_to_matrix)
print(df['matrix'])

df_test['matrix'] = df_test['matrix'].apply(string_to_matrix)

# Drop rows where the conversion failed
df = df.dropna(subset=['matrix'])
df_test = df_test.dropna(subset=['matrix'])

# Prepare the input feature array by stacking the matrices
X = np.stack(df['matrix'].values)
Xt = np.stack(df_test['matrix'].values)

# Normalize the input data
X = X / 2.0  # Normalize to range 0-1
Xt = Xt / 2.0  # Normalize to range 0-1

# Prepare labels
label_dict = {label: idx for idx, label in enumerate(['up', 'down', 'left', 'right'])}
y = to_categorical(df['label'].map(label_dict))  # Convert labels to one-hot encoding
yt = to_categorical(df_test['label'].map(label_dict))  # Convert labels to one-hot encoding

# Reshape input data to fit Keras's CNN input requirements
X = X.reshape(X.shape[0], 9, 9, 1)  # Add channel dimension
Xt = Xt.reshape(Xt.shape[0], 9, 9, 1)  # Add channel dimension

# Define the CNN Architecture
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(9, 9, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(4, activation='softmax')  # Assuming 4 classes for 'up', 'down', 'left', 'right'
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.1)
model.save("test_model.keras", overwrite=True)

# This would require us to have a separate test set

test_loss, test_acc = model.evaluate(Xt, yt)
print(f"Test Accuracy: {test_acc}")
