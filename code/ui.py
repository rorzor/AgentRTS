import pygame
from settings import *

class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

    def show_resources(self,player):
        
        # show organics
        text_surf = self.font.render('Organic: ' + str(int(player.resources['organic'])),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (10,10))
        self.display_surface.blit(text_surf,text_rect)

        # show minerals
        text_surf = self.font.render('Minerals: ' + str(int(player.resources['mineral'])),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (10,30))
        self.display_surface.blit(text_surf,text_rect)

    def display(self,player):
        self.show_resources(player)
        pass