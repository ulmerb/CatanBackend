import Location
import Player
class board:
	#Catan board has 19 tiles, 54 corners, 36 edges
	def __init__(self):
		return 0

	def initialPlacement(self, i, players):
		print str(i) + " places their initial piece"
		return 0

	def rollDice(self):
		return -1

	def assignResources(self, diceRoll):
		print "assigning resources for the dice roll " + str(diceRoll)
		return -1

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