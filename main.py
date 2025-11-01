import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.level = Level()

		# sound 
		main_sound = pygame.mixer.Sound('../audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR)
			self.level.run()

			#game over when player health < 0
			if self.level.player.health < 0:
				self.game_over()

			pygame.display.update()
			self.clock.tick(FPS)

	def game_over(self):
		# Stop the main music
		pygame.mixer.stop()

		# Load and play game over sound
		game_over_sound = pygame.mixer.Sound('../endMenu/gameOver.mp3')
		game_over_sound.set_volume(1.0)
		game_over_sound.play()

		# --- Load background image ---
		bg_image = pygame.image.load('../endMenu/gameOver.webp').convert()
		bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGTH))

		# === Load custom font ===
		# Replace this with your actual pixel or fantasy font file
		# Example fonts: "zelda_font.ttf", "pixel.ttf", "adventure.ttf"
		font_path = "../endMenu/BoldPixels.otf"  # <-- your font file path
		try:
			button_font = pygame.font.Font(font_path, 50)
		except:
			# fallback if font not found
			button_font = pygame.font.Font(None, 50)

		# Create button rectangles
		restart_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGTH // 2, 250, 50)
		menu_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGTH // 2 + 70, 250, 50)
		buttons = [restart_button_rect, menu_button_rect]
		selected_index = 0  # 0 = restart, 1 = menu

		while True:
			# Draw background image
			self.screen.blit(bg_image, (0, 0))

			# --- Load background image ---
			bg_image = pygame.image.load('../endMenu/gameOver.webp').convert()
			bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGTH))

			# Draw buttons with highlight
			for i, rect in enumerate(buttons):
				label = "Restart" if i == 0 else "Main Menu"
				text_color = (0, 0, 0)
				text = button_font.render(label, True, text_color)

				# Draw transparent button (no fill)
				if i == selected_index:
					pygame.draw.rect(self.screen, (207, 154, 85), rect, 0) # hightlight selected box

				# Center text inside button
				self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

			# Handle events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						selected_index = (selected_index - 1) % len(buttons)
					elif event.key == pygame.K_DOWN:
						selected_index = (selected_index + 1) % len(buttons)
					elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						if selected_index == 0:  # Restart
							self.__init__()
							self.run()
							return
						elif selected_index == 1:  # Main Menu
							pass  # <--- Call your main menu function here, self.main_menu()
							return

				if event.type == pygame.MOUSEBUTTONDOWN:
					if restart_button_rect.collidepoint(event.pos):
						self.__init__()
						self.run()
						return
					elif menu_button_rect.collidepoint(event.pos):
						# Go back to main menu
						pass  # <--- Call your main menu function here, self.main_menu()
						return

			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()