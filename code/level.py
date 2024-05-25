import pygame
from random import choice
from settings import *
from tile import Tile
from agent import Agent
from debug import debug
from support import *
from weapon import Weapon
from player import Player
from ui import UI
from resources import Resource

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.attack_sprites = pygame.sprite.Group()
		self.harvestable_sprites = pygame.sprite.Group()

		self.player_agent = None
		# create player
		self.player = Player(self.player_agent,self.obstacle_sprites,self.spawn_agent)

		# sprite setup
		self.create_map()

		# user interface
		self.ui = UI()

	def create_map(self):
		# spawn the player agent
		self.spawn_agent(True)

		# spawn the landed ship
		ship_surf = pygame.image.load('../graphics/ship/ship_1.png').convert_alpha()
		Tile((64,64),[self.visible_sprites,self.obstacle_sprites],'ship',ship_surf)		
		
		# create the layouts
		layouts = {
			'boundary': create_boundary(),
			'resources': create_resources()
		}
		graphics = {
			'organics': import_folder('../graphics/organics'),
			'minerals': import_folder('../graphics/minerals')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != -1:
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'resources':
							# spawn organics
							if col == 51:
								random_plant_image = choice(graphics['organics'])
								Resource((x,y),
			 						[self.visible_sprites,self.obstacle_sprites,self.harvestable_sprites],
									'organic',
									random_plant_image)
							# spawn minerals
							if col == 52:
								random_mineral_image = choice(graphics['minerals'])
								Resource((x,y),
			 						[self.visible_sprites,self.obstacle_sprites,self.harvestable_sprites],
									'mineral',
									random_mineral_image)

	def spawn_agent(self,players_agent = False):
		# check if spawn location is free
		for sprite in self.obstacle_sprites:
			# if sprite.sprite_type == 'ship':
			# 	continue
			if 200 <= sprite.rect.center[0] <= 400 and 200 <= sprite.rect.center[1] <= 400:
				return debug('Spawn Point Occupied')

		# spawn agent.
		if players_agent:
			if self.player_agent is not None:
				self.player_agent.kill()
				if self.player.resources['agents'] > 0:
					self.player.resources['agents'] -= 1
			self.player_agent = Agent(self.player,(300,300),[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites, self.create_attack)
		else:
			Agent(self.player,(300,300),[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites, self.create_attack)

	def create_attack(self,agent):
		Weapon(agent,[self.visible_sprites,self.attack_sprites])

	def agent_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				# check for valid harvest
				if not attack_sprite.harvesting:
					collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.harvestable_sprites,False)
					for target_sprite in collision_sprites:
						for resource_type in resource_harvest.keys():
							if target_sprite.sprite_type == resource_type and not attack_sprite.harvesting:
								target_sprite.capacity -= 1
								self.player.resources[resource_type] += resource_harvest[resource_type]
								attack_sprite.harvesting = True
								if target_sprite.capacity == 0:
									target_sprite.kill()
								break

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player_agent)
		self.visible_sprites.update()
		self.player.update()
		self.agent_attack_logic()
		self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surface = pygame.image.load('../graphics/level/floormap1.png').convert()
		self.floow_rect	= self.floor_surface.get_rect(topleft = (0,0))

	def custom_draw(self,player_agent):

		# getting the offset 
		self.offset.x = player_agent.rect.centerx - self.half_width
		self.offset.y = player_agent.rect.centery - self.half_height

		# draw the floor
		floor_offset_pos = self.floow_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surface,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
