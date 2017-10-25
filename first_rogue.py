import libtcodpy as libtcod
import math
import textwrap
import shelve
import sys

import CONSTANTS

class Object:
# this is a generic object: the player, monster, stairs, tiles, etc...
# this is used for things that are represented by characters on the console.
# can keep adding components to extend our generic object class.

	def __init__(self, x, y, name, char, color, blocks=False,
				 always_visible=None, fighter=None, ai=None, item=None,
				 equipment=None):
	# Create object.
		self.x = x
		self.y = y
		self.name = name
		self.char = char
		self.color = color
		self.blocks = blocks
		self.always_visible = always_visible

		# add fighter component
		self.fighter = fighter
		if self.fighter:
			self.fighter.owner = self
		# add ai component
		self.ai = ai
		if self.ai:
			self.ai.owner = self
		# add item component
		self.item = item
		if self.item:
			self.item.owner = self
		# equipmet component
		self.equipment = equipment
		if self.equipment:
			self.equipment.owner = self
			# there must be an item component for equipment to work
			# it will be picked up and used in a similar way
			self.item = Item()
			self.item.owner = self

	def move(cls, dx, dy):
		# move by given amount if there isn't the tile is not blocked.
		if not is_blocked(cls.x + dx, cls.y + dy):
			cls.x += dx
			cls.y += dy
			# regenerate 1 stamina point per step.
			if cls.fighter.stamina != cls.fighter.max_stamina:
				cls.fighter.stamina += 1
			
	def move_towards(cls, target_x, target_y):
		# vector from this object to tagret object.
		dx = target_x - cls.x
		dy = target_y - cls.y

		# length of vector
		magnitude = math.sqrt(dx ** 2 + dy ** 2)

		# normalize magnitude to 1 (preserving direction), then round it and
		# convert to integer so movement is restricted to map grid.
		dx = int(round(dx / magnitude))
		dy = int(round(dy / magnitude))
		cls.move(dx, dy)
		
	def distance_to(cls, other):
		# return distance between this object and any other Object.
		dx = other.x - cls.x
		dy = other.y - cls.y
		return math.sqrt(dx ** 2 + dy ** 2)
		
	def distance(cls, x, y):
		# return distance from coordinates
		return math.sqrt((x - cls.x) ** 2 + (y - cls.y) ** 2)
		
	def draw(cls):
		# Show object (other than player object) if it's visible to the player.
		if (libtcod.map_is_in_fov(fov_map, cls.x, cls.y) or
			(cls.always_visible and map[cls.x][cls.y].explored)):
			# set color and then draw the character that represents this 
			# object at its position.
			libtcod.console_set_default_foreground(con, cls.color)
			libtcod.console_put_char(con, cls.x, cls.y, 
									 cls.char, libtcod.BKGND_NONE)
		
	def send_to_front(cls):
		# make this object be drawn first to avoid corpse overlap.
		global objects
		objects.remove(cls)
		objects.insert(0, cls)

	def clear(cls):
		# erase the charatcer that represents ths object.
		libtcod.console_put_char(con, cls.x, cls.y, ' ', libtcod.BKGND_NONE)


class Item:
	# definition of item: items can be picked up and used.
	def __init__(self, use_function=None):		
		self.use_function = use_function		

	def use(cls):
		# special case where the item is a piece of equipment,
		# the 'use' function toggles equip/dequip
		if cls.owner.equipment:
			cls.owner.equipment.toggle_equip()
			return

		# call the use function if it is defined.
		if cls.use_function is None:
			message('The ' + cls.owner.name + ' cannot be used.')
		else:
			# call the use function here and see if the return is 'cancelled'
			if cls.use_function() != 'cancelled':
				inventory.remove(cls.owner) # use up item if it wasn't cancelled
		
	def pick_up(cls):
		# add item to player's inventory and remove it from the map.
		if len(inventory) >= 26:
			message('Your inventory is full! Cannot pick up ' 
					+ cls.owner.name 
					+ '.', libtcod.red)
		else:
			inventory.append(cls.owner)
			objects.remove(cls.owner)
			message('Picked up ' + cls.owner.name + '!', libtcod.green)
			
			# special case where the item is a piece of equipment,
			# the 'use' function toggles equip/dequip
			equipment = cls.owner.equipment
			if (equipment 
				and equipment.get_equiped_in_slot(equipment.slot) is None):
				equipment.equip()

	def drop(cls):
		# drop item from inventory and leave it at player's coordinates
		inventory.remove(cls.owner)
		cls.owner.x = player.x
		cls.owner.y = player.y
		objects.append(cls.owner)
		cls.owner.send_to_front()
		message('Dropped ' + cls.owner.name, libtcod.yellow)
		
		# when dropping equipment we need to dequip it
		equipment = cls.owner.equipment
		if equipment and equipment.is_equiped:
			equipment.dequip()


class Equipment:
	# objects that can be equiped to player, automatically adds item component
	def __init__(self, slot, power_bonus=0, defense_bonus=0,
				 max_hp_bonus=0, max_stamina_bonus=0, stamina_usage=0):
		# where on the players person its equiped (i.e. slot)
		self.slot = slot
		self.is_equiped = False
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.max_hp_bonus = max_hp_bonus		
		self.max_stamina_bonus = max_stamina_bonus
		self.stamina_usage = stamina_usage
		
	def toggle_equip(cls): # toggle equip/dequip status
		if cls.is_equiped:
			cls.dequip()
		else:
			cls.equip()
			
	def equip(cls):
		# if the slot is already in use, dequip the item and equip the new one
		old_equip = cls.get_equiped_in_slot(cls.slot)
		if old_equip is not None:
			old_equip.dequip()
	
		# equip object and display message
		cls.is_equiped = True
		message('Equiped ' + cls.owner.name + ' to ' + cls.slot + '.', 
				libtcod.light_green)
				
	def dequip(cls):
		# dequip object and show message
		if not cls.is_equiped: 
			return
		cls.is_equiped = False
		message('Removed ' + cls.owner.name + ' from ' + cls.slot + '.', 
				libtcod.light_yellow)
				
	def get_equiped_in_slot(cls, slot):
		# returns the equipment in a slot, or None of it's empty
		for obj in inventory:
			if (obj.equipment and obj.equipment.slot == slot 
				and obj.equipment.is_equiped):
				return obj.equipment
		return None

	def use_stamina(cls):
		# equipment usage drains stamina
		player.fighter.stamina -= cls.stamina_usage

	
