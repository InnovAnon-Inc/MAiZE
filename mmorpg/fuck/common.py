from pickle import loads, dumps
from struct import pack, unpack

LISTEN  = "0.0.0.0"
CONNECT = "127.0.0.1"
PORT    = 5000

class Common:
	@staticmethod
	def recvall(sock, n):
		# Helper function to recv n bytes or return None if EOF is hit
		data = ''
		while len(data) < n:
			packet = sock.recv(n - len(data))
			if not packet:
				return None
			data += packet
		return data

	@staticmethod
	def recv_msg(sock):
		# Read message length and unpack it into an integer
		raw_msglen = Common.recvall(sock, 4)
		if not raw_msglen:
			return None
		msglen = unpack('>I', raw_msglen)[0]
		# Read the message data
		return Common.recvall(sock, msglen)

	@staticmethod
	def send_msg(sock, msg):
		msg = dumps (msg)
		msg = pack ('>I', len (msg)) + msg
		sock.sendall (msg)
		
	@staticmethod
	def load_recv_msg (sock):
		data = Common.recv_msg (sock)
		if data is None: return None
		data = loads (data)
		return data