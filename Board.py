import Location
import Player
import random 

class board:
	#http://stackoverflow.com/questions/1838656/how-do-i-represent-a-hextile-hex-grid-in-memory

	def __init__(self):
		self.BOARD_LENGTH = 5
		self.robberX = None
		self.robberY = None
		spacesLength = 2 * self.BOARD_LENGTH + 2
		self.edges = [[Location.Edge(i,j) for j in range(spacesLength)] for i in range(spacesLength)]
		self.vertices = [[Location.Vertex(i,j) for j in range(spacesLength)] for i in range(spacesLength)]
		self.tiles = [[Location.Tile(i,j) for j in range(self.BOARD_LENGTH)] for i in range(self.BOARD_LENGTH)]
		self.fillEmpty()
		types = self.getShuffledTypes()
		numbers = self.getShuffledNumbers()
		for i in range(self.BOARD_LENGTH):
			for j in range(self.BOARD_LENGTH):
				if self.tiles[i][j] is not None:
					givenType = types.pop()
					self.tiles[i][j].setType(givenType)
					self.tiles[i][j].setX(i)
					self.tiles[i][j].setY(j)
					if givenType != "desert":
						self.tiles[i][j].setNumber(numbers.pop())	
						self.robberX = i
						self.robberY = j
					else:
						self.tiles[i][j].setRobber(True)
		self.printBoard()

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
			types.append("quarry")
		for i in range(4):
			types.append("forest")
		for i in range(3):
			types.append("brickpit")
		for i in range(4):
			types.append("sheepherd")
		for i in range(4):
			types.append("plain")
		types.append("desert")
		random.shuffle(types)
		return types
	
	def initialPlacement(self, i, players):
		while True:
			try:
				settleLoc = input('Player ' + str(i) + ', enter a settlement location: ')
				x,y = settleLoc
				if self.vertexInBounds(x,y):
					okLocs = self.getPotentialSettlementLocs(i, players, True)
					if self.vertices[x][y] in okLocs:
						self.buildSettlement(i, players, self.vertices[x][y])
						print self.vertices[x][y]
						break
					else:
						print "You may not build there"
				else:
					print "Location is out of bounds."
			except EOFError:
				print "Invalid location"

		return 0

	def rollDice(self):
		return (random.randint(1, 6) + random.randint(1, 6))

	def assignResources(self, diceRoll, players):
		resourceMap = {}
		for row in self.tiles:
			for tile in row:
				if tile is not None and tile.getNumber() == diceRoll:
					for vertex in self.getTileToVertices(tile):
						amount = 0
						if vertex.getSettlement() is not None:
							amount = 1
						if vertex.getCity() is not None:
							amount = 2
						if amount != 0:
							if vertex.getType() == "forest":
								players[vertex.getOwner()].addResource("wood", amount)
							elif vertex.getType() == "quarry":
								players[vertex.getOwner()].addResource("ore", amount)
							elif vertex.getType() == "brickpit":
								players[vertex.getOwner()].addResource("brick", amount)
							elif vertex.getType() == "sheepherd":
								players[vertex.getOwner()].addResource("wool", amount)
							elif vertex.getType() == "plain":
								players[vertex.getOwner()].addResource("grain", amount)




	def getTileToTiles(self, tile):
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

	def getVertexToVertices(self, vertex):
		result = []
		x = vertex.getX()
		y = vertex.getY()
		offset = 1 if x % 2 == y % 2 else -1
		if y+1 < len(self.vertices[0]) and self.vertices[x][y+1] is not None:
			result.append(self.vertices[x][y+1])
		if y > 0 and self.vertices[x][y-1] is not None:
			result.append(self.vertices[x][y-1])
		if x+offset >= 0 and x+offset < len(self.vertices) and self.vertices[x+offset][y] is not None:
			result.append(self.vertices[x+offset][y])
		return result

	def getTileToVertices(self, tile):
		result = []
		x = tile.getX()
		y = tile.getY()
		offset = (x % 2)*-1
		result.append(self.vertices[x][2*y+offset])
		result.append(self.vertices[x][2*y+offset+1])
		result.append(self.vertices[x][2*y+offset+2])
		result.append(self.vertices[x+1][2*y+offset])
		result.append(self.vertices[x+1][2*y+offset+1])
		result.append(self.vertices[x+1][2*y+offset+2])
		return result

	def getTileToEdges(self, tile):
		result = []
		x = tile.getX()
		y = tile.getY()
		offset = (x % 2)*-1
		result.append(self.edges[2*x][2*y+offset])
		result.append(self.edges[2*x][2*y+offset+1])
		result.append(self.edges[2*x+1][2*y+offset+2])
		result.append(self.edges[2*x+1][2*y+offset])
		result.append(self.edges[2*x+2][2*y+offset])
		result.append(self.edges[2*x+2][2*y+offset+1])
		return result

	def getVertexToEdges(self, vertex):
		result = []
		x = vertex.getX()
		y = vertex.getY()
		offset = 1
		if x%2 != y%2:
			offset = -1
		if self.edges[x*2][y] is not None:
			result.append(self.edges[x*2][y])
		if self.edges[x*2][y-1] is not None:
			result.append(self.edges[x*2][y-1])
		if self.edges[x*2+offset][y] is not None:
			result.append(self.edges[x*2+offset][y])
		return result

	def getEdgeToVertices(self, edge):
	    x = edge.x
	    y = edge.y
	    vertexOne = self.vertices[(x-1)/2][y]
	    vertexTwo = self.vertices[(x+1)/2][y]
	    if x%2 == 0:
	      vertexOne = self.vertices[x/2][y]
	      vertexTwo = self.vertices[x/2][y+1]
	    return (vertexOne, vertexTwo)

	def getVertexToTiles(self, vertex):
		result = []
		x = vertex.getX()
		y = vertex.getY()
		xOffset = x % 2
		yOffset = y % 2
		if x < len(self.tiles) and y/2 < len(self.tiles[x]):
			if self.tiles[x][y/2] is not None:
				result.append(self.tiles[x][y/2])

		if x > 0 and x < len(self.tiles) and y/2 < len(self.tiles[x]):
			if self.tiles[x-1][y/2] is not None:
				return result

		xMod = x
		if xOffset + yOffset == 1:
			xMod -=1
		yMod = y/2
		if yOffset == 1:
			yMod += 1
		else:
			yMod -=1
		if xMod >= 0 and xMod < len(self.tiles) and yMod >= 0 and yMOd < len(self.tiles[0]):
			if self.tiles[xMod][yMod] is not None:
				result.append(self.tiles[xMod][yMod])
		return result

	def getAllTiles(self):
		tiles = []
		for row in self.tiles:
			for tile in row:
				tiles.append(tile)
		return tiles

	def moveRobber(self, tile):
		self.tiles[self.robberX][self.robberY].setRobber(False)
		print "Robber moved to " + str(tile)
		if tile is not None:
			tile.setRobber(True)
			self.robberX = tile.getX()
			self.robberY = tile.getY()
		else:
			print "Invalid location"

	def playersToStealFrom(self, players):
		relatedVertices = self.getTileToVertices(self.tiles[self.robberX][self.robberY])
		targets = []
		for vertex in relatedVertices:
			if vertex.getOwner() is not None:
				targets.add(vertex.getOwner())
		return set(targets)

	def getPotentialRoadLocs(self, curPlayer, players):
		result = []
		for row in self.vertices:
			for vertex in row:
				if vertex.getOwner() == curPlayer:
					roadLocs = self.getVertexToEdges(vertex)
					for road in roadLocs:
						if road.getOwner() is None:
							result.append(road)
		return set(result)

	def getPotentialSettlementLocs(self, curPlayer, players, initializing):
		def neighborsUnclaimed(vertex):
			for neighb in self.getVertexToVertices(vertex):
				if neighb.getOwner() is not None:
					return False
			return True

		locs = set()
		if not initializing:
			edges = players[curPlayer].structures.roads
			for edge in edges:
				v1, v2 = self.getEdgeToVertices(edge)
				if neighborsUnclaimed(v1):
					locs.add(v1)
				if neighborsUnclaimed(v2):
					locs.add(v2)
		else:
			for row in self.vertices:
				for vertex in row:
					if vertex.getOwner() is None and neighborsUnclaimed(vertex):
						locs.add(vertex)
		return locs

	def getPotentialCityLocs(self, curPlayer, players):
		result = []
		for row in self.vertices:
			for vertex in row:
				if vertex.getSettlement() == curPlayer:
					result.append(vertex)
		return result

	def buildRoad(self, curPlayer, players, edge):
		edge.buildRoad(curPlayer)

	def buildCity(self, curPlayer, players, vertex):
		vertex.buildCity(curPlayer)

	def buildSettlement(self, curPlayer, players, vertex):
		vertex.buildSettlement(curPlayer)

	def vertexInBounds(self,x, y):
		print 
		return True

		