import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,agent,groups):
        super().__init__(groups)
        direction = agent.status.split('_')[0]

        # graphic
        full_path = f'../graphics/weapons/{agent.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        # timer
        self.deploy_time = pygame.time.get_ticks()
        self.deploy_cooldown = 200
        self.harvesting = False

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = agent.rect.midright)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = agent.rect.midleft)
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = agent.rect.midbottom)
        else:
            self.rect = self.image.get_rect(midbottom = agent.rect.midtop)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.deploy_time >= self.deploy_cooldown:
            self.kill()

    def update(self):
        self.cooldown()