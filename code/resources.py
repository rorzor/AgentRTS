import pygame
from settings import *
from tile import Tile
from random import random

class Resource(Tile):
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE)),create_organic = None, sprout = None):
        super().__init__(pos,groups,sprite_type,surface)
        self.create_organic = create_organic
        self.sprout = sprout

        self.pos = pos
        self.sprite_type = sprite_type
        self.sprout_time = 20000
        
        if sprite_type == 'organic':
            self.capacity = 5
        elif sprite_type == 'mineral':
            self.capacity = 20
        elif sprite_type == 'seed':
            self.start_time = pygame.time.get_ticks()
    
    def sprout_check(self):
        if self.sprite_type == 'seed':
            current_time = pygame.time.get_ticks()
            can_sprout = current_time - self.start_time > self.sprout_time
            if can_sprout and random() < SEED_SPAWN:
                print('Sprout seed')
                self.sprout(self)

    def update(self):
        self.sprout_check()

    