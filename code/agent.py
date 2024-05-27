import pygame 
from settings import *
from support import import_folder
from debug import debug
from random import randint

class Agent(pygame.sprite.Sprite):
	def __init__(self,
			  player,
			  player_agent,
			  pos,
			  groups,
			  obstacle_sprites,
			  create_attack,
			  save_data_frame = None):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/agent/down/idle_down.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		self.obstacle_sprites = obstacle_sprites
		self.sprite_type = 'agent'
		self.player = player
		self.is_player_agent = player_agent
		self.player.resources['agents'] += 1

		# graphics setup
		self.import_agent_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15

		# stats
		self.stats = {'health': 10, 'energy': 10, 'speed': 4}
		self.health = self.stats['health']
		self.energy = self.stats['energy']

		# movement
		self.direction = pygame.math.Vector2()
		self.attacking = False
		self.attack_cooldown = 300
		self.attack_time = 0
		self.rand_walk_time = 250
		self.rand_walk_start = 0

		# data frame saver
		self.save_data_frame = save_data_frame
		self.can_save_frame = True

		# AI model
		self.model = None

		# weapons
		self.create_attack = create_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]

	def import_agent_assets(self):
		path = '../graphics/agent/'
		self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
					 'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
					 'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}
		
		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = import_folder(full_path)
		
	def input(self):
		if self.is_player_agent:
			keys = pygame.key.get_pressed()
			if not self.attacking:
				if keys[pygame.K_UP]:
					self.direction.y = -1
					self.status = 'up'
					self.save_data()
				elif keys[pygame.K_DOWN]:
					self.direction.y = 1
					self.status = 'down'
					self.save_data()
				else:
					self.direction.y = 0

				if keys[pygame.K_RIGHT]:
					self.direction.x = 1
					self.status = 'right'
					self.save_data()

				elif keys[pygame.K_LEFT]:
					self.direction.x = -1
					self.status = 'left'
					self.save_data()

				else:
					self.direction.x = 0

				if keys[pygame.K_SPACE]:
					self.save_data_frame()
		else:
			# random AI
			if self.model is None:
				if pygame.time.get_ticks() - self.rand_walk_start > self.rand_walk_time:
					dir = randint(1,4)
					if dir == 1:
						self.direction.y = -1
						self.status = 'up'
					elif dir == 2:
						self.direction.y = 1
						self.status = 'down'
					elif dir == 3:
						self.direction.x = 1
						self.status = 'right'
					else:
						self.direction.x = -1
						self.status = 'left'
					self.rand_walk_start = pygame.time.get_ticks()

	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','')
				self.status = self.status + '_attack'
		
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
			self.energy -= resource_consumption['agent_move']

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.tile_change_test(self.rect.center,self.hitbox.center)
		self.rect.center = self.hitbox.center

	def attack_check(self,sprite):
		if self.attacking:
			return
		if sprite.sprite_type == 'organic' or sprite.sprite_type == 'mineral':
			self.attack_time = pygame.time.get_ticks()
			self.attacking = True
			self.create_attack(self)
			if sprite.sprite_type == 'organic':
				self.energy += resource_consumption['agent_org_harvest']
				if self.energy >= self.stats['energy']:
					self.energy = self.stats['energy']
			elif sprite.sprite_type == 'mineral':
				self.energy -= resource_consumption['agent_min_harvest']

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite is self:
					continue
				if sprite.hitbox.colliderect(self.hitbox):
					self.attack_check(sprite)
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite is self:
					continue
				if sprite.hitbox.colliderect(self.hitbox):
					self.attack_check(sprite)
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.attack_time >= self.attack_cooldown:
			if self.attacking:
				self.can_save_frame = True
			self.attacking = False
	
	def animate(self):
		animation = self.animations[self.status]
	
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def tile_change_test(self,old_pos,new_pos):
		# TODO add extra offset (TILESIZE * 1.5) to trigger near center of tile if this leads to garbage
		if (old_pos[0] // TILESIZE  != new_pos[0] // TILESIZE) or (old_pos[1] // TILESIZE != new_pos[1] // TILESIZE):
			self.can_save_frame = True

	def save_data(self):
		if self.can_save_frame:
			self.save_data_frame()
			self.can_save_frame = False

	def low_health_energy_check(self):
		if self.energy < 0:
			self.health += self.energy
			self.energy = 0
		if self.health <= 0:
			if self.is_player_agent:
				self.player.spawn_agent(True)
			else:
				self.kill()
				self.player.resources['agents'] -= 1

	def update(self):
		self.input()
		self.low_health_energy_check()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.stats['speed'])