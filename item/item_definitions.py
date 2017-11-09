import libtcodpy as libtcod
# Static definitions of consumables and equipment

# Object class values
	# Name, character, color, always visible (Bool) on explored regions

# Static consumable item definitions
lifegem = 				['lifegem', '!', libtcod.light_yellow, '', True]
soul_of_a_lost_undead = ['Soul of a Lost Undead', 's', libtcod.lightest_magenta, '', True]
rations = 				['rations', 'q', libtcod.sepia, '', True]
lightning_spell = 		['Lighting spell', 'Z', libtcod.yellow, '', True]
fireball = 				['Fireball', 'F', libtcod.orange,'', True]
confuse_spell = 		['Confusion spell', 'C', libtcod.cyan, '', True]
estus_flask = 			['Estus Flask', 'u', libtcod.orange, '', True]

# Static equipment definitions
	# 1. Equipment component values
		# slot, max_hp_bonus, max_stamina_bonus, stamina_usage, level, infusion, requirements
	# 2. Weapon component values
		# phys_atk, fire_atk, lightning_atk, magic_atk, poise_atk, weapon type (i.e., straight sword, dagger, club, etc.)
	# 3. Armor component values
		# phys_def, fire_def, lightning_def, magic_def, poise_def, str_bonus, dex_bonus, int_bonus, armor slot (i.e., head, torso, etc.)
	# 4. Object class values
straight_sword =   {
					'equip_component': ['main hand', 0, 0, 3, 1, None, [3, 2, 1]],
					'weapon_comp': [8, 0, 0, 0, 0, 'straight sword'],
					'armor_comp': None,
					'object': ['Straight Sword', '/', libtcod.sky, '', True]}
dagger = 		   {			
					'equip_component': ['main hand', 0, 0, 2, 1, None, [1, 1, 1]],
					'weapon_comp': [4, 0, 0, 0, 0, 'dagger'],
					'armor_comp': None,
					'object': ['Dagger', '~', libtcod.azure, '', True]}
orcs_right_arm =   {
					'equip_component': ['main hand', 0, 0, 4, 1, None, [4, 1, 1]],
					'weapon_comp': [4, 0, 0, 0, 0, 'club'],
					'armor_comp': None,
					'object': ['Orc\'s Right Arm', 'P', libtcod.light_green, '', True]}
club = 			   {
					'equip_component': ['main hand', 0, 0, 6, 1, None, [10, 1, 1]],
					'weapon_comp': [12, 0, 0, 0, 0, 'club'],
					'armor_comp': None,
					'object': ['Club', 'P', libtcod.sepia, '', True]}
