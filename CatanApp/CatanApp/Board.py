import Location
import Player
import random 
import ASCII.catan_ascii_functions as asc
import csv
import math
import VertexToVertexDict
import VertexToEdgeDict
import TileToVertexDict
import VertexToTileDict
import EdgeToVertexDict
import EdgeToEdgeDict
import os
from settings import IS_RUNNING, BASE_DIR
# IS_RUNNING is True when the django server is running

class board:

	def __init__(self):
		self.BOARD_LENGTH = 5
		self.robberTile = None
		self.asciiToTile = {}
		self.tileToAscii = {}
		self.asciiToVertex = {}
		self.vertexToAscii = {}
		self.asciiToEdge = {}
		self.edgeToAscii = {}
		self.settlements = {}
		#create a mapping of settlement ascii to vertex ascii
		self.vertexToVertexMap = VertexToVertexDict.getMap()
		self.vertexToEdgeMap = VertexToEdgeDict.getMap()
		self.vertexToTileMap = VertexToTileDict.getMap()
		self.tileToVertexMap = TileToVertexDict.getMap()
		self.edgeToVertexMap = EdgeToVertexDict.getMap()
		self.edgeToEdgeMap = EdgeToEdgeDict.getMap()
		self.currentBoardNumber = 1
		self.tiles = [Location.Tile(i) for i in range(20)]
		self.tiles[0] = None
		self.vertices = [Location.Vertex(i) for i in range(55)]
		self.vertices[0] = None
		self.edges = [Location.Edge(i) for i in range(73)]
		self.edges[0] = None
		types = self.getShuffledTypes()
		numbers = self.getShuffledNumbers()
		for i in range(19):
			index = i + 1
			givenType = types.pop()
			self.tiles[index].setType(givenType)
			self.tiles[index].setIndex(index)
			if givenType != "desert":
				self.tiles[index].setNumber(numbers.pop())
			else:
				self.tiles[index].setRobber(True)
				self.robberTile = self.tiles[index]
	  	self.buildASCIIGridMaps()

	def buildASCIIGridMaps(self):
		self.buildASCIIToTiles()
		self.buildASCIIToVertices()
		self.buildASCIIToEdges()

	def buildASCIIToTiles(self):
		for tile in self.tiles:
			if tile is not None:
				asciiKey = str(tile.index) + "T"
				if tile.index < 10:
					asciiKey = "0" + asciiKey
				self.asciiToTile[asciiKey] = tile
				self.tileToAscii[tile] = asciiKey

	def buildASCIIToVertices(self):
		for vertex in self.vertices:
			if vertex is not None:
				asciiKey = str(vertex.index) + "V"
				if vertex.index < 10:
					asciiKey = "0" + asciiKey
				self.asciiToVertex[asciiKey] = vertex
				self.vertexToAscii[vertex] = asciiKey

	def buildASCIIToEdges(self):
		for edge in self.edges:
			if edge is not None and edge.index != 0:
				asciiKey = str(edge.index) + "R"
				if edge.index < 10:
					asciiKey = "0" + asciiKey
				self.asciiToEdge[asciiKey] = edge
				self.edgeToAscii[edge] = asciiKey

	def modifyAsciiToEdge(self, ascii, edge, newAscii):
		if edge is None:
			edge = self.asciiToEdge[ascii]
		elif ascii is None:
			ascii = self.edgeToAscii[edge]
		del self.asciiToEdge[ascii]
		del self.edgeToAscii[edge]
		self.asciiToEdge[newAscii] = edge

	def modifyAsciiToVertex(self, ascii, vertex, newAscii):
		if vertex is None:
			vertex = self.asciiToVertex[ascii]
		elif ascii is None:
			ascii = self.vertexToAscii[vertex]
		del self.asciiToVertex[ascii]
		del self.vertexToAscii[vertex]
		self.asciiToVertex[newAscii] = vertex

	def modifyAsciiToTile(self, ascii, tile, newAscii):
		if tile is None:
			tile = self.asciiToTile[ascii]
		elif ascii is None:
			ascii = self.tileToAscii[tile]
		del self.asciiToTile[ascii]
		del self.tileToAscii[tile]
		self.asciiToTile[newAscii] = tile

	#debugging function
	def printEdges(self):
		for row in self.edges:
			print ','.join([str(e.index) if e is not None else "None" for e in row])

	def printVerts(self):
		for row in self.vertices:
			print ','.join([str(e.index) if e is not None else "None" for e in row])

	def createBatchCSV(self, players):
		if IS_RUNNING:
			path = os.path.join(BASE_DIR, 'ASCII/latest_update.csv')
		else:
			path = 'ASCII/latest_update.csv'
		with open(path, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			# THIS DISPLAYS THE INITINALIZED TILES - matt
			for tile in self.tiles:
				if tile is not None and tile.index != 0:
					tileAscii = self.tileToAscii[tile]
					goalTag = ""
					if(tile.getType() == "desert"):
						goalTag = "ROB"
					else:
						goalTag = str(tile.getType()[0]).capitalize()
						if(tile.getNumber() < 10):
							goalTag += "0"+ str(tile.getNumber())
						else:
							goalTag += str(tile.getNumber())
					# print goalTag
					writer.writerow([tileAscii,goalTag])
			for vertex in self.vertices:
				if vertex is not None and vertex.getOwner() is not None:
					vertexAscii = self.vertexToAscii[vertex]
					if vertex.getCity() is not None:
						writer.writerow([self.vertexSettlementAscii(vertex), self.vertexCityAscii(vertex)])
					else:
						writer.writerow([vertexAscii, self.vertexSettlementAscii(vertex)])
			for edge in self.edges:
				if edge is not None and edge.getOwner() is not None:
					edgeAscii = self.edgeToAscii[edge]
					writer.writerow([edgeAscii, "!R" + str(edge.getOwner())])

	def vertexSettlementAscii(self, vertex):
		return str(vertex.settleNum) + "S" + str(vertex.getOwner()) 

	def vertexCityAscii(self,vertex):
		return str(vertex.cityNum) + "C" + str(vertex.getOwner())

	def batchUpdate(self):
		newBoardNumber = asc.batchUpdate(self.currentBoardNumber)
		self.currentBoardNumber = newBoardNumber

	def printBoard(self):
		asc.printBoard(self.currentBoardNumber)

	def addSettlement(self, location):
		settlementAscii = self.vertexSettlementAscii(location)
		self.settlements[str(settlementAscii)] = self.vertexToAscii[location]
		print settlementAscii, " associated with ", self.vertexToAscii[location]

	def getSettlementFromAscii(self, ascii):
		return self.settlements[str(ascii)]

	def validCityLoc(self, locationAscii):
		if str(locationAscii) in self.settlements:
			return True
		return False

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


	def rollDice(self):
		return (random.randint(1, 6) + random.randint(1, 6))

	def assignResources(self, diceRoll, players):
		resourceMap = {}
		for tile in self.tiles:
			if tile is not None and tile.index != 0 and tile.getNumber() == diceRoll:
				for vertex in self.getTileToVertices(tile):
					amount = 0
					if vertex.getSettlement() is not None:
						amount = 1
					if vertex.getCity() is not None:
						amount = 2
					if amount != 0:
						players[vertex.getOwner()].addResource(tile.getType(), amount)

	def getVertexToVertices(self, vertex):
		result = []
		index = vertex.getIndex()
		for neighbor in self.vertexToVertexMap[index]:
			result.append(self.vertices[neighbor])
		return result

	def getTileToVertices(self, tile):
		result = []
		index = tile.getIndex()
		for neighbor in self.tileToVertexMap[index]:
			result.append(self.vertices[neighbor])
		return result

	def getVertexToEdges(self, vertex):
		result = []
		index = vertex.getIndex()
		for neighbor in self.vertexToEdgeMap[index]:
			result.append(self.edges[neighbor])
		return result 

	def getEdgeToEdges(self, edge):
		result = []
		index = edge.getIndex()
		for neighbor in self.edgeToEdgeMap[index]:
			result.append(self.edges[neighbor])
		return result

	def getEdgeToVertices(self, edge):
	    result = []
	    index = edge.getIndex()
	    for neighbor in self.edgeToVertexMap[index]:
	    	result.append(self.vertices[neighbor])
	    return result

	def getVertexToTiles(self, vertex):
		result = []
		index = vertex.getIndex()
		for neighbor in self.vertexToTileMap[index]:
			result.append(self.tiles[neighbor])
		return result

	def getAllTiles(self):
		tiles = []
		for tile in self.tiles:
			if tile is not None and tile.index != 0:
				tiles.append(tile)
		return tiles

	def moveRobber(self, tile):
		self.robberTile.setRobber(False)
		self.robberTile = None
		print "Robber moved to " + str(self.tileToAscii[tile])
		if tile is not None:
			tile.setRobber(True)
			self.robberTile = tile
		else:
			print "Invalid location"

	def playersToStealFrom(self, players):
		relatedVertices = self.getTileToVertices(self.robberTile)
		targets = []
		for vertex in relatedVertices:
			if vertex.getOwner() is not None:
				targets.append(vertex.getOwner())
		return set(targets)

	def getPotentialRoadLocs(self, curPlayer, players):
		result = []
		for vertex in self.vertices:
			if vertex is not None and vertex.getOwner() == curPlayer:
				roadLocs = self.getVertexToEdges(vertex)
				for road in roadLocs:
					if road.getOwner() is None:
						result.append(road)
		return set(result)

	def neighborsUnclaimed(self, vertex):
		for neighbor in self.getVertexToVertices(vertex):
			if neighbor.getOwner() is not None:
				return False
		return True

	def getPotentialSettlementLocs(self, curPlayer, players, initializing):
		locs = set()
		if not initializing:
			edges = players[curPlayer].structures['roads']
			for edgeNum in edges:
				edge = self.edgeArray[edgeNum]
				v1, v2 = self.getEdgeToVertices(edge)
				if v1 is not None and v1.getOwner() is None and self.neighborsUnclaimed(v1):
					locs.add(v1)
				if v2 is not None and v2.getOwner() is None and self.neighborsUnclaimed(v2):
					locs.add(v2)
		else:
			for vertex in self.vertices:
				if vertex is not None and vertex.getOwner() is None and self.neighborsUnclaimed(vertex):
					locs.add(vertex)
		return locs

	def getPotentialCityLocs(self, curPlayer, players):
		result = []
		for vertex in self.vertices:
			if vertex is not None and vertex.getSettlement() == curPlayer:
				result.append(vertex)
		return result

	def buildRoad(self, curPlayer, players, edge):
		players[curPlayer].buildRoad(edge, self)

	def buildCity(self, curPlayer, players, vertex):
		players[curPlayer].buildCity(vertex)

	def buildSettlement(self, curPlayer, players, vertex):
		players[curPlayer].buildSettlement(vertex, self)

	def vertexInBounds(self,x,y):
		return self.vertices[x][y] is not None

	def edgeInBounds(self, x,y):
		return self.edges[x][y] is not None
