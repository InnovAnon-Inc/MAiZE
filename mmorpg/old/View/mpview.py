from Model.Item.player import Player

from View.view import View

class MPView (View):
	def __init__ (self, player):
		assert isinstance (player, Player)
		self.player = player
	def __repr__ (self): return "MP: %s" % self.player.MP