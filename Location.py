class Location:
	def __init__(self):
		self.x = None
		self.y = None

	def __str__(self):
		return "Location"

	def setX(self, x):
		self.x = x

	def setY(self, y):
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y

class Tile(Location):
	def __init__(self):
		self.type = None
		self.number = None
		self.robber = False
		self.x = None
		self.y = None

	def __str__(self):
		return "Tile"

	def setType(self, givenType):
		self.type = givenType

	def setNumber(self, givenNumber):
		self.number = givenNumber

	def getType(self):
		return self.type

	def getNumber(self):
		return self.number

	def setRobber(self, val):
		self.robber = val


class Edge(Location):
	def __str__(self):
		return "Road"

class Vertex(Location):
	def __str__(self):
		return "Settlement or City"
