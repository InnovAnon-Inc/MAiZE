from Controller.command import Command

from Model.Direction.direction \
import Direction

class Move (Command):
	def __init__ (self, d):
		assert issubclass (d, Direction)
		self.d = d
	def __str__ (self):
		return "%s, %s" % (Command.__str__ (self), self.d)