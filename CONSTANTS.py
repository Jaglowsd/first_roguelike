import libtcodpy as libtcod

# size of window
SCREEN_WIDTH = 90
SCREEN_HEIGHT = 60

# size of first boss prefab map
PREFAB_WIDTH = 100
PREFAB_HEIGHT = 34

# GUI bar size
BAR_WIDTH = 20

# Game message panel positioning and size
MSG_X = BAR_WIDTH + 2
MSG_Y = 0
MSG_PANEL_WIDTH = SCREEN_WIDTH - MSG_X
MSG_PANEL_HEIGHT = 8

# Stats panel positioning and size
STATS_PANEL_WIDTH = MSG_X
STATS_PANEL_HEIGHT = SCREEN_HEIGHT / 2
STATS_X = 0
STATS_Y = 0

# size and positioning of map panel
MAP_WIDTH = 100
MAP_HEIGHT = 100
MAP_X = MSG_X
MAP_Y = MSG_PANEL_HEIGHT

# portion of map shown
# Subtract three for the action panel at the bottom
CAMERA_WIDTH = SCREEN_WIDTH - STATS_PANEL_WIDTH
CAMERA_HEIGHT = SCREEN_HEIGHT - MSG_PANEL_HEIGHT - 3

# Action panel position and size
ACTIONS_PANEL_WIDTH = CAMERA_WIDTH
ACTIONS_PANEL_HEIGHT = 3
ACTIONS_X = MAP_X
ACTIONS_Y = MSG_PANEL_HEIGHT + CAMERA_HEIGHT

# Hotkey panel positioning and size
HOTKEY_PANEL_WIDTH = BAR_WIDTH + 2
HOTKEY_PANEL_HEIGHT = SCREEN_HEIGHT / 2
HOTKEY_X = 0
HOTKEY_Y = STATS_PANEL_HEIGHT
HOTKEY_BIND_WIDTH = 45

# When to end the game
END_LEVEL = 10

# Max and min room size
ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 8

# Max number of rooms
MAX_ROOMS = 30

# Width of menu windows
INVENTORY_WIDTH = 50
LEVEL_SCREEN_WIDTH = 40
CHARACTER_SCREEN_WIDTH = 40
BONFIRE_WIDTH = 20

# Estus flask usage and healing amount
ESTUS_FLASK_MAX = 5
ESTUS_FLASK_HEAL = 40

# Amount to heal player by
HEAL_AMOUNT = 20

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
LEVEL_UP_BASE = 656
LEVEL_UP_FACTOR = 17

# Field of View Constants
FOV_ALGO = 0 # BASIC algorithm
FOV_LIGHT_WALLS = True # light walls or not
TORCH_RADIUS = 10
SQUARED_TORCH_RADIUS = TORCH_RADIUS * TORCH_RADIUS

# 30 frames per second
LIMIT_FPS = 30

# Speed values to simulate real-time combat
DEFAULT_SPEED = 8
PLAYER_SPEED = 2
DEFAULT_ATTACK_SPEED = 20

# Color definitions
color_dark_wall = libtcod.darkest_sepia
color_dark_ground = libtcod.darkest_grey
color_light_wall = libtcod.sepia
color_light_ground = libtcod.grey

# Infusion list
INFUSIONS = {0: 'fire', 1: 'lightning', 2: 'magic'}

# Requirements default
DEFAULT_REQS = [1, 1, 1]

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