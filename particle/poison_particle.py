from particle.boss_particle import BossParticle

class PoisonParticle(BossParticle):
    def __init__(self, pos, frames, opacity=255):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.2

        self.opacity = opacity

        # first frame
        self.image = self.frames[0].copy()
        self.image.set_alpha(self.opacity)

        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            # show next frame
            self.image = self.frames[int(self.frame_index)].copy()
            self.image.set_alpha(self.opacity)