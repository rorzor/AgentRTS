import numpy as np
import pygame
import pandas as pd
from keras.saving import load_model


class Board:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.board[(4,4)] = 2  # Center
        self.resource_count = 0
        self.score = 0

    def grow_resource(self):
        # Define all positions except the center
        possible_positions = [(i, j) for i in range(9) for j in range(9) if (i, j) != (4, 4)]
        
        # Randomly select one of these positions
        random_position = np.random.choice(len(possible_positions))
        chosen_position = possible_positions[random_position]
        
        # Place a '1' at the chosen position
        self.board[chosen_position] = 1

    def update_board(self, direction):
        self.board[(4,4)] = 0  # zero center
        
        # shift existing entries based on input
        if direction == 'left':
            # Shift all columns to the left
            self.board[:, :-1] = self.board[:, 1:]  # Copy every column from the second to the last, to the column to its left
            self.board[:, -1] = 0  # Set the last column to zeros
        elif direction == 'right':
            # Shift all columns to the right
            self.board[:, 1:] = self.board[:, :-1]  # Copy every column from the first to the second last, to the column to its right
            self.board[:, 0] = 0  # Set the first column to zeros
        elif direction == 'up':
            # Shift all rows up
            self.board[:-1, :] = self.board[1:, :]  # Copy each row from the second to the last, to the row above it
            self.board[-1, :] = 0  # Set the last row to zeros
        elif direction == 'down':
            # Shift all rows down
            self.board[1:, :] = self.board[:-1, :]  # Copy each row from the first to the second last, to the row below it
            self.board[0, :] = 0  # Set the first row to zeros
        else:
            raise ValueError("Direction must be 'up', 'down', 'left', or 'right'")
        
        # increment score if resource is at (4,4)
        if self.board[(4,4)] == 1:
            self.score +=1

        # grow a resource if none are available
        self.resource_count = np.count_nonzero(self.board == 1)
        if self.resource_count < 1:
            self.grow_resource()
        
        # potentially grow more resources is fewer than 4 in view
        if self.resource_count < 4:
            if np.random.choice(4) > self.resource_count:
                self.grow_resource()

        self.board[(4,4)] = 2  # reset center
        print(f'Score count: {self.score}')


# Function to save data to a CSV file
def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv('training_data.csv', index=False)

def predict_action(boardstate):
    boardstate = boardstate / 2.0 # normalise
    instance = boardstate.reshape(1, 9, 9, 1)

    # Make a prediction
    prediction = model.predict(instance)[0]
    print(f'Prediction confidence: {prediction}')
    
    # Get the class index with the highest probability
    #predicted_class_index = np.argmax(prediction)

    # Sample from the probability distribution
    predicted_class_index = np.random.choice(len(prediction), p=prediction)
    
    # Optionally, convert the index to a label
    predicted_label = list(label_dict.keys())[predicted_class_index]
    
    # Print or process the result as needed
    print(f"Predicted action = {predicted_label}")
    return predicted_label
    

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((300, 300))  # Initialize a window or screen for display
board = Board()
data = []  # List to store all data entries
selection = None
frames_collected = 0

# Optionally load in a keras model to compare result
print('Load existing model: test_model.keras? y/n')
ans = input()
if ans == 'y':
    # Load a saved model
    model = load_model('test_model.keras')
    # Define a list of labels
    labels = ['up', 'down', 'left', 'right']
    # Create a dictionary that maps each label to a unique index
    label_dict = {label: index for index, label in enumerate(labels)}

running = True
board.grow_resource()

while running:
    print(board.board)
    waiting_for_input = True
    print(f'Q to save and quit. Frames collected: {frames_collected}')
    
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    # Update the board and wait for another input
                    selection = pygame.key.name(event.key)

                    print(f"Detected key press: {selection}")
                    data.append({'matrix': board.board.flatten(), 'label': selection})
                    frames_collected += 1
                    board.update_board(selection)
                    waiting_for_input = False
        
                elif event.key in [pygame.K_m]:
                    # make a prediction based on the pretrained model and take action
                    selection = predict_action(board.board.flatten())
                    board.update_board(selection)
                    waiting_for_input = False
                
                elif event.key in [pygame.K_q]:
                    save_data(data)
                    pygame.quit()
    
pygame.quit()
