from particle.boss_particle import BossParticle
import pygame
from random import randint

class DustParticle(BossParticle):
    def __init__(self, pos, direction=None, speed=4):
        super().__init__()
        size = randint(8, 16)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (randint(180, 255), randint(50, 80), randint(20, 40))
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)

        self.rect = self.image.get_rect(center=pos)

        if direction is None:
            self.direction = pygame.math.Vector2(randint(-3,3), randint(-4,-1)).normalize()
        else:
            self.direction = direction

        self.speed = speed
        self.gravity = 0.5
        self.vspeed = -3
        self.alpha_decay = randint(5,10)

    def update(self):
        self.vspeed += self.gravity
        self.rect.x += int(self.direction.x * self.speed)
        self.rect.y += int(self.direction.y * self.speed + self.vspeed)

        new_alpha = max(self.image.get_alpha() - self.alpha_decay, 0)
        self.image.set_alpha(new_alpha)

        if new_alpha <= 0 or self.rect.y > 1000:
            self.kill()