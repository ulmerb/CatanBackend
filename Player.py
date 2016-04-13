class player:

	def init(self):
		print "test" 

	def hasWon(self):
		return False

	def canBuildCity(self):
		return False

	def canBuildSettlement(self):
		return False

	def canBuildRoad(self):
		return False

	def canBuildDevCard(self):
		return False

	def canPlayDevCard(self):
		return False

	def buildRoad(self):
		return 0

	def buildSettlement(self):
		return 0

	def buildCity(self):
		return 0

	def buildDevCard(self):
		return 0

	def loseRandomCard(self):
		return 0

	def addResource(self, resource, amount):
		return 0

	def loseResource(self, resource, amount):
		return 0