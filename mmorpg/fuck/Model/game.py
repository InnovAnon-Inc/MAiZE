from Model.grid import Grid
from Model.point import Point

from Model.Item.player import Player

from Model.Direction.CardinalDirection.YDirection.north import NORTH
from Model.Direction.CardinalDirection.YDirection.south import SOUTH
from Model.Direction.CardinalDirection.XDirection.west  import WEST
from Model.Direction.CardinalDirection.XDirection.east  import EAST
from Model.Direction.ZDirection.up   import UP
from Model.Direction.ZDirection.down import DOWN
from Model.Direction.DiagonalDirection.se import SE
from Model.Direction.DiagonalDirection.sw import SW
from Model.Direction.DiagonalDirection.ne import NE
from Model.Direction.DiagonalDirection.nw import NW

from View.divider import Divider
from View.hud     import HUD

from Controller.command import Command
from Controller.move import Move
from Controller.look import Look
from Controller.Attack.attack import Attack
from Controller.Attack.meleeattack import MeleeAttack
from Controller.Attack.rangedattack import RangedAttack

class Game:
	def __init__ (self, width, height):
		self.width   = width
		self.height  = height
		self.grid    = Grid (width, height)
		self.players = []
		self.walls   = []
		self.items   = []
	def addPlayer (self, player):
		#point = self.grid.getRandomTraversablePoint0 ()
		#player = Player (point, 100, 100, 0)
		assert self.grid.getCell (player.pt).isTraversable ()
		self.players.append (player)
		#self.grid.addPlayer (player)
		#return player
		self.grid.addPlayer (player)
	def removePlayer (self, player):
		self.players.remove (player)
		self.grid.removePlayer (player)
	def containsPlayer (self, player):
		return self.grid.containsPlayer (player)
	def isAlive (self):
		#return len (filter (
		#	lambda player: player.isAlive (),
		#	self.players)) is not 0
		return len (self.players) is not 0
	def doLookCommand (self, player, command):
		if not isinstance (command, Look): return True
		player.d = command.d
		return True
	def doAttackCommand (self, player, command):
		if not isinstance (command, Attack): return True
		# TODO
		tryPt = self.getTryPt (player, command)
		if tryPt == player.pt: return True
		
		if not self.grid.containsPoint (tryPt): return True
		
		cell = self.grid.getCell (tryPt)
		#c = chain (cell.players, cell.walls, cell.items)
		#tgt = next (c, None)
		#if tgt is None: return
		#tgt.HP -= 1
		#if tgt.HP is 0:
		#	self.removePlayer 
		for p in cell.players:
			assert player is not p
			#if p.isBlocking
			p.HP -= 1
			if p.HP is 0: self.removePlayer (p)
			return True
		for p in cell.walls:
			p.HP -= 1
			if p.HP is 0: self.removeWall (p)
			return True
		for p in cell.items:
			p.HP -= 1
			if p.HP is 0: self.removeItem (p)
			return True
		#player.HP -= 1
		#if player.HP is 0:
		#	self.removePlayer (p)
		#	return False
		return True
	def getTryPt (self, player, command):
		tryX = player.pt.x
		tryY = player.pt.y
		move = command.d
		if move in [NORTH, NE, NW]: tryY -= 1
		if move in [SOUTH, SE, SW]: tryY += 1
		if move in [EAST,  NE, SE]: tryX += 1
		if move in [WEST,  NW, SW]: tryX -= 1
		return Point (tryX, tryY)
	def doMoveCommand (self, player, command):
		if not isinstance (command, Move): return True
		tryPt = self.getTryPt (player, command)
		# TODO resolve UP, DOWN
		if tryPt == player.pt: return True
		
		if not self.grid.containsPoint (tryPt):
			self.removePlayer (player)
			# TODO fall into void?
			# TODO go to another game?
			return False
		
		if not self.grid.getCell (tryPt).isTraversable ():
			# TODO attack
			return True
		
		self.grid.removePlayer (player)
		#grid.getCell (player.pt.y, player.pt.x).items.remove (player)
		player.pt = tryPt
		#grid.getCell (tryY,     tryX).items.add (player)
		self.grid.addPlayer (player)
		return True
	def doMove (self, player, command):
		# TODO check player move timeout before continuing
		cont = self.doLookCommand   (player, command)
		if not cont: return
		cont = self.doAttackCommand (player, command)
		if not cont: return
		cont = self.doMoveCommand   (player, command)
	def toString (self, cb):
		ret  = cb (self.grid)
		divider = Divider (self.grid.width)
		for player in self.players:
			ret += cb (divider)
			ret += cb (HUD (player))
		return ret
	def __repr__ (self): return self.toString (repr)
	def __str__  (self): return self.toString (str)