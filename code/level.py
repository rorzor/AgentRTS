import pygame
import numpy as np
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
from modeller import Modeller

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.attack_sprites = pygame.sprite.Group()
		self.harvestable_sprites = pygame.sprite.Group()

		# model trainer
		self.modeller = Modeller()

		# create player
		self.player = Player(self.obstacle_sprites,self.spawn_agent,self.modeller)
		self.player_agent = None
		
		# sprite setup
		self.graphics = {
			'organics': import_folder('../graphics/organics/plants'),
			'minerals': import_folder('../graphics/minerals'),
			'seeds': 	import_folder('../graphics/organics/seeds')
		}
		self.create_map()

		# user interface
		self.ui = UI()

	def create_map(self):
		# spawn the player agent
		self.spawn_agent(True)

		# spawn the landed ship
		ship_surf = pygame.image.load('../graphics/ship/ship_1.png').convert_alpha()
		Tile((64,128),[self.visible_sprites,self.obstacle_sprites],'ship',ship_surf)		
		
		# create the layouts
		layouts = {
			'boundary': create_boundary(),
			'resources': create_resources()
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
								random_plant_image = choice(self.graphics['organics'])
								Resource((x,y),
			 						[self.visible_sprites,self.obstacle_sprites,self.harvestable_sprites],
									'organic',
									random_plant_image,
									self.create_organic)
							# spawn minerals
							if col == 52:
								random_mineral_image = choice(self.graphics['minerals'])
								Resource((x,y),
			 						[self.visible_sprites,self.obstacle_sprites,self.harvestable_sprites],
									'mineral',
									random_mineral_image)

	def spawn_agent(self,players_agent = False):
		# check if spawn location is free
		for sprite in self.obstacle_sprites:
			if 200 <= sprite.rect.center[0] <= 400 and 200 <= sprite.rect.center[1] <= 400:
				return debug('Spawn Point Occupied')

		if players_agent:
			# spawn player's agent.
			if self.player.resources['agents'] > 0:
					self.player.resources['agents'] -= 1
			self.player.resources['organic'] -= resource_consumption['agent_spawn']
			if self.player_agent:
				self.player_agent.kill()
			self.player_agent = Agent(self.player,
										True,
										(300,300),
										[self.visible_sprites,self.obstacle_sprites],
										self.obstacle_sprites,
										self.create_attack,
										self.get_data_frame)
			print("Respawn player's agent")

		else:
			# spawn AI agent
			if self.player.resources['organic'] < 10:
				return debug('Insufficient Organic Resources') 
			
			self.player.resources['organic'] -= resource_consumption['agent_spawn']

			Agent(self.player,
				False,
				(300,300),
				[self.visible_sprites,self.obstacle_sprites],
				self.obstacle_sprites,
				self.create_attack,
				self.get_data_frame)
			
			print('Spawn new agent')

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
									self.create_organic(target_sprite.rect.topleft,'seed')
									target_sprite.kill()
								break

	def get_data_frame(self,agent):
		nearby_sprites = []
		data = np.zeros((2 * DATAFRAME_RADIUS + 1, 2 * DATAFRAME_RADIUS + 1), dtype=int)
		data[(DATAFRAME_RADIUS,DATAFRAME_RADIUS)] = 0
		x = agent.rect.center[0]
		y = agent.rect.center[1]
		pixel_distance = (DATAFRAME_RADIUS+1) * TILESIZE
		# find all (collision) sprites near player agent
		for sprite in self.obstacle_sprites:
			if sprite is not agent:				
				if abs(sprite.rect.center[0] - x)  <= pixel_distance and abs(sprite.rect.center[1] - y)  <= pixel_distance:
					nearby_sprites.append(sprite)

		for sprite in nearby_sprites:
			posx = (sprite.rect[0]-x) // TILESIZE + DATAFRAME_RADIUS + 1
			posy = (sprite.rect[1]-y) // TILESIZE + DATAFRAME_RADIUS + 1
			try:
				data[posy,posx] = SPRITE_CODES[sprite.sprite_type]
			except:
				pass
		return data.flatten()

	def sprout(self,seed):
		for sprite in self.obstacle_sprites:
			if sprite.sprite_type == 'agent':
				if abs(sprite.rect.center[0] - seed.rect.center[0]) < 100 and abs(sprite.rect.center[1] - seed.rect.center[1]) < 100 :
					return
		self.create_organic(seed.pos,'organic')
		seed.kill()


	def create_organic(self,pos,type):
		if type == 'organic':
			random_plant_image = choice(self.graphics['organics'])
			Resource(pos,
				[self.visible_sprites,self.obstacle_sprites,self.harvestable_sprites],
				'organic',
				random_plant_image)
		elif type == 'seed':
			seed_image = choice(self.graphics['seeds'])
			Resource(pos,
				[self.visible_sprites],
				'seed',
				seed_image,
				self.create_organic,
				self.sprout
				)

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player_agent)
		self.visible_sprites.update()
		self.player.update()
		self.agent_attack_logic()
		self.ui.display(self.player,self.player_agent)

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

		# draw the seeds (or anything else on the floor)
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			try:
				if sprite.sprite_type == 'seed':
					offset_pos = sprite.rect.topleft - self.offset
					self.display_surface.blit(sprite.image,offset_pos)
			except:
				pass
		#draw 3D objects
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			try:
				if sprite.sprite_type == 'seed':
					continue
			except:
				pass
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
