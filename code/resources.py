import pygame
from settings import *
from tile import Tile

class Resource(Tile):
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(pos,groups,sprite_type,surface)

        if sprite_type == 'organic':
            self.capacity = 5
        elif sprite_type == 'mineral':
            self.capacity = 20


