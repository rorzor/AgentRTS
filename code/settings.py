# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

MAPHEIGHT = 100
MAPWIDTH = 100

# UI
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
TEXT_COLOR = '#EEEEEE'


# resources spawning variables
RESOURCEBUFFER = 10
ORGANICPROB = 0.08
STARTINGMINERAL = 20
MINSPACING = 8

# Resource harvest rates
resource_harvest = {
    'organic' : 1,
    'mineral' : 0.1
}

# weapons
weapon_data = {
    'sabre': {'cooldown': 100, 'damage': 15, 'graphic': '../graphics/weapons/sabre'}
}