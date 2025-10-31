import pygame
from settings import *
from utils import import_asset_surfaces
from entity.entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)

        self.import_player_assets()

        self.image = pygame.image.load('./assets/player/down_idle/down_idle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.status = 'down'
        self.obstacle_sprites = obstacle_sprites

        # player's movement
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 300
        self.attack_time = None

        # Create hitbox
        self.hitbox = self.rect.inflate(0, -40)

        # Weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = 0
        self.weapon_switch_cooldown = 200

        # magic 
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = 0
        self.magic_switch_cooldown = 200

        # stats
        self.stats = {
            'health': 100,
            'energy': 100,
        }

        self.max_stats = {
            'health': 100,
            'energy': 100,
        }
        

    def import_player_assets(self):
        path = './assets/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_asset_surfaces(full_path)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_idle' in self.status and not '_attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not '_attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def keyboard_input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # attack
            if keys[pygame.K_p]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic
            if keys[pygame.K_SPACE] and self.can_switch_magic:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

            # switch weapon
            if keys[pygame.K_u] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]
                
            # switch magic
            if keys[pygame.K_i] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def attack_cooldown_check(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            time_passed = current_time - self.attack_time
            if time_passed >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            time_passed = current_time - self.weapon_switch_time
            if time_passed >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.magic_switch_cooldown:
                self.can_switch_magic = True


    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
    def get_weapon_damage(self):
        weapon_damage = weapon_data[self.weapon]['damage']
        return weapon_damage

    def update(self):
        self.keyboard_input()
        self.attack_cooldown_check()
        self.get_status()
        self.animate()
        self.move(self.speed)
 