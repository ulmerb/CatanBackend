# -*- coding: utf-8 -*-
import random

class player:

	def __init__(self, i):
		self.score =  0
		self.resources =  {'wood': 14, 'sheep':12, 'brick': 14, 'ore': 10, 'grain' : 12}
		#self.resources =  {'wood': 4, 'sheep':2, 'brick': 4, 'ore': 0, 'grain' : 2}
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
	
	def bankTrade(self, give, take):
		if self.resources[give] >= 4:
			self.resources[give] -= 4
			self.resources[take] += 1
		else:
			return "Not enough " + give

	def makePortTrade(self, port, give, take):
		if port in self.structures['ports']:
			if port == "three":
				if self.resources[give] >= 3:
					self.resources[give] -= 3
					self.resources[take] += 1
				else:
					return "Not enough " + give
			else:
				error = self.specPortTrade(port, take)
				return error
		else:
			return port + " not owned"

	def specPortTrade(self,port, take):
		if self.resources[port] >= 2:
			self.resources[port] -= 2
			self.resources[take] += 1
		else:
			return "Not enough " + port

	#trade function based on Controller.trade 
	def trade(curPlayer, players, board, AiNum = -2):
		 #   while(trading):
      #       response = raw_input("Would you like to propose a trade?")
      #       if  response == "Yes" or response == "yes" or response == "y":
      #       	bankResponse = raw_input("Would you like to trade with the bank?")
      #       	if  bankResponse == "Yes" or response == "yes" or response == "y":
      #       		toLose = resourceSelector("Which resource do you want to give to the bank? ")
      #       		numberToLose = getAmountFromPlayer()
      #       		toGet = resourceSelector("Which resource do you want to receive? ")
      #       		modifier = findTradeModifier(curPlayer, toLose, board)
      #       		if numberToLose % modifier != 0:
      #       			print "Retry and enter a number that is a multiple of ", modifier
      #       			continue
      #       		else:
						# players[curPlayer].addResource(toGet, numberToLose/modifier)
						# players[curPlayer].loseResource(toLose, numberToLose)
						# print "You know have ", players[curPlayer].resources
						# continue
		print "Trading phase Django"
		trading = True
		curResources = players[curPlayer].checkResources() 
		offer =  {'wood':0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
		# print "What would you like to offer? (Enter an amount for each following resource)"
		offer = tradeHelper(offer, curResources)
		recieve = {'wood':0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
		print "What would you like in return? (Enter an amount for each following resource)"
		recieve = tradeHelper(recieve, curResources, True)
		partner = -1
		potentialPartner = raw_input("Would like to ask a specific player (if so enter the player number you'd like to trade with)")
		if isInt(potentialPartner):
		    potentialPartner = int(potentialPartner)
		    if potentialPartner < len(players) and potentialPartner != curPlayer:
		        partner = potentialPartner
		        print "Proposing trade to player: ", partner
		    else:
		        print "No partner or invalid partner inserted, proposing trade to all players"
		else: # in this case they didn't provid a number so we can assume they want to offer it to anyone
			partner = -3
		if (partner == AiNum and AiNum != -2):
			traded = players[AiNum].evaluateTrade(offer, recieve)
			print "trade executed with AI"
			for r in offer:
				players[curPlayer].loseResource(r, offer[r])
				players[AiNum].addResource(r, offer[r])
			for r in recieve:
				players[curPlayer].addResource(r, recieve[r])
				players[AiNum].loseResource(r, recieve[r])
			for player in players:
				print player
		elif partner != -1 and partner != -3:
		    tradeLogicHelper(curPlayer, partner, players, offer, recieve)
		else:
		    for i in xrange(len(players)):
		        if i == curPlayer:
		            continue
		        if i == AiNum:
		            executed = players[AiNum].evaluateTrade(offer, recieve)
		            if (executed):
						print "trade executed with AI"
						for r in offer:
							players[curPlayer].loseResource(r, offer[r])
							players[AiNum].addResource(r, offer[r])
						for r in recieve:
							players[curPlayer].addResource(r, recieve[r])
							players[AiNum].loseResource(r, recieve[r])
						for player in players:
							print player
						break
		        else:
		            executed = tradeLogicHelper(curPlayer, i, players, offer, recieve)
		            if (executed):
		                break
		# else:
		#     trading = False


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
		print "Found length ", bestFound
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

		    location.buildSettlement(self.playerNumber, len(self.structures['settlements']) + len(self.structures['cities']))

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