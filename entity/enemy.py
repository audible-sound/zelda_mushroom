import pygame
from settings import *
from entity.entity import Entity
from utils import *

class Enemy(Entity):
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):

		super().__init__(groups)
		self.sprite_type = 'enemy'
		self.animations = {'idle':[],'move':[],'attack':[]}
  
		self.import_graphics(monster_name)
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]	
		self.rect = self.image.get_rect(topleft = pos)
  
  
	def import_graphics(self, monster_name):
		path = f'./assets/monsters/{monster_name}/'
		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = import_asset_surfaces(full_path)
  
