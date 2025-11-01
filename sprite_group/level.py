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
from ui.ui import UI
from particle.animation_player import AnimationPlayer
from ui.dialog import Dialog

class Level:
    def __init__(self, on_success_callback=None, on_game_over_callback=None):
        self.on_success_callback = on_success_callback
        self.on_game_over_callback = on_game_over_callback

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
        self.dialog = Dialog()
        self.dialog_queue = []  
        
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        
        self.main_music = pygame.mixer.Sound('./assets/audio/main.ogg')
        self.fire_shroom_music = pygame.mixer.Sound('./assets/audio/fire_shroom_fight.ogg')
        self.zombie_shroom_music = pygame.mixer.Sound('./assets/audio/zombie_shroom_fight.ogg')
        self.success_music = pygame.mixer.Sound('./assets/audio/game_success.mp3')
        self.game_over_music = pygame.mixer.Sound('./assets/audio/game_over.ogg')
        
        self.main_music.set_volume(0.5)
        self.fire_shroom_music.set_volume(0.5)
        self.zombie_shroom_music.set_volume(0.5)
        self.success_music.set_volume(0.6)
        self.game_over_music.set_volume(0.6)
        
        self.current_music = None
        self.current_music_channel = None
        self.music_initialized = False
        
        self.waiting_for_success_screen = False
        self.waiting_for_game_over_screen = False
        self.player_dead = False
        
        # Show initial inner dialog
        self.dialog.show(
            "The quest begins... I've accepted the call to liberate this island from the mushroom menace. My boots touch the shore as I step onto foreign soil, ready to face whatever dark magic has twisted these lands.",
            inner_dialog=True
        )
        
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
                                # Set dialog state for player
                                self.player.dialog_active = self.dialog.active
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
            
            # Check if player is dead
            if self.player.stats['health'] <= 0:
                self.player.stats['health'] = 0
                self.on_player_death()
            
            if attack_type == 'fire_shroom_attack':
                self.animation_player.create_particles('fire_damage',self.player.rect.center,[self.visible_sprites])
            elif attack_type == 'zombie_shroom_attack':
                self.animation_player.create_particles('poison_damage',self.player.rect.center,[self.visible_sprites])
            else:
                self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
                            
    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
    
    def on_zombie_death(self):
        self.visible_sprites.trigger_shake(intensity=15, duration=2000)
        
        # Remove blockade tiles
        for tile in self.blockade_tiles:
            tile.kill()
        self.blockade_tiles.clear()
        
        self.dialog_queue = [
            ("A deep rumble shakes the earth beneath your feet. Something ancient stirs...", False),
            ("The very air grows heavy with malevolent energy. A more terrible evil has awakened.", False),
            ("What... what was that? I can feel its presence even from here. It's... it's stronger than anything I've faced.", True),
            ("My heart pounds in my chest. The ground trembles with each step it takes. This is no ordinary foe.", True),
            ("I must be ready. Whatever nightmare has been unleashed, I will face it. The island's fate depends on it.", True),
        ]
        
        # Show the first dialog in the queue
        if self.dialog_queue:
            text, is_inner = self.dialog_queue.pop(0)
            self.dialog.show(text, inner_dialog=is_inner)

        # Stop zombie shroom music and play main music
        self.play_main_music()
        
        if self.fire_shroom_spawn_pos and not self.fire_shroom:
            self.fire_shroom = FireShroom(
                self.fire_shroom_spawn_pos,
                [self.visible_sprites, 
                 self.attackable_sprites
                ],
                self.obstacle_sprites,
                self.damage_player,
                self.trigger_death_particles,
                self.on_fire_shroom_death
            )
    
    def on_player_death(self):
        self.player_dead = True
        self.stop_current_music()
        
        # Play game over music
        self.current_music = self.game_over_music
        self.current_music_channel = self.game_over_music.play(loops=-1)
        
        # Create dialog sequence
        self.dialog_queue = [
            ("Darkness creeps in... My strength fails me.", True),
            ("The island's corruption has claimed another soul. My quest ends here.", True),
            ("I fought with everything I had, but it wasn't enough. The mushroom menace remains.", True),
            ("As my vision fades, I can only hope that another hero will rise to take my place.", True),
            ("The island still needs a savior. My story ends, but the fight must continue.", True),
        ]
        
        self.waiting_for_game_over_screen = True
        
        # Show the first dialog in the queue
        if self.dialog_queue:
            text, is_inner = self.dialog_queue.pop(0)
            self.dialog.show(text, inner_dialog=is_inner)
    
    def on_fire_shroom_death(self):
        self.stop_current_music()
        
        # Remove all remaining enemies
        enemies_to_remove = []
        for sprite in self.attackable_sprites:
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                enemies_to_remove.append(sprite)
        
        for enemy in enemies_to_remove:
            enemy.kill()
        
        # Play success music
        self.current_music = self.success_music
        self.current_music_channel = self.success_music.play(loops=-1)
        
        # Create dialog sequence
        self.dialog_queue = [
            ("The fire shroom collapses, its flames extinguished. The island falls silent...", False),
            ("It's over. The final guardian has fallen. I stand victorious, but exhausted.", True),
            ("I look around at the scarred battlefield. The mushroom menace that once plagued this land is gone.", True),
            ("As the smoke clears, I feel a sense of peace settle over the island. The corruption has been cleansed.", True),
            ("My journey here is complete. The island is free, and its people can return to their lives without fear.", True),
            ("I've fulfilled my duty. This land, once cursed by darkness, now basks in the light of victory.", True),
        ]
        
        self.waiting_for_success_screen = True
        
        # Show the first dialog in the queue
        if self.dialog_queue:
            text, is_inner = self.dialog_queue.pop(0)
            self.dialog.show(text, inner_dialog=is_inner)
    
    def play_main_music(self):
        self.stop_current_music()
        self.current_music = self.main_music
        self.current_music_channel = self.main_music.play(loops=-1)
    
    def play_fire_shroom_music(self):
        if self.current_music != self.fire_shroom_music:
            self.stop_current_music()
            self.current_music = self.fire_shroom_music
            self.current_music_channel = self.fire_shroom_music.play(loops=-1)
    
    def play_zombie_shroom_music(self):
        if self.current_music != self.zombie_shroom_music:
            self.stop_current_music()
            self.current_music = self.zombie_shroom_music
            self.current_music_channel = self.zombie_shroom_music.play(loops=-1)
    
    def stop_current_music(self):
        if self.current_music_channel:
            self.current_music_channel.stop()
        self.current_music = None
        self.current_music_channel = None
    
    def update_music(self):
        # Initialize music on first run
        if not self.music_initialized:
            self.play_main_music()
            self.music_initialized = True
        
        if self.waiting_for_success_screen or self.current_music == self.success_music:
            return
        
        if self.waiting_for_game_over_screen or self.current_music == self.game_over_music:
            return
        
        # Check if player is in combat range with any boss
        fire_shroom_in_range = False
        zombie_shroom_in_range = False
        
        if self.fire_shroom and self.fire_shroom.health > 0:
            distance = self.fire_shroom.get_player_distance_direction(self.player)[0]
            if distance <= self.fire_shroom.notice_radius:
                fire_shroom_in_range = True
        
        if self.zombie_shroom and self.zombie_shroom.health > 0:
            distance = self.zombie_shroom.get_player_distance_direction(self.player)[0]
            if distance <= self.zombie_shroom.notice_radius:
                zombie_shroom_in_range = True
        
        if fire_shroom_in_range:
            self.play_fire_shroom_music()
        elif zombie_shroom_in_range:
            self.play_zombie_shroom_music()
        elif self.current_music != self.main_music:
            self.play_main_music()

    
    def run(self, events=None):
        # Handle dialog input if dialog is active
        if events:
            dialog_was_dismissed = self.dialog.handle_input(events)
            
            if dialog_was_dismissed and self.dialog_queue:
                text, is_inner = self.dialog_queue.pop(0)
                self.dialog.show(text, inner_dialog=is_inner)
            elif dialog_was_dismissed and self.waiting_for_success_screen and not self.dialog_queue:
                # All dialogs completed, now show success screen
                if self.on_success_callback:
                    self.on_success_callback()
            elif dialog_was_dismissed and self.waiting_for_game_over_screen and not self.dialog_queue:
                # All dialogs completed, now show game over screen
                if self.on_game_over_callback:
                    self.on_game_over_callback()
        
        if not self.player_dead:
            # Update player dialog state
            self.player.dialog_active = self.dialog.active
            
            # update the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player, self.dialog.active)
            self.player_attack_logic()
            self.update_music()
        
        self.visible_sprites.custom_draw_sprites(self.player)
        self.ui.display(self.player)
        
        # Display dialog (always display, even when player is dead)
        self.dialog.display()