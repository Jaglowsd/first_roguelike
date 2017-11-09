import libtcodpy as libtcod
# Static definitions of fighters

# Static fighter definitions
	# 1.  component values
		# hp, stamina, death_function, type, modifier, phys_def, fire_def, 
		# magic_def, lightning_def, phys_atk, fire_atk, lightning_atk,
		# magic_atk, str, dex, int
	# 2. Object class values
player =		   {
					'fighter_comp': [100, 30, 0, None, None, None, 3, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
					'object': ['Player', '@', libtcod.white, True]}
hollow = 		   {			
					'fighter_comp': [35, 1, 35, None, None, None, 1, 0, 0, 0, 4, 0, 0, 0, 1, 1, 1],
					'object': ['Hollow', 'h', libtcod.light_fuchsia, True]}
asylum_demon = 	   {
					'fighter_comp': [100, 1, 5000, None, None, None, 6, 0, 0, 0, 10, 0, 0, 0, 1, 1, 1],
					'object': ['Asylum Demon', 'A', libtcod.darker_yellow, True]}