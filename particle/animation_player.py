from random import choice
from particle.ParticleEffect import ParticleEffect
from utils import import_asset_surfaces


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic particles
            'fire': import_asset_surfaces('./assets/particles/fire/frames'),
			'heal': import_asset_surfaces('./assets/particles/heal/frames'),
            'ice': import_asset_surfaces('./assets/particles/ice/frames'),
   
            # attack particles
            'slash': import_asset_surfaces('./assets/particles/slash'),
            'thunder': import_asset_surfaces('./assets/particles/thunder'),
            'fire_shroom_attack': import_asset_surfaces('./assets/monsters/fire_shroom/attack'),
            'zombie_shroom_attack': import_asset_surfaces('./assets/monsters/zombie_shroom/attack'),
            
            # death particles
            'fire_shroom': import_asset_surfaces('./assets/monsters/fire_shroom/die'),
            'zombie_shroom': import_asset_surfaces('./assets/monsters/zombie_shroom/die'),
            'shroom_goon': import_asset_surfaces('./assets/monsters/shroom_goon/die'),
            'shroom_mob': import_asset_surfaces('./assets/monsters/shroom_mob/die'),
            'spirit': import_asset_surfaces('./assets/monsters/spirit/die'),
            
            'leaf': (
                import_asset_surfaces('./assets/particles/leaf1'),
				import_asset_surfaces('./assets/particles/leaf2'),
				import_asset_surfaces('./assets/particles/leaf3'),
            )
        }
        
    def create_leaf_particles(self,pos,groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos,animation_frames,groups)
        
    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)