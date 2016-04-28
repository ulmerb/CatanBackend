import Location
import Player
import random 

class board:
	#
	#
	#http://stackoverflow.com/questions/1838656/how-do-i-represent-a-hextile-hex-grid-in-memory

	def init(self):
		self.BOARD_LENGTH = 5
		spacesLength = 2 * self.BOARD_LENGTH + 2
		self.edges = [[Location.Edge() for i in range(spacesLength)] for j in range(spacesLength)]
		self.vertices = [[Location.Vertex() for i in range(spacesLength)] for j in range(spacesLength)]
		self.tiles = [[Location.Tile() for i in range(self.BOARD_LENGTH)] for j in range(self.BOARD_LENGTH)]
		self.fillEmpty()
		types = self.getShuffledTypes()
		numbers = self.getShuffledNumbers()
		for i in range(self.BOARD_LENGTH):
			for  j in range(self.BOARD_LENGTH):
				if self.tiles[i][j] is not None:
					givenType = types.pop()
					self.tiles[i][j].setType(givenType)
					self.tiles[i][j].setX(i)
					self.tiles[i][j].setY(j)
					if givenType != "desert":
						self.tiles[i][j].setNumber(numbers.pop())	
					else:
						self.tiles[i][j].setRobber(True)	
		self.printBoard()
		return 0		

	def printBoard(self):
		for i in range(self.BOARD_LENGTH):
			for j in range(self.BOARD_LENGTH):
				print i, j
				if self.tiles[i][j] is not None:
					print self.tiles[i][j].getType()
					print self.tiles[i][j].getNumber()
				else:
					print "None"

	def fillEmpty(self):
		self.tiles[0][0] = None
		self.tiles[0][4] = None
		self.tiles[1][4] = None
		self.tiles[3][4] = None
		self.tiles[4][0] = None
		self.tiles[4][4] = None

	def getShuffledNumbers(self):
		numbers = []
		numbers.append(2)
		numbers.append(2)
		numbers.append(12)
		numbers.append(12)
		for i in range(3, 11):
			if i != 7:
				numbers.append(i)
				numbers.append(i)
				numbers.append(i)
		random.shuffle(numbers)
		return numbers


	def getShuffledTypes(self):
		types = []
		for i in range(3):
			types.append("rock")
		for i in range(4):
			types.append("wood")
		for i in range(3):
			types.append("brick")
		for i in range(4):
			types.append("sheep")
		for i in range(4):
			types.append("wheat")
		types.append("desert")
		random.shuffle(types)
		return types

	def initialPlacement(self, i, players):
		print str(i) + " places their initial piece"
		return 0

	def rollDice(self):
		return (random.randint(1, 6) + random.randint(1, 6))

	def assignResources(self, diceRoll):
		print "assigning resources for the dice roll " + str(diceRoll)
		return -1

	def getTilesNeighborTiles(self, tile):
		result = []
		x = tile.getX()
		y = tile.getY()
		offset = -1
		if x % 2 == 0:
			offset = 1
		if y + 1 < len(self.tiles[0]):
			if self.tiles[x][y+1] is not None:
				result.append(self.tiles[x][y+1])
		if y > 0:
			if self.tiles[x][y-1] is not None:
				result.append(self.tiles[x][y-1])
		if x+1 < len(self.tiles):
			if self.tiles[x+1][y] is not None:
				result.append(self.tiles[x+1][y])
		if x>0:
			if self.tiles[x-1][y] is not None:
				result.append(self.tiles[x-1][y])
		if y+offset >= 0 and y+offset < len(self.tiles[0]):
			if x+1 < len(self.tiles):
				if self.tiles[x+1][y+offset] is not None:
					result.append(self.tiles[x+1][y+offset])
			if x>0:
				if self.tiles[x-1][y+offset] is not None:
					result.append(self.tiles[x-1][y+offset])
		return result

	def getVerticesNeighborVertices(self, vertex):
		result = []
		x = vertex.getX()
		y = vertex.getY()
		offset = 1
		if x % 2 != y % 2:
			offset = -1
		if y+1 < len(self.vertices[0]):
			if self.vertices[x][y+1] != None:
				result.append(self.vertices[x][y+1])


	def getAllTiles(self):
		tiles = []
		tiles.append(Location.Tile())
		tiles.append(Location.Tile())
		return tiles

	def moveRobber(self, location):
		print "Robber moved to " + str(location)

	def playersToStealFrom(self, players):
		targets = []
		targets.append(0)
		targets.append(1)
		return targets

	def getPotentialRoadLocs(self, curPlayer, players):
		return 0

	def getPotentialSettlementLocs(self, curPlayer, players):
		return 0

	def getPotentialCityLocs(self, curPlayer, players):
		return 0

	def buildRoad(self, curPlayer, players, location):
		return 0

	def buildCity(self, curPlayer, players, location):
		return 0

	def buildSettlement(self, curPlayer, players, location):
		return 0