class Fighter:
	# combat related properties and methods (player, monsters, NPCs...)
	def __init__(self, hp, defense, power, stamina, exp, death_function=None,
				 type=None,  modifier=None):
		self.base_max_hp = hp # keep track of hp vs. max hp
		self.hp = hp
		self.base_defense = defense
		self.base_power = power
		self.base_max_stamina = stamina # player stamina
		self.stamina = stamina
		self.exp = exp # amount of experience given to player
		self.death_function = death_function		
		self.type = type # What kind of enemy this object is
		if modifier is not None: # Apply any name base stat modifiers
			self.apply_modifier(modifier)
		
	@property
	def power(self): 
		# return actual power by summing base power to all bonuses
		bonus = sum(equipment.power_bonus for equipment in get_all_equiped(self.owner))
		return self.base_power + bonus
		
	@property
	def defense(self): 
		# return actual defense by summing base defense to all bonuses
		bonus = sum(equipment.defense_bonus for equipment in get_all_equiped(self.owner))
		return self.base_defense + bonus
		
	@property
	def max_hp(self): # return actual max_hp by summing base max hp to all bonuses
		bonus = sum(equipment.max_hp_bonus for equipment in get_all_equiped(self.owner))
		return self.base_max_hp + bonus

	@property
	def max_stamina(self): # return actual stamina by summing base stamina to all bonuses
		bonus = sum(equipment.max_stamina_bonus for equipment in get_all_equiped(self.owner))
		return self.base_max_stamina + bonus

	def take_damage(cls, damage):
		# apply damage if possible
		if damage > 0:
			cls.hp -= damage

			# Check if fighter is dead, then call their death function.
			if cls.hp <= 0:
				d_function = cls.death_function
				# set to 0 to prevent a negative hp bar from being drawn
				cls.hp = 0
				if d_function is not None:
					d_function(cls.owner)
					if cls.owner != player: # yield player exp
						player.fighter.exp += cls.exp

	def attack(cls, target):
		# simple formula to calculate damage and stamina consumption
		(stamina_available, equip) = cls.calculate_stamina_use()
		damage = cls.power - target.fighter.defense
		if stamina_available < 0:
			message('You try to attack but are too exhausted...', libtcod.red)
		elif damage <= 0:
			message(cls.owner.name.capitalize() + ' attacks ' + target.name
					+ ' but it has no effect!')
		else: # Otherwise, target takes damage
			message(cls.owner.name.capitalize() + ' attacks ' + target.name
					+ ' for ' + str(damage) + ' hit points.')
			target.fighter.take_damage(damage)
			equip.use_stamina()

	def monster_attack(cls, target):
		# basic monster attack
		damage = cls.power - target.fighter.defense
		if damage > 0:
			message(cls.owner.name.capitalize() + ' attacks ' + target.name 
					+ ' for ' + str(damage) + ' hit points.')
			target.fighter.take_damage(damage)
		else:
			message(cls.owner.name.capitalize() + ' attacks ' + target.name
					+ ' but it has no effect!')

	def heal(cls, amount):
		# heal player by the given amount, setting hp to max if it goes over
		cls.hp += amount
		if cls.hp > cls.max_hp:
			cls.hp = cls.max_hp
			
	def apply_modifier(cls, modifier_name):
		# mutate the base stats of monster based on their affix modifier
		modifier = CONSTANTS.MONSTER_PRE_MOD[modifier_name]
		cls.base_max_hp = cls.base_max_hp + int(round(cls.base_max_hp * modifier))
		cls.hp = cls.base_max_hp
		cls.base_power = cls.base_power + int(round(cls.base_power * modifier))
		cls.base_defense = cls.base_defense + int(round(cls.base_defense * modifier))
		cls.exp = cls.exp + int(round(cls.exp * modifier))

	def calculate_stamina_use(cls):
		# Calculate equipment stamina usage
		main = None
		equiped = get_all_equiped(player)
		for equipment in equiped:
			if equipment.slot == 'main hand':
				main = equipment

		if main is not None:
			stamina_available = player.fighter.stamina \
								- main.stamina_usage
		else:
			stamina_available = player.fighter.stamina - 1

		return (stamina_available, main)


class BasicMonster:
	# AI for basic monsters
	def take_turn(cls):
		# if monster is in player fov, they will advance towards player.
		monster = cls.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			# move towards player if not within attacking range (1 tile).
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)
				
			# attack player if within 1 tile and player has hp.
			elif player.fighter.hp > 0:
				monster.fighter.monster_attack(player)


class ConfusedMonster:
	# AI for a temporarily confused monster, reverts back to original ai
	def __init__(self, old_ai, num_turns=CONSTANTS.CONFUSE_NUM_TURNS):
		self.old_ai = old_ai
		self.num_turns = num_turns
		
	def take_turn(cls):
		# move in random direction
		if cls.num_turns > 0: # continue being confused
			cls.owner.move(libtcod.random_get_int(0, -1, 1), 
						   libtcod.random_get_int(0, -1, 1))
			cls.num_turns -= 1
			
		else: # revert back to original ai
			cls.owner.ai = cls.old_ai
			message(cls.owner.name + ' is no longer confused.', libtcod.red)


class Tile:
	# Tiles of map and their properties.
	def __init__(self, blocked, block_sight=None):
		# Create tile to be used as wall, ground, etc...
		self.blocked = blocked
		
		# By default, if a tile is blocked, it also blocks sight.
		if block_sight is None:
			block_sight = blocked
		self.block_sight = blocked
		
		# tiles begin unexplored
		self.explored = False


