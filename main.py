import pygame, sys
from settings import *
from sprite_group.level import Level

class Game:
    def __init__(self):
        
        # Game Initialization
        pygame.init()
        pygame.display.set_caption('Zelda Mushroom')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Init Game Level
        self.level = Level()
        
        # Play bgm
        main_sound = pygame.mixer.Sound('./assets/audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.flip()
            self.clock.tick(FPS) 

if __name__ == '__main__':
    game = Game()
    game.run()