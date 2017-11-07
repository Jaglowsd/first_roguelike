# Fighter, monster, and NPC creation functions

import libtcodpy as libtcod
import CONSTANTS as constants
import fighter_definitions as f_defs

# def monster_chance():
	# dictionary of items and there chances of spawn
	# item_chances = {}
	# item_chances['lifegem'] = 25 # heal spawn is floor independent
	# item_chances['confuse_spell'] = from_dungeon_level([[10, 2, constants.END_LEVEL]])
	# item_chances['lightning_spell'] = from_dungeon_level([[25, 4, constants.END_LEVEL]])
	# item_chances['fireball'] = from_dungeon_level([[25, 6, constants.END_LEVEL]])
	# item_chances['straight_sword'] = from_dungeon_level([[2, 1, constants.END_LEVEL]])
	# item_chances['dagger'] = from_dungeon_level([[2, 1, constants.END_LEVEL]])

	# return item_chances

def create_object(definition, x, y, f_component=None, a_component=None):
	# Returns the newly created object with all its components attached
	fighter_object = Object(x, y, definition[0], definition[1], definition[2],
							blocks=definition[3],fighter=f_component,
							ai=a_component)
	return fighter_object

def create_fighter(fighter_name, x, y):
	# create fighter and ai components
	definition = getattr(f_defs, fighter_name)
	if definition:
		# Fighter component
		fighter_component = None
		fighter = definition['fighter_comp']
		if fighter:
			fighter_component = Fighter(hp=fighter[0], stamina=fighter[1], souls=fighter[2], death_function=fighter[3], type=fighter[4], modifier=fighter[5],
										phys_def=fighter[6], fire_def=fighter[7], magic_def=fighter[8], lightning_def=fighter[9], phys_atk=fighter[10],
										fire_atk=fighter[11], lightning_atk=fighter[12], magic_atk=fighter[13], str=fighter[14], dex=fighter[15], int=fighter[16])
		# AI component
		ai_component = None
		if fighter_name != 'player':
			ai_component = BasicMonster()
		return create_object(definition['object'], x, y, f_component=fighter_component, a_component=ai_component)
	return None