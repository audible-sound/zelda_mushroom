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
        'cooldown': 2500,
        'damage': 25,
        'graphic': './assets/weapons/lance/full.png'
    },
    'axe': {
        'cooldown': 5000,
        'damage': 75,
        'graphic': './assets/weapons/axe/full.png'
    },
    'sword': {
        'cooldown': 2000,
        'damage': 15,
        'graphic': './assets/weapons/sword/full.png'
    },
    'sabre': {
        'cooldown': 3500,
        'damage': 50,
        'graphic': './assets/weapons/sabre/full.png'
    },
    'staff': {
        'cooldown': 1200,
        'damage': 10,
        'graphic': './assets/weapons/staff/full.png'
    },
}

# magic
magic_data = {
	'fire': {
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
	'shroom_goon': {'health': 300,'damage':20,'attack_type': 'slash', 'attack_sound':'./assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 300},
	'shroom_mob': {'health': 200,'damage':10,'attack_type': 'slash',  'attack_sound':'./assets/audio/attack/slash.wav','speed': 2, 'resistance': 3, 'attack_radius': 70, 'notice_radius': 350},
    'spirit': {'health': 100,'damage':25,'attack_type': 'thunder', 'attack_sound':'./assets/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 300},
    'zombie_shroom': {'health': 500,'damage':40,'attack_type': 'zombie_shroom_attack', 'attack_sound':'./assets/audio/attack/claw.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 250, 'notice_radius': 400},
    'fire_shroom': {'health': 550,'damage':60,'attack_type': 'fire_shroom_attack', 'attack_sound':'./assets/audio/attack/claw.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 150, 'notice_radius': 400},
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

TITLE_FONT = 'assets/font/slkscr.ttf'
LOGO_IMAGE = 'assets/menu/title.png'
MENU_BG_IMAGE = 'assets/menu/menu_bg.png'
MENU_BUTTON_SOUND = 'assets/audio/menu_button.wav'