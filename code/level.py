import pygame 
from settings import *
from tile import Tile
from agent import Agent
from debug import debug
from support import *
from random import choice
from weapon import Weapon

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		# spawn the player agent
		self.player = Agent((300,300),[self.visible_sprites],self.obstacle_sprites, self.create_attack)
		Agent((500,300),[self.visible_sprites],self.obstacle_sprites, self.create_attack)

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
								Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'organics',random_plant_image)
							# spawn minerals
							if col == 52:
								random_mineral_image = choice(graphics['minerals'])
								Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'minerals',random_mineral_image)

	def create_attack(self,agent):
		Weapon(agent,[self.visible_sprites])

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()


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

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# draw the floor
		floor_offset_pos = self.floow_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surface,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
