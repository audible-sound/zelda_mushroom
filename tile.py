import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.sprite_type = sprite_type

        # Only scale if it's not an object
        if sprite_type == 'object':
            self.image = surface
            # Check image size
            image_width, image_height = self.image.get_size()

            if image_height > TILESIZE:
                # Tall objects sit on the ground
                self.rect = self.image.get_rect(midbottom=(pos[0] + TILESIZE / 2, pos[1] + TILESIZE))
            else:
                # All 64x64 or smaller stay grid-aligned
                self.rect = self.image.get_rect(topleft=pos)
        else:
            self.image = pygame.transform.scale(surface, (TILESIZE, TILESIZE))
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))

        # ---- Hitbox setup ----
        # Create hitbox (optional: adjust differently for object)
        if sprite_type == 'object':
            if self.rect.height > 128:
                # For tall objects (bigger than 128px)
                # Make only the bottom part collidable 30% of image height
                hitbox_height = int(self.rect.height * 0.55)
                hitbox_width = int(self.rect.width * 0.80)
                self.hitbox = pygame.Rect(
                    self.rect.left,
                    self.rect.bottom - hitbox_height,
                    self.rect.width,
                    hitbox_height
                )
                self.hitbox = self.hitbox.inflate(- hitbox_width*0.8, - hitbox_height*0.2)
            elif self.rect.height > 64:
                # For tall objects (bigger than 64px)
                # Make only the bottom part collidable 45% of image height
                hitbox_height = int(self.rect.height * 0.45)
                self.hitbox = pygame.Rect(
                    self.rect.left,
                    self.rect.bottom - hitbox_height,
                    self.rect.width,
                    hitbox_height
                )
            else:
                # For small objects (≤ 64px), just use regular inflate
                self.hitbox = self.rect.inflate(0, -10)

        else:
            # Normal ground tiles
            self.hitbox = self.rect.inflate(0, -10)
