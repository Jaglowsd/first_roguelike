import libtcodpy as libtcod

# size of window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# GUI bar positioning
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

# Game message positioning
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

# size of dungeon
MAP_WIDTH = 80
MAP_HEIGHT = 43

# When to end the game
END_LEVEL = 10

# Max and min room size
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6

# Max number of rooms
MAX_ROOMS = 30

# Width of menu windows
INVENTORY_WIDTH = 50
LEVEL_SCREEN_WIDTH = 40
CHARACTER_SCREEN_WIDTH = 30

# Amount to heal player by
HEAL_AMOUNT = 40

# Number of turns object is confused for
CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8

# Lighting spell properties
LIGHTING_DAMAGE = 40
LIGHTING_RANGE = 5

# Fireball properties
FIREBALL_DAMAGE = 25
FIREBALL_RADIUS = 3

# Experience and level-ups
LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150

# Field of View Constants
FOV_ALGO = 0 # BASIC algorithm
FOV_LIGHT_WALLS = True # light walls or not
TORCH_RADIUS = 10
SQUARED_TORCH_RADIUS = TORCH_RADIUS * TORCH_RADIUS

# 30 frames per second
LIMIT_FPS = 30

# Color definitions
color_dark_wall = libtcod.darker_sepia
color_dark_ground = libtcod.darker_grey
color_light_wall = libtcod.sepia
color_light_ground = libtcod.grey

# Item class drop chances
COMMON = 60
UNCOMMON = 30
RARE = 15
LEGENDARY = 5
GOLD_DROP = 80

# Affixes modifier for monsters
MONSTER_PRE_MOD = {'Weak': -.10, 'Lesser': -.05, 'Greater': .15, 'Badass': .20, 
				   'SuperBadass': .30}
# MONSTER_TIER_SUFFIX = {'lord', 'minion', 'worker', 'fiend'}

# Affix scaling factor
MONSTER_TIER_SCALING = {}

# base monster names
ORC = 'orc'
TROLL = 'troll'

# loot/items
ORA = 'orc\'s right arm'
RATIONS = 'rations'
GOLD = 'gold'
CLUB = 'club'

# monster loot pool
MONSTER_LOOT_POOL = {
					 ORC:
						{
							ORA: RARE,
							RATIONS: COMMON,
							GOLD: GOLD_DROP
						},
				     TROLL:
						{
							CLUB: RARE, 
							RATIONS: COMMON,
							GOLD: GOLD_DROP
						}
					}			