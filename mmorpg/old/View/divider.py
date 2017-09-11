from View.view import View

class Divider (View):
	def __init__ (self, width):
		self.text = '-' * width + "\n"
	def __str__ (self):  return self.text
	def __repr__ (self): return self.text