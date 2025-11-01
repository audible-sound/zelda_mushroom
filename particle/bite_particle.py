import pygame
from particle.boss_particle import BossParticle

class BiteParticle(BossParticle):
    def __init__(self, pos, frames):
        super().__init__()
        
        self.frames = [self.tint_surface(frame, (140, 0, 255, 255)) for frame in frames]

        
        self.frame_index = 0
        self.animation_speed = 0.35

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def tint_surface(self, surface, tint_color):
        tinted = surface.copy()
        tint = pygame.Surface(surface.get_size()).convert_alpha()
        tint.fill(tint_color)  # (R, G, B, A)
        tinted.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
