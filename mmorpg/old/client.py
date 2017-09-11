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

from Queue import Queue, Empty

from common import Common, PORT, CONNECT







import sys
from termios import tcgetattr, tcsetattr
import termios
from tty import setraw
from random import choice




























from shared import Shared	
	
	
				
class Client (Shared):
	@staticmethod
	#def getMove (player):
	def getMove ():
		#ch = getch ()
		ch = sys.stdin.read(1)
		#if ch == '2':
		#	move = getMove (player)
		#	for k in xrange (2): 
		#	return
		if ch == 'j': return MeleeAttack (SOUTH)
		if ch == 'k': return MeleeAttack (NORTH)
		if ch == 'h': return MeleeAttack (WEST)
		if ch == 'l': return MeleeAttack (EAST)
		if ch == 'b': return MeleeAttack (SW)
		if ch == 'n': return MeleeAttack (SE)
		if ch == 'y': return MeleeAttack (NW)
		if ch == 'u': return MeleeAttack (NE)
		
		if ch == 'J': return Look (SOUTH)
		if ch == 'K': return Look (NORTH)
		if ch == 'H': return Look (WEST)
		if ch == 'L': return Look (EAST)
		if ch == 'B': return Look (SW)
		if ch == 'N': return Look (SE)
		if ch == 'Y': return Look (NW)
		if ch == 'U': return Look (NE)
		
		#if ch == 'f': return RangedAttack (player.d) # current direction
		#if ch == 's': return Block (player.d) # current direction
		if ch == 'f': return RangedAttack ()
		if ch == 's': return Block ()
		# TODO toggle mode: repeat last command... fast
		
	def __init__ (self, fd, old_settings):
		Shared.__init__ (self, lambda sock: sock == fd)
		self.fd = fd
		self.old_settings = old_settings
		
	def handleError (self, e, sock):
		Shared.handleError (self, e, sock)
		CONNECTION_LIST.remove (self.fd)
		
	def writeSocket (self, sock):
		# TODO need player facing/heading
		#move = getMove ()
		try:
			move = self.message_queue.get_nowait ()
		except Empty:
			if sock in self.CONNECTION_LIST2: self.CONNECTION_LIST2.remove(sock)
		else: Common.send_msg (sock, move)
		
	def readSocket (self, sock):
		data = Shared.readSocket (self, sock)
		tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
		try: print data
		finally: setraw (self.fd)
		
	def readServerSocket (self):
		move = Client.getMove ()
		self.message_queue.put (move)
						
		#if sock not in CONNECTION_LIST2:
		#	CONNECTION_LIST2.append (sock)
		if self.server_socket not in self.CONNECTION_LIST2:
			self.CONNECTION_LIST2.append (self.server_socket)
			
	def loop_body (self):
		Shared.loop_body (self)
		self.CONNECTION_LIST.append (self.fd)
		self.message_queue = Queue ()	
			
		# TODO terminator
		while self.CONNECTION_LIST:
			# Get the list sockets which are ready to be read through select
			#read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
			read_sockets,write_sockets,error_sockets = select.select(
				self.CONNECTION_LIST,self.CONNECTION_LIST2,self.CONNECTION_LIST)
			self.readSockets (read_sockets)
			self.writeSockets (write_sockets)
	
	def setupSocket (self, address):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#socket.setblocking (0)
		self.server_socket.connect (address)
		Shared.setupSocket (self)
				

def doItRaw (fd, cb):
	old_settings = tcgetattr (fd)
	try:
		setraw (fd)
		cb (old_settings)
	finally:
		tcsetattr (fd, termios.TCSADRAIN, old_settings)
if __name__ == "__main__":
	#sys.stdin.setblocking (0)
	fd = sys.stdin.fileno()
	address = (CONNECT, PORT)
	doItRaw (fd, lambda o: Client (fd, o).setupSocket (address))