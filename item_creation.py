# Consumable and equipment creation functions

import libtcodpy as libtcod
import CONSTANTS as constants
import item_definitions as i_defs
from weapon_armor_class import Weapon, Armor

def from_dungeon_level(table):
	# returns value depending on dungeon level. The table specifies what
	# value occurs after each level, default is 0.
	for (value, min_level, max_level) in reversed(table):
		if dungeon_level >= min_level and dungeon_level <= max_level:
			return value
	return 0

def item_chance():
	# dictionary of items and there chances of spawn
	item_chances = {}
	item_chances['lifegem'] = 25 # heal spawn is floor independent
	item_chances['confuse_spell'] = from_dungeon_level([[10, 2, constants.END_LEVEL]])
	item_chances['lightning_spell'] = from_dungeon_level([[25, 4, constants.END_LEVEL]])
	item_chances['fireball'] = from_dungeon_level([[25, 6, constants.END_LEVEL]])
	item_chances['straight_sword'] = from_dungeon_level([[2, 1, constants.END_LEVEL]])
	item_chances['dagger'] = from_dungeon_level([[2, 1, constants.END_LEVEL]])

	return item_chances

def create_object(definition, x, y, i_component=None, e_component=None):
	# Returns the newly created object with all its components attached
	item_object = Object(x, y, definition[0], definition[1], definition[2],
						equipment=e_component, item=i_component, always_visible=definition[4])
	return item_object

def create_consumable(item_name, x, y, cnt=1):
	# create consumable item component
	item = getattr(i_defs, item_name)
	if item:
		# Item component
		item_component = Item(use_function=None, count=cnt)
		return create_object(item, x, y, i_component=item_component)
	return None

def create_equipment(equip_name, x, y):
	# create equipment, weapon, and armor components
	definition = getattr(i_defs, equip_name)
	if definition:
		# Weapon component
		weapon_comp = None
		w_comp = definition['weapon_comp']
		if w_comp:
			weapon_comp = Weapon(phys_atk=w_comp[0], fire_atk=w_comp[1], lightning_atk=w_comp[2], magic_atk=w_comp[3], poise_atk=w_comp[4], weapon_type=w_comp[5])
		# Armor component
		armor_comp = None
		a_comp = definition['armor_comp']
		if a_comp:
			armor_comp = Armor(phys_def=a_comp[0], fire_def=a_comp[1], lightning_def=a_comp[2], magic_def=a_comp[3], poise_def=a_comp[4],
							   str_bonus=a_comp[5], dex_bonus=a_comp[6], int_bonus=a_comp[7], armor_slot=a_comp[8])
		# Equipment component
		equip_comp = definition['equip_component']
		equip_component = Equipment(slot=equip_comp[0], max_hp_bonus=equip_comp[1], max_stamina_bonus=equip_comp[2], stamina_usage=equip_comp[3],
									level=equip_comp[4], infusion=equip_comp[5], requirements=equip_comp[6], weapon=weapon_comp, armor=armor_comp)
		return create_object(definition['object'], x, y, e_component=equip_component)
	return None

