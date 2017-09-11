from Model.Item.player import Player

from View.view import View

class HPView (View):
	def __init__ (self, player):
		assert isinstance (player, Player)
		self.player = player
	def __repr__ (self): return "HP: %s" % self.player.HP