from Model.Direction.ZDirection.up   import UP
from Model.Direction.ZDirection.down import DOWN

from Model.Item.item import Item

class Stair (Item):
	def __init__ (self, pt, HP, MP, zd):
		Item.__init__ (self, pt, HP, MP)
		self.zd = zd
	def isTraversable (self): return True
	def __str__ (self):
		if self.zd is UP:   return '<'
		if self.zd is DOWN: return '>'
		raise Exception (self.zd)