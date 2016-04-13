class Location:
	def __str__(self):
		return "Location"

class Tile(Location):
	def __str__(self):
		return "Tile"

class RoadLocation(Location):
	def __str__(self):
		return "Road"

class SettlementLocation(Location):
	def __str__(self):
		return "Settlement or City"