class Rectangle:
	# A rectangle on map. Used to represent rooms.
	def __init__(self, x, y, w, h):
		# Top left corner, and bottom right corner of rectangle.
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		
	def center(self):
		# Determine the center of the rectangle.
		center_x = (self.x2 + self.x1) / 2
		center_y = (self.y2 + self.y1) / 2
		return (center_x, center_y)
		
	def intersect(self, other):
		# Determine if two different rectangles intersect.
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def create_room(room):
	# Go through given room making the rectangle passable.
	global map	
	# Range() goes from room.x1 + 1 to room.x2 - 1, so we exclude the borders of
	# the rectangle to create walls.
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			map[x][y].block_sight = False
			map[x][y].blocked = False

def create_h_tunnel(x1, x2, y):
	# make a horizontal tunnel.
	global map
	# Given points to start, end, and a height-we can carve a horizontal tunnel
	# between rooms.
	for x in range(min(x1, x2), max(x1, x2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
	# make a vertical tunnel.
	global map
	# Given points to start, end, and a width-we can carve a vertical tunnel
	# between rooms.
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False

def make_map():
	# randomly generates rooms to design a map.
	global map, objects, stairs, bonfire
	
	# Store our objects to iterate through
	objects = [player]
	
	# Fill map with unblocked tiles.
	map = [[Tile(True)
		for y in range(CONSTANTS.MAP_HEIGHT)]
			for x in range(CONSTANTS.MAP_WIDTH)]
	
	rooms = []
	num_rooms = 0
	
	for r in range(CONSTANTS.MAX_ROOMS):
		# random width and height for rooms.
		w = libtcod.random_get_int(0, CONSTANTS.ROOM_MIN_SIZE,
								   CONSTANTS.ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, CONSTANTS.ROOM_MIN_SIZE,
								   CONSTANTS.ROOM_MAX_SIZE)
		# random position without going out of bounds.
		x = libtcod.random_get_int(0, 0, CONSTANTS.MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0, 0, CONSTANTS.MAP_HEIGHT - h - 1)
		
		# Create the room as a rectangle object.
		new_room = Rectangle(x, y, w ,h)
		
		# Check that new_room does not intersect with existing rooms.
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
			
		# no intersections found, so room is valid.
		if not failed:
			# 'paint' to map's tiles.
			create_room(new_room)

			# center coordinates of new room.
			(new_x, new_y) = new_room.center()

			if num_rooms == 0:
				# first room, where player starts. Place them in center.
				player.x = new_x + 1
				player.y = new_y

				bonfire = Object(new_x, new_y, 'bonfire', '&', libtcod.flame,
									blocks=True, always_visible=True)
				objects.append(bonfire)

			# all rooms after the first.
			# connect it to the previous room with a tunnel.
			else:
				# center coordinates of previous room.
				(prev_x, prev_y) = rooms[num_rooms-1].center()

				# Build tunnel between rooms.
				# flip a coin (i.e. either 0 or 1)
				if libtcod.random_get_int(0, 0, 1) == 1:
					# first horizontally, then vertically.
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					# vertically, then horizontally.
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)

			# Append new room to list.
			rooms.append(new_room)
			num_rooms += 1

			# Place objects in the new room
			place_objects(new_room)

			# Visualization of room drawing order.
			# room_no = Object(new_x, new_y, chr(63+num_rooms), libtcod.white)
			# objects.insert(0, room_no)
			
	# create stairs at the center of the last room
	stairs = Object(new_x, new_y, 'stairs', '>', libtcod.white, 
					always_visible=True)
	objects.append(stairs)
	stairs.send_to_front() # so its drawn below monsters
	
def next_level():
	global dungeon_level
	# bring player to new dungeon level-redraw map and fov
	message('You take a moment to rest and recover your strenth', 
			libtcod.light_violet)
	player.fighter.heal(player.fighter.max_hp/2) # heal player by 50% max hp
	
	message('After a rare moment of peace, you descend depper into the dungeon', 
			libtcod.red)
	dungeon_level += 1
	make_map()
	initialize_fov()

def place_objects(room):
	# place objects on map
	global monster_prefix
	
	# maximum number of monsters per room, floor dependent
	max_monsters = from_dungeon_level([[2, 1, CONSTANTS.END_LEVEL],
									   [3, 4, CONSTANTS.END_LEVEL],
									   [5, 6, CONSTANTS.END_LEVEL]])
	# choose random number of monsters.
	num_monsters = libtcod.random_get_int(0, 0, max_monsters)
	# dictionary of monsters and there chances of spawn
	monster_chances = {}
	monster_chances['orc'] = 80 # orc spawn is floor independent
	monster_chances['troll'] = from_dungeon_level([[15, 3, CONSTANTS.END_LEVEL],
												   [30, 5, CONSTANTS.END_LEVEL],
												   [60, 7, CONSTANTS.END_LEVEL]]
												  )
	# generate chances for a prefix.
	monster_prefix = {}
	monster_prefix['Weak'] = from_dungeon_level([[75, 1, 2], [25, 2, 4]])
	monster_prefix['Lesser'] = from_dungeon_level([[25, 1, 2], [50, 2, 4],
												   [25, 4, 6]])
	monster_prefix['Greater'] = from_dungeon_level([[25, 2, 4], [65, 4, 6],
													[75, 6, 8],
													[50, 6, CONSTANTS.END_LEVEL]])
	monster_prefix['Badass'] = from_dungeon_level([[10, 4, 6], [20, 6, 8],
												  [35, 8, CONSTANTS.END_LEVEL]])
	monster_prefix['SuperBadass'] = from_dungeon_level([[5, 6, 8],
											  [15, 8, CONSTANTS.END_LEVEL]])

	for i in range(num_monsters):
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

		if not is_blocked(x, y):
			choice = random_choice(monster_chances)
			(affixed_name, mod) = choose_affix(choice)
			if choice == 'orc':
				# create orc				
				fighter_component = Fighter(hp=20, defense=0, power=4,
											stamina=1, exp=35,
											death_function=monster_death,
											type=CONSTANTS.ORC, modifier=mod)
				ai_component = BasicMonster()
				monster = Object(x, y, affixed_name, 'o',
								 libtcod.darker_green, blocks=True,
								 fighter=fighter_component, ai=ai_component)
			elif choice == 'troll':
				# create troll
				fighter_component = Fighter(hp=30, defense=2, power=8,
											stamina=1, exp=100,
											death_function=monster_death,
											type=CONSTANTS.TROLL, modifier=mod)
				ai_component = BasicMonster()

				monster = Object(x, y, affixed_name, 'T',
								 libtcod.dark_green, blocks=True,
								 fighter=fighter_component, ai=ai_component)

			objects.append(monster)
		
	# maximum number of items per room, floor dependent
	max_items = from_dungeon_level([[2, 1, CONSTANTS.END_LEVEL],
									[3, 4, CONSTANTS.END_LEVEL],
									[5, 6, CONSTANTS.END_LEVEL]])
	# choose random number of items to spawn
	num_items = libtcod.random_get_int(0, 0, max_items)
	# dictionary of items and there chances of spawn
	item_chances = {}
	item_chances['heal'] = 25 # heal spawn is floor independent
	item_chances['confuse'] = from_dungeon_level([[10, 2, CONSTANTS.END_LEVEL]])
	item_chances['lighting'] = from_dungeon_level([[25, 4, CONSTANTS.END_LEVEL]])
	item_chances['fire'] = from_dungeon_level([[25, 6, CONSTANTS.END_LEVEL]])
	item_chances['sword'] = from_dungeon_level([[5, 4, CONSTANTS.END_LEVEL]])
	item_chances['shield'] = from_dungeon_level([[15, 8, CONSTANTS.END_LEVEL]])
	
	for i in range(num_items):
		# choose random spot for items
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
		
		if not is_blocked(x, y):
			# create a chance for item to spawn
			choice = random_choice(item_chances)
			if choice == 'heal':
				# healing potion (70% chance)
				item_component = Item(use_function=cast_heal)
				item = Object(x, y, 'healing potion', '!', libtcod.white,
							  item=item_component, always_visible=True)
			elif choice == 'lighting':
				# create a lighting spell (10% chance)
				item_component = Item(use_function=cast_lighting)
				item = Object(x, y, 'Lighting spell', 'Z', libtcod.light_yellow,
							  item=item_component, always_visible=True)
			elif choice == 'fire':
				# create a fireball spell (10% chance)
				item_component = Item(use_function=cast_fireball)
				item = Object(x, y, 'Fireball scroll', 'F', libtcod.orange,
							  item=item_component, always_visible=True)
			elif choice =='confuse':
				# create a confusion spell (10% chance)
				item_component = Item(use_function=cast_confuse)
				item = Object(x, y, 'Confusion spell scroll', 'C', libtcod.cyan,
							  item=item_component, always_visible=True)
			elif choice == 'sword':
				# sword (5% chance from floor 4 onwards)
				equip_component = Equipment(slot='main hand', power_bonus=3,
											stamina_usage=3)
				item = Object(x, y, 'Beast Slayer', '/', libtcod.sky,
							  equipment=equip_component)
			elif choice == 'shield':
				# shield (15% chance floor 8 onwards)
				equip_component = Equipment(slot='off hand', defense_bonus=1)
				item = Object(x, y, 'Shield', '[', libtcod.darker_orange,
							  equipment=equip_component)

			objects.append(item)
			item.send_to_front() # item appear below other objects.

def from_dungeon_level(table):
	# returns value depending on dungeon level. The table specifies what
	# value occurs after each level, default is 0.
	for (value, min_level, max_level) in reversed(table):
		if dungeon_level >= min_level and dungeon_level <= max_level:
			return value
	return 0

def random_choice(chances_dict): 
	# choose one option from dictionary of chances, return its key	
	chances = chances_dict.values()
	strings = chances_dict.keys()
	
	return strings[random_choice_index(chances)]
		
def random_choice_index(chances):
	# choose one option from the list of chances, returning its index
	dice = libtcod.random_get_int(0, 1, sum(chances))
	
	# go through all chances, keeping sum so far
	running_sum = 0
	choice = 0
	for w in chances:
		running_sum += w
		# see if the dice landed in the part that corresponds to this choice
		if dice <= running_sum:
			return choice
		choice += 1
		
def choose_affix(base_name):
	# returns an affixed name and the modifier to apply
	global monster_prefix
	
	prefix = libtcod.random_get_int(0, 0, 1)
	if prefix:	
		# chooses which modifier to apply, if any
		modifier = random_choice(monster_prefix)
		# attach the affix to the base name
		affixed_name = attach_affix(base_name, modifier, 'prefix')
		return (affixed_name, modifier)
	else:
		return (base_name, None)
		
def attach_affix(base_name, modifier, affix_type):
	# return base name with affix applied
	if affix_type == 'prefix':
		return (modifier + ' ' + base_name)
	else:
		return (base_name + ' ' + modifier)

def is_blocked(x, y):
	# check if a tile is blocked.
	# first check the map tile
	if map[x][y].blocked:
		return True
	
	# check for blocking objects.
	for object in objects:
		if object.blocks and object.x == x and object.y == y:
			return True
	
	return False

def cast_heal():
	# heal the player
	if player.fighter.hp == player.fighter.max_hp:
		message('Already at full health', libtcod.red)
		return 'cancelled'
	
	message('Your wounds start to feel better!', libtcod.green)
	player.fighter.heal(CONSTANTS.HEAL_AMOUNT)
		
def cast_lighting():
	# cast a lighting spell that hits the nearest target within a range.
	monster = closest_monster(CONSTANTS.LIGHTING_RANGE)
	if monster is None: # no monster in the lighting's range
		message('Monsters out of range!', libtcod.red)
		return 'cancelled'
	
	# strike the closest monster!	
	message('A lighting bolt strikes ' + monster.name 
			+ ' with a loud thunder! The target suffers ' 
			+ str(CONSTANTS.LIGHTING_DAMAGE) + ' damage!', libtcod.light_blue)
	monster.fighter.take_damage(CONSTANTS.LIGHTING_DAMAGE)
	
def cast_confuse():
	# cast confusion spell on selected target.
	message('Left-click a target or right-click to cancel!', libtcod.light_cyan)
	monster = target_monster(CONSTANTS.CONFUSE_RANGE)
	if monster is None: # no monster selected		
		return 'cancelled'
	
	# confuse the closest monster!
	old_ai = monster.ai
	monster.ai = ConfusedMonster(old_ai)
	monster.ai.owner = monster # tell component who owns it
	message('The eys of ' + monster.name + ' look vacant,'
			' as they start to stumble around!', libtcod.light_green)
			
def cast_fireball():
	# cast fireball spell onto a target
	message('Left-click a target or right-click to cancel!', libtcod.light_cyan)
	(x, y) = target_tile()
	if x is None:
		return 'cancelled'
		
	message('The fireball explodes burning everything within ' 
			+ str(CONSTANTS.FIREBALL_RADIUS) + ' tiles!', libtcod.orange)
	for object in objects: # damage all monsters and player in range
		if object.distance(x, y) <= CONSTANTS.FIREBALL_RADIUS and object.fighter:
			message(object.name + ' is caught in the explosion taking ' 
					+ str(CONSTANTS.FIREBALL_DAMAGE) + ' hitpoints.', libtcod.orange)
			object.fighter.take_damage(CONSTANTS.FIREBALL_DAMAGE)

def player_death(player):
	# Modify game state in the event the player dies.
	global game_state
	message('You died!', libtcod.red)
	message('Press ESC for main menu', libtcod.red)
	game_state = 'dead'

	# turn player into a corpse.
	player.char = '%'
	player.color = libtcod.dark_red

def monster_death(monster):
	# Turn monster into corpse and remove their functionality.
	# can't block, attack, move, or be attacked.
	message(monster.name.capitalize() + ' is dead! You gain ' 
			+ str(monster.fighter.exp) + ' experience points.', libtcod.orange)
	monster.char = '%'
	monster.color = libtcod.dark_red
	monster.blocks = False	
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.send_to_front()
	# drop monster associated loot, then set fighter to none
	if monster.fighter and monster.fighter.type:
		loot_drop(monster)
	monster.fighter = None

def loot_drop(monster):
	# drop loot based on a pool of items tied to a monster/NPC
	
	# List of objects that can be dropped, corresponding to the type argument
	type = monster.fighter.type
	loot_chances = CONSTANTS.MONSTER_LOOT_POOL[type]
	choice = random_choice(loot_chances)
	
	item = None
	if type == CONSTANTS.ORC:	
		if choice == CONSTANTS.ORA:
			equip_component = Equipment(slot='main hand',
										power_bonus=3, stamina_usage=3)
			item = Object(monster.x, monster.y, CONSTANTS.ORA, 'R',
						  libtcod.light_green, equipment=equip_component)		
		elif choice == CONSTANTS.RATIONS:
			item_component = Item(use_function=cast_heal)
			item = Object(monster.x, monster.y, CONSTANTS.RATIONS, 'x', libtcod.white,
						  item=item_component, always_visible=True)
		elif choice == CONSTANTS.GOLD:
			message('5 gold was dropped by the orc', libtcod.gold)
	elif type == CONSTANTS.TROLL:
		if choice == CONSTANTS.CLUB:
			equip_component = Equipment(slot='main hand', power_bonus=5,
										stamina_usage=5)
			item = Object(monster.x, monster.y, CONSTANTS.CLUB, 'P',
						  libtcod.brown, equipment=equip_component)
		elif choice == CONSTANTS.GOLD:
			message('8 gold was dropped by the troll', libtcod.gold)
	if item:
		objects.append(item)
		item.send_to_front() # item appear below other objects.
			
def target_tile(max_range=None):
	# return position of tile that player left clicks within fov 
	# (optionally in a range), or (None, None) if right-clicked
	global key, mouse
	while True:
		# render the screen. This erases the inventory and shows the name 
		# of the objects under the mouse. Called from inventory menu
		libtcod.console_flush()
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,
									key, mouse)
		render_all()
		
		(x, y) = (mouse.cx, mouse.cy)
		
		# check for a left-click and within player fov, and 
		# that the max range isn't set or less than given max range
		if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and
			(max_range is None or player.distance(x, y) <= max_range)):
			return (x, y)
			
		if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
			return (None, None) # cancel if they right click or hit escape

