from common import Common

class Shared:
	def __init__ (self, test):
		self.test = test
		
	def handleError (self, e, sock):
		print "err=%s" % e
		if sock in self.CONNECTION_LIST2: self.CONNECTION_LIST2.remove (sock)
		self.CONNECTION_LIST.remove(sock)
		sock.close()
		
	def writeSockets (self, write_sockets):
		for sock in write_sockets:
			try:
				self.writeSocket (sock)
			except any as e:
				self.handleError (e, sock)
				
	def readSocket (self, sock):
		data = Common.load_recv_msg (sock)
		# TODO necessary?
		if data is None: raise Exception ()
		return data
		
	def readSockets (self, read_sockets):
		for sock in read_sockets:			 
			#New connection
			if self.test (sock):
				self.readServerSocket ()
				continue
					 
			#Some incoming message from a client
			# Data recieved from client, process it
			try: self.readSocket (sock)
			# client disconnected, so remove from socket list
			except any as e:
				self.handleError (e, sock)
				
	def loop_body (self):
		self.CONNECTION_LIST  = []    # list of socket clients
		self.CONNECTION_LIST2 = []
		
		# Add server socket to the list of readable connections
		self.CONNECTION_LIST.append(self.server_socket)
		#CONNECTION_LIST2.append (server_socket)
	
	def setupSocket (self):
		try: self.loop_body ()
		finally: self.server_socket.close ()