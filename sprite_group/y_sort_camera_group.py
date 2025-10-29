import pygame

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

    def custom_draw_sprites(self, player):
        # get offset values
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw map
        map_offset_position = self.map_rect.topleft - self.offset
        self.display_surface.blit(self.map_surface, map_offset_position)


        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
    
        for sprite in sorted_sprites:
            offset_value = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_value)