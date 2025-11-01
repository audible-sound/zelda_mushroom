import pygame, sys
import pygame_menu
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

        # setup start menu
        self.bg_image = pygame.image.load(MENU_BG_IMAGE).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))        
        self.game_state = 'MENU'

        self.theme = pygame_menu.themes.THEME_DARK.copy()
        self.theme.background_image = None 
        self.theme.background_color = (0, 0, 0, 0)
        self.theme.widget_font = TITLE_FONT
        self.theme.widget_font_size = 42
        self.theme.title_font = TITLE_FONT
        self.theme.widget_font_color = (255, 255, 255) 
        self.theme.title_font_color = (255, 255, 255)
        self.theme.selection_color = (255, 215, 0) 
        self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

        self.mainMenu = pygame_menu.Menu(
            title='',
            width=WIDTH,
            height=HEIGHT,
            theme=self.theme
        )

        self.mainMenu.add.image(LOGO_IMAGE, scale_smooth=True)
        self.mainMenu.add.vertical_margin(40) 
        self.mainMenu.add.button('Play', self.start_game) # Runs the start_game function
        self.mainMenu.add.vertical_margin(30)
        self.mainMenu.add.button('Exit', pygame.quit)

        button_sound = pygame_menu.sound.Sound()
        button_sound.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, MENU_BUTTON_SOUND)
        self.mainMenu.set_sound(button_sound, recursive=True)
        
        # Play bgm
        main_sound = pygame.mixer.Sound('./assets/audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)

    def start_game(self):
        self.mainMenu.close()
        self.game_state = 'GAME'
        self.mainMenu.disable() # stop the menu from running

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.game_state == 'MENU':
                self.screen.blit(self.bg_image, (0, 0))
                if self.mainMenu.is_enabled():
                    self.mainMenu.update(events)
                if self.mainMenu.is_enabled():
                    self.mainMenu.draw(self.screen)

            elif self.game_state == 'GAME':
                self.screen.fill('black')
                self.level.run()
            
            pygame.display.update()
            self.clock.tick(FPS) 

if __name__ == '__main__':
    game = Game()
    game.run()