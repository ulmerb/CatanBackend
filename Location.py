class Location:
	def __init__(self, x, y):
		self.x = x
		self.y = y

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
	def __init__(self, x, y):
		self.type = None
		self.number = None
		self.robber = False
		self.x = x
		self.y = y

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
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.owner = None

	def __str__(self):
		return "Road"

	def buildRoad(self, player):
		self.owner = player

	def getOwner(self):
		return self.owner


class Vertex(Location):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.settlement = None
		self.city = None

	def __str__(self):
		if self.settlement is not None:
			return "Settlement " + str(self.x) + "," + str(self.y) + " owned by player " + str(self.settlement)
		elif self.city is not None:
			return "City " + str(self.x) + "," + str(self.y) + "owned by player " + str(self.city)
		return "Empty " + str(self.x) + "," + str(self.y)

	def buildSettlement(self, player, settlementNumber):
		self.settlement = player
		self.settleNum = settlementNumber

	def buildCity(self, player):
		self.settlement = None
		self.city = player

	def getSettlement(self):
		return self.settlement

	def getCity(self):
		return self.city

	def getOwner(self):
		if self.settlement is not None:
			return self.settlement
		if self.city is not None:
			return self.city
		return None
