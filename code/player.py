import pygame

class Player:
    def __init__(self):

        # resources
        self.resources = {'organic': 0,
                          'mineral': 0,
                          'agents': 0}
    
    def modify_resource(self,resource,amount):
        self.resources[resource] += amount
    
    