from Controller.look import Look

class Block (Look):
	def __init__ (self, d):
		assert issubclass (d, CardinalDirection)
		Look.__init__ (self, d)
	def __str__ (self):
		return "%s, %s" % (Look.__str__ (self), "ranged")