def target_monster(max_range=None):
	# returns selected monster within player's fov, and None otherwise
	while True:
		(x, y) = target_tile(max_range)
		if x is None: # player cancelled
			return None
			
		# return first clicked monster, otherwise continue looping
		for obj in objects:
			if obj.x == x and obj.y == y and obj.fighter and obj != player:
				return obj

def closest_monster(max_range):
	# find the closest monster to the player within the max_range and player fov
	closest_enemy = None
	closest_dist = max_range + 1 # start with slightly more range

	for object in objects:
		if (object.fighter and not object == player and 
			libtcod.map_is_in_fov(fov_map, object.x, object.y)):
		# calculate new closest distance from object
			dist = player.distance_to(object)
			if dist < closest_dist:
				closest_dist = dist
				closest_enemy = object

	return closest_enemy

def get_names_under_mouse():
	global mouse
	
	# return a string with name of object under the mouse.
	(x, y) = (mouse.cx, mouse.cy)
	# create list with names of all objects at mouse coordinates and player FOV.
	names = [obj.name for obj in objects
		 if obj.x == x and obj.y == y 
					   and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]
	names = ', '.join(names) # join names separated by commas
	return names.capitalize()

def player_move_or_attack(dx, dy):
	# compute player's new position after movement or handle player's attack.
	global fov_recompute
	
	# coordinates player moves to
	x = player.x + dx
	y = player.y + dy
	
	# examine if there is an attackable object
	target = None
	for object in objects:
		if object.fighter and object.x == x and object.y == y:
			target = object
			break
			
	# attack if a target is found, move otherwise
	if target is not None:
		player.fighter.attack(target)
	else:
		player.move(dx, dy)
		fov_recompute = True
		
