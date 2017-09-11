from itertools import chain

from Model.point import Point

from View.itempriorities import ItemPriorities

class Cell:
	def __init__ (self, pt):
		assert isinstance (pt, Point)
		self.pt = pt
		#self.neighbors = {}
		#self.items = {} # including walls and players
		self.players = []
		self.walls   = [] # seems like too many walls
		self.items   = []
		# TODO add floor and ceiling, so you can break through it
	#def setNeighbor (self, direction, cell):
	#	self.neighbors[direction] = cell
	def isTraversable (self):
		if len (filter (
			lambda (item): not item.isTraversable (),
			chain (self.players, self.walls, self.items))) is 0:
			return True
		return False
	"""
	def getItemsOfType (self, T):
		return chain.from_iterable (map (
			lambda (key): self.items.get (key),
			filter (lambda (t): isinstance (t, T), self.items.keySet ())))
	def getItems (self): return chain.from_iterable (self.items.values ())
	"""
	
	def __repr__ (self):
		if len (self.itemViews) is 0: return '.'
		return repr (self.items.values ())
	def __str__ (self):
		#if len (self.items) is 0: return '.'
		#for priority in [Wall] + itemPriorities + [Item]:
		#	items = filter (
		#		lambda (item): isinstance (item, priority),
		#		self.items)
		#	if len (items) is 0: continue
		#	return str (items[0]) # some are not displayed
		#raise Exception (self.items)
		
		c = chain (self.players, self.walls, self.items)
		return str (next (c, '.'))
		
	def addPlayer (self, player):
		assert self.isTraversable ()
		assert self.pt == player.pt
		self.players.append (player)
	def removePlayer (self, player):
		assert self.pt == player.pt
		assert player in self.players
		self.players.remove (player)
	def containsPlayer (self, player):
		assert self.pt == player.pt
		return player in self.players