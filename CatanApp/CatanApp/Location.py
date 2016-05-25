class Location:
	def __init__(self, index):
		self.index = x

	def __str__(self):
		return "Location"

	def setIndex(self, index):
		self.index = index

	def getIndex(self):
		return self.index

class Tile(Location):
	def __init__(self, index):
		self.type = None
		self.number = None
		self.robber = False
		self.index = index

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

	def setIndex(self, index):
		self.index = index

	def getIndex(self):
		return self.index


class Edge(Location):
	def __init__(self, index):
		self.index = index
		self.owner = None

	def __str__(self):
		return "Road"

	def buildRoad(self, player):
		self.owner = player

	def getOwner(self):
		return self.owner

	def setIndex(self, index):
		self.index = index

	def getIndex(self):
		return self.index

class Vertex(Location):
	def __init__(self, index):
		self.index = index
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

	def buildCity(self, player, cityNumber):
		self.settlement = None
		self.city = player
		self.cityNum = cityNumber

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

	def setType(self,resource):
		pass

	def getType(self):
		return self.type

	def setIndex(self, index):
		self.index = index

	def getIndex(self):
		return self.index
