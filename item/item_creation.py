# Consumable and equipment creation functions

import libtcodpy as libtcod
import item_definitions as i_defs
from classes import weapon_armor

def from_dungeon_level(table):
	# returns value depending on dungeon level. The table specifies what
	# value occurs after each level, default is 0.
	for (value, min_level, max_level) in reversed(table):
		if dungeon_level >= min_level and dungeon_level <= max_level:
			return value
	return 0

def item_consumable_chance():
	# dictionary of consumables and there chances of spawn
	cons_chances = {}
	cons_chances['lifegem'] = from_dungeon_level([[30, 1, 3], [40, 4, 6]])
	cons_chances['confuse_spell'] = from_dungeon_level([[10, 2, 3], [20, 4, 5]])
	cons_chances['lightning_spell'] = from_dungeon_level([[10, 3, 5], [15, 5, 6]])
	cons_chances['fireball'] = from_dungeon_level([[5, 4, 6]])
	cons_chances['soul_of_a_lost_undead'] = from_dungeon_level([[20, 1, 3],
																[30, 4, 6]])

	return cons_chances

def item_equipment_chance():
	# dictionary of equipment and there chances of spawn
	equip_chances = {}
	equip_chances['nothing'] = from_dungeon_level([[50, 1, 6]])
	equip_chances['straight_sword'] = from_dungeon_level([[25, 1, 6]])
	equip_chances['dagger'] = from_dungeon_level([[25, 1, 6]])

	return equip_chances

def create_object(definition, x, y, i_component=None, e_component=None):
	# Returns the newly created object with all its components attached
	item_object = Object(x, y, definition[0], definition[1], definition[2],
						equipment=e_component, item=i_component, always_visible=definition[4])
	return item_object

def create_consumable(item_name, x, y, use_func=None, cnt=1):
	# create consumable item component
	item = getattr(i_defs, item_name)
	if item:
		# Item component
		item_component = Item(use_function=use_func, count=cnt)
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
			weapon_comp = weapon_armor.Weapon(phys_atk=w_comp[0], fire_atk=w_comp[1], lightning_atk=w_comp[2], magic_atk=w_comp[3], poise_atk=w_comp[4], weapon_type=w_comp[5])
		# Armor component
		armor_comp = None
		a_comp = definition['armor_comp']
		if a_comp:
			armor_comp = weapon_armor.Armor(phys_def=a_comp[0], fire_def=a_comp[1], lightning_def=a_comp[2], magic_def=a_comp[3], poise_def=a_comp[4],
							   str_bonus=a_comp[5], dex_bonus=a_comp[6], int_bonus=a_comp[7], armor_slot=a_comp[8])
		# Equipment component
		equip_comp = definition['equip_component']
		equip_component = Equipment(slot=equip_comp[0], max_hp_bonus=equip_comp[1], max_stamina_bonus=equip_comp[2], stamina_usage=equip_comp[3],
									level=equip_comp[4], infusion=equip_comp[5], requirements=equip_comp[6], weapon=weapon_comp, armor=armor_comp)
		return create_object(definition['object'], x, y, e_component=equip_component)
	return None

