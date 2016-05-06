# -*- coding: utf-8 -*-
import Player

class ai:
    
    def __init__(self, board):
        self.AI = Player.player()
        #weights for features
        self.centrality = []
        self.incomeIncrease = 1.0
        self.costInTurns = 1.0
        self.costInRes = 1.0
        self.port = 1.0
        self.vp = 1.0
        self.diceProbs = [0.0, 0.0, 0.028,0.056,0.083,0.111,0.139,0.167,0.139,0.111,0.083,0.056,0.028]
        self.income = {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        
    def getBuildLocations(self):
        pass
        
    def updateBuildLocations(self):
        pass
        
    # getResourceCost(buildType,roadsAway)
    # Varible one, build type, "road", "settlement", "city", "devCard"
    # Variable two, number of roads away
    # 
    def getResourceCost(self, buildType,roadsAway):
   	cost =  {'wood':0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
   	if(buildType == "road"):
  		cost['brick'] += 1
  		cost['wood'] += 1
   	elif (buildType == "settlement"):
  		cost['sheep'] += 1
  		cost['brick'] += 1
  		cost['wood'] += 1
  		cost['grain'] += 1
  		cost['brick'] += roadsAway
  		cost['wood'] += roadsAway
   	elif (buildType == "city"):
  		cost['grain'] += 2
  		cost['ore'] += 3
   	elif (buildType == "devCard"):
  		cost['sheep'] += 1
  		cost['grain'] += 1
  		cost['ore'] += 1
   	else:
  		print "invalid getResourceCost() call",buildType,roadsAway
   	
   	return cost
    
    def getVictoryPoints(self):
   	return self.AI.getScore();
    
    def getCostInTurns(self, buildType,roadsAway,incomeMap):
   	resCost = self.getResourceCost(buildType,roadsAway)
   	turnCost = 0.0 
   	ownedResources = self.AI.resources
   	for res in resCost:
   	    dif = 0
   	    temp = resCost[res] - ownedResources[res]
   	    if temp > dif:
   	        dif = temp
   	    resCost[res] = dif
   	for key in resCost.keys():
  		curIncome = incomeMap[key]
  		curCost = resCost[key]
  		if (curIncome == 0):
 			return -1 #sentinel
  		else:
 			val = curCost / curIncome
 			if (val > turnCost):
    				turnCost = val
   	return turnCost
            
    def evaluateLocationBenefit(self, vert):
        tiles = self.board.getVertexToTiles(vert)
        exReturn =  {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        for tile in tiles:
            tileType = tile.getType()
            if tileType == 'desert':
                continue 
            exReturn[tileType] += self.diceProbs[tile.getNumber()]
        return exReturn
             
    def decideMove(self):
        pass
               
    def updateIncome(self, vert):
        #anytime we build on a location whether adding a settlment or changing to city
        #our income increases by one settlment of expected value so we can levarge our
        #benefit function
        gain = self.evaluateLocationBenefit(vert)
        for res in gain:
            self.income[res] += gain[res]
        
    def tests(self):
        print self.AI.roadsRemaining
    