import pygame
import numpy as np
from settings import *
from support import import_folder
from debug import debug
from random import randint
from keras.activations import softmax

class Agent(pygame.sprite.Sprite):
	def __init__(self,
			  player,
			  player_agent,
			  pos,
			  groups,
			  obstacle_sprites,
			  create_attack,
			  get_data_frame):
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
		self.stats = {'health': 10, 'energy': 10, 'speed': 3}
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
		self.get_data_frame = get_data_frame
		self.can_get_frame = True

		# weapons
		self.create_attack = create_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]

		# ai model prediction
		self.can_make_prediction = True
		self.prediction_start = 0
		self.prediction_cooldown = 500

	def import_agent_assets(self):
		path = '../graphics/agent/'
		self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
					 'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
					 'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}
		
		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = import_folder(full_path)
		
	def input(self):
		if not self.attacking:
			if self.is_player_agent:					# Player input logic
				keys = pygame.key.get_pressed()
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
				# debug(f'{self.rect.center[0] // TILESIZE}' + ' - ' + f'{self.rect.center[1] // TILESIZE}')
			else:										# AI logic
				if self.player.modeller.model is None:  # AI random logic
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
				else: 									# AI trained model
					if self.can_make_prediction:
						nearby_sprites = self.get_data_frame(self)
						decision = self.predict_action(nearby_sprites)
						if decision == 'up':
							self.direction.y = -1
							self.direction.x = 0
							self.status = 'up'
						elif decision == 'down':
							self.direction.y = 1
							self.direction.x = 0
							self.status = 'down'
						elif decision == 'left':
							self.direction.y = 0
							self.direction.x = -1
							self.status = 'left'
						elif decision == 'right':
							self.direction.y = 0
							self.direction.x = 1
							self.status = 'right'
						self.can_make_prediction = False
						self.prediction_start = pygame.time.get_ticks()

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
				self.can_get_frame = True
			self.attacking = False
		
		if current_time - self.prediction_start >= self.prediction_cooldown:
			self.can_make_prediction = True
	
	def animate(self):
		animation = self.animations[self.status]
	
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def tile_change_test(self,old_pos,new_pos):
		# TODO add extra offset (TILESIZE * 1.5) to trigger near center of tile if this leads to garbage
		# potentiallly trigger save_data() from here when moving past tile boundary
		if (old_pos[0] // TILESIZE  != new_pos[0] // TILESIZE) or (old_pos[1] // TILESIZE != new_pos[1] // TILESIZE):
			self.can_get_frame = True

	def data_frame_size_check(self):
		if len(self.player.data_set) >= self.player.max_data_frame_size and self.is_player_agent:
			debug('Data frame size is at max')
			self.can_get_frame = False

	def save_data(self):
		if len(self.player.data_set) >= self.player.max_data_frame_size:
			return
		if self.can_get_frame and self.player.can_record_frame:
			self.player.data_set.append({'matrix': self.get_data_frame(self), 'label': self.status})
			self.can_get_frame = False

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

	def predict_action(self,boardstate):
		boardstate = boardstate / len(SPRITE_CODES) # normalise
		instance = boardstate.reshape(1, 2*DATAFRAME_RADIUS+1, 2*DATAFRAME_RADIUS+1, 1)
		prediction = self.player.modeller.model(instance)[0]
		random_fact = randint(1,6)
		if random_fact == 1:
			# Sample from the probability distribution
			probabilities = softmax(prediction).numpy()
			predicted_class_index = np.random.choice(len(prediction), p=probabilities)
		else:
			# Get the class index with the highest probability
			predicted_class_index = np.argmax(prediction)

		# Optionally, convert the index to a label
		predicted_label = list(self.player.modeller.label_dict.keys())[predicted_class_index]

		return predicted_label

	def update(self):
		self.input()
		self.low_health_energy_check()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.data_frame_size_check()
		self.move(self.stats['speed'])

