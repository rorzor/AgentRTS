import pygame

class Player:
    def __init__(self,obstacle_sprites,spawn_agent):

        self.spawn_agent = spawn_agent
        self.obstacle_sprites = obstacle_sprites

        # resources
        self.resources = {'organic': 0,
                          'mineral': 0,
                          'agents': 0}
        

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            print('Spawn new agent')
            self.spawn_agent()
        elif keys[pygame.K_r]:
            print("Respawn player's agent")
            self.spawn_agent(True)

    def update(self):
        self.input()