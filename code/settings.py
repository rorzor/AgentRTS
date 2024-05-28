# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 120
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
ORGANICPROB = 0.15
STARTINGMINERAL = 20
MINSPACING = 8

# Resource harvest rates
resource_harvest = {
    'organic' : 1,
    'mineral' : 0.1
}

# Resource consumption rates
resource_consumption = {
    'agent_min_harvest': 1,      # energy
    'agent_org_harvest': 1,      # energy
    'agent_move': 0.01,             # energy
    'agent_spawn': 10               # organic
}

# weapons
weapon_data = {
    'sabre': {'cooldown': 100, 'damage': 15, 'graphic': '../graphics/weapons/sabre'}
}

# Dataframe variables
DATAFRAME_RADIUS = 5
MAX_FRAME_SIZE = 200
SPRITE_CODES = {
    'invisible' : 1,
    'organic' : 2,
    'mineral' : 3,
    'agent' : 4,
    'ship': 5
}

