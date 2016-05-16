import Location
import Player
import random 
import ASCII.catan_ascii_functions as asc
import csv
import math

class board:
	#http://stackoverflow.com/questions/1838656/how-do-i-represent-a-hextile-hex-grid-in-memory

	def __init__(self):
		self.BOARD_LENGTH = 5
		self.robberX = None
		self.robberY = None
		spacesLength = 2 * self.BOARD_LENGTH + 2
		self.edges = [[Location.Edge(i,j) for j in range(spacesLength)] for i in range(spacesLength - 1)]
		self.vertices = [[Location.Vertex(i,j) for j in range(spacesLength)] for i in range(spacesLength/2)]
		self.tiles = [[Location.Tile(i,j) for j in range(self.BOARD_LENGTH)] for i in range(self.BOARD_LENGTH)]
		self.asciiToTile = {}
		self.asciiToVertex = {}
		self.asciiToEdge = {}
		self.fillEmpty()
		self.currentBoardNumber = 1
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
		
		# This sets non-playable edges and vertices(ones not boarding any tile i.e. the ocean) to None
		verts = []
  		edges = []
		for row in self.tiles:
		    for hex in row:
		      if hex is not None:
		        vs = self.getTileToVertices(hex)
		        es = self.getTileToEdges(hex)
		        verts += vs
		        edges += es
		        #hexes.append(hex)
	  	playableEdges = set(edges)
	  	for i in range(spacesLength - 1):
	  		for j in range(spacesLength):
	  			if self.edges[i][j] not in playableEdges:
	  				self.edges[i][j] = None
	  	playableVertices = set(verts)
	  	for i in range(spacesLength/2):
	  		for j in range(spacesLength):
	  			if self.vertices[i][j] not in playableVertices:
	  				self.vertices[i][j] = None

	  	# Maps the initial board ascii to the tile, edge, or vertex it refers to. Will be updated
	  	# everytime a structure is built
	  	self.buildASCIIGridMaps()
	# formulas generated using lagragian interpolation
	# Takes in a tile's grid coordinates and outputs the appropriate ascii string
	def tileToAscii(self,x,y):
		result = int(round(x**4/float(6) - (3*x**3)/float(2) + (13*x**2)/float(3) + y))
		if result < 10:
			return '0' + str(result) + 'T'
		return str(result) + 'T'

	# Takes in a vertex's grid coordinates and outputs the appropriate ascii string
	def vertexToAscii(self,x,y):
		result = int(round(x**5/float(60) - (5/float(24))*x**4 + 
			(2/float(3))*x**3 + (5/float(24))*x**2 + (439/float(60))*x - 1 + y))
		if result < 10:
			return '0' + str(result) + 'V'
		return str(result) + 'V'

	# Takes in a vertex's grid coordinates and outputs the appropriate ascii string
	def edgeToAscii(self,x,y):
		result = 0
		if x % 2 == 0:
			result = int(round(x**5/float(640) - (float(5)/128)*x**4 + (float(7)/24)*x**3 - (float(15)/32)*x**2 + (float(667)/120)*x - 1 + y))
		else:
			result = int(round(x**4/float(192) - x**3/float(6) + (float(151)/96)*x**2 + (float(13)/6)*x + 1.421875 + math.ceil(0.5*y)))
		if result < 10:
			return '0' + str(result) + 'R'
		return str(result) + 'R'

	def buildASCIIGridMaps(self):
		self.buildASCIIToTiles()
		self.buildASCIIToVertices()
		self.buildASCIIToEdges()

	def buildASCIIToTiles(self):
		for row in self.tiles:
			for tile in row:
				if tile is not None:
					self.asciiToTile[self.tileToAscii(tile.x, tile.y)] = tile

	def buildASCIIToVertices(self):
		for row in self.vertices:
			for v in row:
				if v is not None:
					self.asciiToVertex[self.vertexToAscii(v.x, v.y)] = v

	def buildASCIIToEdges(self):
		for row in self.edges:
			for e in row:
				if e is not None:
					self.asciiToEdge[self.edgeToAscii(e.x, e.y)] = e

	def createBatchCSV(self, players):
		with open('ASCII/latest_update.csv', 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for row in self.vertices:
				for vert in row:
					if vert is not None and vert.getOwner() is not None:
						vertAscii = self.vertexToAscii(vert.x, vert.y)
						writer.writerow([vertAscii, str(vert.settleNum) + "S" + str(vert.getOwner())])
						

	def batchUpdate(self):
		newBoardNumber = asc.batchUpdate(self.currentBoardNumber)
		self.currentBoardNumber = newBoardNumber

	def printBoard(self):
		asc.printBoard(1)


	def fillEmpty(self):
		self.tiles[0][0] = None
		self.tiles[0][4] = None
		self.tiles[1][0] = None
		self.tiles[3][0] = None
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
			types.append("ore")
		for i in range(4):
			types.append("wood")
		for i in range(3):
			types.append("brick")
		for i in range(4):
			types.append("sheep")
		for i in range(4):
			types.append("grain")
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
						        players[vertex.getOwner()].addResource(tile.getType(), amount)

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
		x = vertex.x
		y = vertex.y
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
		x = tile.x
		y = tile.y
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
				if v1 is not None and neighborsUnclaimed(v1) and v1.getOwner() is None:
					locs.add(v1)
				if v2 is not None and neighborsUnclaimed(v2) and v2.getOwner() is None:
					locs.add(v2)
		else:
			for row in self.vertices:
				for vertex in row:
					if vertex is not None and vertex.getOwner() is None and neighborsUnclaimed(vertex):
						locs.add(vertex)
		return locs

	def getPotentialCityLocs(self, curPlayer, players):
		result = []
		for row in self.vertices:
			for vertex in row:
				if vertex is not None and vertex.getSettlement() == curPlayer:
					result.append(vertex)
		return result

	def buildRoad(self, curPlayer, players, edge):
		players[curPlayer].buildRoad(edge)

	def buildCity(self, curPlayer, players, vertex):
		players[curPlayer].buildCity(vertex)

	def buildSettlement(self, curPlayer, players, vertex):
		players[curPlayer].buildSettlement(vertex)

	def vertexInBounds(self,x,y):
		return self.vertices[x][y] is not None

	def edgeInBounds(self, x,y):
		return self.edges[x][y] is not None
