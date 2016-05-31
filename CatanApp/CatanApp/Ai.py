# -*- coding: utf-8 -*-
# Feature discussion
# Weighting of resources
#   Ovearll Best
#   Availability
#   What's in your hand
#   What's in your income

# Vertex Cost Location
#   Turns away
#   Resources used


# Vertex Reward Valuation
#   Centraility
#   Income increase
#   Resource Weighting (from above)
#   Ports
#   Variability (not in alpha)
#   Vertex Cost (from above)
#   Current VP (when at 9VP, cost is all that matters)
#   Total Turns remaaining in the game (not in 1-player)


 




import math
import Player

class ai:
    
    def __init__(self, i):
        self.AI = Player.player(i)
        #weights for features
        self.weights =  {'incomeIncrease' : 1000, 'centrality' : 1.0, 'costInTurns' : -1.0, 'costInRes' : -1.0, 'port' : 1.0, 'vp' : 1.0}
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
    '''
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
   '''	
    def findNeed(self, cost, income):
        if len(cost) == 0:
            return None
        print cost
        maxNeed = (0, 0)
        need = cost.keys()[0]
        for r in cost:
            if income[r] == 0:
                temp = (float('inf'), cost[r])
            else:
                temp = (cost[r]/income[r], cost[r])
            if temp[0] > maxNeed[0] or ((temp[0] == maxNeed[0]) and(temp[1] > maxNeed[1])):
                need = r
                maxNeed = temp
        return need

    def getCostInTurns(self, buildType,roadsAway,incomeMap):
        print "###############################3"
        print buildType
        print roadsAway
        print self.AI.resources
        print incomeMap, "income"
   	resCost = self.getResourceCost(buildType,roadsAway)
   	print resCost
   	modResCost = {}
   	turnCost = 0.0 
   	ownedResources = self.AI.resources.copy()
   	stockpile = ownedResources.copy()
   	for r in stockpile:
   	    stockpile[r] = 0
   	baseTurns = 0
   	baseTurnSet = False
   	for res in resCost:
   	    dif = 0
   	    temp = resCost[res] - ownedResources[res]

   	    if temp > dif:
   	        dif = temp
   	    else:
   	        stockpile[res] = -temp
   	    if temp <= 0:
   	        baseTurnSet = True
   	    if dif != 0:
   	        modResCost[res] = dif
        if not baseTurnSet:
            baseTurnSet = float('inf')
            for r in modResCost:
                turns = int(math.ceil(modResCost[r] / incomeMap[r]))
                if turns < baseTurnSet:
                    baseTurnSet = turns
   	#delete fields from needs increment while needs not empty
   	#when we hit overflow give to largest gap
   	#encode ports knowledge
   	print baseTurns, "base turns"
   	print stockpile, "stock1"
   	print modResCost, "mod1"
   	turnCost = baseTurns
   	for r in incomeMap:
   	    stockpile[r] += incomeMap[r] * baseTurns
   	print incomeMap, "income"
   	print stockpile, "stock2"  	
   	while(len(modResCost) > 0):
   	    for r in stockpile:
   	        if r in modResCost:
   	            if stockpile[r] >= 1:
   	                if modResCost[r] <= stockpile[r]:
   	                    stockpile[r] -= modResCost[r]
   	                    modResCost.pop(r)
   	                else:
   	                    modResCost[r] -= int(stockpile[r])
   	                    stockpile[r] -= int(stockpile[r])
   	        elif stockpile[r] >= 4:
   	            while(stockpile[r] >= 4):
           	            exchange = self.findNeed(modResCost, incomeMap)
           	            if exchange == None:
           	                print turnCost, "<<<<<<<<<<<<<<<<<<"
           	                return turnCost
           	            print "exchanging", r, exchange
           	            stockpile[r] -= 4
           	            modResCost[exchange] -= 1
           	            if modResCost[exchange] == 0:
           	                modResCost.pop(exchange)
   	    if len(modResCost) == 0:
   	        break
   	    if turnCost > 100:
   	        break
   	    turnCost +=1
   	    for r in stockpile:
   	        stockpile[r] += incomeMap[r]
   	    print incomeMap, "income Map"
   	    print stockpile, "stock loop"
   	    print modResCost, "mod loop"
   	print turnCost, "<<<<<<<<<<<<<<<<<<"
   	return turnCost
   	        
    def evaluateLocationBenefit(self, vert, board):
        tiles = board.getVertexToTiles(vert)
        # print len(tiles)
        exReturn =  {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        for tile in tiles:
            tileType = tile.getType()
            if tileType == 'desert':
                continue 
            exReturn[tileType] += self.diceProbs[tile.getNumber()]
        return exReturn
    
    #still doesnt handle other players roads that block paths
    def findPlayableLocations(self, vert, x, board):
        print vert, x, board, "find plays 1"
        trash = set()
        cur = [vert]
        #we use sets to keep the spots unique in case of longer distances
        cur = set(cur)
        #this dictates how many steps away we look (ie, x = 2 means we look for all spots 2 away)
        for i in xrange(x):
            temp = set()
            for v in cur:
                #this board function should return all of a vertex's neighbors
                for n in board.getVertexToVertices(v):
                    #we dont want to back track hence the trash list
                    if n not in trash:
                        #if we're one road away from the spots we're looking we don't
                        #need to consider neighbors of an owned vetex
                        if i == x-2 and n.getOwner() != None:
                            continue
                        temp.add(n)
            trash = trash.union(cur)
            cur = temp
        #this check is still needeed despite above neighbor check, should be more efficient to have both as is
        cur = list(cur)
        for v in cur:
            if v.getOwner() != None:
                cur.remove(v)
                print "v", v.getIndex(), "removed 1", v.getOwner()
                continue
            #print "v", v.getIndex()
            for n in board.getVertexToVertices(v):
                if n.getOwner() != None:
                    cur.remove(v)
                    print "v", v.getIndex(), "removed 2", n.getOwner()
                    break
        for v in cur:
            print "V", v.index
        return cur            
    def evaluateTrade(self, gain, lose):
        print "gain",gain,"lose",lose
        currentResources  = self.AI.resources
        print "currentResources",currentResources
        available = False
        difference = {key: currentResources[key] - lose.get(key, 0) for key in currentResources.keys()}
        print difference
        
        gainTotal = sum(gain.values())
        loseTotal = sum(lose.values())


        print "gainTotal", gainTotal, "loseTotal",loseTotal
        print "The AI is too naive to trade right now"
        return False
        
    def decideMove(self, players, board, firstTurn):
# Look at spots available to build on (settlement locations)
# What does it take to get there (how many turns?) expected value
# This is a cost
# Cost vs reward for each spot
# Learned by getting to 10
# Manually change a ratio parameter
# Additional value for ports
# Centrality value
# Longest road length
# At 7+ points different math
# ignore robber at first
# Add ability to automatically branch the game
# ignore trading at first
# Start at each settlement, search for spots 2 away, if not enough, 
# search further, etc. UNTIL we find N+ (start with N=5)
      #don't ignore the update income if something is built
      if firstTurn:
          locs = list(board.getPotentialSettlementLocs(self.AI.playerNumber, players, True))
          maxIncome = 0
          bestloc = 0
          for i in xrange(len(locs)):
            benefit = self.evaluateLocationBenefit(locs[i], board)
            gain = 0.0
            for r in benefit:
                gain += benefit[r]
            # print "*******"
            # print locs[i].index
            # print benefit
            # print "******"
            if gain > maxIncome:
                bestloc = i
                maxIncome = gain
          self.AI.buildSettlement(locs[bestloc], board)
          self.updateIncome(locs[bestloc], board)
          builtSettlementSpot = locs[bestloc].getIndex()
          roadOptions = board.vertexToEdgeMap[builtSettlementSpot]
          print builtSettlementSpot, "roadOptions", roadOptions
          print "currently just choosing the first road on the list" # Currentliy just building at the first option
          roadChoice = board.edges[roadOptions[0]]
          self.AI.buildRoad(roadChoice, board) 
      else:
        curDistanceAway = 4
        devCardCost = sum(self.getResourceCost('devCard', 0).values())
        options = {"devCard": {'costInRes' : devCardCost},"pass": {} }
        curSettlements = self.AI.structures['settlements']
        while(True):
            for settlement in curSettlements:
                s = board.vertices[settlement]
                playableLocations = self.findPlayableLocations(s,curDistanceAway,board)
                for playableS in playableLocations:
                    #ideally object to ascii
                    benefit = self.evaluateLocationBenefit(playableS, board)
                    turnCost = self.getCostInTurns('settlement', curDistanceAway, self.income)
                    resCost = sum(self.getResourceCost('settlement', curDistanceAway).values())
                    asciiRepresentation = str(board.vertexToAscii[playableS])
                    options[asciiRepresentation] = {'incomeIncrease': sum(benefit.values()), 'costInTurns' : turnCost, 'costInRes' : resCost}
            if (len(options) >= 7 or curDistanceAway >= 5):
                break
            curDistanceAway += 1
        for settle in self.AI.structures['settlements']:
            s = board.vertices[settle]
            benefit = self.evaluateLocationBenefit(s, board)
            turnCost = self.getCostInTurns('city', 0, self.income)
            resCost = sum(self.getResourceCost('city', 0).values())
            asciiRepresentation = ""#str(board.vertexSettlementAscii[settle])
            options[asciiRepresentation] = {'incomeIncrease': sum(benefit.values()), 'costInTurns' : turnCost, 'costInRes' : resCost}
          #need to add more options and expand the curDistanceAway
        print options
        print self.evaluateOptions(options)
        print "The Ai was caught sleeping, it does nothing"
    def evaluateOptions(self, options):
        bestOption = ""
        bestScore = -float('inf')
        for opt in options:
            score = 0.0
            for field in options[opt]:
                    score += options[opt][field] * self.weights[field]
            if score > bestScore:
                bestOption = opt
                bestScore = score
        return bestOption, bestScore
    def placeRobber(self, board):
        newRobberLocation = board.asciiToTile['01T']
        board.moveRobber(newRobberLocation)
        targets = list(board.playersToStealFrom(newRobberLocation))
        if len(targets) > 0:
            return targets[0]
        else:
            return None

    def updateIncome(self, vert, board):
        #anytime we build on a location whether adding a settlment or changing to city
        #our income increases by one settlment of expected value so we can levarge our
        #benefit function
        gain = self.evaluateLocationBenefit(vert, board)
        for res in gain:
            self.income[res] += gain[res]
    def addResource(self, res, amount):
        self.AI.addResource(res, amount)
        
    def loseResource(self, res, amount, verbose = False):
        self.AI.loseResource(res, amount)
        
    def loseRandomCard(self):
        self.AI.loseRandomCard()   
             
    def tests(self):
        print self.AI.roadsRemaining
    