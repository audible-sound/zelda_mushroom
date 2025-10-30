# Set window size
WIDTH = 1280
HEIGHT = 720

# Set frames per second
FPS = 60

# Set tile size
TILESIZE = 64

# Weapons
weapon_data = {
    'lance': {
        'cooldown': 250,
        'damage': 25,
        'graphic': './assets/weapons/lance/full.png'
    }
}

# magic
magic_data = {
	'flame': {
        'strength': 15,
        'cost': 20,''
        'graphic':'./assets/particles/fire/fire.png'
    },
	'heal' : {
        'strength': 30,
        'cost': 40,
        'graphic':'./assets/particles/heal/heal.png'
        },
    'ice': {
        'strength': 20,
        'cost': 25,
        'graphic':'./assets/particles/ice/ice.png'
    }
}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
 }

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 200
UI_BORDER_COLOR = '#111111'
UI_BORDER_COLOR_ACTIVE = 'gold'
ITEM_BOX_SIZE = 80
UI_FONT = './assets/font/ByteBounce.ttf'
UI_FONT_SIZE = 18
UI_BG_COLOR = '#222222'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'