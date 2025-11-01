import pygame
from settings import *


class Dialog:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.width = 1100
        self.height = 140
        self.padding = 20
        self.border_width = 3
        
        # Position at bottom center with some margin
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - self.height - 30
        
        # Fonts
        self.font = pygame.font.Font(UI_FONT, 22)
        self.prompt_font = pygame.font.Font(UI_FONT, 16)
        
        # State
        self.active = False
        self.text = ""
        self.prompt_text = "Press ENTER to continue"
        self.is_inner_dialog = False  # Flag for inner/monologue dialog
        
        # Colors
        self.bg_color = UI_BG_COLOR
        self.border_color = UI_BORDER_COLOR_ACTIVE
        self.text_color = (255, 255, 255)
        self.prompt_color = (200, 200, 200)
        self.inner_dialog_color = (200, 200, 255)  # Slightly different color for inner dialog
    
    def show(self, text, prompt=None, inner_dialog=False):
        self.text = text
        self.active = True
        self.is_inner_dialog = inner_dialog
        if prompt:
            self.prompt_text = prompt
    
    def hide(self):
        self.active = False
    
    def handle_input(self, events):
        if not self.active:
            return False
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.hide()
                    return True
        return False
    
    def _wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0
        
        space_surface = self.font.render(' ', True, self.text_color)
        space_width = space_surface.get_width()
        
        for word in words:
            word_surface = self.font.render(word, True, self.text_color)
            word_width = word_surface.get_width()
            
            if current_width + word_width > max_width and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width + space_width
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def display(self):
        if not self.active:
            return
        
        # Create dialog rect
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Draw background
        pygame.draw.rect(self.display_surface, self.bg_color, dialog_rect)
        pygame.draw.rect(self.display_surface, self.border_color, dialog_rect, self.border_width)
        
        # Wrap and render text
        text_area_width = self.width - (self.padding * 2)
        text_lines = self._wrap_text(self.text, text_area_width)
        
        # Calculate starting y position for text (centered vertically)
        total_text_height = len(text_lines) * self.font.get_height()
        start_y = self.y + (self.height - total_text_height) // 2 - 10
        
        # Choose text color based on dialog type
        dialog_text_color = self.inner_dialog_color if self.is_inner_dialog else self.text_color
        
        # Draw each line of text
        for i, line in enumerate(text_lines):
            text_surface = self.font.render(line, True, dialog_text_color)
            text_x = self.x + self.padding
            text_y = start_y + (i * self.font.get_height())
            self.display_surface.blit(text_surface, (text_x, text_y))
        
        # Draw prompt text at bottom
        prompt_surface = self.prompt_font.render(self.prompt_text, True, self.prompt_color)
        prompt_x = self.x + (self.width - prompt_surface.get_width()) // 2
        prompt_y = self.y + self.height - 30
        self.display_surface.blit(prompt_surface, (prompt_x, prompt_y))

