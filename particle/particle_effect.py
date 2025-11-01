import pygame

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,animation_frames,groups,direction=None):
		super().__init__(groups)
		self.sprite_type = 'magic'
		self.frame_index = 0
		self.animation_speed = 0.15
		self.frames = animation_frames
		self.direction = direction
		self.image = self.frames[self.frame_index]
		if self.direction:
			self.image = self.apply_direction(self.image)
		self.rect = self.image.get_rect(center = pos)

	# Rotate image if original image only faces right
	def apply_direction(self, image):
		if self.direction:
			if self.direction.x < 0:  # Left
				image = pygame.transform.flip(image, True, False)
			elif self.direction.y < 0:  # Up
				image = pygame.transform.rotate(image, 90)
			elif self.direction.y > 0:  # Down
				image = pygame.transform.rotate(image, -90)
		return image

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			old_center = self.rect.center
			self.image = self.frames[int(self.frame_index)]
			if self.direction:
				self.image = self.apply_direction(self.image)
			self.rect = self.image.get_rect(center=old_center)

	def update(self):
		self.animate()