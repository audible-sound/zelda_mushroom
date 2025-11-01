import pygame
from settings import *


class SuccessScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        # Screen dimensions
        self.width = 1280
        self.height = 720
        self.padding = 40
        self.border_width = 4
        
        # Position at center
        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.height) // 2
        
        # Fonts
        self.title_font = pygame.font.Font(TITLE_FONT, 64)
        self.message_font = pygame.font.Font(UI_FONT, 28)
        self.button_font = pygame.font.Font(UI_FONT, 32)
        
        # State
        self.active = False
        
        # Colors
        self.bg_color = UI_BG_COLOR
        self.border_color = UI_BORDER_COLOR_ACTIVE
        self.title_color = (255, 215, 0)  # Gold
        self.message_color = (255, 255, 255)
        self.button_color = (100, 150, 100)
        self.button_hover_color = (120, 180, 120)
        self.button_text_color = (255, 255, 255)
        
        # Button dimensions
        self.button_width = 250
        self.button_height = 60
        self.button_x = self.x + (self.width - self.button_width) // 2
        self.button_y = self.y + self.height - 100
        
        # Button state
        self.button_hovered = False
        
    def show(self, on_return_to_menu_callback, skip_music=False):
        self.active = True
        self.on_return_to_menu = on_return_to_menu_callback
    
    def hide(self):
        self.active = False
    
    def handle_input(self, events):
        if not self.active:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Check if mouse is over button
        button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        self.button_hovered = button_rect.collidepoint(mouse_pos)
        
        # Handle input events
        for event in events:
            # Handle mouse click on button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_hovered:
                    # Play button sound if available
                    try:
                        button_sound = pygame.mixer.Sound(MENU_BUTTON_SOUND)
                        button_sound.set_volume(0.5)
                        button_sound.play()
                    except:
                        pass
                    
                    self.hide()
                    if self.on_return_to_menu:
                        self.on_return_to_menu()
                    return True
            
            # Handle keyboard input (Enter or Escape)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                    self.hide()
                    if self.on_return_to_menu:
                        self.on_return_to_menu()
                    return True
        
        return False
    
    def display(self):
        if not self.active:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Create main rect
        main_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Draw background
        pygame.draw.rect(self.display_surface, self.bg_color, main_rect)
        pygame.draw.rect(self.display_surface, self.border_color, main_rect, self.border_width)
        
        # Draw title
        title_text = "VICTORY!"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_x = self.x + (self.width - title_surface.get_width()) // 2
        title_y = self.y + 60
        self.display_surface.blit(title_surface, (title_x, title_y))
        
        # Draw message
        message_text = "You have saved the island!"
        message_surface = self.message_font.render(message_text, True, self.message_color)
        message_x = self.x + (self.width - message_surface.get_width()) // 2
        message_y = self.y + 180
        self.display_surface.blit(message_surface, (message_x, message_y))
        
        # Draw button
        button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        button_color = self.button_hover_color if self.button_hovered else self.button_color
        
        pygame.draw.rect(self.display_surface, button_color, button_rect)
        pygame.draw.rect(self.display_surface, self.border_color, button_rect, 3)
        
        # Draw button text
        button_text = "Main Menu"
        button_text_surface = self.button_font.render(button_text, True, self.button_text_color)
        button_text_x = self.button_x + (self.button_width - button_text_surface.get_width()) // 2
        button_text_y = self.button_y + (self.button_height - button_text_surface.get_height()) // 2
        self.display_surface.blit(button_text_surface, (button_text_x, button_text_y))

