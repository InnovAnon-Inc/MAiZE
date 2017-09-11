from Model.Item.item import Item

from Model.Direction.CardinalDirection.YDirection.north import NORTH
from Model.Direction.CardinalDirection.YDirection.south import SOUTH
from Model.Direction.CardinalDirection.XDirection.east  import EAST
from Model.Direction.CardinalDirection.XDirection.west  import WEST

class Door (Item):
	def __init__ (self, pt, HP, MP, cd):
		Item.__init__ (self, pt, HP, MP)
		self.cd = cd
	def isTraversable (self):
		if self.door.state is CLOSED: return False
		if self.door.state is OPEN:   return True
		raise Exception (self.door.state)
	def __str__ (self):
		if self.door.state is CLOSED: return '+'
		assert self.door.state is OPEN
		if self.cd is NORTH: return '|'
		if self.cd is SOUTH: return '|'
		if self.cd is EAST:  return '-'
		if self.cd is WEST:  return '-'
		raise Exception (self.cd)
	# TODO __repr__