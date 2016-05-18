import random

class devcards:

	#names of card:
	# knight, victoryPoint, roadBuild, monopoly, yearOfPlenty

	def __init__(self):
		self.numDevCards = 25
		self.numKnights = 14
		self.numVictoryPoints = 5
		self.numRoadBuild = 2
		self.numMonopoly = 2
		self.numYearOfPlenty = 2
		self.devCardsArr = []
		for i in range(1,26):
			if i <=14:
				self.devCardsArr.append("knight")
			elif i <=19:
				self.devCardsArr.append("victoryPoint")
			elif i <=21:
				self.devCardsArr.append("roadBuild")
			elif i <=23:
				self.devCardsArr.append("monopoly")
			else:
				self.devCardsArr.append("yearOfPlenty")


	def getRandomDevCard(self):
		if len(self.devCardsArr) == 0:
			return "no more dev cards"
		else: 
			self.numDevCards -= 1
			cardName = self.devCardsArr.pop(0)
			print cardName
			return cardName

	def getNumDevCards(self):
		return self.numDevCards



