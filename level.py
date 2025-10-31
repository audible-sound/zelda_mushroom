import pygame
from settings import *
from sprite_group.y_sort_camera_group import YSortCameraGroup
from tile import Tile
from player import Player
from utils import import_csv_layout, import_asset_surfaces
from random import choice

class Level:
    def __init__(self):

        # init sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
 
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('assets/tilemap/map_boundary.csv'),
            'grass': import_csv_layout('assets/tilemap/map_grass.csv'),
            'objects': import_csv_layout('assets/tilemap/map_objects.csv'),
        }

        graphics = {
            'grass': import_asset_surfaces('assets/grass'),
            'objects': import_asset_surfaces('assets/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'grass':
                            grass_image = graphics['grass'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', grass_image)

                        if style == 'objects':
                            object_image = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_image)

        self.player = Player((100, 100), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw_sprites(self.player)
        self.visible_sprites.update()