from Model.point import Point
from Model.Direction.direction import Direction

class Item:
	def __init__ (self, pt, HP, MP, d):
		assert isinstance (pt, Point)
		assert isinstance (HP, int)
		assert isinstance (MP, int)
		assert issubclass (d, Direction)
		self.pt = pt
		self.HP = HP
		self.MP = MP
	def __str__ (self): return '?'
	def __repr__ (self):
		return "%c pt=%s, HP=%d, MP=%d, d=%s" % (
			str (self), self.pt, self.HP, self.MP)