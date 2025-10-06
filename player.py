import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        self.image = pygame.image.load('./assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)

        self.obstacle_sprites = obstacle_sprites

        # player's movement
        self.direction = pygame.math.Vector2()
        self.speed = 5

        # Create hitbox
        self.hitbox = self.rect.inflate(0, -40)

    def keyboard_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        # normalise movement vector to prevent faster diagonal movement
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horziontal movement
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        # Vertical movement
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # Check if sprite collides with player
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Player is moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # Player is moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Player is moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # Player is moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.keyboard_input()
        self.move(self.speed)
 