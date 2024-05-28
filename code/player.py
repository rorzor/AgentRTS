import pygame
from settings import *
import pandas as pd

class Player:
    def __init__(self,obstacle_sprites,spawn_agent,modeller):

        self.spawn_agent = spawn_agent
        self.obstacle_sprites = obstacle_sprites

        # resources
        self.resources = {'organic': 0,
                          'mineral': 0,
                          'agents': 0}
        
        self.max_data_frame_size = MAX_FRAME_SIZE
        self.data_set = []
        self.df_save_cooldown = 500
        self.df_save_time = 0
        self.modeller = modeller

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            self.spawn_agent()
        elif keys[pygame.K_r]:
            self.spawn_agent(True)
        elif keys[pygame.K_p]:
            self.save_dataset()
        elif keys[pygame.K_t]:
            self.train_model()
        elif keys[pygame.K_SPACE]:
            self.data_set = []

    def save_dataset(self):
        if self.can_save:
            print("Saving data set")
            df = pd.DataFrame(self.data_set)
            df.to_csv('training_data.csv', index=False)
            self.df_save_time = pygame.time.get_ticks()
            self.can_save = False
    
    def train_model(self):
        self.modeller.train_model()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.df_save_time >= self.df_save_cooldown:
            self.can_save = True

    def update(self):
        self.input()
        self.cooldowns()