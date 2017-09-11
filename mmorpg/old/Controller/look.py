from Controller.command import Command

from Model.Direction.CardinalDirection.cardinaldirection \
import CardinalDirection

class Look (Command):
	def __init__ (self, d):
		assert issubclass (d, CardinalDirection)
		self.d = d
	def __str__ (self):
		return "%s, %s" % (Command.__str__ (self), self.d)