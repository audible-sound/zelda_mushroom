import pygame
from settings import *
from entity import Entity
from utils import *

class Enemy(Entity):
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):

		super().__init__(groups)
		self.sprite_type = 'enemy'