import pandas as pd
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.saving import load_model
from settings import *

class Modeller:
    def __init__(self):
        self.model = None
        # Define a list of labels
        self.labels = ['up', 'down', 'left', 'right']
        # Create a dictionary that maps each label to a unique index
        self.label_dict = {label: index for index, label in enumerate(self.labels)}

    def string_to_matrix(self,matrix_string):
        # Remove square brackets if present
        clean_string = matrix_string.strip("[]")
        try:
            # Convert string to float list
            matrix = np.array(clean_string.split(), dtype=float).reshape(2*DATAFRAME_RADIUS+1, 2*DATAFRAME_RADIUS+1)
            return matrix
        except ValueError:
            # This will catch strings that don't split into 81 items
            return None
    
    def train_model(self):
        # Load the dataset
        df = pd.read_csv('training_data.csv')
        #df_test = pd.read_csv('training_dataTEST.csv')

        # Convert the 'matrix' column to 9x9 numpy arrays
        df['matrix'] = df['matrix'].apply(self.string_to_matrix)
        #df_test['matrix'] = df_test['matrix'].apply(self.string_to_matrix)

        # Drop rows where the conversion failed
        df = df.dropna(subset=['matrix'])
        #df_test = df_test.dropna(subset=['matrix'])

        # Prepare the input feature array by stacking the matrices
        X = np.stack(df['matrix'].values)
        #Xt = np.stack(df_test['matrix'].values)

        # Normalize the input data
        X = X / len(SPRITE_CODES)  # Normalize to range 0-1
        #Xt = Xt / 2.0  # Normalize to range 0-1

        # Prepare labels
        label_dict = {label: idx for idx, label in enumerate(['up', 'down', 'left', 'right'])}
        y = to_categorical(df['label'].map(label_dict))  # Convert labels to one-hot encoding
        #yt = to_categorical(df_test['label'].map(label_dict))  # Convert labels to one-hot encoding

        # Reshape input data to fit Keras's CNN input requirements
        X = X.reshape(X.shape[0], 2*DATAFRAME_RADIUS+1, 2*DATAFRAME_RADIUS+1, 1)  # Add channel dimension
        #Xt = Xt.reshape(Xt.shape[0], 11, 11, 1)  # Add channel dimension

        # Define the CNN Architecture
        model = Sequential([
            Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(2*DATAFRAME_RADIUS+1, 2*DATAFRAME_RADIUS+1, 1)),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(4, activation='softmax')  # Assuming 4 classes for 'up', 'down', 'left', 'right'
        ])

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Train the model
        model.fit(X, y, epochs=10, batch_size=32, validation_split=0.1)
        model.save("test_model.keras", overwrite=True)
        self.model_loader()
        # This would require us to have a separate test set

        #test_loss, test_acc = model.evaluate(Xt, yt)
        #print(f"Test Accuracy: {test_acc}")

    def model_loader(self):
        # Load a saved model
        self.model = load_model('test_model.keras')