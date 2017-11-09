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