def get_all_equiped(obj):
	# return everything equiped to object
	if obj == player:
		equiped_list = []
		for item in inventory:
			if item.equipment and item.equipment.is_equiped:
				equiped_list.append(item.equipment)
		return equiped_list
	else:
		return [] # other objects by default do not have equipment

def check_level_up():
	# check if player has enough exp to level up
	level_up_exp = (CONSTANTS.LEVEL_UP_BASE 
				   + (player.level * CONSTANTS.LEVEL_UP_FACTOR))
	if player.fighter.exp >= level_up_exp:
		# level up y'all!
		player.level += 1
		player.fighter.exp -= level_up_exp
		message('Your battle skills grow stronger! You reached level ' 
				+ str(player.level) + '!', libtcod.yellow)
		# increase hp, def, or power
		choice = None
		while choice is None:
			choice = menu('Choose which stat to raise:\n',
						  ['Constitution (+20 HP, from ' + str(player.fighter.max_hp) + '->' + str(player.fighter.max_hp + 20) + ')',
						  'Strength (+1 Attack, from ' + str(player.fighter.power) + '->' + str(player.fighter.power + 1) + ')',
						  'Defense (+1 Defense, from ' + str(player.fighter.defense) + '->' + str(player.fighter.defense + 1) + ')'], 
						  CONSTANTS.LEVEL_SCREEN_WIDTH, 'Level up!')
			if choice == 0:
				player.fighter.base_max_hp += 20
				player.fighter.hp = player.fighter.max_hp
			elif choice == 1:
				player.fighter.base_power += 1
				player.fighter.hp = player.fighter.max_hp
			elif choice == 2:
				player.fighter.base_defense += 1
				player.fighter.hp = player.fighter.max_hp
	
