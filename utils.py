from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        layout = reader(map, delimiter=',')
        for row in layout:
            terrain_map.append(row)
    return terrain_map

def import_asset_surfaces(path):
    paths = []
    surfaces = []

    for _, __, img_files in walk(path):
        for img in img_files:
            full_path= path + '/' + img
            print(full_path)
            paths.append(full_path)
            
    paths.sort()
    
    for full_path in paths:
        surface = pygame.image.load(full_path).convert_alpha()
        surfaces.append(surface)
        
    return surfaces