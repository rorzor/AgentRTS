from settings import *
from os import walk
import pygame
from random import random, randint

def create_boundary():
    n = MAPWIDTH
    m = MAPHEIGHT
    
    # initialise list
    boundary = [[-1 for _ in range(n)] for _ in range(m)]
    
    # Set the edges to 50
    for i in range(m):
        for j in range(n):
            if i == 0 or i == m-1 or j == 0 or j == n-1:
                boundary[i][j] = 50
    
    return boundary

def create_resources():
    
    # Function to check if a position is at least 'l' distance away from all existing 52s
    def is_valid_position(x, y, positions, l):
        for px, py in positions:
            if abs(x - px) == 0 or abs(y - py) == 0 or (x < RESOURCEBUFFER and y < RESOURCEBUFFER):
                return False
        return True
    
    n = MAPWIDTH
    m = MAPHEIGHT
    p = ORGANICPROB
    max_mins = STARTINGMINERAL
    l = MINSPACING

    # Initialize the matrix with -1
    matrix = [[-1 for _ in range(n)] for _ in range(m)]
    
    # Set the inner values to organic (51) based on probability p
    for i in range(1, m-1):
        for j in range(1, n-1):
            if random() < p:
                matrix[i][j] = 51

    # Place exactly 'k' entries of mineral (52) in the matrix
    min_positions = []
    attempts = 0
    max_attempts = 1000  # To prevent infinite loop in case placement is impossible
    while len(min_positions) < max_mins and attempts < max_attempts:
        x = randint(1, m-2)
        y = randint(1, n-2)
        if is_valid_position(x, y, min_positions, l):
            matrix[x][y] = 52
            min_positions.append((x, y))
        attempts += 1

    if len(min_positions) < max_mins:
        print("Warning: Could not place all entries with the given constraints.")

    # place more minerals around seeded ones

    for px, py in min_positions:
        for n in range(10):
            ranx = randint(1,3)
            rany = randint(1,3)
            if ranx == 1:
                px += 1
            elif ranx == 2:
                px -= 1
            if rany == 1:
                py += 1
            elif rany == 2:
                py -= 1

            if 10 > px > n or 10 > py > m:
                continue

            matrix[px][py] = 52

            if random() > MINERALPROB:
                continue


    # reset to -1 around spawn just in case 
    for i in range(1, RESOURCEBUFFER):
        for j in range(1, RESOURCEBUFFER):
            matrix[i][j] = -1
    return matrix

def import_folder(path):

    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
            