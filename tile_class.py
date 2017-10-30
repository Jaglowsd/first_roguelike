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