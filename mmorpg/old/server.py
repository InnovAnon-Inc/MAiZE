from random import choice
	
from Model.game        import Game
from Model.grid        import Grid
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

from Controller.command import Command
from Controller.move import Move
from Controller.look import Look
from Controller.Attack.attack import Attack
from Controller.Attack.meleeattack import MeleeAttack
from Controller.Attack.rangedattack import RangedAttack





import socket, select


from common import Common, PORT, LISTEN



from shared import Shared


			
class Server (Shared):
	def __init__ (self):
		Shared.__init__ (self, lambda sock: sock == self.server_socket)
		
	def handleError (self, e, sock):
		#broadcast_data(sock, "Client (%s, %s) is offline" % addr)
		#print "Client (%s, %s) is offline" % addr
					
		player = self.players[sock.fileno ()]
		assert player is not None
		assert self.game.containsPlayer (player)
		#player = players[sock]
		self.game.removePlayer (player)
		self.players[sock.fileno ()] = None
		del self.players[sock.fileno ()]
		#del players[sock]

		# TODO don't remove from game... just keep track as zombie... give to next player
	
		Shared.handleError (self, e, sock)
		
	def writeSocket (self, sock):
		assert sock != self.server_socket
		if not self.players.has_key (sock.fileno ()): return
		#if not players.has_key (sock): continue

		player = self.players[sock.fileno ()]
		if player is None: return
		#player = players[sock]
		if not self.game.containsPlayer (player):
			self.players[sock.fileno ()] = None
			del self.players[sock.fileno ()]
							
			self.CONNECTION_LIST.remove (sock)
			if sock in self.CONNECTION_LIST2: self.CONNECTION_LIST2.remove (sock)
			sock.close ()
			#raise Exception ()
			return
		try:
			player.isSelf = True
			msg = str (self.game)
		finally: player.isSelf = False
						
		print msg
						
		Common.send_msg (sock, msg)
		
	def readSocket (self, sock):
		#In Windows, sometimes when a TCP program closes abruptly,
		# a "Connection reset by peer" exception will be thrown
		move = Shared.readSocket (self, sock)
		
		print "move=%s" % move
						
		player = self.players[sock.fileno ()]    
		assert player is not None
		#player = players[sock]    
		assert self.game.containsPlayer (player)
		self.game.doMove (player, move)
						
		# TODO handle other players
		if not self.game.containsPlayer (player):
			if sock in self.CONNECTION_LIST2: self.CONNECTION_LIST2.remove (sock)
			self.CONNECTION_LIST.remove(sock)
			self.players[sock.fileno ()] = None
			del self.players[sock.fileno ()]
			sock.close ()
			return
						
		print "did move=%s" % move
		
	def readServerSocket (self):
		# Handle the case in which there is a new connection recieved through server_socket
		sockfd, addr = self.server_socket.accept()
		sockfd.setblocking (0)
		self.CONNECTION_LIST.append(sockfd)
		#CONNECTION_LIST2.append (sockfd)
		print "Client (%s, %s) connected" % addr
					
		# TODO recycle zombie
		point = self.game.grid.getRandomTraversablePoint0 ()
		c = choice ([NORTH, SOUTH, EAST, WEST])
		# TODO 
		player = Player (point, 100, 100, c, 0, False)
		self.game.addPlayer (player)
		assert self.game.containsPlayer (player)
		self.players[sockfd.fileno ()] = player
		#players[sockfd] = player
					
		assert sockfd not in self.CONNECTION_LIST2
		self.CONNECTION_LIST2.append (sockfd)
					
		print "ADDED PLAYER"

	def loop_body (self):
		Shared.loop_body (self)
		
		DEFAULT_WIDTH  = 80
		DEFAULT_HEIGHT = 40
		self.game = Game (DEFAULT_WIDTH, DEFAULT_HEIGHT)
		self.players = {}
		
		flag = True
		flag2 = True
		while flag2 or len (self.CONNECTION_LIST) > 1:
			flag2 = False
			read_sockets,write_sockets,error_sockets = select.select(self.CONNECTION_LIST,self.CONNECTION_LIST2,self.CONNECTION_LIST)
			if flag:
				if len (write_sockets): flag = False
				self.writeSockets (write_sockets)
			if len (read_sockets): flag = True
			self.readSockets (read_sockets)

	def setupSocket (self, address, nclient):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setblocking (0)
		# this has no effect, why ?
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind(address)
		self.server_socket.listen(nclient)
		Shared.setupSocket (self)

if __name__ == "__main__":
	address = (LISTEN, PORT)
	Server ().setupSocket (address, 10)