import pygame

class BossParticle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_type = "particle"