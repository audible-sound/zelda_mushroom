import pygame
from entity.enemy import Enemy
from particle.burst_particle import BurstParticle
from particle.dust_particle import DustParticle
from particle.sweep_particle import SweepParticle
from utils import import_asset_surfaces
from settings import TILESIZE

class FireShroom(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles):
        super().__init__(
            'fire_shroom',
            pos,
            groups,
            obstacle_sprites,
            damage_player,
            trigger_death_particles
        )
        
        self.visible_sprites = groups[0] if groups else None
        self.vulnerable = True
        
        self.attack_mode = 0 
        self.attack_started = False
        self.attack_cooldown = 800
        
    def create_fire_burst(self):
        num_flames = 16
        radius = TILESIZE * 2  # spawn slightly away from boss center
        center_x, center_y = self.rect.center

        if not hasattr(self, 'flame_frames'):
            self.flame_frames = import_asset_surfaces('./assets/particles/fire/frames')

        for i in range(num_flames):
            angle = (360 / num_flames) * i
            direction = pygame.math.Vector2(1, 0).rotate(angle)  # radial direction

            # spawn position slightly offset
            pos_x = center_x + direction.x * radius
            pos_y = center_y + direction.y * radius

            flame = BurstParticle((pos_x, pos_y), self.flame_frames, direction=direction, speed=4)
            if self.visible_sprites:
                self.visible_sprites.add(flame)
    
    def create_dust_burst(self):
        num_particles = 25
        offset_x = -60
        center_x, center_y = self.rect.midbottom
        center_x += offset_x
        for _ in range(num_particles):
            dust = DustParticle((center_x, center_y))
            if self.visible_sprites:
                self.visible_sprites.add(dust)
   
    def attack_sweep(self):
        if not hasattr(self, 'sweep_frames'):
            self.sweep_frames = import_asset_surfaces(f'./assets/monsters/{self.monster_name}/attack_particles')

        offset_x = -90  
        offset_y = 0

        sweep_pos = (self.rect.centerx + offset_x, self.rect.centery + offset_y)

        sweep = SweepParticle(sweep_pos, self.sweep_frames)
        if self.visible_sprites:
            self.visible_sprites.add(sweep)
  
    def attack_fire(self):
        self.create_fire_burst()

    def attack_dust(self):
        self.create_dust_burst()
    
    def actions(self, player):
        if self.status == 'attack':
            if not self.attack_started:
                self.attack_started = True
                self.attack_time = pygame.time.get_ticks()
                self.frame_index = 0
                self.attack_sound.play()
                self.damage_applied = False
        elif self.status == 'move':
            desired_direction = self.get_player_distance_direction(player)[1]
            
            if self.can_move_in_direction(desired_direction, self.speed):
                self.direction = desired_direction
            else:
                # Try to move in X direction only
                x_direction = pygame.math.Vector2(desired_direction.x, 0)
                if self.can_move_in_direction(x_direction, self.speed):
                    self.direction = x_direction
                else:
                    # Try to move in Y direction only
                    y_direction = pygame.math.Vector2(0, desired_direction.y)
                    if self.can_move_in_direction(y_direction, self.speed):
                        self.direction = y_direction
                    else:
                        self.direction = pygame.math.Vector2()
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
                self.attack_started = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if self.status == 'attack' and self.attack_started:
            frame = int(self.frame_index)

            if 5 <= frame <= 8:
                self.damage_player(self.attack_damage, self.attack_type)

            # trigger one-time attack burst at frame 5
            if frame == 5 and not hasattr(self, 'attack_triggered'):
                if self.attack_mode == 0:
                    self.attack_fire()
                elif self.attack_mode == 1:
                    self.attack_sweep()
                elif self.attack_mode == 2:
                    self.attack_dust()

                self.attack_mode = (self.attack_mode + 1) % 3

                self.attack_triggered = True
    
        else:
            if hasattr(self, 'attack_triggered'):
                del self.attack_triggered

            if hasattr(self, 'sweep_started'):
                del self.sweep_started

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

