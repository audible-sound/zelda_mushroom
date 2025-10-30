import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player_direction = player.status.split('_')[0]

        image_path = f'./assets/weapons/{player.weapon}/{self.player_direction}.png'
        self.image = pygame.image.load(image_path).convert_alpha()

        vertical_offset = pygame.math.Vector2(0, 16)
        horizontal_offset = pygame.math.Vector2(-10, 0)
        
        if self.player_direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + vertical_offset)
        elif self.player_direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + vertical_offset)
        elif self.player_direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + horizontal_offset)
        elif self.player_direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + horizontal_offset)