from settings import *
from os import walk
import pygame
from random import random

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
    n = MAPWIDTH
    m = MAPHEIGHT
    p = ORGANICPROB

    # Initialize the matrix with -1
    matrix = [[-1 for _ in range(n)] for _ in range(m)]
    
    # Set the inner values based on probability p
    for i in range(1, m-1):
        for j in range(1, n-1):
            if random() < p:
                matrix[i][j] = 51
    return matrix

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
            