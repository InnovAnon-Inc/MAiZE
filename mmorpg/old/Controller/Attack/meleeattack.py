from Controller.Attack.attack import Attack
from Controller.move import Move
from Model.Direction.CardinalDirection.cardinaldirection \
import CardinalDirection

class MeleeAttack (Attack, Move):
	def __init__ (self, d):
		assert issubclass (d, CardinalDirection)
		Move.__init__ (self, d)
	def __str__ (self):
		return "%s, %s" % (Move.__str__ (self), "melee")