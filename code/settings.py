# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

MAPHEIGHT = 100
MAPWIDTH = 100

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

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