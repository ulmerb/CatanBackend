class Location:
	def __str__(self):
		return "Location"

class Tile(Location):
	def __str__(self):
		return "Tile"
	def __init__(self, resource, diceNumber):
		# if resource == None then it is desert tile
		self.resource = resource
		self.isDesert = not resource
		self.diceNumber = diceNumber
		self.points = []
		self.edges = []

	def addPoint(settlementLoc):
		self.points.append(settlementLoc)
		settlementLoc.addTile(self)

	def addRoad(roadLoc):
		self.edges.append(roadLoc)
		roadLoc.addTile(self)

class RoadLocation(Location):
	def __str__(self):
		return "Road"
	def __init__(self,pointA,pointB):
		self.points = [pointA, pointB]
		self.tiles = []
		pointA.addRoadLoc(self)
		pointB.addRoadLoc(self)

	def addTile(tile):
		self.tiles.append(tile)

class SettlementLocation(Location):
	def __str__(self):
		return "Settlement or City"
	def __init__(self):
		self.edges = []
		self.tiles = []

	def addTile(tile):
		self.tiles.append(tile)

	def addRoadLoc(roadLoc):
		self.edges.append(roadLoc)
