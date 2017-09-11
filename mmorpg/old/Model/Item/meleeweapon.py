from Model.Item.item import Item

class MeleeWeapon (Item):
	def __init__ (self, pt, HP, MP):
		Item.__init__ (self, pt, HP, MP)
	def isTraversable (self): return True # ?
	def __str__ (self): return '/'