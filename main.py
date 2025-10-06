import pygame, sys
from settings import *

class Game:
    def __init__(self):
        
        # Game Initialization
        pygame.init()
        pygame.display.set_caption('Zelda Mushroom')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            pygame.display.flip()
            self.clock.tick(FPS) 

if __name__ == '__main__':
    game = Game()
    game.run()