from particle.boss_particle import BossParticle
import pygame
from random import randint

class BurstParticle(BossParticle):
    def __init__(self, pos, frames, direction=None, speed=3):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = 0.25

        if direction is None:
            self.direction = pygame.math.Vector2(randint(-1,1), randint(-1,1)).normalize()
        else:
            self.direction = direction.normalize()

        self.speed = speed

    def update(self):
        self.rect.centerx += self.direction.x * self.speed
        self.rect.centery += self.direction.y * self.speed

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]