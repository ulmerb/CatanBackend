# -*- coding: utf-8 -*-
import random

class player:

	def __init__(self, i):
		self.score =  0
		#self.resources =  {'wood':14, 'sheep':14, 'brick': 14, 'ore': 16, 'grain' : 14}
		self.resources =  {'wood': 4, 'sheep':2, 'brick': 4, 'ore': 0, 'grain' : 2}
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
                 
	def getRoadLength(self, board):
		roads = set(self.structures['roads'])
		print "I have ", len(roads), " roads"
		bestFound = 0
		for road in roads:
			roads.remove(road)
			cur = self.findPathFromRoad(road, None, roads, board) + 1
			if cur > bestFound:
				bestFound = cur
			roads.add(road)
		print "Found lenght ", bestFound
		return bestFound

	def findPathFromRoad(self, start, end, roads, board):
		best = 0
		for road in roads:
			cur = 0
			if end is None:
				if road in board.edgeToEdgeMap[start]:
					roads.remove(road)
					cur = self.findPathFromRoad(start, road, roads, board) + 1
					roads.add(road)
			else:
				if road in board.edgeToEdgeMap[start]:
					roads.remove(road)
					cur = self.findPathFromRoad(road, end, roads, board) + 1 
					roads.add(road)
				elif road in board.edgeToEdgeMap[end]:
					roads.remove(road)
					cur = self.findPathFromRoad(start, road, roads, board) + 1
					roads.add(road)
			if cur > best:
				best = cur
		return best

	def hasWon(self):
	        if self.score >= 10:
	            return True
		return False
        #on all of these methods I'll leave the option to check a specific location for now
	def canBuildCity(self, location):
	    if location.city is not None:
	        return False
   	    if self.resources['grain'] >= 2 and self.resources['ore'] >= 3 and self.citiesRemaining > 0:
   	        if location.index in self.structures['settlements']:
   	        	return True
		return False
		
	def canBuildSettlement(self, board, gridLoc):
		if gridLoc.getOwner() is not None:
		        print "already owned"
			return False
		if not (self.resources['brick'] >= 1 and self.resources['wood'] >= 1 and self.resources['grain'] >= 1 and self.resources['sheep'] >= 1 and self.settlementsRemaining > 0):
			print "Insufficent resources, ", self.resources
			return False
		adjRoads = board.getVertexToEdges(gridLoc)
		playerHasRoad = False
		for adjRoad in adjRoads:
			index = adjRoad.index
			if index in self.structures['roads']:
				playerHasRoad = True
				break
		if not playerHasRoad:
			print "No linking roads"
			return False
		for n in board.getVertexToVertices(gridLoc):
			if n.getOwner() is not None:
				print "Settlements need to be at least 2 away"
				return False
		return True

	def validSpaceForRoad(self, location, board):
		if location.getOwner() is not None:
			print "already owned"
			return False
		for neighbV in board.getEdgeToVertices(location):
			if neighbV.getOwner() == self.playerNumber:
				return True
		for neigbE in board.getEdgeToEdges(location):
			if neigbE.getOwner() == self.playerNumber:
				return True
				print "Success!"
		return False

	def canBuildRoad(self, location, board):
		# print board.edgeToAscii[location], location.index
		# for edge in board.edges:
		# 	if edge is not None and edge.index != 0:
		# 		print edge.index, edge.getOwner()
		if not (self.resources['brick'] >= 1 and self.resources['wood'] >= 1 and self.roadsRemaining > 0):
			print "Not enough resources"
			return False
		return self.validSpaceForRoad(location, board)

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
	  		return True

	def getDevCards(self):
		return self.devCardsHeld

	def totalResources(self):
		count = 0
		for item in self.resources:
			count += self.resources[item]
		return count

	def playDevCard(self, card):
 		if self.canPlayDevCard(card):
			self.devCardsHeld.remove(card)
			self.devCardsPlayed.append(card)
			print "you have played: ", card
		else:
			print "You don't have that card"
    
	def getKnightsPlayed(self):
		count = 0
		for card in self.devCardsPlayed:
			if card == "knight":
				count += 1
		return count

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
		if self.canBuildSettlement(board, location) or (self.settlementsRemaining > 3 and self.citiesRemaining == 4):
		    #we will need a deck to draw from
		    self.settlementsRemaining -=1
		    self.resources['wood'] -= 1
		    self.resources['brick'] -= 1
		    self.resources['grain'] -= 1
		    self.resources['sheep'] -= 1
		    self.structures['settlements'].append(location.index)
		    self.score += 1
		    location.buildSettlement(self.playerNumber, len(self.structures['settlements']))
		    ind = location.index
		    three = [5,6,3,4,28,17,53,54]
		    ore = [39,40]
		    sheep = [8,9]
		    grain = [50,51]
		    wood = [37,47]
		    brick = [16, 26]
		    if ind in three:
		        self.structures['ports'].append('three')
		        print "You've gained a 3:1 port"
		    elif ind in ore:
		        self.structures['ports'].append('ore')
		        print "You've gained an ore port"
		    elif ind in sheep:
		        self.structures['ports'].append('sheep')
		        print "you've gained a sheep port"
		    elif ind in grain:
		        print "you've gained a grain port"
		        self.structures['ports'].append('grain')
		    elif ind in wood:
		        print "youve'gained a wood port"
		        self.structures['ports'].append('wood')
		    elif ind in brick:
		        print "you've gained a brick port"
		        self.structures['ports'].append('brick')
		    board.addSettlement(location)
		else:
			print "You cannot build a settlement there"
			# return "You cannot build a settlement there"

	def buildCity(self, location, board):
		if self.canBuildCity(location):
		    #we will need a deck to draw from
		    self.citiesRemaining -=1
		    self.settlementsRemaining +=1
		    self.resources['ore'] -= 3
		    self.resources['grain'] -= 2
		    self.structures['settlements'].remove(location.index)
		    self.structures['cities'].append(location.index)
		    self.score +=1
		    location.buildCity(self.playerNumber, len(self.structures['cities']))
		else:
		    print "You cannot build a city there"
	def canAffordDevCard(self):
	    return self.resources['sheep'] > 0 and self.resources['grain'] > 0 and self.resources['ore'] > 0

	def buildDevCard(self, deck):
		if self.canAffordDevCard():
		    #we will need a deck to draw from
		    nameCard = deck.getRandomDevCard()
		    print "You have built ", nameCard
		    if nameCard == "victoryPoint":
		    	self.devCardsPlayed.append(nameCard)
		    	self.incrementScore(1)
		    	print "Your score has been increased by 1"
		    else: 
		    	self.devCardsHeld.append(nameCard)
		    self.resources['sheep'] -= 1
		    self.resources['grain'] -= 1
		    self.resources['ore'] -=1
		    return None, nameCard
		else:
		    return "You can't afford that" , None

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

	def numResources(self, resource):
		return self.resources[resource]