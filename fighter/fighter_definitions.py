import libtcodpy as libtcod
# Static definitions of fighters

# Static fighter definitions
	# 1.  component values
		# hp, stamina, souls, death_function, type, modifier,
		# phys_def, fire_def, lightning_def, magic_def,
		# phys_atk, fire_atk, lightning_atk, magic_atk,
		# str, dex, int
	# 2. Object class values
player =	   {
					'fighter_comp': [100, 40, 0, None, None, None,
					3, 1, 1, 1, # Defense
					1, 0, 0, 0, # Attack
					1, 1, 1], # Base stats
					'object': ['Player', '@', libtcod.white, True]}
hollow = 	   {
					'fighter_comp': [35, 1, 92, None, None, None,
					1, 0, 0, 0,
					4, 0, 0, 0,
					1, 1, 1],
					'object': ['Hollow', 'h', libtcod.light_fuchsia, True]}
undead_rat = 	{
					'fighter_comp': [15, 1, 60, None, None, None,
					0, 0, 0, 0,
					3, 0, 0, 0,
					1, 1, 1],
					'object': ['Rat', 'r', libtcod.dark_sepia, True]}
undead_soldier= {
					'fighter_comp': [50, 1, 146, None, None, None,
					4, 0, 0, 0,
					8, 0, 0, 0,
					1, 1, 1],
					'object': ['Undead Soldier', 's', libtcod.silver, True]}
black_knight_sword={
					'fighter_comp': [50, 1, 450, None, None, None,
					7, 3, 1, 1,
					10, 0, 0, 0,
					1, 1, 1],
					'object': ['Black Knight', 'B', libtcod.black, True]}
asylum_demon = 	   {
					'fighter_comp': [100, 1, 5000, None, None, None,
					6, 0, 0, 0,
					10, 0, 0, 0,
					1, 1, 1],
					'object': ['Asylum Demon', 'A', libtcod.darker_yellow, True]}