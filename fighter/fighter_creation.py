# Fighter, monster, and NPC creation functions

import libtcodpy as libtcod
import CONSTANTS as constants
import fighter_definitions as f_defs

def from_dungeon_level(table):
	# returns value depending on dungeon level. The table specifies what
	# value occurs after each level, default is 0.
	for (value, min_level, max_level) in reversed(table):
		if dungeon_level >= min_level and dungeon_level <= max_level:
			return value
	return 0

def monster_chance():
	# dictionary of monsters and there chances of spawn
	monster_chances = {}
	monster_chances['undead_rat'] = from_dungeon_level([[60, 1, 1],
													 [40, 2, 2],
													 [25, 3, 4]])
	monster_chances['hollow'] = from_dungeon_level([[40, 1, 1],
													 [60, 2, 2],
													 [45, 3, 4],
													 [35, 5, 6]])
	monster_chances['undead_soldier'] = from_dungeon_level([[30, 3, 4],
													 [50, 5, 6]])
	monster_chances['black_knight_sword'] = from_dungeon_level([[15, 5, 6]])
	return monster_chances

def create_object(definition, x, y, f_component=None, a_component=None):
	# Returns the newly created object with all its components attached
	fighter_object = Object(x, y, definition[0], definition[1], definition[2],
							blocks=definition[3],fighter=f_component,
							ai=a_component)
	return fighter_object

def create_fighter(fighter_name, x, y, death_func=None):
	# create fighter and ai components
	definition = getattr(f_defs, fighter_name)
	if definition:
		# Fighter component
		fighter_component = None
		fighter = definition['fighter_comp']
		if fighter:
			fighter_component = Fighter(hp=fighter[0], stamina=fighter[1], souls=fighter[2], death_function=death_func, type=fighter[4], modifier=fighter[5],
										phys_def=fighter[6], fire_def=fighter[7], magic_def=fighter[8], lightning_def=fighter[9], phys_atk=fighter[10],
										fire_atk=fighter[11], lightning_atk=fighter[12], magic_atk=fighter[13], str=fighter[14], dex=fighter[15], int=fighter[16])
		# AI component
		ai_component = None
		if fighter_name != 'player':
			ai_component = BasicMonster()
		return create_object(definition['object'], x, y, f_component=fighter_component, a_component=ai_component)
	return None