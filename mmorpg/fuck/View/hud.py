from Model.Item.player import Player

from View.view import View
from View.hpview import HPView
from View.mpview import MPView
from View.xpview import XPView

class HUD (View):
	def __init__ (self, player):
		assert isinstance (player, Player)
		self.HPView = HPView (player)
		self.MPView = MPView (player)
		self.XPView = XPView (player)
	def __repr__ (self):
		return repr (self.HPView) + "\n" + \
		        repr (self.MPView) + "\n" + \
		        repr (self.XPView) + "\n"