def handle_keys():
	# Handle key presses inputted by player.
	global key, stairs
	#key = libtcod.console_check_for_keypress()  #real-time
	#key = libtcod.console_wait_for_keypress(True) # turn-based

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		# Left-Alt and Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return 'exit' # exit game


	if game_state == 'playing':
		# movement keys
		if key.vk == libtcod.KEY_UP:
			player_move_or_attack(0, -1)
		elif key.vk == libtcod.KEY_DOWN:
			player_move_or_attack(0, 1)
		elif key.vk == libtcod.KEY_LEFT:
			player_move_or_attack(-1, 0)
		elif key.vk == libtcod.KEY_RIGHT:
			player_move_or_attack(1, 0)
		elif chr(key.c) == 'p':
			# regenerate 1 stamina while waiting
			if player.fighter.stamina != player.fighter.max_stamina:
				player.fighter.stamina += 1
			pass # do nothing, i.e. waste a turn

		else:
			# test for other key presses.
			key_chr = chr(key.c)

			if key_chr == 'g': # pick up an item
				for object in objects:
					if (object.x == player.x and object.y == player.y 
						and object.item):
						object.item.pick_up()
						break
			if key_chr == 'i': # open inventory menu
				chosen_item = inventory_menu('Press the key next '
											 'to the item to use it, '
											 'or any other to cancel.\n')
				if chosen_item is not None:
					chosen_item.use()
			if key_chr == 'd': # drop an item in the inventory
				chosen_item = inventory_menu('Press the key next '
											 'to the item to drop, '
											 'or any other to cancel.\n')
				if chosen_item is not None:
					chosen_item.drop()
			if key.vk == libtcod.KEY_ENTER: # go down stairs
				if stairs.x == player.x and stairs.y == player.y:
					next_level()
			if key_chr == 'c': # check character information
				level_up_exp = (CONSTANTS.LEVEL_UP_BASE 
								+ player.level * CONSTANTS.LEVEL_UP_FACTOR)
				msgbox('Stats\n\nLevel ' + str(player.level) + '\nExperience: '
					   + str(player.fighter.exp) + '\nExperience to level up: '
					   + str(level_up_exp) + '\n\nMaximum HP: ' 
					   + str(player.fighter.max_hp) + '\nAttack: ' 
					   + str(player.fighter.power) + '\nDefense: ' 
					   + str(player.fighter.defense),
					   CONSTANTS.CHARACTER_SCREEN_WIDTH)
			if key_chr == '/': # player controls
				text = ('Controls - Any key to cancel\n\nInventory: i'
						'\nDrop item: d\nPick up/loot: g\nCharacter stats: c\n'
						'Wait: p\nMovement: arrow keys\n')
				menu(text, [], CONSTANTS.CHARACTER_SCREEN_WIDTH)

			return 'didn\'t-take-turn'

