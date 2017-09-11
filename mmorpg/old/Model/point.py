class Point:
	def __init__ (self, x, y):
		self.x = x
		self.y = y
	def __repr__ (self): return "(%d, %d)" % (self.x, self.y)
	def __str__  (self): return repr (self)
	def __eq__ (self, pt): return self.x is pt.x and self.y is pt.y