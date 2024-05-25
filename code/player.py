import pygame

class Player:
    def __init__(self,agent,obstacle_sprites,spawn_agent):

        self.spawn_agent = spawn_agent

        # resources
        self.resources = {'organic': 0,
                          'mineral': 0,
                          'agents': 0}
        
    def save_data_frame_saver(self):
        # TODO write logic to save surrounding sprites by type and position
        # must be in a 9x9 grid around the player_agent in the middle
        # all other sprites within that field are placed into one of the remainign 'squares'
        # should be called whenever the player inputs a move command, and save that command along with the grid at that time
        pass

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