from Model.Item.player import Player

from View.view import View

class XPView (View):
	def __init__ (self, player):
		assert isinstance (player, Player)
		self.player = player
	def __repr__ (self): return "XP: %s" % self.player.XP