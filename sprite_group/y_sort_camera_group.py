import pygame
import random

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Center player to the middle of screen
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() 

        # Create map surface
        self.map_surface = pygame.image.load('assets/tilemap/map.png').convert()
        self.map_rect = self.map_surface.get_rect(topleft=(0, 0))
        
        # Screen shake
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_start_time = 0
        self.shake_offset = pygame.math.Vector2()

    def trigger_shake(self, intensity, duration):
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_start_time = pygame.time.get_ticks()
    
    def update_shake(self):
        if self.shake_duration > 0:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.shake_start_time
            
            if elapsed < self.shake_duration:
                # Calculate shake progress (0.0 to 1.0)
                progress = elapsed / self.shake_duration
                # Decay intensity over time (starts strong, fades out)
                current_intensity = self.shake_intensity * (1.0 - progress)
                
                # Generate random shake offset
                self.shake_offset.x = random.uniform(-current_intensity, current_intensity)
                self.shake_offset.y = random.uniform(-current_intensity, current_intensity)
            else:
                # Shake complete
                self.shake_duration = 0
                self.shake_intensity = 0
                self.shake_offset = pygame.math.Vector2()
        else:
            self.shake_offset = pygame.math.Vector2()

    def custom_draw_sprites(self, player):
        # Update shake effect
        self.update_shake()
        
        # get offset values
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.offset.x = max(0, min(self.offset.x, self.map_rect.width - self.display_surface.get_width()))
        self.offset.y = max(0, min(self.offset.y, self.map_rect.height - self.display_surface.get_height()))

        # Apply shake offset
        final_offset = self.offset + self.shake_offset

        # Draw map
        map_offset_position = self.map_rect.topleft - final_offset
        self.display_surface.blit(self.map_surface, map_offset_position)


        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
    
        for sprite in sorted_sprites:
            offset_value = sprite.rect.topleft - final_offset
            self.display_surface.blit(sprite.image, offset_value)
            
    def enemy_update(self,player,dialog_active=False):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player,dialog_active)