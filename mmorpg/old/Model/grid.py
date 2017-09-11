from itertools import chain
from random import choice

from Model.cell  import Cell
from Model.point import Point

from Model.Item.item   import Item
from Model.Item.player import Player
from Model.Item.wall   import Wall

class Grid:
	def __init__ (self, width, height):
		self.width  = width
		self.height = height
		self.grid = [
			[Cell (Point (x, y)) for x in xrange (width)]
			for y in xrange (height)]
		#self.items = {}
		#for t in [Item, Wall, Player]:
		#	self.items[t] = []
	def getGrid (self):       return chain.from_iterable (self.grid)
	def getRow  (self, r):    return self.grid[r]
	def getCol  (self, c):    return [row[c] for row in self.grid]
	def getCell (self, r, c): return self.grid[r][c]
	def getCell (self, pt):   return self.grid[pt.y][pt.x]
	
	def setWallUp (self, pt):
		cell = self.grid[pt.y][pt.x]
		walls = filter (
			lambda item: isinstance (item, Wall),
			cell.items)
		if len (walls) is not 0: return
		cell.items.append (Wall (pt))
	def setWallDown (self, pt):
		cell = self.grid[y][x]
		cell.items = filter (
			lambda item: not isinstance (item, Wall),
			cell.items)

	def traverseRC (self, cb):
		return map (
			lambda y: map (
				lambda x: cb (x, y),
				xrange (self.width)),
			xrange (self.height))
	def traverseCR (self, cb):
		return map (
			lambda x: map (
				lambda y: cb (x, y),
				xrange (self.height)),
			xrange (self.width))
	def traversePerimeterRC (self, cb):
		return map (
			lambda y: map (
				lambda x: cb (x, y),
				[0, self.width - 1]),
			xrange (self.height))
	def traversePerimeterCR (self, cb):
		return map (
			lambda y: map (
				lambda x: cb (x, y),
				xrange (self.width)),
			[0, self.height - 1])
	
	def getPointsRC (self):
		return chain.from_iterable (self.traverseRC (Point))
	def getPointsCR (self):
		return chain.from_iterable (self.traverseCR (Point))
	def getPerimeterPointsRC (self):
		return chain.from_iterable (self.traversePerimeterRC (Point))
	def getPerimeterPointsCR (self):
		return chain.from_iterable (self.traversePerimeterCR (Point))
		
	def getCellsRC (self):
		return chain.from_iterable (self.traverseRC (
			lambda x, y: self.grid[y][x]))
	def getCellsCR (self):
		return chain.from_iterable (self.traverseCR (
			lambda x, y: self.grid[y][x]))
	def getPerimeterCellsRC (self):
		return chain.from_iterable (self.traversePerimeterRC (
			lambda x, y: self.grid[y][x]))
	def getPerimeterCellsCR (self):
		return chain.from_iterable (self.traversePerimeterCR (
			lambda x, y: self.grid[y][x]))



	def setWallsDownRC (self): map (setWallDown, self.traverseRC (Point))
	def setWallsDownCR (self): map (setWallDown, self.traverseCR (Point))
	def setPerimeterDownRC (self):
		map (setWallDown, self.traversePerimeterRC (Point))
	def setPerimeterDownCR (self):
		map (setWallDown, self.traversePerimeterCR (Point))

	def setWallsUpRC (self): map (setWallUp, self.traverseRC (Point))
	def setWallsUpCR (self): map (setWallUp, self.traverseCR (Point))
	def setPerimeterUpRC (self):
		map (setWallUp, self.traversePerimeterRC (Point))
	def setPerimeterUpCR (self):
		map (setWallUp, self.traversePerimeterCR (Point))
	
	def getTraversableCells (self):
		return filter (
			lambda cell: cell.isTraversable (),
			self.getCellsRC ())
	def getRandomTraversableCell (self):
		return choice (self.getTraversableCells ())
	def getTraversablePoints (self):
		return map (
			lambda cell: cell.pt,
			self.getTraversableCells ())
	def getRandomTraversablePoint0 (self):
		return choice (list (self.getTraversablePoints ()))
	def getRandomTraversablePoint1 (self):
		return self.getRandomTraversableCell ().pt
		
	"""
	def addPlayer (self, player):
		cell = self.getCell (player.pt)
		assert cell.isTraversable ()
		if not self.items.has_key (Player):
			players = []
			self.items[Player] = players
		else:
			players = self.items.get (Player)
		players.append (player)
		players.append (player)
	"""
	
	
	"""
	def getItemsOfType (self, T):
		return chain.from_iterable (map (
			lambda key: self.items.get (key),
			filter (lambda t: isinstance (t, T), self.items.keySet ())))
	"""	
			
			
			
	def toString (self, cb):
		lines = ""
		for y in xrange (self.height):
			line = ""
			for x in xrange (self.width):
				line += cb (self.grid[y][x])
			assert len (line)
			line += "\n"
			lines += line
		return lines
	def __repr__ (self): return self.toString (repr)
	def __str__  (self): return self.toString (str)
	
	def addPlayer (self, player):
		pt = player.pt
		cell = self.grid[pt.y][pt.x]
		cell.addPlayer (player)
	def removePlayer (self, player):
		pt = player.pt
		cell = self.grid[pt.y][pt.x]
		cell.removePlayer (player)
	def containsPoint (self, pt):
		if pt.x < 0:            return False
		if pt.x >= self.width:  return False
		if pt.y < 0:            return False
		if pt.y >= self.height: return False
		return True
	def containsPlayer (self, player):
		pt = player.pt
		cell = self.grid[pt.y][pt.x]
		return cell.containsPlayer (player)