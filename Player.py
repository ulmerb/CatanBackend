# -*- coding: utf-8 -*-
import random

class player:

	def __init__(self, i):
	        self.score =  0
	        self.resources =  {'wood':4, 'sheep':4, 'brick': 4, 'ore': 4, 'grain' : 4}
	        self.roadsRemaining = 15
	        self.citiesRemaining = 4
	        self.settlementsRemaining = 5
	        #we may want to handle this differently but it seems useful for the player to have internal knowledge
	        #of where its built, for now initialize as an empty list for each that can be filled to match board 
	        #loactions however we choose to store those
	        self.structures = {'roads' : [], 'settlements' : [], 'cities' : [], 'ports' : []}
	        self.playerNumber = i
		self.devCardsHeld = []
		self.devCardsPlayed = []

	def __str__(self):
		return str(self.playerNumber) + " resources:" + str(self.resources) + " score: " + str(self.score)
	
	def getScore(self):
                 return self.score   
                
        def incrementScore(self, s = 1):
                 self.score += s
                 
	def hasWon(self):
	        if self.score >= 10:
	            return True
		return False
        #on all of these methods I'll leave the option to check a specific location for now
	def canBuildCity(self, location):
   	    if self.resources['grain'] >= 2 and self.resources['ore'] >= 3 and self.citiesRemaining > 0:
   	        if location in self.structures['settlements']:
   	            return True
		return False
		
	def canBuildSettlement(self, board, gridLoc):
		if gridLoc.getOwner() is not None:
			return False
		if not (self.resources['brick'] >= 1 and self.resources['wood'] >= 1 and self.resources['grain'] >= 1 and self.resources['sheep'] >= 1 and self.settlementsRemaining > 0):
			print "Insufficent resources, ", self.resources
			return False
		adjRoads = board.getVertexToEdges(gridLoc)
		playerHasRoad = False
		for road in self.structures['roads']:
			if road in adjRoads:
				playerHasRoad = True
				break
		if not playerHasRoad:
			return False
		for n in board.getVertexToVertices(gridLoc):
			if n.getOwner() is not None:
				return False
		else:
			print self, " cannot play there"
		return True

	def canBuildRoad(self, location, board):
		if location.getOwner() is not None:
			return False
		if not (self.resources['brick'] >= 1 and self.resources['wood'] >= 1 and self.roadsRemaining > 0):
			return False
		for neighbV in board.getEdgeToVertices(location):
			if neighbV.getOwner() == self.playerNumber:
				return True
		for neigbE in board.getEdgeToEdges(location):
			if neigbE.getOwner() == self.playerNumber:
				return True
		return False

	def canBuildDevCard(self):
	        if self.resources['sheep'] >= 1 and self.resources['grain'] >= 1 and self.resources['ore'] >= 1:
	           return True
		return False

	def canPlayDevCard(self, card = ""):
	        #option to check for specific devCard, controller should handle not allowing
	        #player to play multiple devCards on a turn if thats a rule
	        if card == "":
	            return len(self.devCardsHeld) != 0
	        else:
	            return card in self.devCardsHeld
        def playDevCard(self, card):
            if self.canPlayDevCard(card):
                #we'll need to program in effects of different cards here
                self.devCardsHeld.remove(card)
                self.devCardsPlayed.append(card)
                print "you have played: ", card
            else:
                print "You don't have that card"
            
	def buildRoad(self, location, board):
		if self.canBuildRoad(location, board):
		    #we will need a deck to draw from
		    self.roadsRemaining -=1
		    self.resources['wood'] -= 1
		    self.resources['brick'] -= 1
		    self.structures['roads'].append(location.index)
		    location.buildRoad(self.playerNumber)
		else:
		    print "You cannot build a road there"

	def buildSettlement(self, location, board):
		if self.canBuildSettlement(location, board) or self.settlementsRemaining > 3:
		    #we will need a deck to draw from
		    self.settlementsRemaining -=1
		    self.resources['wood'] -= 1
		    self.resources['brick'] -= 1
		    self.resources['grain'] -= 1
		    self.resources['sheep'] -= 1
		    self.structures['settlements'].append(location.index)
		    location.buildSettlement(self.playerNumber, len(self.structures['settlements']))
		else:
		    print "You cannot build a settlement there"

	def buildCity(self, location):
		if self.canBuildCity(location):
		    #we will need a deck to draw from
		    self.citiesRemaining -=1
		    self.resources['ore'] -= 3
		    self.resources['grain'] -= 2
		    self.structures['settlements'].remove(location.index)
		    self.structures['cities'].append(location.index)
		    location.buildCity(self.playerNumber)

		else:
		    print "You cannot build a city there"

	def buildDevCard(self, deck):
		if self.canPlayDevCard:
		    #we will need a deck to draw from
		    nameCard = deck.getRandomDevCard()
		    self.devCardsHeld.append(nameCard)
		    self.resources['sheep'] -= 1
		    self.resources['grain'] -= 1
		    self.resources['ore'] -=1
		else:
		    print "You cannot draw a development card right now"

	def loseRandomCard(self):
       	    resources = []
       	    for r in self.resources:
       	        if self.resources[r] != 0:
       	            for _ in xrange(self.resources[r]):
      	                 resources.append(r)
       	    if len(resources) == 0:
       	        print "No resources to steal"
       	        return None
       	    else:
              	 i = random.randint(0, len(resources) - 1)
              	 print "1 ", resources[i], " was stolen"
                 self.loseResource(resources[i], 1)
                 return resources[i]

	def addResource(self, resource, amount, verbose = False):
	       self.resources[resource] += amount
	       if verbose:
	           print "Now you have: ", self.resources

	def loseResource(self, resource, amount, verbose = False):
		self.resources[resource] -= amount
		if verbose:
	           print "Now you have: ", self.resources
	#I added these two mostly for testing but could be useful
	def checkResources(self):
	        return self.resources
	def checkStructures(self):
	        return self.structures