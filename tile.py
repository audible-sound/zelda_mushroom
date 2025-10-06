import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.image.load('./assets/rock.png').convert_alpha()
        # change size of image
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # Create hitbox
        self.hitbox = self.rect.inflate(0, -10)
