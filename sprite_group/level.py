from random import randint
import pygame
from entity.enemy import Enemy
from entity.fire_shroom import FireShroom
from entity.zombie_shroom import ZombieShroom
from particle.magic_player import MagicPlayer
from settings import *
from sprite_group.y_sort_camera_group import YSortCameraGroup
from tile import Tile
from entity.player import Player
from utils import import_csv_layout, import_asset_surfaces
from attack.weapon import Weapon
from ui import UI
from particle.animation_player import AnimationPlayer

class Level:
    def __init__(self):

        # init sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        self.zombie_shroom = None
        self.fire_shroom = None
        self.fire_shroom_spawn_pos = None
        self.blockade_tiles = []
        
        self.ui = UI()
        
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('assets/tilemap/map_boundary.csv'),
            'grass': import_csv_layout('assets/tilemap/map_grass.csv'),
            'objects': import_csv_layout('assets/tilemap/map_objects.csv'),
            'entities': import_csv_layout('assets/tilemap/map_entities.csv')
        }

        graphics = {
            'grass': import_asset_surfaces('assets/grass'),
            'objects': import_asset_surfaces('assets/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        elif style == 'grass':
                            grass_image = graphics['grass'][int(col)]
                            Tile((x, y), 
                                 [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 
                                 'grass', 
                                 grass_image)

                        elif style == 'objects':
                            sprite_group = [self.visible_sprites, self.obstacle_sprites]
                            object_image = graphics['objects'][int(col)]
                            tile = Tile((x, y), sprite_group, 'object', object_image)

                            if col == '23':
                                self.blockade_tiles.append(tile)
                        
                        elif style == 'entities':
                            if col == '0':
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                    )
                            else:
                                monster_name = 'shroom_goon'
                                if col == '1':
                                    monster_name = 'shroom_goon'
                                elif col == '2':
                                    monster_name = 'shroom_mob'
                                elif col == '3':
                                    self.fire_shroom_spawn_pos = (x, y)
                                    continue
                                elif col == '4':
                                    self.zombie_shroom = ZombieShroom(
                                        (x, y),
                                        [self.visible_sprites, 
                                         self.attackable_sprites
                                        ],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.on_zombie_death
                                    )
                                    continue
                                elif col == '5':
                                    monster_name = 'spirit'
                        
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, 
                                     self.attackable_sprites
                                    ],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles
                                )
                            

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        
    def create_magic(self,type,strength,cost):
        if type == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

        if type == 'fire':
            self.magic_player.fire(self.player,cost,[self.visible_sprites,self.attack_sprites])
            
        if type == 'ice':
            self.magic_player.ice(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None
            
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for _ in range(randint(3,6)):
                                self.animation_player.create_leaf_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)
                            
    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.stats['health'] -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            
            if attack_type == 'fire_shroom_attack':
                self.animation_player.create_particles('fire_damage',self.player.rect.center,[self.visible_sprites])
            elif attack_type == 'zombie_shroom_attack':
                self.animation_player.create_particles('poison_damage',self.player.rect.center,[self.visible_sprites])
            else:
                self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
                            
    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
    
    def on_zombie_death(self):
        # Remove blockade tiles
        for tile in self.blockade_tiles:
            tile.kill()
        self.blockade_tiles.clear()
        
        if self.fire_shroom_spawn_pos and not self.fire_shroom:
            self.fire_shroom = FireShroom(
                self.fire_shroom_spawn_pos,
                [self.visible_sprites, 
                 self.attackable_sprites
                ],
                self.obstacle_sprites,
                self.damage_player,
                self.trigger_death_particles
            )

    def run(self):
        # update and draw the game
        self.visible_sprites.update()
        self.visible_sprites.custom_draw_sprites(self.player)
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)
        self.player_attack_logic()