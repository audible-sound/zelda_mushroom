from particle.boss_particle import BossParticle

class SweepParticle(BossParticle):
    def __init__(self, pos, frames):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.35

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]