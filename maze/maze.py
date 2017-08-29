from random import randint, choice, shuffle, getrandbits
from itertools import product, chain

class Maze:
	@staticmethod
	def getNeighbors (current):
		x, y = current
		north = x, y - 2
		west = x - 2, y
		east = x + 2, y
		south = x, y + 2
		return [north, east, south, west]
	def __init__ (self, nrow=10, ncol=20):
		#self.matrix = [[1] * ncol] * nrow
		#self.matrix = [[]] * nrow
		#for row in xrange (nrow):
		#	self.matrix[row] = [1] * ncol
		self.nrow, self.ncol = nrow, ncol
		self.matrix = map (lambda r: [1] * ncol, xrange (nrow))
	def setAll (self, up=1):
		#for x, y in product (xrange (self.ncol), xrange (self.nrow)):
		for y in xrange (self.nrow):
			for x in xrange (self.ncol):
				#if not self.matrix[y][x]:
				self.matrix[y][x] = up
	def setWalls (self, up=1):
		for x, y in self.getWallPositions ():
			#if not self.matrix[y][x]:
			self.matrix[y][x] = up
	def setNonWalls (self, up=0):
		for x, y in self.getNonWallPositions ():
			#if self.matrix is 1:
			self.matrix[y][x] = up
	def isValidPosition (self, current):
		nrow, ncol = self.nrow, self.ncol
		x, y = current
		if x < 0:     return False
		if x >= ncol: return False
		if y < 0:     return False
		if y >= nrow: return False
		return True
	def getValidNeighbors (self, current):
		nrow, ncol = self.nrow, self.ncol
		return filter (
			lambda n: self.isValidPosition (n),
			Maze.getNeighbors (current))
	def isTraversablePosition (self, current):
		x, y = current
		return not self.matrix[y][x]
	def getUnvisitedNeighbors (self, current, unvisited):
		return filter (
			lambda n: n in unvisited,
			self.getValidNeighbors (current))
	def removeWall (self, a, b):
		assert b in Maze.getNeighbors (a)
		assert a in Maze.getNeighbors (b)
		ax, ay = a
		bx, by = b
		wallx = (ax + bx) / 2
		wally = (ay + by) / 2
		assert wallx * 2 is ax + bx
		assert wally * 2 is ay + by
		assert self.matrix[wally][wallx] is 1
		self.matrix[wally][wallx] = 0
	#def getRandomPosition (self):
	#	return randint (0, self.ncol - 1), randint (0, self.nrow - 1)
	def getRandomWallPosition (self):
		return randint (0, (self.ncol - 1) / 2) * 2 + 0, \
		        randint (0, (self.nrow - 1) / 2) * 2 + 0
	def getRandomNonWallPosition (self):
		return randint (0, (self.ncol - 1) / 2) * 2 + 1, \
		        randint (0, (self.nrow - 1) / 2) * 2 + 1
	def getWallPositions (self):
		return list (product (
			xrange (0, self.ncol, 2),
			xrange (0, self.nrow, 2)))
	def getDividingWallPositions (self):
		return list (chain (
				product (
					xrange (1, self.ncol, 2),
					xrange (0, self.nrow, 2)),
				product (
					xrange (0, self.ncol, 2),
					xrange (1, self.nrow, 2))))
	def getNonWallPositions (self):
		return list (product (
			xrange (1, self.ncol, 2),
			xrange (1, self.nrow, 2)))
	def getAllNonWallPositions (self):
		#return list (chain (
		#		product (
		#			xrange (1, self.ncol, 2),
		#			xrange (0, self.nrow, 2)),
		#		product (
		#			xrange (0, self.ncol, 2),
		#			xrange (1, self.nrow, 2))))
		return chain (
			self.getDividingWallPositions (),
			self.getNonWallPositions ())
	def getCellsDividedByWall (self, wall):
		x, y = wall
		ret = []
		if x % 2 is 0:
			ret.append ((x - 1, y))
			ret.append ((x + 1, y))
		if y % 2 is 0:
			ret.append ((x, y - 1))
			ret.append ((x, y + 1))
		return filter (self.isValidPosition, ret)
	def getWallsAdjacentToCell (self, cell):
		x, y = cell
		ret = []
		if x % 2 is 1:
			ret.append ((x - 1, y))
			ret.append ((x + 1, y))
		if y % 2 is 1:
			ret.append ((x, y - 1))
			ret.append ((x, y + 1))
		return filter (self.isValidPosition, ret)
	def recursiveBacktracker (self):
		self.setAll ()
		visited = []
		unvisited = self.getNonWallPositions ()
		current = self.getRandomNonWallPosition ()
		visited.append (current)

		while unvisited:
			#visited.append (current)
			if current in unvisited: unvisited.remove (current)
			x, y = current
			#assert self.matrix[y][x] is 1
			self.matrix[y][x] = 0
			
			unvisitedNeighbors = self.getUnvisitedNeighbors (current, unvisited)
			if unvisitedNeighbors:
				n = choice (unvisitedNeighbors)
				visited.append (current)
				self.removeWall (current, n)
				current = n
			else:
				#if unvisited: current = choice (unvisited)
				if visited: current = choice (visited)
	def randomizedKruskalsAlgorithm (self):
		self.setAll ()
		self.setNonWalls ()
		allWalls = self.getDividingWallPositions ()
		#print allWalls
		allCells = dict ()
		#for cell in self.getAllNonWallPositions ():
		for cell in self.getNonWallPositions ():
			allCells[cell] = set ([cell])
		shuffle (allWalls)
		for wall in allWalls:
			cells = self.getCellsDividedByWall (wall)
			assert len (cells) <= 2
			for cell in cells:
				assert len (cell)
			intersection = set.intersection (*map (lambda cell: allCells[cell], cells))
			if intersection: continue
			x, y = wall
			self.matrix[y][x] = 0
			union = set ().union (*map (lambda cell: allCells[cell], cells))
			for cell in cells:
				allCells[cell] = union
	def randomizedPrimsAlgorithm (self):
		self.setAll ()
		current = self.getRandomNonWallPosition ()
		x, y = current
		self.matrix[y][x] = 0
		walls = self.getWallsAdjacentToCell (current)
		while walls:
			wall = choice (walls)
			cells = self.getCellsDividedByWall (wall)
			f = filter (lambda (x, y): self.matrix[y][x], cells)
			if len (f) is 1:
				x, y = wall
				self.matrix[y][x] = 0
				x, y = f[0]
				self.matrix[y][x] = 0
				map (lambda c: walls.append (c), self.getWallsAdjacentToCell (f[0]))
			if wall in walls: walls.remove (wall)
	def setXWall (self, x, mn, mx):
		#print mn, mx
		for y in xrange (mn, mx):
			#print x, y
			self.matrix[y][x] = 1
	def setYWall (self, y, mn, mx):
		#print mn, mx
		for x in xrange (mn, mx):
			#print x, y
			self.matrix[y][x] = 1
	def verticalDivision (self, xmin, xmax, ymin, ymax, s=2):
		# -1? +1?
		x = xmin + randint (0, (xmax - xmin - 1) / 2) * 2 + 0
		#x = xmin + randint (0, xmax - xmin - 1)
		y = ymin + randint (0, (ymax - ymin - 1) / 2) * 2 + 1
		#y = ymin + randint (0, ymax - ymin - 1)
		#print x, y
		#print self
		self.setXWall (x, ymin, ymax)
		self.matrix[y][x] = 0
		#self.recursiveDivision (xmin, x - s, ymin, ymax)
		self.recursiveDivision (xmin, x, ymin, ymax)
		self.recursiveDivision (x + s, xmax, ymin, ymax)
		#self.recursiveDivision (x, xmax, ymin, ymax)
	def horizontalDivision (self, xmin, xmax, ymin, ymax, s=2):
		y = ymin + randint (0, (ymax - ymin - 1) / 2) * 2 + 0
		#y = ymin + randint (0, ymax - ymin - 1)
		x = xmin + randint (0, (xmax - xmin - 1) / 2) * 2 + 1
		#x = xmin + randint (0, xmax - xmin - 1)
		#print x, y
		self.setYWall (y, xmin, xmax)
		self.matrix[y][x] = 0
		#self.recursiveDivision (xmin, xmax, ymin, y - s)
		self.recursiveDivision (xmin, xmax, ymin, y)
		self.recursiveDivision (xmin, xmax, y + s, ymax)
		#self.recursiveDivision (xmin, xmax, y, ymax)
	def recursiveDivision (self, xmin=0, xmax=None, ymin=0, ymax=None):
		if xmax is None or ymax is None: self.setAll (0)
		if xmax is None: xmax = self.ncol
		if ymax is None: ymax = self.nrow
		if xmin >= xmax - 1: return
		if ymin >= ymax - 1: return
		#print xmin, xmax, ymin, ymax
		
		#if xmin >= xmax:
		#	if ymin >= ymax: return
		#	self.verticalDivision (xmax, xmax, ymin, ymax)
		#	return
		#if ymin >= ymax:
		#	if xmin >= xmax: return
		#	self.horizontalDivision (xmin, xmax, ymax, ymax)
		#	return
		
		# TODO getrandbits always returns the same value
		if getrandbits (1):
			self.verticalDivision (xmin, xmax, ymin, ymax)
		else:
			self.horizontalDivision (xmin, xmax, ymin, ymax)
			
	@staticmethod
	def cellRepr (cell):
		if not cell: return '.'
		if cell is 1: return '#'
		return '?'
	@staticmethod
	def rowRepr (row):
		return "".join (map (Maze.cellRepr, row))
	def __repr__ (self):
		return '\n'.join (map (Maze.rowRepr, self.matrix)) + "\n"
m = Maze ()
#print m
#m.setAll (0)
#print m
#m.setAll ()
#print m
#m.setNonWalls ()
#print m
#m.setAll ()
#print m
#m.setWalls (0)
#print m
m.recursiveBacktracker ()
print m
m.randomizedKruskalsAlgorithm ()
print m
m.randomizedPrimsAlgorithm ()
print m
m.recursiveDivision ()
print m



# on success: finding an exit
#    create grid of mazes
#    
# on failure: getting trapped
#    delete current cell in mega grid
#    regenerate that cell