def render_all():
	# renders player's fov, draw objects, draw panel...
	global fov_map, fov_recompute
	global noise, fov_torchx, fov_noise

	# Change in noise
	dx = 0.0
	dy = 0.0
	di = 0.0
	fov_px = player.x
	fov_py = player.y

	if fov_recompute:
		# recompute fov if needed.
		fov_recompute = False
		libtcod.map_compute_fov(fov_map, player.x, player.y, 
								CONSTANTS.TORCH_RADIUS, 
								CONSTANTS.FOV_LIGHT_WALLS, CONSTANTS.FOV_ALGO)

	# slightly change the perlin noise parameter
	fov_torchx += 0.2
	# randomize the light position between -1.5 and 1.5
	tdx = [fov_torchx + 20.0]
	dx = libtcod.noise_get(noise, tdx, libtcod.NOISE_SIMPLEX) * 1.5
	tdx[0] += 30.0
	dy = libtcod.noise_get(noise, tdx, libtcod.NOISE_SIMPLEX) * 1.5
	di = 0.2 * libtcod.noise_get(noise, [fov_torchx], libtcod.NOISE_SIMPLEX)

	# go through all tiles, and set their background color according to FOV.
	# add torch effect in player's fov
	for y in range(CONSTANTS.MAP_HEIGHT):
		for x in range(CONSTANTS.MAP_WIDTH):
			visible = libtcod.map_is_in_fov(fov_map, x, y)
			wall = map[x][y].block_sight
			if not visible:
				# player can only see if not explored.
				if map[x][y].explored:
				# out of player's fov
					if wall:
						libtcod.console_put_char_ex(con, x, y, '#',
							libtcod.lighter_sepia, CONSTANTS.color_dark_wall)
					else:
						libtcod.console_put_char_ex(con, x, y, '-',
							libtcod.lighter_sepia, CONSTANTS.color_dark_ground)
			else:
				# in player's FOV
				if wall:
					base = CONSTANTS.color_dark_wall
					light = CONSTANTS.color_light_wall
					char = '#'
				else:
					base = CONSTANTS.color_dark_ground
					light = CONSTANTS.color_light_ground
					char = '-'

				r = float(x - fov_px + dx) * (x - fov_px + dx) + \
					(y - fov_py + dy) * (y - fov_py + dy)
				if r < CONSTANTS.SQUARED_TORCH_RADIUS:
					# Calculate coefficient for interpolation
					l = (CONSTANTS.SQUARED_TORCH_RADIUS - r) / \
						CONSTANTS.SQUARED_TORCH_RADIUS \
						+ di
					if l < 0.0:
						l = 0.0
					elif l > 1.0:
						l = 1.0
					# Interpolate between a dark and lit (wall or ground) color
					base = libtcod.color_lerp(base, light, l)
					libtcod.console_put_char_ex(con, x, y, char,
								libtcod.lightest_grey, base)
				# since it's visible, set explored to true.
				map[x][y].explored = True
	# draw player last to ensure corpes are not drawn over player.
	for object in objects:
		if object != player:
			object.draw()
	player.draw()

	# Blitting to the console we created,
	# draws everything we put onto the destination console.
	libtcod.console_blit(con, 0, 0, CONSTANTS.SCREEN_WIDTH, 
						 CONSTANTS.SCREEN_HEIGHT, 0, 0, 0)
	
	# prepare to render GUI panel.
	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)
	
	# print game feed, one message at a time.	
	y = 1
	for (line, color) in game_msgs:
		libtcod.console_set_default_foreground(panel, color)
		libtcod.console_print_ex(panel, CONSTANTS.MSG_X, y,
								 libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1	

	# show player stats
	render_bar(1, 1, CONSTANTS.BAR_WIDTH, 'HP', player.fighter.hp,
			   player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
	render_bar(1, 2, CONSTANTS.BAR_WIDTH, 'Stamina', player.fighter.stamina,
			   player.fighter.max_stamina, libtcod.dark_green,
			   libtcod.darkest_green)
			   
	# display current dungeon level to player
	libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
							'Dungeon Level ' + str(dungeon_level))

	# Player controls
	if dungeon_level == 1:
		text = 'Press / for controls'
		libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
							text)

	# display names of objects under the mouse.
	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE,
							 libtcod.LEFT, get_names_under_mouse())
	
	# blit contents of 'panel' to root console
	libtcod.console_blit(panel, 0, 0, CONSTANTS.SCREEN_WIDTH, 
						 CONSTANTS.PANEL_HEIGHT, 0, 0, CONSTANTS.PANEL_Y)

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
	# render bar (HP, exp, etc...) Calculate width of bar.
	bar_width = int(float(value) / maximum * total_width)

	# render the background first
	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width,
						 1, False, libtcod.BKGND_SCREEN)

	# render bar on top
	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width,
							 1, False, libtcod.BKGND_SCREEN)

	# text with values to clarify the bar
	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE,
							 libtcod.CENTER,
							 name + ': ' + str(value) + '/' + str(maximum))

def message(new_msg, color=libtcod.white):
	# Append messages to game feed while removing old ones if buffer is full.

	# split message among multiple lines if needed.
	new_msg_lines = textwrap.wrap(new_msg, CONSTANTS.MSG_WIDTH)

	for line in new_msg_lines:
		# if the buffer is full, remove 1st line to make room for new one.
		if len(game_msgs) == CONSTANTS.MSG_HEIGHT:
			del game_msgs[0]

		# add the new line as a tuple, with text and color.
		game_msgs.append( (line, color) )

def msgbox(text, width=50):
	menu(text, [], width) # use menu() as a sort of 'message box'

def menu(header, options, width):
	global key, mouse
	# currently limited to 26 options because we allow at most chars A-Z
	if len(options) > 26:
		raise ValueError('Cannot have a menu with more than 26 options.')

	# calculate total height for the header (after auto wrap) and 1 line/option
	header_height = libtcod.console_get_height_rect(con, 0, 0, width,
													CONSTANTS.SCREEN_HEIGHT,
													header)
	if header == '':
		header_height = 0
	height = len(options) + header_height

	# create an off-screen console that represents the menu's window
	window = libtcod.console_new(width, height)

	# print the header, with auto-wrap
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height,
								  libtcod.BKGND_NONE, libtcod.LEFT, header)

	# print all the options
	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ')' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE,
								 libtcod.LEFT, text)
		y += 1
		letter_index += 1

	# blit the contents of 'window' to the root console
	x = CONSTANTS.SCREEN_WIDTH/2 - width/2
	y = CONSTANTS.SCREEN_HEIGHT/2 - height/2
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

	# present the root console to the player and wait for a key press
	libtcod.console_flush()
	key = libtcod.console_wait_for_keypress(True)

	if key.vk == libtcod.KEY_ENTER and key.lalt: # toggle fullscreen keys
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	# convert ASCII code to an index, if it corresponds to an option return it
	index = key.c - ord('a')
	if index >= 0 and index < len(options):
		return index

	return None

