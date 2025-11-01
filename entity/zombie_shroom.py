import pygame
from entity.enemy import Enemy
from particle.burst_particle import BurstParticle
from particle.sweep_particle import SweepParticle
from particle.poison_particle import PoisonParticle
from particle.bite_particle import BiteParticle
from utils import import_asset_surfaces
from settings import TILESIZE

class ZombieShroom(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, on_death_callback=None):
        super().__init__(
            'zombie_shroom',
            pos,
            groups,
            obstacle_sprites,
            damage_player,
            trigger_death_particles
        )
        
        self.on_death_callback = on_death_callback
        
        self.visible_sprites = groups[0] if groups else None
        
        # Attack animation state
        self.attack_mode = 0  # rotates between 0, 1, 2
        self.attack_started = False
        self.attack_cooldown = 800

    def import_graphics(self, monster_name):
        path = f'./assets/monsters/{monster_name}/'
        self.animations = {
            'idle': [],
            'move': [],
            'attack0': [],
            'attack1': [],
            'attack2': []
        }
        self.animations['idle'] = import_asset_surfaces(path + 'idle')
        self.animations['move'] = import_asset_surfaces(path + 'move')
        self.animations['attack0'] = import_asset_surfaces(path + 'attack')
        self.animations['attack1'] = import_asset_surfaces(path + 'attack2')
        self.animations['attack2'] = import_asset_surfaces(path + 'attack3')

    def get_status(self, player, dialog_active=False):
        # If dialog is active, force idle
        if dialog_active:
            self.status = 'idle'
            return
        
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status not in ['attack0', 'attack1', 'attack2']:
                self.frame_index = 0
            if self.attack_mode == 0:
                self.status = 'attack0'
            elif self.attack_mode == 1:
                self.status = 'attack1'
            else:
                self.status = 'attack2'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player, dialog_active=False):
        # If dialog is active, don't move or attack
        if dialog_active:
            self.direction = pygame.math.Vector2()
            return
        
        if 'attack' in self.status:
            if not self.attack_started:
                self.attack_started = True
                self.attack_time = pygame.time.get_ticks()
                self.frame_index = 0
                self.attack_sound.play()
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

    def create_poison_burst(self):
        num_flames = 16
        radius = TILESIZE * 2
        cx, cy = self.rect.center
        if not hasattr(self, 'flame_frames'):
            self.flame_frames = import_asset_surfaces('./assets/particles/poison')
        for i in range(num_flames):
            angle = (360 / num_flames) * i
            direction = pygame.math.Vector2(1, 0).rotate(angle)
            flame = BurstParticle((cx + direction.x * radius, cy + direction.y * radius), self.flame_frames, direction, 4)
            if self.visible_sprites:
                self.visible_sprites.add(flame)

    def attack_sweep(self):
        if not hasattr(self, 'sweep_frames'):
            self.sweep_frames = import_asset_surfaces(f'./assets/monsters/{self.monster_name}/attack_particles')
            
        offset_x = 100
        offset_y = 0
        sweep_pos = (self.rect.centerx + offset_x, self.rect.centery + offset_y)
        
        sweep = SweepParticle(sweep_pos, self.sweep_frames)
        
        if self.visible_sprites:
            self.visible_sprites.add(sweep)

    def attack_bite(self):
        if not hasattr(self, 'bite_frames'):
            self.bite_frames = import_asset_surfaces(f'./assets/monsters/{self.monster_name}/attack_particles2')
            
        offset_x = 60
        offset_y = 0
        bite_pos = (self.rect.centerx + offset_x, self.rect.centery + offset_y)
        
        bite = BiteParticle(bite_pos, self.bite_frames)
        
        if self.visible_sprites:
            self.visible_sprites.add(bite)
        
    def poison_attack(self):
        if not hasattr(self, 'poison_frames'):
            self.poison_frames = import_asset_surfaces(f'./assets/monsters/{self.monster_name}/attack_particles3')
            
        offset_x = 0 
        offset_y = -20
        poison_pos = (self.rect.centerx + offset_x, self.rect.centery + offset_y)
        
        poison = PoisonParticle(poison_pos, self.poison_frames)
        
        if self.visible_sprites:
            self.visible_sprites.add(poison)

    def do_attack_effect(self):
        if self.attack_mode == 0:
            self.attack_sweep()
        elif self.attack_mode == 1:
            self.attack_bite()
        elif self.attack_mode == 2:
            self.create_poison_burst()
            self.poison_attack()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if 'attack' in self.status:
                self.can_attack = False
                self.attack_started = False
                self.attack_mode = (self.attack_mode + 1) % 3
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if 'attack' in self.status and self.attack_started:
            frame = int(self.frame_index)
            if 5 <= frame <= 8:
                self.damage_player(self.attack_damage, self.attack_type)
            if frame == 5 and not hasattr(self, 'attack_triggered'):
                self.do_attack_effect()
                self.attack_triggered = True
        else:
            if hasattr(self, 'attack_triggered'):
                del self.attack_triggered

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True
        if not self.vulnerable and current_time - self.hit_time >= self.invincibility_duration:
            self.vulnerable = True
    
    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.death_sound.play()

            if self.on_death_callback:
                self.on_death_callback()

