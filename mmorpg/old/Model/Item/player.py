from Model.Item.item import Item
from Model.point import Point

class Player (Item):
	def __init__ (self, pt, HP, MP, d, XP, isSelf):
		assert isinstance (XP, int)
		assert isinstance (isSelf, bool)
		Item.__init__ (self, pt, HP, MP, d)
		self.XP = XP
		self.isSelf = isSelf
		# TODO time until action completion
	def isTraversable (self): return False
	#def isAlive (self): return self.HP is not 0
	def __str__ (self):
		if self.isSelf: return '@'
		return '&'
	def __repr__ (self):
		return "%s, XP=%d" % (Item.__repr__ (self), self.XP)