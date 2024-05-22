import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,agent,groups):
        super().__init__(groups)
        direction = agent.status.split('_')[0]

        # graphic
        self.image = pygame.Surface((40,40))
        
        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = agent.rect.midright)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = agent.rect.midleft)
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = agent.rect.midbottom)
        else:
            self.rect = self.image.get_rect(midbottom = agent.rect.midtop)


