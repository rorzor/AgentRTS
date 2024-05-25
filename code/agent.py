import pygame 
from settings import *
from support import import_folder
from debug import debug
from weapon import Weapon

class Agent(pygame.sprite.Sprite):
	def __init__(self,player,pos,groups,obstacle_sprites,create_attack):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/agent/down/idle_down.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		self.obstacle_sprites = obstacle_sprites
		self.sprite_type = 'agent'
		self.player = player
		self.player.resources['agents'] += 1

		# graphics setup
		self.import_agent_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement
		self.direction = pygame.math.Vector2()
		self.speed = 4
		self.attacking = False
		self.attack_cooldown = 300
		self.attack_time = 0

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
		keys = pygame.key.get_pressed()

		if not self.attacking:
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'

			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'

			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

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

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def attack_check(self,sprite):
		if self.attacking:
			return
		if sprite.sprite_type == 'organic' or sprite.sprite_type == 'mineral':
			self.attack_time = pygame.time.get_ticks()
			self.attacking = True
			self.create_attack(self)

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
			self.attacking = False
	
	def animate(self):
		animation = self.animations[self.status]
	
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)