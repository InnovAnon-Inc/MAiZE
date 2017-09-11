from Model.Item.item import Item

class Wall (Item):
	def __init__ (self, pt, HP, MP):
		Item.__init__ (self, pt, HP, MP)
	def isTraversable (self): return False
	def __str__ (self): return '#'