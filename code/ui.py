import pygame
from settings import *

class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_resources(self,player):
        x = self.display_surface.get_size()[0] - 300

        # show organics
        text_surf = self.font.render('Organic: ' + str(int(player.resources['organic'])),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (x,10))
        self.display_surface.blit(text_surf,text_rect)

        # show minerals
        text_surf = self.font.render('Minerals: ' + str(int(player.resources['mineral'])),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (x,30))
        self.display_surface.blit(text_surf,text_rect)

        # show minerals
        text_surf = self.font.render('Agents: ' + str(int(player.resources['agents'])),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (x,50))
        self.display_surface.blit(text_surf,text_rect)

        # show data frames
        text_surf = self.font.render('Data Frames: ' + str(int(len(player.data_set))) + '/' + str(int(player.max_data_frame_size)),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (x,70))
        self.display_surface.blit(text_surf,text_rect)

        # show model
        model = 'Random' if player.modeller.model is None else 'AI'
        text_surf = self.font.render(f'Model: {model}',False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (x,90))
        self.display_surface.blit(text_surf,text_rect)

    def show_recording(self,player):
        x = self.display_surface.get_size()[0] / 2 - 100
        state = 'ON' if player.can_record_frame else 'OFF'
        colour = RECORDING if player.can_record_frame else NOT_RECORDING
        text_surf = self.font.render(f'Recording: {state}',False,colour)
        text_rect = text_surf.get_rect(topleft = (x,10))
        self.display_surface.blit(text_surf,text_rect)

    def show_bar(self,current,max_amount,bg_rect,color):

        # draw background
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        # convert stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

    def display(self,player,agent):
        self.show_bar(agent.health,agent.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(agent.energy,agent.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
        self.show_recording(player)
        self.show_resources(player)
        pass