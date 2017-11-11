# Weapon and Armor class definitions

class Weapon:
	# Weapons are subsets to equipment so that we can define attack ratings
	def __init__(self, phys_atk, fire_atk, lightning_atk, magic_atk, poise_atk,
				 weapon_type):
		self.phys_atk = phys_atk
		self.fire_atk = fire_atk
		self.lightning_atk = lightning_atk
		self.magic_atk = magic_atk
		self.poise_atk = poise_atk
		self.weapon_type = weapon_type


class Armor:
	# Armor is a subset to equipment so that we can define defensive ratings
	def __init__(self, phys_def, fire_def, lightning_def, magic_def,
				 poise_def, str_bonus, dex_bonus, int_bonus):
		self.phys_def = phys_def
		self.fire_def = fire_def
		self.lightning_def = lightning_def
		self.magic_def = magic_def
		self.poise_def = poise_def
		self.str_bonus = str_bonus
		self.dex_bonus = dex_bonus
		self.int_bonus = int_bonus