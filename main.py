import pygame, sys
import pygame_menu
from settings import *
from sprite_group.level import Level
from ui.success_screen import SuccessScreen
from ui.game_over_screen import GameOverScreen

class Game:
    def __init__(self):
        
        # Game Initialization
        pygame.init()
        pygame.display.set_caption('Zelda Mushroom')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Init Success Screen
        self.success_screen = SuccessScreen()
        
        # Init Game Over Screen
        self.game_over_screen = GameOverScreen()

        # Init Game Level (pass callbacks to trigger success/game over screens)
        self.level = Level(self.on_game_success, self.on_game_over)

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
        self.mainMenu.add.button('Play', self.start_game)
        self.mainMenu.add.vertical_margin(30)
        self.mainMenu.add.button('Exit', pygame.quit)

        button_sound = pygame_menu.sound.Sound()
        button_sound.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, MENU_BUTTON_SOUND)
        self.mainMenu.set_sound(button_sound, recursive=True)
        
        # Play bgm for menu
        self.main_sound = pygame.mixer.Sound('./assets/audio/main.ogg')
        self.main_sound.set_volume(0.5)
        self.main_sound_channel = self.main_sound.play(loops = -1)

    def start_game(self):
        if self.main_sound_channel:
            self.main_sound_channel.stop()
        self.mainMenu.close()
        self.game_state = 'GAME'
        self.mainMenu.disable() # stop the menu from running
        # Reinitialize level for new game
        self.level = Level(self.on_game_success, self.on_game_over)
        self.success_screen.hide()
        self.game_over_screen.hide()
    
    def on_game_success(self):
        self.game_state = 'SUCCESS'
        self.success_screen.show(self.return_to_menu, skip_music=True)
    
    def on_game_over(self):
        self.game_state = 'GAME_OVER'
        self.game_over_screen.show(self.return_to_menu, skip_music=True)
    
    def return_to_menu(self):
        self.game_state = 'MENU'
        self.mainMenu.enable()
        self.mainMenu.reset(1)
        # Stop level music
        if self.level:
            self.level.stop_current_music()
        # Restart menu music
        if self.main_sound_channel:
            self.main_sound_channel.stop()
        self.main_sound_channel = self.main_sound.play(loops=-1)

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
                self.level.run(events)
            
            elif self.game_state == 'SUCCESS':
                # Draw the game behind the success screen
                self.screen.fill('black')
                self.level.run([])
                # Display and handle success screen
                self.success_screen.handle_input(events)
                self.success_screen.display()
            
            elif self.game_state == 'GAME_OVER':
                # Draw the game behind the game over screen
                self.screen.fill('black')
                self.level.run([])
                # Display and handle game over screen
                self.game_over_screen.handle_input(events)
                self.game_over_screen.display()
            
            pygame.display.update()
            self.clock.tick(FPS) 

if __name__ == '__main__':
    game = Game()
    game.run()