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
        self.can_record_frame = True
        self.data_set = []
        self.df_save_cooldown = 500
        self.df_save_time = 0
        self.modeller = modeller

        self.input_cooldown = 200
        self.input_start = 0
        self.can_input = True

    def input(self):
        if self.can_input:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_s]:
                self.spawn_agent()
            elif keys[pygame.K_r]:
                self.spawn_agent(True)
            elif keys[pygame.K_p]:
                self.save_dataset()
                self.input_start = pygame.time.get_ticks()
                self.can_input = False
            elif keys[pygame.K_t]:
                self.train_model()
                self.input_start = pygame.time.get_ticks()
                self.can_input = False
            elif keys[pygame.K_SPACE]:
                self.can_record_frame = not self.can_record_frame
                self.input_start = pygame.time.get_ticks()
                self.can_input = False
            elif keys[pygame.K_BACKSPACE]:
                self.data_set = []
                self.input_start = pygame.time.get_ticks()
                self.can_input = False

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
        if current_time - self.input_start >= self.input_cooldown:
            self.can_input = True

    def update(self):
        self.input()
        self.cooldowns()