def inventory_menu(header):
	# show a menu with each item of the inventory as an option
	if len(inventory) == 0:
		options = ['Inventory is empty']
	else:
		options = []
		for item in inventory:
			text = item.name
			# show additional info about equipment
			if item.equipment and item.equipment.is_equiped:
				text += ' (on ' + item.equipment.slot + ')'
			options.append(text)

	index = menu(header, options, CONSTANTS.INVENTORY_WIDTH)

	# if an item was chosen, return it
	if index is None or len(inventory) == 0:
		return None

	return inventory[index].item

def main_menu():
	# main menu of game
	img = libtcod.image_load('menu_background.png')
	
	while not libtcod.console_is_window_closed():		
		# show the background image, at twice the regular console resolution
		libtcod.image_blit_2x(img, 0, 0, 0)
		
		# title of game and author
		libtcod.console_set_default_foreground(0, libtcod.light_yellow)
		libtcod.console_print_ex(0, CONSTANTS.SCREEN_WIDTH/2,
								 CONSTANTS.SCREEN_HEIGHT/2-4,
								 libtcod.BKGND_NONE, libtcod.CENTER, 
								 'TOMBS OF THE ANCIENT KINGS')
		libtcod.console_print_ex(0, CONSTANTS.SCREEN_WIDTH/2,
								 CONSTANTS.SCREEN_HEIGHT-2,
								 libtcod.BKGND_NONE, libtcod.CENTER, 
								 'By David')
		
		# show options and wait for the player's choice	
		choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)
		
		if choice == 0: # new game
			new_game()
			play_game()
		elif choice == 1: # load game
			try:
				load_game()
			except:
				msgbox('\n No saved game to load.\n', 24)
				continue
			play_game()
		elif choice == 2: # quit
			break
			
def new_game():
	# pieces needed to start a new game
	global player, inventory, game_msgs, game_state, dungeon_level
	
	# initialize player object
	fighter_component = Fighter(hp=100, defense=1, power=2, stamina=30, exp=0,
								death_function=player_death)
	player = Object(0, 0, 'David', '@', libtcod.white, 
					blocks=True, fighter=fighter_component)
	player.level = 1
	
	# initialize our map
	dungeon_level = 1
	make_map()
	initialize_fov()
	
	# keep track of player state
	game_state = 'playing'
	
	# player inventory, list of objects
	inventory = []
	
	# Message log - composed of message and message color
	game_msgs = []
	
	# test message, welcoming player to dungeon.
	message('Welcome stranger! Prepare to perish in the Tombs '
			'of the Ancient King.', libtcod.yellow)
			
	# starting equipment for player
	equip_component = Equipment(slot='main hand', power_bonus=2,
								stamina_usage=2)
	dagger = Object(0, 0, 'dagger', '-',
					libtcod.sky, equipment=equip_component)
	inventory.append(dagger)
	equip_component.equip()
	dagger.always_visible = True
			
def load_game():
	# load shelved game
	global map, objects, inventory, player, game_msgs, game_state
	global stairs, dungeon_level
	
	file = shelve.open('savegame.sav', 'r')
	map = file['map']
	objects = file['objects']
	inventory = file['inventory']
	player = objects[file['player_index']]
	game_msgs = file['game_msgs']
	game_state = file['game_state']
	dungeon_level = file['dungeon_level']
	stairs = objects[file['stairs_index']]
	file.close()
	
	initialize_fov()
	
def save_game():
	# save current state of game
	# shelves make use of Python's dictionary. 
	# Basically a key valeu pair from PHP
	# open an empty shelf (possible overwriting an old one) to write game data
	file = shelve.open('savegame.sav', 'n')
	file['map'] = map
	file['objects'] = objects
	file['player_index'] = objects.index(player)
	file['inventory'] = inventory
	file['game_msgs'] = game_msgs
	file['game_state'] = game_state
	file['dungeon_level'] = dungeon_level
	file['stairs_index'] = objects.index(stairs)
	file.close()
			
def initialize_fov():
	# create fov map
	global fov_map, fov_recompute, fov_noise, noise
	
	# clear the console to prevent old games from leaving behind the map
	libtcod.console_clear(con)
	
	# On player movement or tile change, recompute fov.
	fov_recompute = True
	
	# field of view map
	fov_map = libtcod.map_new(CONSTANTS.MAP_WIDTH, CONSTANTS.MAP_HEIGHT)
	for y in range(CONSTANTS.MAP_HEIGHT):
		for x in range(CONSTANTS.MAP_WIDTH):
			libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, 
									   not map[x][y].blocked)
	noise = libtcod.noise_new(2)
	fov_noise = libtcod.noise_new(1, 1.0, 1.0)

def play_game():
	global key, mouse, fov_torchx
	
	player_action = None
	
	fov_torchx = 0.0

	# mouse and keyboard information
	mouse = libtcod.Mouse()
	key = libtcod.Key()
	
	# While the conosle is not closed, run game loop.
	while not libtcod.console_is_window_closed():
		# mouse and key event handling.
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, 
									key, mouse)
		
		# render screen
		render_all()
		
		# Flush our changes to the console.
		libtcod.console_flush()
		
		# check if player has leveled up
		check_level_up()
		
		# Clear objects in list.
		for object in objects:
			object.clear()

		# Handle keys and exit game if needed.	
		player_action = handle_keys()
		if player_action == 'exit':
			save_game()
			break

		# Allow monster to take turn.
		if game_state == 'playing' and player_action != 'didn\'t-take-turn':
			for object in objects:
				if object.ai:
					object.ai.take_turn()

# set up console
libtcod.console_set_custom_font('fonts/consolas12x12_gs_tc.png',
								libtcod.FONT_TYPE_GREYSCALE 
								| libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(CONSTANTS.SCREEN_WIDTH, CONSTANTS.SCREEN_HEIGHT, 
						  'python/libtcod tutorial', False)
libtcod.sys_set_fps(CONSTANTS.LIMIT_FPS)
con = libtcod.console_new(CONSTANTS.MAP_WIDTH, CONSTANTS.MAP_HEIGHT)
panel = libtcod.console_new(CONSTANTS.SCREEN_WIDTH, CONSTANTS.PANEL_HEIGHT)

# start this bad boy
main_menu()